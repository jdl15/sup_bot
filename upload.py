import hashlib
import io
import os

from dotenv import load_dotenv
from openai import OpenAI


class Uploader:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI()
        self.vector_store_id = os.getenv("VECTOR_STORE_ID")

    # def compute_hash(self, file_path):
    def compute_hash(self, content: str) -> str:
        return hashlib.md5(content).hexdigest()

    def get_existing_files(self):
        files = self.client.vector_stores.files.list(
            vector_store_id=self.vector_store_id
        )
        existing_files_mapping = {}
        for file in files.data:
            hash = file.attributes.get("hash")
            file_name = file.attributes.get("file_name")
            if hash and file_name:
                existing_files_mapping[file_name] = {"file_id": file.id, "hash": hash}
        return existing_files_mapping

    def upload_file(self, article: dict, existing_files):
        file_name = f"{article['slug']}.md"
        file_content = article["markdown"].encode("utf-8")
        file_hash = self.compute_hash(file_content)
        # Check for existing file
        if file_name in existing_files:
            print("file name:", file_name)
            exist_file = existing_files[file_name]
            if exist_file["hash"] == file_hash:
                print("File already exists nothing change so skip")
                return
            else:
                delete = self.client.vector_stores.files.delete(
                    vector_store_id=self.vector_store_id, file_id=exist_file["file_id"]
                )
                self.client.files.delete(exist_file["file_id"])
                print("file delete:", delete)

        # Upload file
        file_obj = io.BytesIO(file_content)
        file_obj.name = file_name
        uploaded_file = self.client.files.create(file=file_obj, purpose="assistants")
        file_id = uploaded_file.id

        # Attach to vector store
        self.client.vector_stores.files.create(
            vector_store_id=self.vector_store_id,
            file_id=file_id,
            attributes={
                "hash": file_hash,
                "file_name": file_name,
                "url": article["url"],
            },
        )
        print(file_name, file_id, file_hash)

    def run(self, articles: list[dict]):
        existing_files = self.get_existing_files()

        for article in articles:
            self.upload_file(article, existing_files)
