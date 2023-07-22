import weaviate 

client = weaviate.Client("http://localhost:8080")

print(f"{client.schema.get()} \n")


from llama_index.vector_stores import WeaviateVectorStore
from llama_index import VectorStoreIndex, ListIndex
from llama_index.storage.storage_context import StorageContext

print("Connecting to Weaviate!")

vector_store = WeaviateVectorStore(weaviate_client=client, class_prefix="PodClip")

#storage_context = StorageContext.from_defaults(vector_store=vector_store)

print("Building PodClip index!")

PodClip_index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

# Set OpenAI Key in Environment

print("Constructing Query Engine!")

#chat_engine = PodClip_index.as_chat_engine(chat_mode="react", verbose=True)
chat_engine = PodClip_index.as_chat_engine()

# More development needed for Weaviate integration in the Chat Engine, shouldn't be a long project though.

print("Asking Question!")
response = chat_engine.chat("Can you please use the tool to tell me something about Weaviate?")
print(f"{response} \n")

# chat_engine.chat_repl()