# -*- coding: utf-8 -*-
"""Chat with your documents.ipynb

Automatically generated by Colab.

# Chat with any documents using langchain

[OpenAI token limit](https://platform.openai.com/docs/models/gpt-4)  
OpenAI's embedding model has 1536 dimensions.  
After the data is turned into embeddings, they are stored in a vectorstore database, such as Pinecone, Chroma and Faiss, etc.  
Once the query is provided, the most relevant chunks of data is queried based on the similarity (semantic search)

## Setup
"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install openai langchain  tiktoken pypdf unstructured[local-inference] gradio chromadb

# Commented out IPython magic to ensure Python compatibility.
# %reload_ext watermark
# %watermark -a "Harsha Gadekar" -vmp langchain,openai,chromadb

import os
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone, Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI

os.environ['OPENAI_API_KEY'] ="OPENAI_API_KEY"

#llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

"""[LangChain Document Loader](https://python.langchain.com/en/latest/modules/indexes/document_loaders.html)"""

from langchain.document_loaders import DirectoryLoader

pdf_loader = DirectoryLoader('/content/Documents/', glob="**/*.pdf")
readme_loader = DirectoryLoader('/content/Documents/', glob="**/*.md")
txt_loader = DirectoryLoader('/content/Documents/', glob="**/*.txt")

#take all the loader
loaders = [pdf_loader, readme_loader, txt_loader]

#lets create document
documents = []
for loader in loaders:
    documents.extend(loader.load())

print (f'You have {len(documents)} document(s) in your data')
print (f'There are {len(documents[0].page_content)} characters in your document')

documents[0]

"""## Split the Text from the documents"""

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=40) #chunk overlap seems to work better
documents = text_splitter.split_documents(documents)
print(len(documents))

documents[0]

documents[1]

"""## Embeddings and storing it in Vectorestore"""

embeddings = OpenAIEmbeddings()

"""### Using Chroma for storing vectors"""

from langchain.vectorstores import Chroma

vectorstore = Chroma.from_documents(documents, embeddings)

"""### Using pinecone for storing vectors"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install pinecone-client

"""- [Pinecone langchain doc](https://python.langchain.com/en/latest/modules/indexes/vectorstores/examples/pinecone.html?highlight=pinecone#pinecone
)
- What is [vectorstore](https://www.pinecone.io/learn/vector-database/)
- Get your pinecone api key and env -> https://app.pinecone.io/
"""

import os
import getpass
PINECONE_API_KEY = getpass.getpass('Pinecone API Key:')

PINECONE_ENV = getpass.getpass('Pinecone Environment:')

import pinecone

# initialize pinecone
pinecone.init(
    api_key=PINECONE_API_KEY,  # find at app.pinecone.io
    environment=PINECONE_ENV  # next to api key in console
)

index_name = "langchain-demo"

vectorstore = Pinecone.from_documents(documents, embeddings, index_name=index_name)

# if you already have an index, you can load it like this
import pinecone
from tqdm.autonotebook import tqdm

# initialize pinecone
pinecone.init(
    api_key=PINECONE_API_KEY,  # find at app.pinecone.io
    environment=PINECONE_ENV  # next to api key in console
)

index_name = "langchain-demo"
vectorstore = Pinecone.from_existing_index(index_name, embeddings)

"""#### We had 23 documents so there are 23 vectors being created in Pinecone."""

query = "Who are the authors of gpt4all paper ?"
docs = vectorstore.similarity_search(query)

len(docs) #it went on and search on the 4 different vectors to find the similarity

print(docs[0].page_content)

print(docs[1].page_content)

"""## Now the langchain part (Chaining with Chat History) --> With One line of Code (Fantastic)
- There are many chains but we use this [link](https://python.langchain.com/en/latest/modules/chains/index_examples/chat_vector_db.html)
"""

from langchain.llms import OpenAI

retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k":2})
qa = ConversationalRetrievalChain.from_llm(OpenAI(temperature=0), retriever)



chat_history = []
query = "How much is spent for training the gpt4all model?"
result = qa({"question": query, "chat_history": chat_history})
result["answer"]

chat_history.append((query, result["answer"]))
chat_history

query = "What is this number multiplied by 2?"
result = qa({"question": query, "chat_history": chat_history})
result["answer"]

"""## Create a chatbot with memory with simple widgets"""

from IPython.display import display
import ipywidgets as widgets

chat_history = []

def on_submit(_):
    query = input_box.value
    input_box.value = ""

    if query.lower() == 'exit':
        print("Thanks for the chat!")
        return

    result = qa({"question": query, "chat_history": chat_history})
    chat_history.append((query, result['answer']))

    display(widgets.HTML(f'<b>User:</b> {query}'))
    display(widgets.HTML(f'<b><font color="Orange">Chatbot:</font></b> {result["answer"]}'))

print("Chat with your data. Type 'exit' to stop")

input_box = widgets.Text(placeholder='Please enter your question:')
input_box.on_submit(on_submit)

display(input_box)

"""## Gradio Part (Building the [chatbot like UI](https://gradio.app/docs/#chatbot))

### Gradio sample example
"""

import gradio as gr
import random

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")

    def respond(message, chat_history):
        print(message)
        print(chat_history)
        bot_message = random.choice(["How are you?", "I love you", "I'm very hungry"])
        chat_history.append((message, bot_message))
        print(chat_history)
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

demo.launch(debug=True, share=True)

"""### Gradio langchain example"""

import gradio as gr
with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")

    def respond(user_message, chat_history):
        print(user_message)
        print(chat_history)
        # Get response from QA chain
        response = qa({"question": user_message, "chat_history": chat_history})
        # Append user message and response to chat history
        chat_history.append((user_message, response["answer"]))
        print(chat_history)
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot], queue=False)
    clear.click(lambda: None, None, chatbot, queue=False)

demo.launch(debug=True, share=True)

