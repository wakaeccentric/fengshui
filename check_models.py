import google.generativeai as genai
import os

# API key should be set in environment or passed directly
# For this script, we'll ask the user to input it or try to read from env if possible,
# but since I can't interactively ask in a script easily without input,
# I'll assume the user might have set it or I'll catch the error.

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Please set GEMINI_API_KEY environment variable or modify this script.")
else:
    genai.configure(api_key=api_key)
    try:
        print("Listing available models...")
        for m in genai.list_models():
            if "generateContent" in m.supported_generation_methods:
                print(f"Model: {m.name}")
    except Exception as e:
        print(f"Error: {e}")
