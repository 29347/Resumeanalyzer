import os
import json
from flask import Flask, render_template, request
from google import genai
from google.genai import types

app = Flask(__name__)

# --- CONFIGURATION ---
# Get API Key from Render Environment Variables
# TEMPORARY FOR TESTING (Remove before uploading to GitHub!)
GEMINI_API_KEY = os.environ.get("AIzaSyBUQXZnjyu5d5OjOarmaptgV2ydprJps70")
client = genai.Client(api_key=GEMINI_API_KEY)


def score_resume_pdf(file_bytes):
    """
    Sends PDF bytes directly to Gemini for analysis.
    """
    try:
        prompt = """
        You are an expert technical recruiter. Review this attached resume PDF.
        
        1. Analyze the layout, skills, and impact.
        2. Assign a score from 0-100.
        3. Provide 3-5 specific, harsh but constructive improvements.
        
        STRICTLY return the result as this JSON format:
        {
            "score": 85,
            "feedback": ["Point 1", "Point 2", "Point 3"]
        }
        """

        # We pass the raw PDF bytes directly to the model!
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(
                    data=file_bytes, mime_type="application/pdf"),
                prompt
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        result = json.loads(response.text)
        return result.get("score", 0), result.get("feedback", [])

    except Exception as e:
        print(f"Error calling Gemini: {e}")
        return 0, [f"Error processing PDF. Please ensure it is a valid PDF file."]


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if file is present in the request
        if 'resume_file' not in request.files:
            return render_template('index.html', error="No file uploaded.")

        file = request.files['resume_file']

        if file.filename == '':
            return render_template('index.html', error="No selected file.")

        if file:
            # Read the file into memory (bytes)
            file_bytes = file.read()
            final_score, feedback = score_resume_pdf(file_bytes)

            return render_template('index.html',
                                   score=final_score,
                                   feedback=feedback)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

