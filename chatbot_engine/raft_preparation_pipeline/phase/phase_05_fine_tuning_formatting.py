from chatbot_engine.llm_client import GPTClient
import logging


class PhaseFiveFineTuningFormatting:
    def __init__(self, api_key, model="gpt-4o"):
        self.gpt_client = GPTClient(api_key=api_key, model=model)
        self.logger = logging.getLogger("PhaseFiveFineTuningFormatting")

    def _format_questions(self, grouped):
        grouped = grouped or []
        return "\n".join(
            f"Q{i+1}: {item.get('survey_question','')}"
            for i, item in enumerate(grouped)
        )

    def _format_scores(self, grouped):
        grouped = grouped or []
        return "\n".join(
            f"Q{i+1} Question: {item.get('survey_question','')} - Score: {item.get('score','')}"
            for i, item in enumerate(grouped)
        )

    def run(self, augmented_dialogs):
        fine_tuning_formatted_dialogs = []

        for dialog in augmented_dialogs:
            formatted_messages = []
            messages = dialog.get("messages", [])
            last_section = ""

            for i, msg in enumerate(messages):
                current_section = msg.get("section", "")
                current_group_id = 1
                
                if current_section != last_section:
                    current_group_id = 1
                else:
                    current_group_id += 1
                
                last_section = current_section

                msg_type = msg.get("type")

                next_msg = messages[i+1] if i + 1 < len(messages) else {}

                if msg_type == "Opening":

                    next_questions = next_msg.get("grouped_questions_score", [])

                    formatted_messages.append({
                        "role": "user",
                        "content": {
                            "type": "Opening",
                            "section": current_section,
                            "group_id": current_group_id,
                            "user_answer": msg.get("user_content", ""),
                            "next_questions": next_questions,
                            "scoring_system": next_msg.get("scoring_system", [])
                        }
                    })

                    formatted_messages.append({
                        "role": "assistant",
                        "content": {
                            "assistant_question": next_msg.get("assistant_content", "")
                        }
                    })

                elif msg_type == "Survey":

                    current_group = msg.get("grouped_questions_score", [])
                    next_group = next_msg.get("grouped_questions_score", [])

                    formatted_messages.append({
                        "role": "user",
                        "content": {
                            "type": "Survey",
                            "section": current_section,
                            "group_id": current_group_id,
                            "user_answer": msg.get("user_content", ""),
                            "next_questions": next_group,
                            "scoring_system": next_msg.get("scoring_system", []),
                            "set_of_documents": msg.get("set_of_documents", [])
                        }
                    })

                    formatted_messages.append({
                        "role": "assistant",
                        "content": {
                            "scores": current_group,
                            "chain_of_thought": msg.get("cot_augmentation", ""),
                            "assistant_question": next_msg.get("assistant_content", "")
                        }
                    })

                elif msg_type == "Ending":

                    formatted_messages.append({
                        "role": "user",
                        "content": {
                            "type": "Ending",
                            "user_answer": msg.get("user_content", "")
                        }
                    })

            fine_tuning_formatted_dialogs.append({
                "dialog_id": dialog.get("dialog_id"),
                "name": dialog.get("name"),
                "messages": formatted_messages
            })

        return fine_tuning_formatted_dialogs
