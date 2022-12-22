import weaviate
import time

client = weaviate.Client("http://localhost:8080")

schema = {
   "classes": [
       {
           "class": "PodClip",
           "description": "A podcast clip.",
           "moduleConfig": {
               "text2vec-transformers": {
                    "skip": False,
                    "vectorizeClassName": False,
                    "vectorizePropertyName": False
                }
           },
           "vectorIndexType": "hnsw",
           "vectorizer": "text2vec-transformers",
           "properties": [
               {
                   "name": "content",
                   "dataType": ["text"],
                   "description": "The text content of the podcast clip",
                   "moduleConfig": {
                    "text2vec-transformers": {
                        "skip": False,
                        "vectorizePropertyName": False,
                        "vectorizeClassName": False
                    }
                   }
               },
               {
                   "name": "podNum",
                   "dataType": ["int"],
                   "description": "The podcast number.",
                   "moduleConfig": {
                    "text2vec-transformers": {
                        "skip": True,
                        "vectorizePropertyName": False,
                        "vectorizeClassName": False
                    }
                   }
               },
           ]
       }
   ]
}

client.schema.create(schema)