
import google.generativeai as genai
import json

# Directly configure API key
genai.configure(api_key="AIzaSyDbkU3RBUWu04dd6KBWKSpxA2KcmOYgdF4")

class AIClient:

    def __init__(self):

        # Use Gemini 2.5 Flash
        self.model = genai.GenerativeModel("gemini-2.5-flash")


    def chat_completion(self, system_prompt, prompt):

        full_prompt = system_prompt + "\n\n" + prompt

        response = self.model.generate_content(full_prompt)

        return response.text


    def extract_json_and_summary(self, text):

        try:

            start = text.find("{")
            end = text.rfind("}") + 1

            json_text = text[start:end]

            data = json.loads(json_text)

            summary = text[end:]

            return {
                "itinerary_json": data,
                "summary_text": summary
            }

        except:

            return {
                "itinerary_json": {},
                "summary_text": text
            }
