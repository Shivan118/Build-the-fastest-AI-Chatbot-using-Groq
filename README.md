# Groq Chat Assistant
**Groq Chat Assistant** is an interactive chatbot application built with Streamlit that lets users engage with an AI model in a conversational way. It provides a customizable and dynamic chat experience, tailored to meet various user needs, from simple information gathering to expert advice and creative brainstorming.

## Features
1. **AI Model and Persona Selection**

- Choose between different AI models for optimal performance based on user preferences.
- Select conversation styles (personas) like:
    - Default: Friendly and helpful AI assistant.
    - Expert: In-depth, technical, and detailed responses.
    - Creative: Imaginative responses with analogies and creative language.

2. **Contextual Memory**

- The chatbot remembers recent messages, providing context-aware responses.
- Users can set how many previous messages the chatbot remembers for personalized and coherent conversations.

3. **Clear Chat Interface**

- Displays chat history with easy-to-read formatting for user messages and AI responses.
- Includes options to clear chat history and start new conversations.

4. **Real-Time Statistics**

- Tracks and displays useful chat stats like total message count and chat duration.

5. **Error Handling and Security**

- Handles any errors gracefully, providing clear feedback to the user.
- Keeps sensitive data secure by loading API keys from environment variables.

### Project Setup

#### 1. Clone the Repository
```bash
git clone <repository-url>
cd <project-folder>
```

#### 2. Create a Virtual Environment
```bash
conda create -p env python=3.10 -y
```

#### 3. Activate the Virtual Environment
```bash
conda activate env/
```

#### 4. Install Project Requirements
```bash
pip install -r requirements.txt
```

#### 5. Environment Variables
Create a .env file and add the required key-value pairs:
```bash
GROQ_API_KEY = your_api_key
```

#### 6. How to Run the Project
```bash
streamlit run app.py
```

## Usage
1. **Model & Persona Selection:** Choose an AI model and persona from the sidebar.
2. **Memory Configuration:** Set how many previous messages the chatbot should remember.
3. **Chat:** Type your messages and engage with the assistant in real time.
4. **Clear Chat & New Topics:** Clear the chat history or start a new topic as needed.
5. **View Stats:** Check the sidebar for conversation stats.
