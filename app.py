
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

QUESTIONS = [
    {
        "id": 1,
        "question": "Which language is used to create web page structure?",
        "options": ["Python", "HTML", "SQL", "C++"],
        "correct_answer": "HTML"
    },
    {
        "id": 2,
        "question": "Which of these is a Python data type?",
        "options": ["integer", "browser", "keyboard", "monitor"],
        "correct_answer": "integer"
    },
    {
        "id": 3,
        "question": "Which tag is used for the largest HTML heading?",
        "options": ["<h6>", "<head>", "<h1>", "<p>"],
        "correct_answer": "<h1>"
    },
    {
        "id": 4,
        "question": "Which language is commonly used to style web pages?",
        "options": ["CSS", "SQL", "C", "Bash"],
        "correct_answer": "CSS"
    },
    {
        "id": 5,
        "question": "Which keyword defines a function in Python?",
        "options": ["function", "define", "func", "def"],
        "correct_answer": "def"
    }
]


@app.route("/")
def home():
    # Do not expose correct answers to the browser.
    public_questions = [
        {
            "id": q["id"],
            "question": q["question"],
            "options": q["options"]
        }
        for q in QUESTIONS
    ]
    return render_template("index.html", questions=public_questions)


@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid submission"}), 400

    answers = data.get("answers")

    if not isinstance(answers, dict):
        return jsonify({"error": "Answers must be provided"}), 400

    allowed_ids = {str(q["id"]) for q in QUESTIONS}
    if not set(answers.keys()).issubset(allowed_ids):
        return jsonify({"error": "Invalid question ID"}), 400

    allowed_options = {
        str(q["id"]): q["options"] for q in QUESTIONS
    }

    for question_id, answer in answers.items():
        if (
            not isinstance(answer, str)
            or answer not in allowed_options[question_id]
        ):
            return jsonify({"error": "Invalid answer option"}), 400

    # Calculate the score on the server.
    correct_answers = {
        str(q["id"]): q["correct_answer"] for q in QUESTIONS
    }

    score = sum(
        1
        for question_id, answer in answers.items()
        if answer == correct_answers[question_id]
    )

    total_questions = len(QUESTIONS)

    return jsonify({
        "message": "Your quiz has been submitted successfully.",
        "submitted": True,
        "score": score,
        "total": total_questions
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
