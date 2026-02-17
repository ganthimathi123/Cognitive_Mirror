import os
from google import genai

# Initialize client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

try:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Give me 2 productivity tips."
    )

    if response.candidates:
        text = response.candidates[0].content.parts[0].text
        print("API Working ✅")
        print(text)
    else:
        print("No response generated.")

except Exception as e:
    print("Error ❌:", e)
