import json
from flask import current_app
from google.cloud import storage

storage_client = storage.Client()
bucket_name = 'kongres-383107.appspot.com'


def gs_download(filepath) -> str:
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(filepath)
        s = blob.download_as_string()
        return json.loads(s)
    except Exception as e:
        current_app.logger.error(f"gs_download exception: {e}")


def gs_upload(filepath, s: str):
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(filepath)
        blob.upload_from_string(s)
    except Exception as e:
        current_app.logger.error(f"gs_upload exception: {e}")
