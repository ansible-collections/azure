"""Integration-test stub for azure_rm_ml_job.

Emits a valid MLflow ``pyfunc`` model to ``--model_dir`` so the downstream
``azure_rm_ml_model`` task can register it.  The goal is to exercise
``azure_rm_ml_job``/``azure_rm_ml_model`` code paths end-to-end without
depending on brittle third-party data-loading or CPU training runtime.
"""
import argparse
import shutil
from pathlib import Path

import mlflow.pyfunc


class ConstantModel(mlflow.pyfunc.PythonModel):
    def predict(self, context, model_input, params=None):
        return [0] * len(model_input)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", dest="data_dir", default=".")
    parser.add_argument("--model_dir", dest="model_dir", required=True)
    args = parser.parse_args()

    model_dir = Path(args.model_dir)
    # AzureML pre-creates the mlflow_model output as an empty rw_mount dir,
    # but ``mlflow.pyfunc.save_model`` refuses to write when the target path
    # already exists, so clear it first.
    if model_dir.exists():
        shutil.rmtree(model_dir, ignore_errors=True)

    mlflow.pyfunc.save_model(path=str(model_dir), python_model=ConstantModel())


if __name__ == "__main__":
    main()
