from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain_community.llms import Ollama

class FrenchTutorAgent:
    def __init__(self, model_name="llama3"):
        """Initialize the French tutor agent with the specified model."""
        self.llm = Ollama(model=model_name)
        self.chat_history = [
            SystemMessage(content="""You are a helpful French language tutor.
            Help users learn French vocabulary, grammar, and practice conversation.
            When they write in French, correct any mistakes and explain the corrections.
            Be encouraging and supportive.""")
        ]
    
    def get_response(self, user_input):
        """Process user input and generate a response."""
        self.chat_history.append(HumanMessage(content=user_input))
        
        # Generate response based on the chat history
        response = self.llm.invoke(self.chat_history)
        
        # Handle the response (could be string or object depending on LangChain version)
        if isinstance(response, str):
            response_text = response
            response_message = AIMessage(content=response_text)
        else:
            response_text = response.content
            response_message = response
        
        # Add the response to chat history
        self.chat_history.append(response_message)
        
        return response_text