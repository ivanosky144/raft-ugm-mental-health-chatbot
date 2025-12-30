import json
import logging
from chatbot_engine.llm_client import GPTClient


class PhaseTwoDialogExpansion:
    def __init__(self, api_key, model="gpt-4o"):
        self.gpt_client = GPTClient(api_key=api_key, model=model)

    def run(self, personas):
        """
        personas: list of persona objects from Phase One output
        returns: list of conversation objects
        """

        conversations = []

        system_prompt = """
You are a clinical dialog generator.

Return ONLY valid JSON. No markdown. No explanations.

Generate ONE object:
{
  "messages": []
}

Rules:
- Follow section order exactly
- Ask ALL survey questions
- Rephrase each survey question naturally in Indonesian but preserve its meaning
- Generate user answer in Indonesian based on persona
- After each user answer to the question asked by the assistant, output a function call:
  name: score_response
  content must include:
    section
    survey_question (exact original text)
    score (the scale is based on the scoring_system in the section currently asked)

Scoring system:
Based on the scoring_system given in each section
"""

        for persona in personas:
            user_prompt = f"""
Persona data (JSON):

{json.dumps(persona, ensure_ascii=False)}

Generate the full conversation now.
"""

            raw_output = self.gpt_client.run_prompt(system_prompt, user_prompt)

            try:
                data = json.loads(raw_output)
            except json.JSONDecodeError as e:
                logging.error(
                    f"PhaseTwo JSON parse failed for dialog_id={persona.get('dialog_id')}: {e}"
                )
                continue

            if "messages" not in data:
                logging.error(
                    f"PhaseTwo output missing 'messages' for dialog_id={persona.get('dialog_id')}"
                )
                continue

            conversations.append({
                "dialog_id": persona.get("dialog_id"),
                "name": persona.get("name"),
                "messages": data["messages"]
            })

        return conversations
