# Tool 1: search_knowledge_base(query: str)
# Uses RAG retriever to search company docs
# Returns relevant text chunks

# Tool 2: create_support_ticket(issue: str, customer_name: str)  
# Simulates creating a ticket (just saves to a .json file)
# Returns ticket ID

# Tool 3: escalate_to_human(reason: str)
# Returns a message that human support will follow up
# Used when agent cannot resolve the issue

from langchain.tools import tool
from backend import Rag 
import json
import os
import uuid
from datetime import datetime

TICKETS_FILE = "tickets.json"

@tool
def search_knowledge_base(query:str)->str:
    """
    Searches the company knowledge base for answers to customer questions.
    Always use this tool FIRST when a customer asks about policies, products, returns, or shipping.
    """
    # Fetch the relevant chunks
    retriever=Rag.get_retriever()
    results = retriever.invoke(query)
    
    combined_context = ""
    if not results:
        # Return a string so the agent knows the search failed and can adjust its strategy
        return "No results found in the knowledge base for that query."
    
    # Combine all retrieved chunks so the agent gets the full context
    combined_context = ""
    for i, doc in enumerate(results):
        combined_context += f"--- Relevant Chunk {i+1} ---\n{doc.page_content}\n\n"
        
    return combined_context.strip()

# Tool 2: create_support_ticket(issue: str, customer_name: str)  
# Simulates creating a ticket (just saves to a .json file)
# Returns ticket ID
@tool
def create_support_ticket(issue: str, customer_name: str) -> str:
    """
    Creates a support ticket for the customer.
    Use this tool ONLY if the knowledge base does not have the answer, or if the user explicitly asks to open a ticket.
    """
    # FIX 1: Added () to .upper()
    ticket_id = f"TKT-{str(uuid.uuid4())[:5].upper()}"
    
    new_ticket = {
        "ticket_id": ticket_id,
        "customer_name": customer_name,
        "issue": issue,
        "status": "Open",
        "created_at": datetime.now().isoformat()
    }
    
    # Load existing tickets
    tickets = []
    if os.path.exists(TICKETS_FILE):
        try:
            with open(TICKETS_FILE, "r") as f:
                tickets = json.load(f)
        except json.JSONDecodeError:
            pass # Catch error if file is completely empty
            
    # FIX 2: Append the dictionary, not the list itself
    tickets.append(new_ticket)
    
    # FIX 3: Use "w" to write a clean JSON array, and add indent=4 for readability
    with open(TICKETS_FILE, "w") as f:
        json.dump(tickets, f, indent=4)

    return f"Success! Ticket {ticket_id} has been created for {customer_name}. A support agent will review it shortly."

# Tool 3: escalate_to_human(reason: str)
# Returns a message that human support will follow up
# Used when agent cannot resolve the issue

@tool
def escalate_to_human(reason: str) -> str:
    """
    Escalates the conversation to a human agent.
    Use this tool if the customer is angry, explicitly asks to speak to a human, or if you cannot help them after searching the knowledge base.
    """
    # In a real app, this might trigger an email or Slack message to the support team
    return f"ESCALATION TRIGGERED: The system has notified a human agent to take over because: {reason}. Please tell the customer a human will be with them shortly."