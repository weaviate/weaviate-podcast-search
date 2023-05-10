import weaviate

client = weaviate.Client("http://localhost:8080")

generatePrompt = """
Please write a 1 or 2 sentence summary of the following podcast clip.
Speaker: {speaker}
Podcast clip: {content}
"""

generate_properties = ["speaker", "content"]

podcasts = [25,26,27,28,30,31,32,33,34,35,36]

where_template = {
    "path": ["podNum"],
    "operator": "Equal",
    "valueInt": 0
}

for podcast in podcasts:
    where_template["valueInt"] = podcast

    summaries = client.query\
            .get("PodClip", generate_properties)\
            .with_generate(single_prompt=generatePrompt)\
            .with_where(where_template)\
            .with_additional(["id"])\
            .do()["data"]["Get"]["PodClip"]

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