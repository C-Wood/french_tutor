from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain_community.llms import Ollama
import json

class SentenceGeneratorAgent:
    def __init__(self, model_name="llama3"):
        """Initialize the sentence generator agent."""
        self.llm = Ollama(model=model_name)
        self.system_prompt = SystemMessage(content="""You are a French language sentence generator.
            Your job is to generate appropriate French sentences at the requested difficulty level
            along with their English translations. 
            
            Always respond in the following JSON format:
            {"english": "English sentence", "french": "French translation"}
            
            Ensure your translations are accurate and appropriate for the level.""")
    
    def generate_sentence(self, difficulty="beginner", topic=None):
        """Generate a sentence at the specified difficulty level and optionally on a specific topic."""
        prompt = f"Generate a {difficulty} level French sentence"
        if topic:
            prompt += f" about {topic}"
        
        messages = [
            self.system_prompt,
            HumanMessage(content=prompt)
        ]
        
        # Generate response
        response = self.llm.invoke(messages)
        
        # Extract JSON data from the response
        try:
            # Handle the response (could be string or object)
            response_text = response if isinstance(response, str) else response.content
            
            # Find JSON in the response
            response_text = response_text.strip()
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx >= 0 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                data = json.loads(json_str)
                return data
            else:
                # Fallback if JSON parsing fails
                return {
                    "english": "The cat is on the table.",
                    "french": "Le chat est sur la table."
                }
        except Exception as e:
            print(f"Error parsing generator response: {e}")
            return {
                "english": "The cat is on the table.",
                "french": "Le chat est sur la table."
            }