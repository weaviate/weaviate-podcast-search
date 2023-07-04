podNumber = "55"

f = open(f"./{podNumber}-clean-text.txt")

content = f.readlines()

all_data = ""
for line in content:
    all_data += line

all_data = all_data.replace("\n", "")
all_data = all_data.replace("  ", " ")

speaker1 = "Connor"
speaker2 = "Aleksa"
#speaker3 = "Gunjan"
#speaker4 = "Marco"



chunked = all_data.split("*")

transcriptions = []
for counter, line in enumerate(chunked):
    print(line)
    line = line.replace('\u2019', '')
    print("\n")
    if f"{speaker1}:" in line:
        line = line.replace(f"{speaker1}:", "")
        transcriptions.append({
            "speaker": f"{speaker1} Shorten",
            "content": line,
            "podNumber": int(podNumber),
            "clipNumber": counter
        })
    elif f"{speaker2}:" in line:
        line = line.replace(f"{speaker2}:", "")
        transcriptions.append({
            "speaker": f"{speaker2} Gordcic",
            "content": line,
            "podNumber": int(podNumber),
            "clipNumber": counter
        })
    '''
    elif f"{speaker3}:" in line:
        line = line.replace(f"{speaker3}:", "")
        transcriptions.append({
            "speaker": f"{speaker3} Bhattarai",
            "content": line,
            "podNumber": int(podNumber),
            "clipNumber": counter
        })
    '''
    '''
    elif f"{speaker4}:" in line:
        line = line.replace(f"{speaker4}:", "")
        transcriptions.append({
            "speaker": f"{speaker4} Bianco",
            "content": line,
            "podNumber": int(podNumber),
            "clipNumber": counter
        })
    '''


import json
json_object = json.dumps(transcriptions, indent=4)
with open(f"data/{podNumber}.json", "w") as outfile:
    outfile.write(json_object)
