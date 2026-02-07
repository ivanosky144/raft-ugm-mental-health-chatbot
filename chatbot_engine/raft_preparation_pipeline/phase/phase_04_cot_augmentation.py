from chatbot_engine.llm_client import GPTClient
import json
import logging

class PhaseFourCoTAugmentation:
    def __init__(self, api_key, model = "gpt-4o"):
        self.gpt_client = GPTClient(api_key=api_key, model=model)
        self.logger = logging.getLogger("PhaseFourCOTAugmentation")
        pass
        
    def augment_question(self, original_question, user_answer, reference_texts):
        system_prompt = """
You are a COT (Chain of Thought) augmentation generator.
Your task is to rewrite the assistant's question so that it sounds more emphatetic, human-like, and clinically appropriate.\n\n
You will be given:\n
1. The original question asked by the assistant.\n
2. The user's answer to that question.\n
3. A set of 5 reference texts from psychology books and theories.\n\n

Return ONLY valid JSON with this format:\n
{
    "chain_of_thought": "...",
    "rewritten_question": "..."
}

Rules:\n
Rules:
1. First, internally select the most relevant reference text(s) from the provided set to guide the rewriting.
2. Generate the chain_of_thought in Indonesian as internal reasoning only.
   - Do NOT address the user.
   - Do NOT use second-person pronouns (Anda, kamu, dsb.).
   - Do NOT sound like psychoeducation or a response to the user.
   - Focus on why certain reference text(s) are relevant or irrelevant based on the user's answer NOT the original question.
   - Explicitly reflect the clinical stance (e.g., normalizing, clarifying, grounding, exploratory).
3. Do not quote, name, or mention any psychological theories, frameworks, or book concepts.
4. Use the selected reference text(s) only to guide tone, sensitivity, and clinical understanding when rewriting the question.
5. The rewritten_question must be suitable for a mental health assessment conversation and phrased naturally for the user.
6. Return ONLY valid JSON that matches the required format.
        """

        user_prompt = f"""
ORIGINAL QUESTION:
{original_question}

USER ANSWER:
{user_answer}

REFERENCE TEXTS (select the most relevant ones to guide your rewriting):
{reference_texts}
        """

        response = self.gpt_client.run_prompt(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        return json.loads(response)
    

    def run(self, refined_dialogs):
        augmented_dialogs = []

        for dialog in refined_dialogs:
            dialog_id = dialog.get("dialog_id")
            self.logger.info(f"Augmenting dialog_id={dialog_id}")

            augmented_messages = []

            for msg in dialog.get("messages", []):
                if msg["type"] == "Opening":        
                    augmented_messages.append(msg)
                    continue

                if msg["type"] == "Survey":
                    documents = msg.get("set_of_documents", [])
                    if not documents:
                        augmented_messages.append(msg)
                        continue

                    try:
                        output = self.augment_question(
                            original_question=msg.get("assistant_question", ""),
                            user_answer=msg.get("user_answer", ""),
                            reference_texts="\n\n".join(
                                doc["chunk"]
                                for doc in documents
                            )
                        )

                        augmented_messages.append({
                            **msg,
                            "cot_augmentation": output["chain_of_thought"],
                            "assistant_content": output["rewritten_question"]
                        })

                    except Exception as e:
                        self.logger.error(
                            f"PhaseFour COT augmentation failed for dialog_id={dialog_id} message_id={msg.get('message_id')}: {e}"
                        )


            augmented_dialogs.append({
                "dialog_id": dialog_id,
                "name": dialog.get("name"),
                "messages": augmented_messages
            })

        
        return augmented_dialogs
            