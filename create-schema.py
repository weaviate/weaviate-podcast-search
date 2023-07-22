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
                },
                "generative-openai": {
                    "model": "text-davinci-003"
                }
           },
           "vectorIndexType": "hnsw",
           "vectorizer": "text2vec-transformers",
           "properties": [
               {
                   "name": "summary",
                   "dataType": ["text"],
                   "description": "An LLM-generated summary of the podcast clip.",
                   "moduleConfig": {
                       "text2vec-transformers": {
                           "skip": True,
                           "vectorizePropertyName": False,
                           "vectorizeClassName": False
                       }
                   }
               },
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
                "dataType": ["text"],
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
                   "name": "clipNumber",
                   "dataType": ["int"],
                   "description": "The clip number within the podcast.",
                   "moduleConfig": {
                    "text2vec-transformers": {
                        "skip": True,
                        "vectorizePropertyName": False,
                        "vectorizeClassName": False
                    }
                   }
               },
               {
                "name": "inPodcast",
                "dataType": ["Podcast"],
                "description": "The podcast this clip was sourced from.",
                "moduleConfig": {
                    "text2vec-transformers": {
                        "skip": True,
                        "vectorizePropertyName": False,
                        "vectorizeClassName": False
                    }
                }
               },
               {
                "name": "inChapter",
                "dataType": ["Chapter"],
                "description": "The chapter this clip is associated with.",
                "moduleConfig": {
                    "text2vec-transformers": {
                        "skip": True,
                        "vectorizePropertyName": False,
                        "vectorizeClassName": False
                    }
                }
               }
           ]
       },
       {
        "class": "Podcast",
           "description": "A Weaviate Podcast!",
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
                   "name": "summary",
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
                "name": "hasClip",
                "dataType": ["PodClip"],
                "description": "A clip contained in the podcast",
                "moduleConfig": {
                    "text2vec-transformers": {
                        "skip": True,
                        "vectorizePropertyName": False,
                        "vectorizeClassName": False
                    }
                }
               },
               {
                "name": "hasChapter",
                "dataType": ["Chapter"],
                "description": "A chapter contained in the podcast",
                "moduleConfig": {
                    "text2vec-transformers": {
                        "skip": True,
                        "vectorizePropertyName": False,
                        "vectorizeClassName": False
                    }
                }
               }
           ]
       },
       {
           "class": "Chapter",
           "description": "A Podcast Chapter",
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
                   "name": "description",
                   "dataType": ["text"],
                   "description": "A description of the chapter",
                   "moduleConfig": {
                       "text2vec-transformers": {
                           "skip": False,
                           "vectorizePropertyName": False,
                           "vectorizeClassName": False
                       }
                   }
               },
               {
                   "name": "title",
                   "dataType": ["text"],
                   "description": "The title of the chapter",
                   "moduleConfig": {
                       "text2vec-transformers": {
                           "skip": True,
                           "vectorizePropertyName": False,
                           "vectorizeClassName": False
                       }
                   }
               },
               {
                   "name": "timeStart",
                   "dataType": ["int"],
                   "description": "The timestamp where this chapter begins",
                   "moduleConfig": {
                       "text2vec-transformers": {
                           "skip": True,
                           "vectorizePropertyName": False,
                           "vectorizeClassName": False
                       }
                   }
               },
               {
                   "name": "timeEnd",
                   "dataType": ["int"],
                   "description": "The title of the chapter",
                   "moduleConfig": {
                       "text2vec-transformers": {
                           "skip": True,
                           "vectorizePropertyName": False,
                           "vectorizeClassName": False
                       }
                   }
               },
               {
                   "name": "duration",
                   "dataType": ["int"],
                   "description": "The title of the chapter",
                   "moduleConfig": {
                       "text2vec-transformers": {
                           "skip": True,
                           "vectorizePropertyName": False,
                           "vectorizeClassName": False
                       }
                   }
               },
               {
                   "name": "fromPodcast",
                   "dataType": ["Podcast"],
                   "description": "The podcast this chapter was sourced from.",
                   "moduleConfig": {
                       "text2vec-transformers": {
                           "skip": True,
                           "vectorizePropertyName": False,
                           "vectorizeClassName": False
                       }
                   }
               },
               {
                   "name": "hasClip",
                   "dataType": ["PodClip"],
                   "description": "Podcast clips associated with this chapter.",
                   "moduleConfig": {
                       "text2vec-transformers": {
                           "skip": True,
                           "vectorizePropertyName": False,
                           "vectorizeClassName": False
                       }
                   }
               }
           ]
       }
   ]
}

client.schema.create(schema)