'''
This example will show you how to get all of your data
out of Weaviate and into a JSON file using the Cursor API!
'''
import weaviate
import json
import time
start = time.time()

client = weaviate.Client("http://localhost:8080")

# Step 1 - Get the UUID of the first object inserted into Weaviate

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
uuid_cursor = results["data"]["Get"]["PodClip"][0]["_additional"]["id"]

# Step 2 - Get the Total Objects in Weaviate

total_objs_query = """
{
    Aggregate {
        PodClip {
            meta {
                count
            }
        }
    }
}
"""

results = client.query.raw(total_objs_query)
total_objects = results["data"]["Aggregate"]["PodClip"][0]["meta"]["count"]

# Step 3 - Iterate through Weaviate with the Cursor
increment = 50
data = []
for i in range(0, total_objects, increment):
    results = (
        client.query.get("PodClip", ["content", "speaker", "podNum"])
        .with_additional(["id", "vector"])
        .with_limit(50)
        .with_after(uuid_cursor)
        .do()
    )["data"]["Get"]["PodClip"]
    # extract data from result into JSON
    for result in results:
        new_obj = {}
        for key in result.keys():
            if key == "_additional":
                new_obj["_additional"] = {}
                for additionalKey in result[key].keys():
                    new_obj["_additional"][additionalKey] = result[key][additionalKey]
            new_obj[key] = result[key]
        data.append(new_obj)
    # update uuid cursor to continue the loop
    # we have just exited a loop where result holds the last obj
    uuid_cursor = result["_additional"]["id"]

# save JSON
file_path = "my_data.json"
with open(file_path, 'w') as json_file:
    json.dump(data, json_file)

print("Your data is out of Weaviate!")
print(f"Extracted {total_objects} in {time.time() - start} seconds.")

import pandas as pd

# Load data from a JSON file
df = pd.read_json('my_data.json')

# Display the DataFrame
print(len(df))
print(df.head(5))
