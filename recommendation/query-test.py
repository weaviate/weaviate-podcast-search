import weaviate

client = weaviate.Client("http://localhost:8080")

query_str = """
    {
        Get {
            PodClip {
            _additional {
                vector
            }
        }
    }
    }
"""

#print(client.query.raw(query_str))

print(len(client.query.raw(query_str)["data"]["Get"]["PodClip"][0]["_additional"]["vector"]))
