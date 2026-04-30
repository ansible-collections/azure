# Copyright (c) 2025 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Helpers for spawning and managing an ``az network bastion tunnel`` subprocess.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import errno
import os
import shutil
import signal
import socket
import subprocess
import threading
import time


class BastionTunnelError(Exception):
    """Raised when starting/operating the Bastion tunnel fails."""


def pick_free_port():
    """Bind to port 0 on loopback to let the OS hand us a free port, then
    release it. Caller must accept the small TOCTOU race between picking
    and the subprocess binding.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]
    finally:
        sock.close()


def is_port_in_use(port, host="127.0.0.1"):
    """Return True if some process is already listening on host:port."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    try:
        sock.connect((host, port))
    except OSError:
        return False
    else:
        return True
    finally:
        try:
            sock.close()
        except Exception:
            pass


# Per-process cache so we only run `az extension list` once per controller
# invocation, keyed by resolved az binary path.
_EXTENSION_CHECK_CACHE = set()
_EXTENSION_CHECK_LOCK = threading.Lock()


def check_az_available(az_path):
    """Verify the ``az`` CLI binary is on PATH (or at the given path).
    Returns the resolved absolute path. Raises BastionTunnelError otherwise.
    """
    resolved = shutil.which(az_path) if not os.path.isabs(az_path) else (
        az_path if os.path.isfile(az_path) and os.access(az_path, os.X_OK) else None
    )
    if not resolved:
        raise BastionTunnelError(
            "Could not find the Azure CLI binary '%s' on PATH. "
            "Install it from https://aka.ms/azcli and ensure it is in PATH on the Ansible controller." % az_path
        )
    return resolved


def check_bastion_extension(az_path):
    """Verify that the ``bastion`` az CLI extension is installed.
    Raises BastionTunnelError with the remediation command if not.
    Result is cached per-process for the lifetime of the controller.
    """
    with _EXTENSION_CHECK_LOCK:
        if az_path in _EXTENSION_CHECK_CACHE:
            return
    try:
        completed = subprocess.run(
            [az_path, "extension", "list", "--query", "[].name", "-o", "tsv"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise BastionTunnelError("Failed to query az extensions: %s" % exc)
    if completed.returncode != 0:
        raise BastionTunnelError(
            "Failed to query az extensions (rc=%d): %s"
            % (completed.returncode, completed.stderr.decode("utf-8", "replace").strip())
        )
    installed = set(completed.stdout.decode("utf-8", "replace").split())
    if "bastion" not in installed:
        raise BastionTunnelError(
            "The 'bastion' az CLI extension is not installed. "
            "Install it on the Ansible controller with: az extension add --name bastion"
        )
    with _EXTENSION_CHECK_LOCK:
        _EXTENSION_CHECK_CACHE.add(az_path)


def start_tunnel(az_path, bastion_name, resource_group, target_resource_id,
                 target_port, local_port, subscription=None, extra_env=None):
    """Spawn ``az network bastion tunnel`` as a subprocess.

    Returns the subprocess.Popen handle. Caller is responsible for
    polling readiness via :func:`wait_for_port` and for terminating
    the process via :func:`terminate_tunnel`.
    """
    cmd = [
        az_path, "network", "bastion", "tunnel",
        "--name", bastion_name,
        "--resource-group", resource_group,
        "--target-resource-id", target_resource_id,
        "--resource-port", str(target_port),
        "--port", str(local_port),
    ]
    if subscription:
        cmd.extend(["--subscription", subscription])

    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)
    # Suppress interactive prompts; az should not ask us anything here.
    env.setdefault("AZURE_CORE_OUTPUT", "none")
    env.setdefault("AZURE_CORE_ONLY_SHOW_ERRORS", "true")

    try:
        proc = subprocess.Popen(  # noqa: S603 - args list, not shell
            cmd,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            start_new_session=True,
        )
    except OSError as exc:
        raise BastionTunnelError("Failed to spawn az tunnel subprocess: %s" % exc)
    return proc


def drain_stream_to_buffer(stream, buf, max_bytes=64 * 1024):
    """Read from ``stream`` until EOF in a daemon thread, appending into a
    bytearray buffer (capped at ``max_bytes``). Used to keep the tunnel's
    stderr/stdout pipes from filling and blocking the subprocess after
    readiness. Returns the started Thread.
    """
    def _drain():
        try:
            while True:
                chunk = stream.read(4096)
                if not chunk:
                    break
                if len(buf) < max_bytes:
                    buf.extend(chunk[: max(0, max_bytes - len(buf))])
        except Exception:
            pass
        finally:
            try:
                stream.close()
            except Exception:
                pass

    thread = threading.Thread(target=_drain, daemon=True)
    thread.start()
    return thread


def wait_for_port(port, timeout, proc=None, host="127.0.0.1"):
    """Poll a TCP port until it accepts a connection or ``timeout`` elapses.

    If ``proc`` is provided and exits before the port is ready, raise
    BastionTunnelError including any captured stderr (most common cause:
    Bastion SKU does not support tunneling, or auth failure).
    """
    deadline = time.monotonic() + timeout
    last_err = None
    while time.monotonic() < deadline:
        if proc is not None and proc.poll() is not None:
            stderr = b""
            try:
                stderr = proc.stderr.read() or b""
            except Exception:
                pass
            raise BastionTunnelError(
                "az network bastion tunnel exited prematurely (rc=%d): %s"
                % (proc.returncode, stderr.decode("utf-8", "replace").strip()
                   or "no stderr captured. Verify the Bastion SKU is Standard or higher with "
                   "enableTunneling=true, and that the target resource id is correct.")
            )
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0)
        try:
            sock.connect((host, port))
            sock.close()
            return
        except OSError as exc:
            last_err = exc
            if exc.errno not in (errno.ECONNREFUSED, errno.EHOSTUNREACH, errno.ETIMEDOUT, errno.EAGAIN):
                # Unexpected error — propagate.
                sock.close()
                raise BastionTunnelError("Unexpected error probing tunnel port %d: %s" % (port, exc))
        finally:
            try:
                sock.close()
            except Exception:
                pass
        time.sleep(0.25)
    raise BastionTunnelError(
        "Timed out after %ss waiting for az bastion tunnel to listen on 127.0.0.1:%d (last error: %s)"
        % (timeout, port, last_err)
    )


def terminate_tunnel(proc, grace_seconds=5):
    """Politely terminate the tunnel subprocess, escalating to KILL.

    Safe to call multiple times. No-op if proc is None or already exited.
    """
    if proc is None:
        return
    if proc.poll() is not None:
        return
    try:
        # We started the subprocess in its own session; signal the whole group
        # so any child forks (the az CLI sometimes spawns helpers) also exit.
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        except (ProcessLookupError, PermissionError, OSError):
            proc.terminate()
    except Exception:
        try:
            proc.terminate()
        except Exception:
            pass
    try:
        proc.wait(timeout=grace_seconds)
        return
    except subprocess.TimeoutExpired:
        pass
    try:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except (ProcessLookupError, PermissionError, OSError):
            proc.kill()
    except Exception:
        pass
    try:
        proc.wait(timeout=grace_seconds)
    except subprocess.TimeoutExpired:
        pass
