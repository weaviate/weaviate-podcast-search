from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import logging

import numpy as np
import weaviate
from weaviate.util import get_valid_uuid
from uuid import uuid4

from backend.queries import populate_query, get_prod_uuid, get_user_vector_and_clicks, searchbar_query

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


client = weaviate.Client("http://localhost:8080")
# start a new User session
data_properties = {"sessionNumber": 0}
user_id = get_valid_uuid(uuid4())
client.data_object.create(data_properties, "User", user_id)

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    random_vector = np.random.rand(384) # check this
    data = populate_query(random_vector, client)
    context = {"request": request, "data": data}
    return templates.TemplateResponse("index.html", context=context)

@app.post("/clip-clicked")
async def image_clicked(data: dict, request: Request):
    id_clicked = data.get("id")
    _, user_clicks = get_user_vector_and_clicks(user_id, client)
    if id_clicked in user_clicks:
        client.data_object.reference.delete(
            from_uuid = user_id,
            from_property_name = "likedClip",
            to_uuid = id_clicked
        )
    else:
        client.data_object.reference.add(
            from_uuid = user_id,
            from_property_name = "likedClip",
            to_uuid = id_clicked
        )

    user_vector, user_clicks = get_user_vector_and_clicks(user_id, client)
    print("\n")
    print("USER CLICKS AFTER")
    print(user_clicks)
    print("\n")
    
    if len(user_vector) < 1:
        print("HERE GENERATING RANDOM VECTOR TO SEARCH WITH")
        user_vector = np.random.rand(384,)

    data = populate_query(user_vector, client)
    return_dict = {
        "data": data,
        "user_clicks": user_clicks
    }
    return return_dict

@app.post("/text-search")
def text_search(data: dict, request: Request):
    text_query = data.get("searchQuery")
    _, user_clicks = get_user_vector_and_clicks(user_id, client)
    data = searchbar_query(text_query, user_id, user_clicks, client)
    return_dict = {
        "data": data,
        "user_clicks": user_clicks
    }
    # will need something with the user_clicks also
    return return_dict