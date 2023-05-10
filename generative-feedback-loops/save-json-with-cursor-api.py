import weaviate

client = weaviate.Client("http://localhost:8080")

get_first_object_weaviate_query = """
{
  Get {
    PodClip(
      sort: 
      [{
        path: ["_creationTimeUnix"], 
        order: desc
      }]){
      _additional {
        id
      }
    }
  }
}
"""

results = client.query.raw(get_first_object_weaviate_query)
first_inserted_uuid = results["data"]["Get"]["PodClip"][0]["_additional"]["id"]

result = (
    client.query.get("PodClip", ["content", "speaker", "podNum", "summary"])
    .with_additional(["id"])
    .with_limit(500)
    .with_after(first_inserted_uuid)
    .do()
)

print(len(result["data"]["Get"]["PodClip"]))

