from chatbot_engine.llm_client import GPTClient
import logging

class PhaseFiveFineTuningFormatting:
    def __init__(self, api_key, model = "gpt-4o"):
        self.gpt_client = GPTClient(api_key=api_key, model=model)
        pass
        
    def run(self):
        result = self.process_prompt()

        return result
    
    def process_prompt(self, content):
        system_prompt = ""
        result = self.gpt_client.run_prompt(system_prompt, content)
        return result
