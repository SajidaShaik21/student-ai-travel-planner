
import google.generativeai as genai
import streamlit as st
import json

class AIClient:

    def __init__(self):

        # get API key from Streamlit secrets
        api_key = st.secrets["GEMINI_API_KEY"]

        genai.configure(api_key=api_key)

        # safest working model
        self.model = genai.GenerativeModel(model_name="gemini-1.5-flash")


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
