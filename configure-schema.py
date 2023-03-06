import weaviate

client = weaviate.Client("http://localhost:8080")

class_obj = {
    "invertedIndexConfig": {
        "stopwords": { 
            "preset": "en",
            "additions": ["is", "exactly"]                                         
        }
    }
}

client.schema.update_config("PodClip", class_obj)