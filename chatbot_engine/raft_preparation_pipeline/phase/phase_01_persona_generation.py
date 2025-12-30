import json
import logging
from chatbot_engine.llm_client import GPTClient

class PhaseOnePersonaGeneration:

    def __init__(self, api_key, model="gpt-4o"):
        self.gpt_client = GPTClient(api_key, model)
        return
    
    def run(self, grouped_questions):
        system_prompt = """
You are a JSON generator.

Return ONLY a raw JSON array. Do not include ``` or any markdown. Do not explain anything.

Generate exactly 10 items. Each item must contain:
- dialog_id (integer)
- name (string)
- persona (string)
- sections (array of strings)

Rules:
- Name must be a realistic Indoensian college student name.
- Persona must be 2–4 sentences in Indonesian.
- Sections must always begin with "Opening" and end with "Ending".
- Choose 4 random middle sections from:
  Depression, Anger, Mania, Anxiety, Somatic, Suicidal, Psychosis, Sleep Disturbance, Memory, Dissociation, Substance Use, Repetitive Thought

Output only JSON. No extra text.

Example
"""     
        user_prompt =  """ same instruction """
        raw_data = self.gpt_client.run_prompt(system_prompt, user_prompt)

        try: 
            data = json.loads(raw_data)
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse model output as JSON: {e}")
            return []
        
        question_lookup = {
            item["section"]: {
                "scoring_system": item.get("scoring_system", []),
                "grouped_questions": item.get("grouped_questions", [])
            }
            for item in grouped_questions
        }

        for persona in data:
            sections = persona.get("sections", [])
            persona["question_map"] = {}

            for section in sections:
                if section in ("Opening", "Ending"):
                    continue

                if section in question_lookup:
                    persona["question_map"][section] = question_lookup[section]

        return data
            


