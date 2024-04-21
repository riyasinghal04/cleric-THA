from flask import Flask, request, jsonify, render_template
from pydantic import BaseModel
from typing import List
import asyncio
from get_facts import get_facts
from http.server import BaseHTTPRequestHandler

app = Flask(__name__)

class SubmitQuestionAndDocumentsRequest(BaseModel):
    question: str
    documents: List[str]

class GetQuestionAndFactsResponse(BaseModel):
    question: str
    facts: List[str]
    status: str

processed_facts = None
question = None

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        question = request.form.get('question')
        documents = request.form.get('documents').split("\n") #list 
        facts = get_facts(question, documents)
        return render_template('output.html', question=question, facts=facts)
    else:
        return render_template('index.html')
        
@app.route('/test', methods=['GET', 'POST'])
def test():
    return "hello"


@app.route('/submit_question_and_documents', methods=['POST'])
def submit_question_and_documents():
    data = request.json

    global question
    question = data.get('question')
    documents = data.get('documents')

    global processed_facts
    processed_facts = get_facts(question, documents)

    return jsonify({'status': 'done'}), 200


@app.route('/get_question_and_facts', methods=['GET'])
def get_question_and_facts():
    global processed_facts
    global question

    if processed_facts:
        return jsonify({
            'question':question ,  
            'facts': processed_facts,
            'status': 'done'
        }), 200
    else:
        return jsonify({
            'question': question,  
            'facts': [],
            'status': 'processing'
        }), 200



if __name__ == '__main__':
    app.run(debug=True)
