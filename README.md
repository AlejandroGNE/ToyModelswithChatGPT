# ToyModelswithChatGPT
Creating a ChatGPT version that can build toy PLEXOS models.

### First Step: Choosing A Large Language Model(LLM)
In this script, the llama 3.1 LLM was used with the help of Ollama to run the LLM locally.
Go to https://ollama.com/ and install ollama.
Choose an LLM, run the following command in the terminal/cmd in order to download the LLM:
        
    ollama pull llama3.1
To test, run the following and type a prompt:
    
    ollama run llama3.1 
### Second Step: Gather Data
Gather the data on which you wish to train your model. So far, we've tested plain text files, python files, and XML files. A folder named Extracted_Data contains the data that will be included in the Retrival Augmented Generation of the LLM.

### Third Step: RAG Script
Install the following dependencies 
        
    pip install llama-index
    pip install llama-index-llms-ollama
    pip install llama_index.embeddings.huggingface
Note: if you are using windows you have to do this extra step:
    
    pip uninstall torch
    pip install torch==2.2

The RAG.py has two functions 

    construct_index()
        this function takes in a dirctory path, loads the files, then generates an index
        and saves it in the model Folder/Directory
    
    load_index()
        this function takes the model Folder/Directory from the storage returns it as an index
        
### Fourth Step: Run the flask website
install the following dependencies:
    
    pip install flask
run the app.py script which is a flask website that integrates the LLM model with the a website
then head to the page http://127.0.0.1:3000/views

first press the generate button, it will generate our model, everytime you start up the website press load model.
These buttons calls the RAG.py
