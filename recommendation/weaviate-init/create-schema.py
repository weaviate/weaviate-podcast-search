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
                "name": "speaker",
                "dataType": ["string"],
                "description": "The speaker in the podcast",
                "moduleConfig": {
                    "text2vec-transformers": {
                        "skip": True,
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
               {
                "name": "summary",
                "dataType": ["text"],
                "description": "An LLM-generated summary of a podcast clip.",
                "moduleConfig": {
                    "text2vec-transformers": {
                        "skip": True,
                        "vectorizePropertyName": False,
                        "vectorizeClassName": False
                    }
                   }
               }
           ]
       },{
          "class": "User",
          "description": "A user of the podcast recommendation app.",
          "properties": [
            {
                "name": "sessionNumber",
                "description": "May Deprecate.",
                "dataType": ["int"]
            },{
                "name": "likedClip",
                "description": "Creef to liked clips, used to vectorize User.",
                "dataType": ["PodClip"]
            }
          ],
          "moduleConfig": {
            "ref2vec-centroid": {
                "referenceProperties": ["likedClip"]
            }
          },
          "vectorizer": "ref2vec-centroid"
       }
   ]
}

client.schema.create(schema)