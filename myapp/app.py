import pickle
from flask import Flask,request,app,render_template
from sklearn.metrics.pairwise import cosine_similarity
import torch
import os


app=Flask(__name__)
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


# Load pre-trained BERT model and tokenizer
tokenizer=pickle.load(open("My_tokenizer.pkl",'rb'))
model=pickle.load(open("My_model.pkl",'rb'))

def calculate_similarity_score(sen1,sen2):
    # Tokenize input sentences
    sentences = [sen1,sen2]
    encoded_inputs = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')

    # Compute BERT embeddings for input sentences
    with torch.no_grad():
        outputs = model(**encoded_inputs)

    # Get last layer hidden states as sentence embeddings
    embeddings = outputs.last_hidden_state[:, 0, :]

    # Compute cosine similarity between two sentence embeddings

    similarity = cosine_similarity(embeddings[0].unsqueeze(0), embeddings[1].unsqueeze(0))
    return f"{similarity[0][0]*100:.2f}"

@app.route('/similarityScore',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      sen1 = request.form['sentence1']
      sen2 = request.form['sentence2']
      #print(sen1,sen2)
      score=calculate_similarity_score(sen1,sen2)
      return render_template('index.html',result = score)
   
if __name__=="__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)