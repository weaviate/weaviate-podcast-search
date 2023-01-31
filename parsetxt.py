podNumber = "25"

f = open(f"./text-data/{podNumber}-text-dump.txt")

content = f.readlines()

all_data = ""
for line in content:
    all_data += line

all_data = all_data.replace("\n", "")
all_data = all_data.replace("  ", " ")

speaker1 = "Connor"
speaker2 = "Erik"
speaker3 = "Etienne"
#speaker4 = "Marco"



chunked = all_data.split("*")

transcriptions = []
for line in chunked:
    print(line)
    print("\n")
    if f"{speaker1}:" in line:
        line = line.replace(f"{speaker1}:", "")
        transcriptions.append({
            "speaker": f"{speaker1} Shorten",
            "content": line,
            "podNumber": int(podNumber)
        })
    elif f"{speaker2}:" in line:
        line = line.replace(f"{speaker2}:", "")
        transcriptions.append({
            "speaker": f"{speaker2} Bernhardsson",
            "content": line,
            "podNumber": int(podNumber)
        })
    elif f"{speaker3}:" in line:
        line = line.replace(f"{speaker3}:", "")
        transcriptions.append({
            "speaker": f"{speaker3} Dilocker",
            "content": line,
            "podNumber": int(podNumber)
        })
    '''
    elif f"{speaker4}:" in line:
        line = line.replace(f"{speaker4}:", "")
        transcriptions.append({
            "speaker": f"{speaker4} Bianco",
            "content": line,
            "podNumber": int(podNumber)
        })
    '''


import json
json_object = json.dumps(transcriptions, indent=4)
with open(f"data/Weaviate-Podcast-{podNumber}.json", "w") as outfile:
    outfile.write(json_object)
