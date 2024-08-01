import os.path
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
    Settings
)
import logging
import sys

context_data = "context_for_ChatGPT" # Path to the context data for initial index creationg

# Want to see what's happening under the hood? Let's add some logging. 
# Add these lines to the top of your script:
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG) # level=logging.DEBUG for more detailed output, .INFO for less
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# check if storage already exists
'''
By default, the data you just loaded is stored in memory as a series of vector embeddings. 
You can save time (and requests to OpenAI) by saving the embeddings to disk. That can be done with this line:
index.storage_context.persist() 
'''
PERSIST_DIR = "./stored_context"
if not os.path.exists(PERSIST_DIR): # If the storage directory named 'storage' does not exist
    # load the documents and create the index
    documents = SimpleDirectoryReader(context_data).load_data() # Load the context data
    index = VectorStoreIndex.from_documents(documents) # Construct the index from the context data
    # store it for later
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    # load the existing index
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

# Create a query engine from the index
query_engine = index.as_query_engine(
    streaming=True # print beginning of response before full response is ready -reduces perceived latency
) 
response = query_engine.query("Write a PLEXOS model that has one generator of each category") # Query the index (submit a question to ChatGPT)
print(response) # Print the response from ChatGPT


