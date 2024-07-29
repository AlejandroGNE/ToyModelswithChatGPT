# ToyModelswithChatGPT
Creating a ChatGPT version that can build toy PLEXOS models.
## Welcome to the first steps of creating a PLEXOS AI

### First Step: Choosing A Large Language Model(LLM)
In this script, the llama 3.1 LLM was used with the help of Ollama to run the LLM locally
Go to https://ollama.com/ and install ollama 
Choose an LLM, run the following command in the terminal/cmd in order to download the LLM
        
    ollama pull llama3.1
To test, run the following and type a prompt:
    
    ollama run llama3.1 
### Second Step: Gather Data
Gather the data on which you wish to train your model. So far, we've tested plain text files, python files, and XML files.

### Third Step: RAG Script
Install the following dependencies 
        
    pip install llama-index
    pip install llama-index-llms-ollama
    pip install llama_index.embeddings.huggingface

The RAG.py has two functions 

    construct_index()
        this function takes in a dirctory path, loads the files, then generates an index
        and saves it in the model Folder/Directory
    
    load_index()
        this function takes the model Folder/Directory from the storage returns it as an index
        
### Fourth Step: Run the program
This commented out line only needs to be ran when new data is placed in the folder to be indexed

    ChatIndex = construct_index(directory_path="TrainData")
Once the model is generated, use the load_index() function instead.

There is a loop that asks for a prompt, if "quit" is entered then the program ends.
