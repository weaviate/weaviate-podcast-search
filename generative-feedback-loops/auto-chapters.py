import weaviate
from weaviate.util import get_valid_uuid
from uuid import uuid4
import os
import openai
import json

client = weaviate.Client("http://localhost:8080")

openai.api_key = "sk-foobar"

def openai_call(prompt):
    ''''
    # Didn't find great results with this.
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": prompt
            }
        ]
    ).choices[0].message["content"]
    '''
    try:
      return openai.Completion.create(
          model="text-davinci-003",
          prompt=prompt,
          temperature=0,
          max_tokens=2048,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0
      )["choices"][0]["text"]
    except:
       return openai_call(prompt)

get_clips_query = """
{
	Get {
    PodClip (
      where: {
        path: ["podNum"],
        operator: Equal,
        valueInt: 55
      },
    	sort: {
        path: ["clipNumber"],
        order: asc
      }
    ){
      summary
      speaker
      clipNumber
      _additional {
        id
      }
    }
  }
}
"""

clips = client.query.raw(get_clips_query)["data"]["Get"]["PodClip"]

#print(clips)

chapters = []

current_topic = {
  "chapter": "INTRODUCTION",
  "start": 0,
  "end": "",
  "podclipIDs": []
}

for idx in range(1, len(clips)-1):
    template = """
    Your task is to annotate chapters in a podcast.

    You will receive a podcast clip and the current chapter topic.

    IF the conversation in the clip discusses the same topic, PLEASE OUTPUT 0
    IF the content in the clip is very short such as a joke or a "thank you" or something minor like this, PLEASE OUTPUT 0

    However, if the conversation in the clip discusses a new topic, PLEASE OUTPUT 1

    The current topic is: %s

    You will receive the current clip, as well as the previous and next clip for additional reference.
    PREVIOUS CLIP: %s
    NEXT CLIP: %s
    CURRENT CLIP: %s

    As a reminder, please ONLY output either 0 or 1 as described above.
    """ % (current_topic["chapter"], clips[idx-1]["summary"], clips[idx]["summary"], clips[idx+1]["summary"])

    topic_response = int(openai_call(template))

    if topic_response == 1:
       current_topic["end"] = idx
       chapters.append(current_topic)
       new_topic_prompt = """
       Please write an abstract description of the conversation topic discussed in the current podcast clip.
       For the sake of reference you will receive the previous and next clips as well to help further contextualize the abstract description of the conversation topic.
       PREVIOUS CLIP: %s
       CURRENT CLIP: %s
       NEXT CLIP: %s

       Please write a MAXIMUM 6 word description of the conversation topic discussed in the CURRENT CLIP.
       """ % (clips[idx-1]["summary"], clips[idx]["summary"], clips[idx+1]["summary"])
       current_topic["chapter"] = openai_call(new_topic_prompt)
       current_topic["start"] = idx

    current_topic["podclipIDs"].append(clips[idx]["_additional"]["id"])
    print("%s \n" % current_topic["chapter"])

print("Saving...\n")
# Save new Chapter objects

# Get Podcast ID
get_pod_id_query = """
{
  Get {
    Podcast (
      where: {
        path: ["podNum"],
        operator: Equal,
        valueInt: 55
      }
    ){
    _additional {
      id
      }
    }
  }
}"""

podcastID = client.query.raw(get_pod_id_query)["data"]["Get"]["Podcast"][0]["_additional"]["id"]

for chapter in chapters:
  # Create New Chapter Object
  chapter_props = {
     "chapter": chapter["chapter"],
     "start": chapter["start"],
     "end": chapter["end"]
  }
  chapter_id = get_valid_uuid(uuid4())
  client.data_object.create(
     data_object = chapter_props,
     class_name="Chapter",
     uuid=chapter_id
  )
  for podclipID in chapter["podclipIDs"]:
    # Link PodClips to Chapter
    client.data_object.reference.add(
      from_class_name = "PodClip",
      from_uuid = podclipID,
      from_property_name="inChapter",
      to_class_name="Chapter",
      to_uuid = chapter_id
    )
    # Link Chapter to PodClips
    client.data_object.reference.add(
       from_class_name="Chapter",
       from_uuid = chapter_id,
       from_property_name="hasClip",
       to_class_name="PodClip",
       to_uuid=podclipID
    )
  # Link Chapter to Podcast
  client.data_object.reference.add(
     from_class_name = "Chapter",
     from_uuid = chapter_id,
     from_property_name="fromPodcast",
     to_class_name="Podcast",
     to_uuid=podcastID
  )
  # Link Podcast to Chapters
  client.data_object.reference.add(
     from_class_name="Podcast",
     from_uuid = podcastID,
     from_property_name="hasChapter",
     to_class_name="Chapter",
     to_uuid=chapter_id
  )

