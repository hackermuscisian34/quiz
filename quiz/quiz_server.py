from flask import Flask, render_template_string, request, session, redirect, url_for
import random
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Quiz questions database
QUESTIONS = [
    {
        "id": 1,
        "question": "What is the primary function of Advanced IP Scanner?",
        "options": [
            "Scanning documents",
            "Network discovery and scanning",
            "Virus scanning",
            "File compression"
        ],
        "correct": 1  # Index of correct answer (0-based)
    },
    {
        "id": 2,
        "question": "Which of the following information can Advanced IP Scanner retrieve about network devices?",
        "options": [
            "MAC addresses",
            "Device names",
            "Shared folders",
            "All of the above"
        ],
        "correct": 3
    },
    # Add more questions here...
]

# HTML template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Advanced IP Scanner Quiz</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .question {
            margin-bottom: 20px;
        }
        .options label {
            display: block;
            margin: 10px 0;
            padding: 10px;
            background-color: #f8f9fa;
            border-radius: 4px;
            cursor: pointer;
        }
        .options label:hover {
            background-color: #e9ecef;
        }
        .button {
            background-color: #007bff;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        .button:hover {
            background-color: #0056b3;
        }
        .result {
            margin-top: 20px;
            padding: 20px;
            background-color: #d4edda;
            border-radius: 4px;
            text-align: center;
        }
        .progress {
            margin-bottom: 20px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        {% if show_result %}
            <div class="result">
                <h2>Quiz Complete!</h2>
                <p>Your Score: {{ score }}/{{ total_questions }}</p>
                <p>Percentage: {{ (score/total_questions * 100)|round(2) }}%</p>
                <a href="/" class="button">Retake Quiz</a>
            </div>
        {% else %}
            <div class="progress">
                Question {{ current_question + 1 }} of {{ total_questions }}
            </div>
            <form method="POST">
                <div class="question">
                    <h3>{{ question.question }}</h3>
                    <div class="options">
                        {% for option in question.options %}
                            <label>
                                <input type="radio" name="answer" value="{{ loop.index0 }}" required>
                                {{ option }}
                            </label>
                        {% endfor %}
                    </div>
                </div>
                <button type="submit" class="button">Next Question</button>
            </form>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def quiz():
    if request.method == 'GET':
        # Initialize or reset the quiz
        session['questions'] = random.sample(QUESTIONS, len(QUESTIONS))
        session['current_question'] = 0
        session['score'] = 0
    
    if request.method == 'POST':
        # Check answer and update score
        question = session['questions'][session['current_question']]
        user_answer = int(request.form['answer'])
        if user_answer == question['correct']:
            session['score'] = session.get('score', 0) + 1
        
        # Move to next question
        session['current_question'] = session.get('current_question', 0) + 1

    # Show result if quiz is complete
    if session.get('current_question', 0) >= len(QUESTIONS):
        return render_template_string(
            HTML_TEMPLATE,
            show_result=True,
            score=session.get('score', 0),
            total_questions=len(QUESTIONS)
        )

    # Show next question
    question = session['questions'][session['current_question']]
    return render_template_string(
        HTML_TEMPLATE,
        show_result=False,
        question=question,
        current_question=session['current_question'],
        total_questions=len(QUESTIONS)
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)