from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain_community.llms import Ollama
import json
import re
from langchain_ollama import OllamaLLM

class GraderAgent:
    def __init__(self, model_name="llama3"):
        """Initialize the grading agent."""
        self.llm = OllamaLLM(model=model_name)
        self.system_prompt = SystemMessage(content="""You are a French language grading assistant.
            Your job is to evaluate French translations by comparing student responses to correct translations.
            
            You should:
            1. Assign a score from 0.0 to 1.0 (0 = completely wrong, 1 = perfect)
            2. Provide constructive feedback on errors
            3. Offer suggestions for improvement
            
            Respond in the following JSON format:
            {"score": 0.85, "feedback": "Your detailed feedback here"}
            
            Be fair but thorough in your evaluation.""")
    
    def parse_llm_json(self, response_text):
        """Parse JSON from LLM response with robust error handling."""
        try:
            if not isinstance(response_text, str):
                response_text = response_text.content

            # Remove control characters
            response_text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', response_text)

            # Extract the first JSON object
            match = re.search(r'\{.*?\}', response_text, re.DOTALL)
            if match:
                json_str = match.group(0)
                # Fix invalid backslashes
                json_str = re.sub(r'\\(?!["\\/bfnrtu])', r"\\\\", json_str)
                return json.loads(json_str)
            else:
                raise ValueError("No JSON object found in response")
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            print(f"Response text: {response_text}")
            return None
    
    def grade_translation(self, correct_french, user_translation):
        """Grade a user's French translation against the correct version."""
        prompt = f"""Please grade this French translation:
        
        Original (correct): {correct_french}
        Student translation: {user_translation}
        
        Provide a score and specific feedback on any errors."""
        
        messages = [
            self.system_prompt,
            HumanMessage(content=prompt)
        ]
        
        # Generate response
        response = self.llm.invoke(messages)
        
        # Parse the response
        data = self.parse_llm_json(response)
        
        if data and "score" in data and "feedback" in data:
            return data
        else:
            # Fallback if JSON parsing fails
            return {
                "score": 0.5,
                "feedback": "Unable to parse grader response properly. Please check your translation manually."
            }