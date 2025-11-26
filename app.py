import os
import json
from flask import Flask, render_template, request
from google import genai
from google.genai import types

app = Flask(__name__)

# Paste your API Key here (keep the quotes!)
GEMINI_API_KEY = os.environ.get("AIzaSyCGRh9FiKGa7K7f1V-7QYiElnmtsSTEDck")

# Initialize the Google GenAI Client
client = genai.Client(api_key=GEMINI_API_KEY)


def score_resume(resume_text):
    """
    Sends the resume text to Google Gemini (Flash model) to analyze.
    """
    try:
        # The prompt defines the persona and the strict JSON output format
        prompt = f"""
        You are an expert career coach and resume critic. Review the following resume text.
        
        1. Analyze it for Clarity, Impact (action verbs, metrics), and Structure.
        2. Assign a score from 0 to 100.
        3. Provide 3-5 specific, actionable improvements.
        
        STRICTLY return the result as a JSON object with this structure:
        {{
            "score": 85,
            "feedback": ["First improvement...", "Second improvement...", "Third improvement..."]
        }}

        Resume Text:
        {resume_text}
        """

        # Call the API using the Flash model (Fast & Free-tier eligible)
        # We use 'response_mime_type' to ensure Gemini gives us valid JSON
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        # Parse the JSON response
        # Gemini usually returns raw text, but with JSON mode, it's clean
        result = json.loads(response.text)

        return result.get("score", 0), result.get("feedback", [])

    except Exception as e:
        print(f"Error calling Gemini: {e}")
        return 0, [f"Error: {str(e)}. Check your API Key or Internet."]

# --- FLASK ROUTES ---


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        resume_text = request.form.get('resume_input')

        if not resume_text:
            return render_template('index.html', error="Please paste your resume text.")

        final_score, feedback = score_resume(resume_text)

        return render_template('index.html',
                               score=final_score,
                               feedback=feedback,
                               input_text=resume_text)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

