from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from openai import OpenAI
import os
from dotenv import load_dotenv

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

project_folder = os.path.expanduser('~/svarog')
load_dotenv(os.path.join(project_folder, '.env'))

key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key = key)

def generate_text(prompt):
    """Generates active recall questions based on a given prompt."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Give 1-2 active recall questions to user based on topics they studied or notes inputted. "
                           "Do not number the questions, separate the questions by the string |Ð|, and return all of "
                           "the questions on one line. For example: 'What did you learn about a random subject?|Ð|What "
                           "are the reasonings behind blank?'",
            },
            {"role": "user", "content": prompt},
        ]
    )
    return response

def check_answer(qa_obj):
    """Checks if the answer is correct, incorrect, or half-correct."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Based on the question and answer, determine if the answer is correct, incorrect, or half correct. "
                           "If the answer is correct, respond with 'C|Ð|Correct!'. If the answer is incorrect, respond with 'I'. "
                           "If the answer is half correct, respond with 'H'. After giving the grade, if the answer is not correct, "
                           "explain why, separated by the string |Ð|. Example: 'I|Ð|Because 2+2 does not equal 4.'",
            },
            {"role": "user", "content": qa_obj},
        ]
    )
    return response

@app.route("/generate_text", methods=["GET", "POST"])
def generate_text_endpoint():
    data = request.json
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Give 1-2 active recall questions to user based on topics they studied or notes inputted. "
                           "Do not number the questions, separate the questions by the string |Ð|, and return all of "
                           "the questions on one line. For example: 'What did you learn about a random subject?|Ð|What "
                           "are the reasonings behind blank?'",
            },
            {"role": "user", "content": prompt},
        ]
    )
    return jsonify({"response": response.choices[0].message.content})

@app.route("/check_answer", methods=["GET", "POST"])
@cross_origin()
def check_answer_endpoint():
    data = request.json
    qa_obj = data.get("qaObj", "")
    if not qa_obj:
        return jsonify({"error": "QA object is required"}), 400
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Based on the question and answer, determine if the answer is correct, incorrect, or half correct. "
                           "If the answer is correct, respond with 'C|Ð|Correct!'. If the answer is incorrect, respond with 'I'. "
                           "If the answer is half correct, respond with 'H'. After giving the grade, if the answer is not correct, "
                           "explain why, separated by the string |Ð|. Example: 'I|Ð|Because 2+2 does not equal 4.'",
            },
            {"role": "user", "content": qa_obj},
        ]
    )
    print(response.choices[0].message.content)
    return jsonify({"response": response.choices[0].message.content})

if __name__ == "__main__":
    app.run()
