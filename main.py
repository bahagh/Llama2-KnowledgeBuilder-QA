from flask import Flask, request, jsonify, render_template
import urllib.request
import xml.etree.ElementTree as ET
import re
import openai
import yaml
with open('key.yml', 'r') as file:
    data = yaml.safe_load(file)
app = Flask(__name__)
openai.api_key = data.get('api').get('key')

def fetch_papers():
    """Fetches papers from the arXiv API and returns them as a list of strings."""
    url = 'http://export.arxiv.org/api/query?search_query=ti:llama&start=0&max_results=70'
    response = urllib.request.urlopen(url)
    data = response.read().decode('utf-8')
    root = ET.fromstring(data)

    papers_list = []

    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        title = entry.find('{http://www.w3.org/2005/Atom}title').text
        summary = entry.find('{http://www.w3.org/2005/Atom}summary').text
        paper_info = f"Title: {title}\nSummary: {summary}\n"
        papers_list.append(paper_info)

    return papers_list

def clean_text(text):
    """Remove unwanted characters and symbols from the text."""
    cleaned_text = re.sub(r"[^a-zA-Z0-9.,!?]", " ", text)
    cleaned_text2 = re.sub("\n", " ", cleaned_text)
    return cleaned_text2

def generate_embeddings(papers_list):
    """Generate embeddings from the cleaned data based on OpenAI embedding algorithms."""
    embeddings = []

    for paper_info in papers_list:
        cleaned_paper_info = clean_text(paper_info)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"{cleaned_paper_info}"}
            ],
            max_tokens=1000
        )
        embedding = response['choices'][0]['message']['content']
        embeddings.append(embedding)

    return embeddings

papers_list = fetch_papers()
embeddings = generate_embeddings(papers_list)

def answer_question(question, papers_list, embeddings):
    """Answer a question based on the provided papers_list and embeddings."""
    cleaned_question = clean_text(question)
    messages = [{"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"{cleaned_question}"}]

    total_tokens = 0
    for paper_info, embedding in zip(papers_list, embeddings):
        message_length = len(f"Paper Info: {clean_text(paper_info)}\nEmbedding: {embedding}")

        if total_tokens + message_length <= 4097:
            messages.append({"role": "assistant", "content": f"Paper Info: {clean_text(paper_info)}\nEmbedding: {embedding}"})
            total_tokens += message_length
        else:
            break

    # Generate the answer using OpenAI's GPT-3.5 Turbo
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1500
    )

    answer = response['choices'][0]['message']['content']
    return answer

@app.route('/')
def home():
    return render_template('iii.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('user_input', '')
    answer = answer_question(user_input, papers_list, embeddings)
    return jsonify({'response': answer})

if __name__ == '__main__':
    app.run(debug=False)
