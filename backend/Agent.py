import os
from dotenv import load_dotenv

# LangChain AI & Agent imports
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor

# Memory imports
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Import your custom tools
from backend import tool
# Load environment variables
load_dotenv()


# llm_obj=HuggingFaceEndpoint(model="deepseek-ai/DeepSeek-V4-Pro")
llm_obj=HuggingFaceEndpoint(model="Qwen/Qwen3-Coder-30B-A3B-Instruct")
chat_model=ChatHuggingFace(llm=llm_obj)

# agent.py — what to build
# 1. Load Groq LLM (llama3-70b-8192)
# 2. Load all 3 tools from tools.py
# 3. Create system prompt:
#    "You are a helpful customer support agent for [Company].
#     Use the search_knowledge_base tool to find answers.
#     If you cannot resolve, create a ticket or escalate.
#     Always be polite and professional."
# 4. Create AgentExecutor with memory
# 5. Expose function: run_agent(message, session_id) → returns response


# Load all 3 tools from tools.py

tools=[
    tool.search_knowledge_base,
    tool.create_support_ticket,
    tool.escalate_to_human
]

# 3. Define the System Prompt & Rules
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a highly capable customer support agent for SmartSupport.
    Your main goal is to help customers quickly and accurately.
    
    RULES:
    1. ALWAYS use the `search_knowledge_base` tool FIRST when a user asks a question about policies, shipping, or products.
    2. Do NOT make up answers. If the knowledge base does not contain the answer, tell the user.
    3. If the user asks to open a ticket, or if you cannot solve their issue, use the `create_support_ticket` tool.
    4. If the user is angry or asks for a human, use the `escalate_to_human` tool.
    5. Keep your final answers polite, professional, and concise.
    """),
    # This placeholder holds the memory of the conversation
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    # This placeholder is the agent's "scratchpad" where it writes down its tool results
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])
# 4. Create AgentExecutor with memory
agent_calling=create_tool_calling_agent(
    llm=chat_model,
    tools=tools,
    prompt=prompt
)

#exentexucation
agent_executor=AgentExecutor(
    agent=agent_calling,
    tools=tools,
    verbose=True
)
# 5. Set up Memory (Session History)
# This dictionary temporarily stores conversations based on session IDs
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# Wrap the executor in the memory module
agent_with_memory = RunnableWithMessageHistory(
    agent_executor,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

def run_agent(message: str, session_id: str) -> str:
    """
    Main function to be called by your FastAPI backend or Streamlit UI.
    Takes a user message and a session ID, returns the AI's response.
    """
    response = agent_with_memory.invoke(
        {"input": message},
        config={"configurable": {"session_id": session_id}}
    )
    return response["output"]


# ---------------------------------------------------------
# Terminal Testing Block
# ---------------------------------------------------------
if __name__ == "__main__":
    print("🤖 SmartSupport AI Agent Initialized! Type 'exit' to quit.")
    print("-" * 50)
    
    test_session_id = "terminal_user_1"
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['exit', 'quit']:
            break
            
        print("\nThinking...")
        answer = run_agent(user_input, test_session_id)
        print(f"\nAgent: {answer}")