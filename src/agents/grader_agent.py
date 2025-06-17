from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain_community.llms import Ollama
import json

class GraderAgent:
    def __init__(self, model_name="llama3"):
        """Initialize the grading agent."""
        self.llm = Ollama(model=model_name)
        self.system_prompt = SystemMessage(content="""You are a French language grading assistant.
            Your job is to evaluate French translations by comparing student responses to correct translations.
            
            You should:
            1. Assign a score from 0.0 to 1.0 (0 = completely wrong, 1 = perfect)
            2. Provide constructive feedback on errors
            3. Offer suggestions for improvement
            
            Respond in the following JSON format:
            {"score": 0.85, "feedback": "Your detailed feedback here"}
            
            Be fair but thorough in your evaluation. Ignore incorrect accents or minor typos unless they significantly change the meaning.
            Focus on overall accuracy and fluency of the translation.""")
    
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
                    "score": 0.5,
                    "feedback": "Unable to parse grader response properly. Please check your translation manually."
                }
        except Exception as e:
            print(f"Error parsing grader response: {e}")
            return {
                "score": 0.5,
                "feedback": f"Error during grading: {str(e)}"
            }