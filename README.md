
## Authors📝

- [@harshaygadekar](https://www.github.com/harshaygadekar)


## Chat with your documents using LangChain🔗

<b>This Python script demonstrates how to use the LangChain library to build a conversational AI assistant that can interact with documents of various formats (PDF, Markdown, and text files) stored in a directory. 

The script performs the following steps:

- Loads and combines the documents from the specified directory using different document loaders.
- Splits the text from the documents into smaller chunks using a text splitter.
- Generates embeddings (vector representations) for the text chunks using OpenAI's embedding model.
- Stores the embeddings and associated text chunks in a vector database (Chroma or Pinecone) for efficient similarity search.
- Sets up a conversational retrieval chain that uses the stored embeddings to retrieve relevant text chunks based on user queries.

Provides two user interfaces:

- A simple widget-based interface using IPython and ipywidgets, where users can enter questions, and the assistant responds with relevant information from the documents.
- A Gradio-based chat interface with a more polished UI, where users can engage in a conversational interaction with the assistant.</b>
## Tech Stack💻

<b>Python, LangChain, OpenAI API Key, Pinecone API Key, Jupyter Notebook.</b>


## License

[apache-2.0](https://choosealicense.com/licenses/apache-2.0/)


## FAQ 💬

#### Is there a tutorial to test this?

Yes, I have uploaded both Jupyter Notebook file and Python File with written tutorial and instructions to run this project.

#### What is the applications of this project?

Applications for this LangChain conversational AI assistant project:

- Knowledge base Q&A
- Document retrieval and research
- Customer support
- Education and learning
- Personal knowledge management
- Data analysis and exploration
- Content summarization and exploration

