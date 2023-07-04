import weaviate

client = weaviate.Client("http://localhost:8080")

generatePrompt = """
Please write a short summary of the following podcast clip.
Speaker: {speaker}
Podcast clip: {content}
"""

generate_properties = ["speaker", "content"]

podcast = 55

where_template = {
    "path": ["podNum"],
    "operator": "Equal",
    "valueInt": 0
}

where_template["valueInt"] = podcast

# 10 at a time
get_total_clips = """
{
    Aggregate {
        PodClip (
            where: {
                path: ["podNum"],
                operator: Equal,
                valueInt: 55
            }
        ){
            meta {
                count
            }
        }
    }
}
"""
total_clips = int(client.query.raw(get_total_clips)["data"]["Aggregate"]["PodClip"][0]["meta"]["count"])


for offset in range(0, total_clips, 10):
    summaries = client.query\
        .get("PodClip", generate_properties)\
        .with_generate(single_prompt=generatePrompt)\
        .with_where(where_template)\
        .with_offset(offset)\
        .with_limit(10)\
        .with_additional(["id"])\
        .do()["data"]["Get"]["PodClip"]

    print(f"{summaries}\n")
    print(offset)

    for summary in summaries:
        new_property = {
            "summary": summary["_additional"]["generate"]["singleResult"]
        }
        id = summary["_additional"]["id"]
        client.data_object.update(
            new_property,
            class_name = "PodClip",
            uuid=id
        )
