import weaviate
import time

client = weaviate.Client("http://localhost:8080")

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

client.schema.create(schema)