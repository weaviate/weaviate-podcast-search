import weaviate
import json

client = weaviate.Client("http://localhost:8080")

result = client.backup.restore(
    backup_id="podclips-with-summaries",
    backend='filesystem',
    wait_for_completion=True
)

print(json.dumps(result, indent=4))