import gradio as gr
import requests
import uuid

# Configuration
API_URL = "http://127.0.0.1:8000/chat"

def chat_with_agent(message, history, session_id):
    """
    This function sends the user's message and session ID to your FastAPI backend
    and returns the agent's response to the Gradio chat window.
    """
    payload = {
        "message": message,
        "session_id": session_id
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        
        if response.status_code == 200:
            return response.json().get("response")
        else:
            return f"⚠️ Backend Error: {response.text}"
            
    except requests.exceptions.ConnectionError:
        return "⚠️ Cannot connect to the backend. Is your FastAPI server running?"

# Build the Gradio UI
with gr.Blocks(title="SmartSupport AI", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 🤖 SmartSupport AI Desk
        Welcome to the customer support portal. This agent can search our knowledge base, open support tickets, and escalate issues to human representatives.
        """
    )
    
    # Store a unique session ID for the user invisibly
    session_id = gr.State(value=lambda: str(uuid.uuid4()))
    
    # Gradio's built-in chat interface
    chat_interface = gr.ChatInterface(
        fn=chat_with_agent,
        additional_inputs=[session_id],
        chatbot=gr.Chatbot(height=500),
        textbox=gr.Textbox(placeholder="Type your message here...", container=False, scale=7),
    )

if __name__ == "__main__":
    demo.launch()