import weaviate
import time
import argparse


import json
import os

corpus = []

clean_pods_path = "./data/"
for clean_pod_path in os.listdir(clean_pods_path):
    if "DS_Store" not in clean_pod_path:
        f = open(clean_pods_path + clean_pod_path, "r")
        json_data = json.load(f, strict=False)
        f.close()
        for json_dict in json_data:
            new_doc_obj = {}
            for key in json_dict.keys():
                new_doc_obj[key] = json_dict[key]
            new_doc_obj["podNum"] = int(clean_pod_path.replace("Weaviate-Podcast-", "").strip(".json"))
            corpus.append(new_doc_obj)

client = weaviate.Client("http://localhost:8080")

from weaviate.util import generate_uuid5

doc_upload_start = time.time()
for doc_idx, doc in enumerate(corpus):
    data_properties = {
        "content": doc["content"],
        "speaker": doc["speaker"],
        "podNum": doc["podNum"]
    }
    id = generate_uuid5(doc_idx)
    #client.batch.add_data_object(data_properties, "Document", id, doc_vector)
    client.data_object.create(
        data_object = data_properties,
        class_name = "PodClip",
        uuid=id
    )

print(f"Uploaded {len(corpus)} documents in {time.time() - doc_upload_start} seconds.")