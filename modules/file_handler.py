import os
import boto3
import requests

class FileHandler:
    def __init__(self, s3_bucket="your-s3-bucket-name"):
        self.s3_client = boto3.client("s3")
        self.s3_bucket = s3_bucket

    def save_file_locally(self, file, save_path):
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        file.save(save_path)
        return save_path

    def upload_to_s3(self, file_path):
        file_name = os.path.basename(file_path)
        self.s3_client.upload_file(file_path, self.s3_bucket, file_name)
        return f"https://{self.s3_bucket}.s3.amazonaws.com/{file_name}"
    
    def download_from_s3(self, file_name, download_path):
        self.s3_client.download_file(self.s3_bucket, file_name, download_path)
        return download_path
    
    def upload_to_autodesk(self, file_path, access_token):
        url = "https://developer.api.autodesk.com/oss/v2/buckets/your-bucket-name/objects/" + os.path.basename(file_path)
        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/octet-stream"}
        with open(file_path, "rb") as file_data:
            response = requests.put(url, headers=headers, data=file_data)
        return response.json()
    
if __name__ == "__main__":
    handler = FileHandler()
    handler.upload_to_s3("test_file.rcp")

