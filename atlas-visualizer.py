import weaviate
from nomic import AtlasProject
import numpy as np
import nomic

nomic.login("my-nomic-token")

client = weaviate.Client("http://localhost:8080")

schema = client.schema.get()


classes = ["PodClips"]
props = ["content"]

def get_batch_with_cursor(
    client, class_name, class_properties, batch_size, cursor=None
):
    query = (
        client.query.get(class_name, class_properties)
        .with_additional(["vector", "id"])
        .with_limit(batch_size)
    )

    if cursor is not None:
        return query.with_after(cursor).do()
    else:
        return query.do()


for c, p in zip(classes, props):
    project = AtlasProject(
        name=c,
        unique_id_field="id",
        modality="embedding",
    )
    count = 0
    cursor = None
    while True:
        response = get_batch_with_cursor(client, c, p, 10000, cursor)
        count += 1
        if len(response["data"]["Get"][c]) == 0:
            break
        cursor = response["data"]["Get"][c][-1]["_additional"]["id"]
        vectors = []
        for i in response["data"]["Get"][c]:
            vectors.append(i["_additional"]["vector"])

        embeddings = np.array(vectors)
        data = []
        not_data = ["_additional"]
        un_data = ["vector"]
        for i in response["data"]["Get"][c]:
            j = {key: value for key, value in i.items() if key not in not_data}
            k = {
                key: value
                for key, value in i["_additional"].items()
                if key not in un_data
            }
            j = j | k
            data.append(j)
        with project.wait_for_project_lock():
            project.add_embeddings(
                embeddings=embeddings,
                data=data,
            )
    project.rebuild_maps()
    project.create_index(
        name=c,
        topic_label_field='content',
        colorable_fields=[p],
        build_topic_model=True,
    )