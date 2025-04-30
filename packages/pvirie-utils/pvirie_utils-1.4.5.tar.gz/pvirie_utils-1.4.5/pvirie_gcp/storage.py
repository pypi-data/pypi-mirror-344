from . import gcp
from google.cloud import storage 

# Access Cloud Storage

def get_session(credentials=None):
    if credentials is None:
        credentials = gcp.get_credentials()
    storage_client = storage.Client(credentials=credentials)
    return storage_client


class GCS:
    def __init__(self, bucket_name, credentials=None):
        self.session = get_session(credentials)
        self.bucket_name = bucket_name
        self.bucket = self.session.bucket(bucket_name)


    def upload_file(self, local_file_path, gcs_blob_name):
        """
        Upload a file to Google Cloud Storage.
        """
        blob = self.bucket.blob(gcs_blob_name)
        blob.upload_from_filename(local_file_path)
        print(f"Uploaded {local_file_path} to {gcs_blob_name} in bucket {self.bucket_name}")


    def upload_bytes(self, data: bytes, gcs_blob_name):
        """
        Upload bytes to Google Cloud Storage.
        """
        blob = self.bucket.blob(gcs_blob_name)
        blob.upload_from_string(data)
        print(f"Uploaded bytes to {gcs_blob_name} in bucket {self.bucket_name}")


    def download_file(self, gcs_blob_name, local_file_path):
        """
        Download a file from Google Cloud Storage.
        """
        blob = self.bucket.blob(gcs_blob_name)
        blob.download_to_filename(local_file_path)
        print(f"Downloaded {gcs_blob_name} from bucket {self.bucket_name} to {local_file_path}")


    def list_blobs(self, prefix=None):
        """
        List blobs in the bucket with an optional prefix.
        """
        blobs = self.bucket.list_blobs(prefix=prefix)
        for blob in blobs:
            yield blob.name
    

    def probe_size(self, prefix=None):
        """
        Calculate the total size of blobs in the bucket with an optional prefix.
        """
        total_size = 0
        blobs = self.bucket.list_blobs(prefix=prefix)
        for blob in blobs:
            yield blob.name, blob.size


    def generate_presigned_url(self, gcs_blob_name, expiration=3600):
        """
        Generate a presigned URL for a blob in the bucket.
        """
        blob = self.bucket.blob(gcs_blob_name)
        url = blob.generate_signed_url(expiration=expiration)
        return url
    

    def delete_blob(self, gcs_blob_name):
        """
        Delete a blob from the bucket.
        """
        blob = self.bucket.blob(gcs_blob_name)
        blob.delete()
        print(f"Deleted {gcs_blob_name} from bucket {self.bucket_name}")


    def delete_blobs(self, blob_names):
        """
        Delete multiple blobs from the bucket.
        """
        for blob_name in blob_names:
            self.delete_blob(blob_name)
