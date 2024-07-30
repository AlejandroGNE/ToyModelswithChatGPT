from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama


def construct_index(directory_path):
    Settings.llm = Ollama(model="llama3.1", request_timeout=360.0)
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
    documents = SimpleDirectoryReader(directory_path).load_data()
    storage_context = StorageContext.from_defaults()
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        show_progress=True
    )
    storage_context.persist(persist_dir='model')
    print("Construction Complete!")
    return index


def load_index():
    print("Loading last model ...")
    Settings.llm = Ollama(model="llama3.1", request_timeout=360.0)
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
    storage_context = StorageContext.from_defaults(persist_dir=f'model')
    index = load_index_from_storage(storage_context=storage_context)
    print("Loading Complete!")
    return index


#ChatIndex = construct_index(directory_path="Extracted_Data")
#ChatIndex = load_index()

