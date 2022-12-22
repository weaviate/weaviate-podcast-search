import weaviate
import json

w1 = weaviate.Client("http://localhost:8080")

# add an extra check to make sure we aren't overwriting an existing backup!!

result = w1.backup.create(
    backup_id="weaviate-pod",
    backend='filesystem',
)

print(json.dumps(result, indent=4))