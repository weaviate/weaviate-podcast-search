import weaviate
from weaviate.util import get_valid_uuid
from uuid import uuid4
import time
import argparse
import json
import os

corpus = []

clean_pods_path = "../data/"
for clean_pod_path in os.listdir(clean_pods_path):
    if "DS_Store" not in clean_pod_path:
        f = open(clean_pods_path + clean_pod_path, "r")
        json_data = json.load(f, strict=False)
        f.close()
        for json_dict in json_data:
            new_doc_obj = {"content": json_dict["content"]} # TODO - add vector from cursor backup
            corpus.append(new_doc_obj)

client = weaviate.Client("http://localhost:8080")

doc_upload_start = time.time()
for doc_idx, doc in enumerate(corpus):
    data_properties = {
            "content": doc["content"]
    }
    # TODO - vector from cursor backup
    id = get_valid_uuid(uuid4())
    client.data_object.create(
        data_object = data_properties,
        class_name = "PodClips",
        uuid=id
    ) # TODO - add vector from cursor backup

print(f"Uploaded {len(corpus)} documents in {time.time() - doc_upload_start} seconds.")
