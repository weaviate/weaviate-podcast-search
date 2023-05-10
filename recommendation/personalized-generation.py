import weaviate
from backend.queries import get_user_vector_and_clicks
import argparse

client = weaviate.Client("http://localhost:8080")

generateTask = """
Please write a summary of this podcast based on the following podcast clips.
"""

parser = argparse.ArgumentParser(description="User ID for Generation")
parser.add_argument("--userid", type=str)
args = parser.parse_args()

myVector = {
    "vector": get_user_vector_and_clicks(args.userid, client)[0]
}

summary = client.query\
    .get("PodClip", ["summary"])\
    .with_generate(grouped_task=generateTask)\
    .with_near_vector(myVector)\
    .with_limit(1)\
    .do()

print(summary["data"]["Get"]["PodClip"][0]["_additional"]["generate"]["groupedResult"])