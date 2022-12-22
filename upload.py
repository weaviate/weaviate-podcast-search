import weaviate
import time
import argparse


import json

f = open("./text-files/vectorized-raw-pod-texts.json")
import json
json_data = json.load(f)
f.close()
json_list = list(json_data)

corpus = []

for json_dict in json_list:
  new_doc_obj = {}
  for key in json_dict.keys():
    new_doc_obj[key] = json_dict[key]
  corpus.append(new_doc_obj)

client = weaviate.Client("http://localhost:8080")

from weaviate.util import generate_uuid5

# batch import, will update this very soon
'''
client.batch.configure(
    batch_size=16,
    dynamic=True,
    timeout_retries=3,
    callback=None,
)
'''

doc_upload_start = time.time()
for doc_idx, doc in enumerate(corpus):
    data_properties = {
        "content": doc["sentence"],
        "podNum": doc["pod_num"]
    }
    id = generate_uuid5(doc_idx)
    doc_vector = doc["vector"]
    #client.batch.add_data_object(data_properties, "Document", id, doc_vector)
    client.data_object.create(
        data_object = data_properties,
        class_name = "PodClip",
        vector = doc_vector,
        uuid=id
    )

print(f"Uploaded {len(corpus)} documents in {time.time() - doc_upload_start} seconds.")