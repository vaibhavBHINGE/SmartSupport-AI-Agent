SmartSupport AI Workspace

An intelligent, enterprise-grade customer support agent designed to automate documentation lookup and streamline user assistance. The system leverages a Retrieval-Augmented Generation (RAG) architecture to securely query a localized company knowledge base, enabling precise, context-aware responses without data leakage.

🚀 Key Features
Contextual RAG Retrieval: Queries a persistent, pre-built vector database to fetch exact text segments matching user inquiries.

Intelligent Conversation Memory: Maintains a continuous stateful chat history across sessions for fluid, natural dialogue.

Deterministic Tool Routing: Orchestrates actions dynamically, allowing the agent to switch between document lookups, ticket creation, and human escalation workflows.

Production-Ready Split Architecture: Decouples the lightweight client interface from the heavy server-side AI processing engine via RESTful endpoints.

🛠️ Tech Stack
Frontend UI: Gradio

Backend API Framework: FastAPI & Uvicorn

Orchestration Framework: LangChain

LLM Engine: NVIDIA Nemotron Mini 4B (via langchain-nvidia-ai-endpoints)

Vector Store: ChromaDB

Environment Management: Python Dotenv

📁 Project Structure
Plaintext
smart_support_ai/
│
├── backend/
│   ├
│   ├── main.py               # FastAPI application hosting the /chat endpoint
│   ├── Agent.py              # LangChain execution engine & memory layer
│   └── tools.py              # Core tools (ChromaDB search, Ticket engine)
│
├── frontend/
│   ├
│   └── app.py                # Gradio web interface client application
│
├── data/
│   └── company_faqs.txt      # Source documentation file for company data
│
├── chroma_db/                # Persistent directory containing pre-built vector embeddings
│
├── requirements.txt          # Explicit project dependency listings
└── .env                      # Local environment secrets and API keys

⚡ Installation & Local Setup
1. Clone and Navigate to the Repository
Bash
cd smart_support_ai

2. Configure the Environment Variables
Create a file named .env in the root directory of your project and populate it with your credentials:

Plaintext
HUGGINFACE_API_KEY=your_api_key_here

3. Install System Dependencies
Install all required third-party packages using pip:

Bash
pip install fastapi uvicorn gradio langchain langchain-nvidia-ai-endpoints chromadb python-dotenv
🏃 How to Run the Application
To run the full stack, execute the backend server and frontend interface concurrently in separate terminal windows.

Step 1: Initialize the FastAPI Backend
Launch the backend server application. It will initialize the LangChain engine and expose the necessary API routes on port 8000.

Bash
uvicorn backend.main:app --reload
Verification: Navigate to http://127.0.0.1:8000/docs in your browser to inspect the interactive Swagger API documentation.

Step 2: Launch the Gradio Frontend Client
In a new terminal window, spin up the web interface layer to connect to the active backend gateway.

Bash
python frontend/app.py
Access Link: Open http://127.0.0.1:7860 in your web browser to interact with the operational support desk.