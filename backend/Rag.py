import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from dotenv import load_dotenv
load_dotenv()
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

embedding_model=HuggingFaceEndpointEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")
load_dotenv()

# 2. Use same HuggingFace embeddings
# Note: Switched to HuggingFaceEmbeddings for local model execution
embedding_model = HuggingFaceEndpointEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")
#path configuration

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#DATA_DIR="./knowedge_base"
#CHROMA_DIR="./croma_db"

DATA_DIR = os.path.join(PROJECT_ROOT, "knowedge_base")
CHROMA_DIR= os.path.join(PROJECT_ROOT, "croma_db")


print("dirrrrrrrrrrrrrrrrrrrrrrrrrr",DATA_DIR)
print("cromammmmmmmmmmmmmmmm",CHROMA_DIR)

# text loading
def cunking_docs():
    print("loading documnet fom knowedgebase:")
    loader = DirectoryLoader(DATA_DIR, glob="**/*.txt", loader_cls=TextLoader)
    # documents = loader.load()
    # if not documents:
    #     print(" Add documnet to knowedge base")
    #     return
    # print(f"Loaded doc length of doc: {len(documents)}")
    # # text chunking 
    # print( "creating splitters:")
    # text_splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=40)
    # chunks=text_splitter.split_documents(documents)
    # print(f"Split into lenght: {len(chunks)} chunks.")

    # # storing chunks in vector db by creating embedding
    # print("embedding the chunks and storing in CromaDB: ")
    # vectorstore=Chroma.from_documents(
    #     documents=chunks,
    #     embedding=embedding_model,
    #     persist_directory=CHROMA_DIR
    # )
    # print(f"stroing verctor at{CHROMA_DIR}: ")
    documents = loader.load()

    print("Documents loaded:", len(documents))

    for doc in documents:
     print("File:", doc.metadata)

    if not documents:
     print("No documents found!")

   # text chunking 
    print( "creating splitters:")
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=40)
    chunks=text_splitter.split_documents(documents)
    print(f"Split into lenght: {len(chunks)} chunks.")

    chunks = text_splitter.split_documents(documents)

    print("Chunks created:", len(chunks))

    vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory=CHROMA_DIR
    )

    print("Stored documents:", vectorstore._collection.count())

# 1. Force the absolute path to the root folder


# 4. Expose a function: get_retriever()
def get_retriever():
    print(f"Loading ChromaDB from {CHROMA_DIR} and creating retriever...")
    
    vectorstore = Chroma(
        embedding_function=embedding_model,
        persist_directory=CHROMA_DIR
    )
    
    # 3. Create retriever (k=3 most relevant chunks)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    return retriever

if __name__ == "__main__":
    cunking_docs()  # Create embeddings and store in Chroma

    print("Testing the RAG retriever...")
    test_retriever = get_retriever()

    test_query = "What is your return policy?"
    results = test_retriever.invoke(test_query)

    print("Results found:", len(results))