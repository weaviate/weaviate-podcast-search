import weaviate
import numpy as np

def populate_query(query_vector, client):
    '''
    ToDo, extend with where etc. 
    '''

    query_str = """
    {
        Get {
            PodClip (
                nearVector: {
                    vector: %s
                }
            ){
            content
            speaker
            summary
            podNum
            _additional {
                id
                }
            }
        }
    }
    """ % query_vector
    
    results = client.query.raw(query_str)["data"]["Get"]["PodClip"]

    data = {}
    for idx, result in enumerate(results):
        data[idx] = {
            "content":  result["content"],
            "speaker":  result["speaker"],
            "summary":  result["summary"],
            "podNum":   result["podNum"],
            "id":       result["_additional"]["id"]
        }

    return data

def get_prod_uuid(labelName, client):
    query_str = """
    {
	Get {
        PodClip (
            where: {
                path: "labelName"
                operator: Equal
                valueText: "%s"
            }
        ){
		_additional {
            id
          }
        }
      }
    }
    """ % labelName

    results = client.query.raw(query_str)["data"]["Get"]["User"][0]["_additional"]["id"]
    return results

def get_user_vector_and_clicks(user_id, client):
    query_str = """
    {
    Get {
    User (
        where: {
        path: ["id"]
        operator: Equal
        valueString: "%s"
        }
    ){
        likedClip {
        ... on PodClip {
            _additional {
                id
              }
            }
        }
        _additional {
          vector
        }
    }
    }
    }
    """ % user_id

    


    results = client.query.raw(query_str)["data"]["Get"]["User"]
    user_vector = results[0]["_additional"]["vector"]
    likedClips = results[0]["likedClip"]
    if likedClips == None:
        ids_only = []
    else:
        ids_only = [clip["_additional"]["id"] for clip in likedClips]

    return user_vector, ids_only

# not used
def searchbar_query(text, user_id, user_clicks, client):

    if len(user_clicks) > 0:
        print("here")
        query_str = """
        {
            Get {
                Product(
                    nearText: {
                        concepts: ["%s"]
                    }
                ){
                labelName
                _additional {
                  vector
                  }
                }
            }
        }
        """ % text
        results = client.query.raw(query_str)["data"]["Get"]["Product"]
        product_vectors = [result["_additional"]["vector"] for result in results]
        labels = [result["labelName"] for result in results]
        user_vector, _ = get_user_vector_and_clicks(user_id, client)

        import numpy as np

        # Combine product_vectors with their corresponding labels
        vector_label_pairs = list(zip(product_vectors, labels))

        # Compute the dot product similarity between each product vector and the user vector
        # Store the results with their corresponding labels in a list
        similarity_label_pairs = [(np.dot(vector_label_pair[0], user_vector), vector_label_pair[1]) for vector_label_pair in vector_label_pairs]

        # Sort the pairs by similarity in descending order
        sorted_similarity_label_pairs = sorted(similarity_label_pairs, key=lambda x: x[0], reverse=True)

        # Retrieve the top 100 results
        top_100_results = sorted_similarity_label_pairs[:100]

        data = {}
        
        for idx, result in enumerate(top_100_results):
            similarity, label = result
            if similarity < 0.00005:
                similarity = 0
            data[idx] = {
                "image_path": "images/" + label + ".jpg",
                "distance": similarity
            }
        
        return data

    else:
        print("here2")
        query_str = """
            {
                Get {
                    Product (
                        nearText: {
                            concepts: ["%s"]
                        }
                    ){
                    labelName
                    _additional {
                        distance
                        }
                    }
                }
            }
        """ % text

        results = client.query.raw(query_str)["data"]["Get"]["Product"]
        
        data = {}
        for idx, result in enumerate(results):
            dist = result["_additional"]["distance"]
            if dist < 0.00005:
                dist = 0
            data[idx] = {
                "image_path":   "images/" + result["labelName"] + ".jpg",
                "distance":     dist
            }
        return data