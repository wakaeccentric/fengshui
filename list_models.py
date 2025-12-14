import google.generativeai as genai
import os

# .envファイルからAPIキーを読み込む
api_key = ""
try:
    with open("c:/opt/data/ai/fengshui/.env", "r") as f:
        for line in f:
            if line.startswith("GEMINI_API_KEY="):
                api_key = line.split("=", 1)[1].strip()
                break
except FileNotFoundError:
    print("Error: .env file not found")
    exit(1)

if not api_key or api_key == "your_api_key_here":
    print("Error: Please set your actual API key in .env file")
    exit(1)

print(f"Using API key: {api_key[:10]}...")

genai.configure(api_key=api_key)

print("\nListing all available models:")
try:
    models = list(genai.list_models())
    print(f"Total models found: {len(models)}\n")

    vision_models = []
    for m in models:
        try:
            if "generateContent" in m.supported_generation_methods:
                vision_models.append(m.name)
                print(f"✓ {m.name}")
        except Exception as e:
            print(f"✗ {m.name} - Error: {e}")

    print(f"\n\nTotal vision models: {len(vision_models)}")

    if vision_models:
        print("\nCopy these model names to fengshui_analyzer.py:")
        for model in vision_models:
            print(f"    '{model}',")
    else:
        print("\nNo vision models found!")

except Exception as e:
    print(f"Error listing models: {e}")
