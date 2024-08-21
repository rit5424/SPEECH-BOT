import streamlit as st
import ollama as ol
from voice import record_voice

# Set up page configuration with a custom theme color
st.set_page_config(
    page_title="Speech-to-Text Chat Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS for styling
st.markdown("""
    <style>
        .main-title {
            font-size: 3rem;
            font-weight: bold;
            color: #4CAF50;
            text-align: center;
            margin-bottom: 2rem;
        }
        .sidebar-title {
            font-size: 1.5rem;
            color: #FF5722;
            text-align: center;
            margin-top: 2rem;
        }
        .chat-message-user {
            background-color: #F1F1F1;
            border-radius: 10px;
            padding: 10px;
            margin: 10px 0;
            max-width: 80%;
            align-self: flex-end;
        }
        .chat-message-assistant {
            background-color: #E8F5E9;
            border-radius: 10px;
            padding: 10px;
            margin: 10px 0;
            max-width: 80%;
            align-self: flex-start;
        }
        .sidebar .sidebar-content {
            padding: 20px;
        }
        .chat-container {
            display: flex;
            flex-direction: column;
            max-width: 800px;
            margin: 0 auto;
            background-color: #FAFAFA;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
    </style>
""", unsafe_allow_html=True)

# Title and Sidebar Titles with Custom Classes
st.markdown("<h1 class='main-title'>Speech-to-Text Chat Bot</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<h2 class='sidebar-title'>Speak with LLMs</h2>", unsafe_allow_html=True)

# Function to Select Language (Default: English)
def language_selector():
    return "en"

# Function to Select LLM Model from Ollama
def llm_selector():
    ollama_models = [m['name'] for m in ol.list()['models']]
    return st.sidebar.selectbox("Choose a Model", ollama_models)

# Function to Display Text with Right-to-Left Support for Arabic
def print_txt(text):
    if any("\u0600" <= c <= "\u06FF" for c in text):  # Check if text contains Arabic characters
        text = f"<p style='direction: rtl; text-align: right;'>{text}</p>"
    st.markdown(text, unsafe_allow_html=True)

# Function to Display Chat Messages
def print_chat_message(message):
    text = message["content"]
    if message["role"] == "user":
        st.markdown(f"<div class='chat-message-user'>{text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-message-assistant'>{text}</div>", unsafe_allow_html=True)

# Main Function to Run the App
def main():
    model = llm_selector()
    language = language_selector()

    # Sidebar Voice Input
    with st.sidebar:
        question = record_voice(language=language)
    
    # Initialize Chat History
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = {}
    if model not in st.session_state.chat_history:
        st.session_state.chat_history[model] = []
    chat_history = st.session_state.chat_history[model]
    
    # Chat Container to Display Conversation
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    
    # Display Previous Conversation
    for message in chat_history:
        print_chat_message(message)

    # Handle User Input and AI Response
    if question:
        user_message = {"role": "user", "content": question}
        print_chat_message(user_message)
        chat_history.append(user_message)

        response = ol.chat(model=model, messages=chat_history)
        answer = response['message']['content']
        ai_message = {"role": "assistant", "content": answer}
        print_chat_message(ai_message)
        chat_history.append(ai_message)

        # Keep Chat History Limited to Last 20 Messages
        if len(chat_history) > 20:
            chat_history = chat_history[-20:]
        
        # Update Session State with Chat History
        st.session_state.chat_history[model] = chat_history
    
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
