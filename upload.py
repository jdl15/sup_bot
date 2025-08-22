import hashlib
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

# Load API key from .env
load_dotenv()
# api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()
vector_store_id = os.getenv("VECTOR_STORE_ID")
mapping_file = "file_mapping.json"

# Load previous mapping
if os.path.exists(mapping_file):
    with open(mapping_file, "r") as f:
        file_mapping = json.load(f)  # convert
else:
    file_mapping = {}

for file_name in os.listdir("support/"):
    if not file_name.endswith(".md"):
        continue
    file_path = os.path.join("support/", file_name)

    # Compute hash
    with open(file_path, "rb") as f:
        content = f.read()
        file_hash = hashlib.md5(content).hexdigest()

    # file name already exist in mapping
    if file_name in file_mapping:
        exist_file = file_mapping[file_name]
        # file doesn't change
        if exist_file["hash"] == file_hash:
            continue
        # file change, delete from vector store and general storage
        client.vector_stores.files.delete(
            vector_store_id=vector_store_id, file_id=exist_file["file_id"]
        )
        client.files.delete(exist_file["file_id"])

    # Upload
    with open(file_path, "rb") as f:
        uploaded_file = client.files.create(file=f, purpose="assistants")
        file_id = uploaded_file.id

    # Attach to vector store
    vs_file = client.vector_stores.files.create(
        vector_store_id=vector_store_id, file_id=file_id
    )

    # Update mapping
    file_mapping[file_name] = {"hash": file_hash, "file_id": file_id}

with open(mapping_file, "w") as f:
    json.dump(file_mapping, f, indent=2)
