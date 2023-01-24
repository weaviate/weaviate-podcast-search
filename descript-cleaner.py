import re


pod_num = "26"

f = open(f"{pod_num}.txt")

list_content = f.readlines()
f.close()

content = ""
for str_line in list_content:
    content += str_line

speaker1 = "Connor Shorten"
speaker2 = "Jonathan Frankle"
#speaker3 = "Etienne Dilocker"
#speaker4 = "Abdel Rodriguez"

content = re.sub(r"\[.*?\]", "", content)
content = content.replace(f"{speaker1}:", f"*{speaker1}:")
content = content.replace(f"{speaker2}:", f"*{speaker2}:")
#content = content.replace(f"{speaker3}:", f"*{speaker3}:")
#content = content.replace(f"{speaker4}", f"*{speaker4}:")

all_lines = content.split("*")

final_data = []

import json
for line in all_lines:
    if f"{speaker1}:" in line:
        line = line.replace(f"{speaker1}:", "")
        final_data.append({
            "speaker": f"{speaker1}",
            "text": line
        })
    elif f"{speaker2}:" in line:
        line = line.replace(f"{speaker2}:", "")
        final_data.append({
            "speaker": f"{speaker2}",
            "text": line
        })
    '''
    elif f"{speaker3}:" in line:
        line = line.replace(f"{speaker3}:", "")
        final_data.append({
            "speaker": f"{speaker3}",
            "text": line
        })
    elif f"{speaker4}:" in line:
        line = line.replace(f"{speaker4}:", "")
        final_data.append({
            "speaker": f"{speaker4}",
            "text": line
        })
    '''

with_data_key = {"data": final_data}

json_object = json.dumps(with_data_key, indent=4)
with open(f"../speaker-labels/{pod_num}.json", "w") as outfile:
    outfile.write(json_object)
