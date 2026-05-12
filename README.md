# AI RAG Agent Chatbot

A conversational AI chatbot built using FastAPI, Streamlit, OpenAI, and ChromaDB. The project supports document-based question answering using RAG (Retrieval Augmented Generation) along with simple agent/tool capabilities.

The application allows users to upload PDF or text documents, store document embeddings in a vector database, and ask contextual questions from the uploaded content.

In addition to document-based Q&A, the chatbot can also perform utility-based tasks like calculations and date/time retrieval.


# Features

* Upload PDF and text files
* Extract and process document content
* Generate embeddings using OpenAI
* Store embeddings in ChromaDB
* Context-aware document question answering
* Multi-turn conversation support
* Tool-based responses (calculator and date/time)
* FastAPI backend
* Streamlit frontend



# Technologies Used

* Python
* FastAPI
* Streamlit
* OpenAI API
* ChromaDB
* DuckDuckGo Search


# How to Run the Project

## Step 1: Clone the repository

Clone the repository from GitHub and move into the project directory.

git clone [https://github.com/shwetakinger37/ai_rag_agent.git](https://github.com/shwetakinger37/ai_rag_agent.git)
cd ai_rag_agent

## Step 2: Create virtual environment

Create a Python virtual environment for the project.

python -m venv .venv

## Step 3: Activate virtual environment

For Windows systems, activate the virtual environment using:

.venv\Scripts\activate

## Step 4: Install dependencies

Install all required dependencies from the requirements file.

pip install -r requirements.txt

## Step 5: Create .env file

Create a `.env` file in the root directory and add the following environment variables.

OPENAI_API_KEY=your_openai_api_key
CHAT_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small
CHROMA_DIR=data/chroma
UPLOAD_DIR=data/uploads
TOP_K=4

## Step 6: Run FastAPI backend

Start the FastAPI backend server using the following command.

uvicorn app.main:app --reload

Swagger API documentation will be available at:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Step 7: Run Streamlit frontend

Open another terminal window and start the Streamlit frontend.

streamlit run frontend/streamlit_app.py



# How the Application Works

The user uploads a document through the frontend interface. The backend extracts the text content from the document and splits it into smaller chunks.

Embeddings are generated for these chunks and stored in ChromaDB.

When the user asks a question, the application retrieves the most relevant chunks using similarity search and sends them to the language model as context.

The chatbot then generates a response based on the retrieved information.

If the question requires a utility action such as calculation or date retrieval, the request is routed to the appropriate tool.



# Design Decisions

The project was intentionally kept simple and modular for easier understanding and debugging.

FastAPI was used for backend APIs because of its speed and async support.

ChromaDB was selected as a lightweight local vector database suitable for interview assignments and local development.

Streamlit was added as a minimal frontend to quickly test document upload and chatbot functionality.



# Notes

* The `.env` file should not be pushed to GitHub.
* API keys should always remain private.
* Uploaded files and vector database files are ignored through `.gitignore`.



# Future Improvements

* Add authentication
* Add conversation persistence in database
* Add advanced agent workflows 
