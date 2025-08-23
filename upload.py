import datetime
import hashlib
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


class Uploader:
    def __init__(
        self,
        support_dir="support",
        mapping_file="file_mapping.json",
        url_mapping_file="url_mapping.json",
        logs_dir="logs",
    ):
        load_dotenv()
        self.client = OpenAI()
        self.vector_store_id = os.getenv("VECTOR_STORE_ID")
        self.support_dir = Path(support_dir)
        self.mapping_file = Path(mapping_file)
        self.url_mapping_file = Path(url_mapping_file)
        self.logs_dir = Path(logs_dir)
        self.added_count = 0
        self.updated_count = 0
        self.skipped_count = 0
        self.processed_files = []

        # Load previous mappings
        if os.path.exists(self.mapping_file):
            with open(self.mapping_file, "r", encoding="utf-8") as f:
                self.file_mapping = json.load(f)
        else:
            self.file_mapping = {}
        if os.path.exists(self.url_mapping_file):
            with open(self.url_mapping_file, "r", encoding="utf-8") as f:
                self.url_mapping = json.load(f)
        else:
            self.url_mapping = {}

    def compute_hash(self, file_path):
        with open(file_path, "rb") as f:
            content = f.read()
            return hashlib.md5(content).hexdigest()

    def upload_file(self, file_path):
        file_name = file_path.name
        file_hash = self.compute_hash(file_path)

        # Check for existing file
        if file_name in self.file_mapping:
            exist_file = self.file_mapping[file_name]
            if exist_file["hash"] == file_hash:
                self.skipped_count += 1
                return
            # delete previous version
            self.updated_count += 1
            self.client.vector_stores.files.delete(
                vector_store_id=self.vector_store_id, file_id=exist_file["file_id"]
            )
            self.client.files.delete(exist_file["file_id"])
        else:
            self.added_count += 1

        # Upload file
        with open(file_path, "rb") as f:
            uploaded_file = self.client.files.create(file=f, purpose="assistants")
            file_id = uploaded_file.id

        # Attach to vector store
        self.client.vector_stores.files.create(
            vector_store_id=self.vector_store_id,
            file_id=file_id,
            attributes={"url": self.url_mapping.get(file_name)},
        )

        # Update mapping
        self.file_mapping[file_name] = {"hash": file_hash, "file_id": file_id}
        self.processed_files.append(
            {
                "file_name": file_name,
                "file_id": file_id,
            }
        )

    def run(self):
        for file_path in self.support_dir.glob("*.md"):
            self.upload_file(file_path)
        # save mapping
        with open(self.mapping_file, "w", encoding="utf-8") as f:
            json.dump(self.file_mapping, f, indent=2)
        self.logs_dir.mkdir(exist_ok=True)
        log_file = (
            self.logs_dir
            / f"last_run_{datetime.datetime.now().strftime('%Y%m%dT%H%M%S')}.json"
        )
        log = {
            "timestamp": datetime.datetime.now().strftime("%Y%m%dT%H%M%S"),
            "added": self.added_count,
            "updated": self.updated_count,
            "skipped": self.skipped_count,
            "files": self.processed_files,
        }
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(log, f, indent=2)
