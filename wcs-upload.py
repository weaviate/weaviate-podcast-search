import weaviate
from weaviate.util import get_valid_uuid
from uuid import uuid4
import time
import argparse
import json
import os

client = weaviate.Client(
  url="https://my-weaviate-cluster.weaviate.network",  # URL of your Weaviate instance
  additional_headers={
      "X-OpenAI-Api-Key": "sk-foobar",
  }
)

print(client.schema.get())

schema = {
   "classes": [
       {
           "class": "PodClips",
           "description": "A podcast clip.",
           "moduleConfig": {
               "text2vec-openai": {
                    "model": "ada",
                    "modelVersion": "002",
                    "type": "text"
                },
           },
           "vectorIndexType": "hnsw",
           "vectorizer": "text2vec-openai",
           "properties": [
               {
                   "name": "content",
                   "dataType": ["text"],
                   "description": "The text content of the podcast clip",
                   "moduleConfig": {
                    "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": False,
                        "vectorizeClassName": False
                    }
                   }
               },
           ]
       }
   ]
}

client.schema.delete_class("PodClips")
client.schema.create(schema)

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
            new_doc_obj["podNum"] = int(clean_pod_path.strip(".json"))
            corpus.append(new_doc_obj)

doc_upload_start = time.time()
for doc_idx, doc in enumerate(corpus):
    data_properties = {
            "content": doc["content"]
    }
    id = get_valid_uuid(uuid4())
    #client.batch.add_data_object(data_properties, "Document", id, doc_vector)
    client.data_object.create(
        data_object = data_properties,
        class_name = "PodClips",
        uuid=id
    )

print(f"Uploaded {len(corpus)} documents in {time.time() - doc_upload_start} seconds.")