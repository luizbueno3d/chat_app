from flask import Flask, request, render_template, jsonify
import os
from groq import Client

app = Flask(__name__)

# Retrieve API key from environment variable
api_key = os.getenv('GROQ_API_KEY')
client = Client(api_key=api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['message']
    with open('train.txt', 'r') as file:
        training_data = file.read()

    # Combine training data and user input for context
    prompt = f"{training_data}\n\nUser: {user_input}\nAssistant:"

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama3-8b-8192"
    )

    answer = response.choices[0].message.content
    return jsonify({'response': answer})

if __name__ == '__main__':
    app.run(debug=True)