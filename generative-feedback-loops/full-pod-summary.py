import weaviate
import os
import openai
import requests

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
    }
  }
}
"""

clips = client.query.raw(get_clips_query)["data"]["Get"]["PodClip"]

current_summary = ""

for idx, clip in enumerate(clips):
    refine_summary_prompt = """
    Please write a summary of the following podcast. 
    You will receive the clips one at a time, as well as the summary generated so far.
    
    Current Summary so far: %s
    In the next podcast clip, speaker: %s said %s
    New Summary:
    """ % (current_summary, clip["speaker"], clip["summary"])

    current_summary = openai_call(refine_summary_prompt)
    print(idx)
    print(current_summary)

    compress_summary_prompt = """
    Please re-write this summary to make it shorter.
    Please be careful about losing too much information when re-writing.

    Summary: %s

    New Summary:
    """ % (current_summary)
    
    current_summary = openai_call(compress_summary_prompt)
    print("Rewritten...\n")
    print(current_summary)

print("Saving...\n")
# Save new Podcast object
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
}
"""

save_pod_id = client.query.raw(get_pod_id_query)["data"]["Get"]["Podcast"][0]["_additional"]["id"]
summary_update = {
    "summary": current_summary
}
client.data_object.update(
  summary_update,
  class_name = "Podcast",
  uuid = save_pod_id
)