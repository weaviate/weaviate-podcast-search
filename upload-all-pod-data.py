import weaviate
from weaviate.util import get_valid_uuid
from uuid import uuid4
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
            new_doc_obj["podNum"] = int(clean_pod_path.strip(".json"))
            corpus.append(new_doc_obj)

client = weaviate.Client("http://localhost:8080")

podNums_uploaded = set()

doc_upload_start = time.time()

podcast_ID = 0
for doc_idx, doc in enumerate(corpus):
    clip_props = {
            "content": doc["content"],
            "speaker": doc["speaker"],
            "podNum": doc["podNum"]
    }
    if "clipNumber" in doc.keys():
        clip_props["clipNumber"]  = doc["clipNumber"]
    clip_id = get_valid_uuid(uuid4())
    #client.batch.add_data_object(data_properties, "Document", id, doc_vector)
    client.data_object.create(
        data_object = clip_props,
        class_name = "PodClip",
        uuid=clip_id
    )
    if doc["podNum"] not in podNums_uploaded:
        podcast_ID = get_valid_uuid(uuid4())
        podcast_props = {"podNum": doc["podNum"]}
        # create podcast object
        client.data_object.create(
            data_object = podcast_props,
            class_name = "Podcast",
            uuid=podcast_ID
        )
        podNums_uploaded.add(doc["podNum"])
    # add cref from clipID to podcastID
    client.data_object.reference.add(
        from_class_name="PodClip",
        from_uuid=clip_id,
        from_property_name="inPodcast",
        to_class_name="Podcast",
        to_uuid=podcast_ID
    )
    # add cref from podcastID to clipID
    client.data_object.reference.add(
        from_class_name="Podcast",
        from_uuid=podcast_ID,
        from_property_name="hasClip",
        to_class_name="PodClip",
        to_uuid=clip_id        
    )



print(f"Uploaded {len(corpus)} documents in {time.time() - doc_upload_start} seconds.")
