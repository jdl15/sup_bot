import hashlib
import io
import os

import tiktoken
from dotenv import load_dotenv
from openai import OpenAI


class Uploader:

    def __init__(self, chunk_size=700, overlap=300, model="text-embedding-3-large"):
        load_dotenv()
        self.client = OpenAI()
        self.vector_store_id = os.getenv("VECTOR_STORE_ID")
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.model = model
        self.added_count = 0
        self.updated_count = 0
        self.skipped_count = 0
        self.file_status = False
        self.files = 0

    # compute unique hash for file content
    def compute_hash(self, content: bytes) -> str:
        return hashlib.md5(content).hexdigest()

    # return existing files in the vector store and obtain their file_id and hash for comparison
    def get_existing_files(self) -> dict[str, dict[str, str]]:
        files = self.client.vector_stores.files.list(
            vector_store_id=self.vector_store_id
        )
        existing_files_mapping = {}
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

    # chunk the article
    def chunk_text(self, text: str) -> list[str]:
        enc = tiktoken.encoding_for_model(self.model)
        tokens = enc.encode(text)
        chunks = []
        start = 0
        while start < len(tokens):
            end = min(start + self.chunk_size, len(tokens))
            chunk_tokens = tokens[start:end]
            chunk_text = enc.decode(chunk_tokens)
            chunks.append(chunk_text)
            if end == len(tokens):
                break
            start += self.chunk_size - self.overlap
        return chunks

    # Prepend URL to each chunk
    def attach_url_to_chunks(self, chunks: list[str], url: str) -> list[str]:
        return [f"Article URL: {url}\n\n{chunk}" for chunk in chunks]

    # handle the upload for each chunk
    def upload_chunk(
        self,
        chunk_text: str,
        chunk_name: str,
        existing_files: dict,
    ):
        chunk_bytes = chunk_text.encode("utf-8")
        chunk_hash = self.compute_hash(chunk_bytes)

        if chunk_name in existing_files:
            existing = existing_files[chunk_name]
            if existing["hash"] == chunk_hash:
                self.skipped_count += 1
                return
            # Delete old chunk
            self.client.vector_stores.files.delete(
                vector_store_id=self.vector_store_id, file_id=existing["file_id"]
            )
            self.client.files.delete(existing["file_id"])
            self.updated_count += 1
            self.file_status = True
        else:
            self.added_count += 1
            self.file_status = True

        file_obj = io.BytesIO(chunk_bytes)
        file_obj.name = chunk_name
        uploaded_file = self.client.files.create(file=file_obj, purpose="assistants")
        self.client.vector_stores.files.create(
            vector_store_id=self.vector_store_id,
            file_id=uploaded_file.id,
            attributes={
                "hash": chunk_hash,
                "file_name": chunk_name,
            },
        )
        existing_files[chunk_name] = {"file_id": uploaded_file.id, "hash": chunk_hash}

    # process the article
    def upload_article(self, article: dict, existing_files: dict):
        chunks = self.chunk_text(article["markdown"])
        chunks = self.attach_url_to_chunks(chunks, article["url"])
        print(len(chunks), "chunks found for", article["slug"])
        new_chunk_names = []
        for i, chunk in enumerate(chunks):
            chunk_name = f"{article['slug']}_chunk{i+1}.md"
            new_chunk_names.append(chunk_name)
            self.upload_chunk(chunk, chunk_name, existing_files)
        if self.file_status:
            self.files += 1
            self.file_status = False
        # handle the case if the new article shrinks
        old_chunks = []
        for name in existing_files.keys():
            if name.startswith(article["slug"]):
                old_chunks.append(name)
        for old_chunk in old_chunks:
            if old_chunk not in new_chunk_names:
                file_id = existing_files[old_chunk]["file_id"]
                self.client.vector_stores.files.delete(
                    vector_store_id=self.vector_store_id, file_id=file_id
                )
                self.client.files.delete(file_id)
                del existing_files[old_chunk]
                print(f"Deleted stale chunk: {old_chunk}")

    def run(self, articles: list[dict]):
        existing_files = self.get_existing_files()
        print(len(existing_files), "existing chunks found in vector store.")
        for article in articles:
            self.upload_article(article, existing_files)
        print(
            f"Files Added or Updated: {self.files}, Chunks Added: {self.added_count}, Chunks Updated: {self.updated_count}, Chunks Skipped: {self.skipped_count}"
        )
