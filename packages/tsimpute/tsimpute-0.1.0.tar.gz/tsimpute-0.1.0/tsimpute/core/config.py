from typing import Any, Tuple
import os
import minio
import mlflow
from tsimpute.core.logger import log


def env_debugger(*variables: Tuple[str, Any, int]):
    for var in variables:
        msg = var[1]
        if len(var) == 3:
            msg = msg[:var[2]] + '*' * (len(msg) - var[2])
        log.debug(f"{var[0]}: {msg}")


# Minio configuration
MINIO_ENDPOINT = f"{os.getenv('MINIO_HOST', 'localhost')}:{os.getenv('MINIO_PORT', 9000)}"
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', 'minioadmin')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', 'minioadmin')
minio_client = minio.Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)
env_debugger(
    ('MINIO_ENDPOINT', MINIO_ENDPOINT),
    ('MINIO_ACCESS_KEY', MINIO_ACCESS_KEY, 3),
    ('MINIO_SECRET_KEY', MINIO_SECRET_KEY, 3)
)

# MLFlow configuration
os.environ["AWS_ACCESS_KEY_ID"] = MINIO_ACCESS_KEY
os.environ["AWS_SECRET_ACCESS_KEY"] = MINIO_SECRET_KEY
os.environ["MLFLOW_S3_ENDPOINT_URL"] = f"http://{MINIO_ENDPOINT}"
MLFLOW_ENDPOINT = os.getenv('MLFLOW_HOST', 'localhost')
MLFLOW_PORT = os.getenv('MLFLOW_PORT', 5000)
mlflow.set_tracking_uri(f"http://{MLFLOW_ENDPOINT}:{MLFLOW_PORT}")
env_debugger(
    ('MLFLOW_ENDPOINT', MLFLOW_ENDPOINT),
    ('MLFLOW_PORT', MLFLOW_PORT)
)
