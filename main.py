import streamlit as st
import os
from groq import Groq
from datetime import datetime
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
groq_api_key = os.environ['GROQ_API_KEY']

# Page configuration
st.set_page_config(
    page_title="Groq Chat Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initialize session state variables"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'total_messages' not in st.session_state:
        st.session_state.total_messages = 0
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None

def get_custom_prompt():
    """Get custom prompt template based on selected persona"""
    persona = st.session_state.get('selected_persona', 'Default')
    
    personas = {
        'Default': """You are a helpful AI assistant.
                     Current conversation:
                     {history}
                     Human: {input}
                     AI:""",
        'Expert': """You are an expert consultant with deep knowledge across multiple fields.
                    Please provide detailed, technical responses when appropriate.
                    Current conversation:
                    {history}
                    Human: {input}
                    Expert:""",
        'Creative': """You are a creative and imaginative AI that thinks outside the box.
                      Feel free to use metaphors and analogies in your responses.
                      Current conversation:
                      {history}
                      Human: {input}
                      Creative AI:"""
    }
    
    return PromptTemplate(
        input_variables=["history", "input"],
        template=personas[persona]
    )

def main():
    initialize_session_state()
    
    # Sidebar Configuration
    with st.sidebar:
        st.title("🛠️ Chat Settings")
        
        # Model selection with custom styling
        st.subheader("Model Selection")
        model = st.selectbox(
            'Choose your model:',
            ['mixtral-8x7b-32768', 'llama2-70b-4096'],
            help="Select the AI model for your conversation"
        )
        
        # Memory configuration
        st.subheader("Memory Settings")
        memory_length = st.slider(
            'Conversation Memory (messages)',
            1, 10, 5,
            help="Number of previous messages to remember"
        )
        
        # Persona selection
        st.subheader("AI Persona")
        st.session_state.selected_persona = st.selectbox(
            'Select conversation style:',
            ['Default', 'Expert', 'Creative']
        )
        
        # Chat statistics
        if st.session_state.start_time:
            st.subheader("📊 Chat Statistics")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Messages", len(st.session_state.chat_history))
            with col2:
                duration = datetime.now() - st.session_state.start_time
                st.metric("Duration", f"{duration.seconds // 60}m {duration.seconds % 60}s")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.start_time = None
            st.rerun()

    # Main chat interface
    st.title("🤖 Groq Chat Assistant")
    
    # Initialize chat components
    memory = ConversationBufferWindowMemory(k=memory_length)
    groq_chat = ChatGroq(
        groq_api_key=groq_api_key,
        model_name=model
    )
    
    conversation = ConversationChain(
        llm=groq_chat,
        memory=memory,
        prompt=get_custom_prompt()
    )

    # Load chat history into memory
    for message in st.session_state.chat_history:
        memory.save_context(
            {'input': message['human']},
            {'output': message['AI']}
        )

    # Display chat history
    for message in st.session_state.chat_history:
        # User message
        with st.container():
            st.write(f"👤 You")
            st.info(message['human'])
        
        # AI response
        with st.container():
            st.write(f"🤖 Assistant ({st.session_state.selected_persona} mode)")
            st.success(message['AI'])
        
        # Add some spacing
        st.write("")

    # User input section
    st.markdown("### 💭 Your Message")
    user_question = st.text_area(
        "",
        height=100,
        placeholder="Type your message here... (Shift + Enter to send)",
        key="user_input",
        help="Type your message and press Shift + Enter or click the Send button"
    )

    # Input buttons
    col1, col2, col3 = st.columns([3, 1, 1])
    with col2:
        send_button = st.button("📤 Send", use_container_width=True)
    with col3:
        if st.button("🔄 New Topic", use_container_width=True):
            memory.clear()
            st.success("Memory cleared for new topic!")

    if send_button and user_question:
        if not st.session_state.start_time:
            st.session_state.start_time = datetime.now()

        with st.spinner('🤔 Thinking...'):
            try:
                response = conversation(user_question)
                message = {
                    'human': user_question,
                    'AI': response['response']
                }
                st.session_state.chat_history.append(message)
                st.rerun()
            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")

    # Footer
    st.markdown("---")
    st.markdown(
        "Using Groq AI with "
        f"{st.session_state.selected_persona.lower()} persona | "
        f"Memory: {memory_length} messages"
    )

if __name__ == "__main__":
    main()