from langchain_community.vectorstores import Pinecone as LangPinecone
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
import os, time
from dotenv import load_dotenv

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = os.getenv("PINECONE_INDEX")
region = os.getenv("PINECONE_REGION", "us-east-1")
index = pc.Index(index_name)
spec = ServerlessSpec(
    cloud="aws", region=region
)
existing_indexes = [
    index_info["name"] for index_info in pc.list_indexes()
]

# check if index already exists (it shouldn't if this is first time)
if index_name not in existing_indexes:
    # if does not exist, create index
    pc.create_index(
        index_name,
        dimension=1536,  # dimensionality of ada 002
        metric='dotproduct',
        spec=spec
    )
    # wait for index to be initialized
    while not pc.describe_index(index_name).status['ready']:
        time.sleep(1)
def get_memory(user_id: str):
    embeddings = OpenAIEmbeddings()

    return LangPinecone.from_existing_index(
        index_name=index_name,
        embedding=embeddings,
        namespace=user_id
    ).as_retriever(search_kwargs={"k": 5})


# Optional: retrieve user memory history
def get_chat_history(user_id: str):
    namespace_data = index.fetch(ids=[], namespace=user_id)
    return namespace_data.to_dict()
