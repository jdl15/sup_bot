import datetime
import hashlib
import io
import os
import tempfile

import tiktoken
from dotenv import load_dotenv
from openai import OpenAI, uploads


class Uploader:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI()
        self.vector_store_id = os.getenv("VECTOR_STORE_ID")
        self.added_count = 0
        self.updated_count = 0
        self.skipped_count = 0

    # def compute_hash(self, file_path):
    def compute_hash(self, content: bytes) -> str:
        return hashlib.md5(content).hexdigest()

    def get_existing_files(self):
        files = self.client.vector_stores.files.list(
            vector_store_id=self.vector_store_id
        )
        existing_files_mapping = {}
        # for file in files.data:
        #     hash = file.attributes.get("hash")
        #     file_name = file.attributes.get("file_name")
        #     if hash and file_name:
        #         existing_files_mapping[file_name] = {"file_id": file.id, "hash": hash}
        while True:
            for file in files.data:
                hash = file.attributes.get("hash")
                file_name = file.attributes.get("file_name")
                if hash and file_name:
                    existing_files_mapping[file_name] = {
                        "file_id": file.id,
                        "hash": hash,
                    }
            if not files.has_more:
                break
            last_id = files.data[-1].id
            files = self.client.vector_stores.files.list(
                vector_store_id=self.vector_store_id, after=last_id
            )

        return existing_files_mapping

    def count_chunks(
        self,
        text,
        chunk_size=int(800),
        overlap=int(400),
        model="text-embedding-3-small",
    ):
        enc = tiktoken.encoding_for_model(model)
        tokens = enc.encode(text)
        total_tokens = len(tokens)
        chunk_count = 0
        start = 0
        while start < total_tokens:
            end = min(start + chunk_size, total_tokens)
            chunk_count += 1
            if end == total_tokens:
                break
            start += chunk_size - overlap

        return chunk_count

    def upload_file(self, article: dict, existing_files):
        chunk = self.count_chunks(article["markdown"])
        file_name = f"{article['slug']}.md"
        file_content = article["markdown"].encode("utf-8")
        file_hash = self.compute_hash(file_content)

        # Check for existing file
        if file_name in existing_files:
            # print("file name:", file_name)
            exist_file = existing_files[file_name]
            if exist_file["hash"] == file_hash:
                self.skipped_count += 1
                return
            delete = self.client.vector_stores.files.delete(
                vector_store_id=self.vector_store_id, file_id=exist_file["file_id"]
            )
            self.client.files.delete(exist_file["file_id"])
            self.updated_count += 1
            print("file delete:", delete)
        else:
            self.added_count += 1

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
        existing_files[file_name] = {"file_id": file_id, "hash": file_hash}
        print(f"{file_name} is uploaded and the estimate chunk is {chunk}")

    def run(self, articles: list[dict]):
        existing_files = self.get_existing_files()
        print(len(existing_files), "existing files found")
        print("timestamp:", datetime.datetime.now())
        for article in articles:
            self.upload_file(article, existing_files)
        print(
            f"Added: {self.added_count}, Updated: {self.updated_count}, Skipped: {self.skipped_count}"
        )
