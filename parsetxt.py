f = open("./data/34-text-dump.txt")

content = f.readlines()

all_data = ""
for line in content:
    all_data += line

all_data = all_data.replace("\n", "")
all_data = all_data.replace("  ", " ")
chunked = all_data.split("Connor*")[1:]

transcriptions = []
for chunk in chunked:
    new_chunk = chunk.split("Dmitry*")
    transcriptions.append({
        "speaker": "Connor",
        "content": new_chunk[0]
    })
    transcriptions.append({
        "speaker": "Dmitry",
        "content": new_chunk[1]
    })

import json
json_object = json.dumps(transcriptions, indent=4)
with open("Weaviate-Podcast-34.json", "w") as outfile:
    outfile.write(json_object)