from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain_community.llms import Ollama
import json
import re
from langchain_ollama import OllamaLLM

class SentenceGeneratorAgent:
    def __init__(self, model_name="llama3"):
        """Initialize the sentence generator agent."""
        self.llm = OllamaLLM(model=model_name)
        self.system_prompt = SystemMessage(content="""You are a French language sentence generator.
            Your job is to generate appropriate French sentences at the requested difficulty level
            along with their English translations. 
            
            Always respond in the following JSON format:
            {"english": "English sentence", "french": "French translation"}
            
            Ensure your translations are accurate and appropriate for the level.""")
    
    def parse_llm_json(self, response_text):
        """Parse JSON from LLM response with robust error handling."""
        try:
            # Handle the response (could be string or object)
            if not isinstance(response_text, str):
                response_text = response_text.content
            
            # Clean the response text of control characters
            # This regex replaces control characters with empty strings
            response_text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', response_text)
            
            # Find JSON in the response
            response_text = response_text.strip()
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx >= 0 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                return json.loads(json_str)
            else:
                raise ValueError("No JSON object found in response")
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            print(f"Response text: {response_text}")
            return None
    
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
        
        # Parse the response
        data = self.parse_llm_json(response)
        
        if data and "english" in data and "french" in data:
            return data
        else:
            # Fallback if JSON parsing fails
            return {
                "english": "The cat is on the table.",
                "french": "Le chat est sur la table."
            }