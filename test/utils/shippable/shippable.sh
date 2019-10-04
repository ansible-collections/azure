#!/usr/bin/env bash

set -o pipefail -eux

declare -a args
IFS='/:' read -ra args <<< "$1"

script="${args[0]}"

test="$1"

docker images ansible/ansible
docker images quay.io/ansible/*
docker ps

for container in $(docker ps --format '{{.Image}} {{.ID}}' | grep -v '^drydock/' | sed 's/^.* //'); do
    docker rm -f "${container}" || true  # ignore errors
done

docker ps

if [ -d /home/shippable/cache/ ]; then
    ls -la /home/shippable/cache/
fi

command -v python
python -V

command -v pip
pip --version
pip list --disable-pip-version-check

export PATH="${PWD}/bin:${PATH}"
export PYTHONIOENCODING='utf-8'

if [ "${JOB_TRIGGERED_BY_NAME:-}" == "nightly-trigger" ]; then
    COVERAGE=yes
    COMPLETE=yes
fi

if [ -n "${COVERAGE:-}" ]; then
    # on-demand coverage reporting triggered by setting the COVERAGE environment variable to a non-empty value
    export COVERAGE="--coverage"
elif [[ "${COMMIT_MESSAGE}" =~ ci_coverage ]]; then
    # on-demand coverage reporting triggered by having 'ci_coverage' in the latest commit message
    export COVERAGE="--coverage"
else
    # on-demand coverage reporting disabled (default behavior, always-on coverage reporting remains enabled)
    export COVERAGE="--coverage-check"
fi

if [ -n "${COMPLETE:-}" ]; then
    # disable change detection triggered by setting the COMPLETE environment variable to a non-empty value
    export CHANGED=""
elif [[ "${COMMIT_MESSAGE}" =~ ci_complete ]]; then
    # disable change detection triggered by having 'ci_complete' in the latest commit message
    export CHANGED=""
else
    # enable change detection (default behavior)
    export CHANGED="--changed"
fi

if [ "${IS_PULL_REQUEST:-}" == "true" ]; then
    # run unstable tests which are targeted by focused changes on PRs
    export UNSTABLE="--allow-unstable-changed"
else
    # do not run unstable tests outside PRs
    export UNSTABLE=""
fi

virtualenv --python /usr/bin/python3.7 ~/ansible-venv
set +ux
. ~/ansible-venv/bin/activate
set -ux

pip install ansible==2.9.0rc2

function cleanup
{
    if [ -d test/results/coverage/ ]; then
        if find test/results/coverage/ -mindepth 1 -name '.*' -prune -o -print -quit | grep -q .; then
            # for complete on-demand coverage generate a report for all files with no coverage on the "other" job so we only have one copy
            if [ "${COVERAGE}" == "--coverage" ] && [ "${CHANGED}" == "" ] && [ "${test}" == "sanity/1" ]; then
                stub="--stub"
            else
                stub=""
            fi

            # shellcheck disable=SC2086
            ansible-test coverage xml --color -v --requirements --group-by command --group-by version ${stub:+"$stub"}
            cp -a test/results/reports/coverage=*.xml shippable/codecoverage/
        fi
    fi

    if [ -d  test/results/junit/ ]; then
      cp -aT test/results/junit/ shippable/testresults/
    fi

    if [ -d test/results/data/ ]; then
      cp -a test/results/data/ shippable/testresults/
    fi

    if [ -d  test/results/bot/ ]; then
      cp -aT test/results/bot/ shippable/testresults/
    fi
}

trap cleanup EXIT

if [[ "${COVERAGE:-}" == "--coverage" ]]; then
    timeout=60
else
    timeout=45
fi

ansible-test env --dump --show --timeout "${timeout}" --color -v

"test/utils/shippable/check_matrix.py"
"test/utils/shippable/${script}.sh" "${test}"
