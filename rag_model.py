from transformers import AutoTokenizer, AutoModel
import torch
import faiss

tokenizer = AutoTokenizer.from_pretrained('facebook/dpr-question_encoder-single-nq-base')
model = AutoModel.from_pretrained('facebook/dpr-question_encoder-single-nq-base')


generator_tokenizer = AutoTokenizer.from_pretrained("gpt2")
generator_model = AutoModel.from_pretrained("gpt2")

with open(file='pregnancy_precautions.txt', mode='r') as f:
    corpus = f.readlines()


corpus_embeddings = []

for text in corpus:
    inputs = tokenizer(text=text, return_tensors='pt')
    embeddings = model(**inputs).pooler_output
    corpus_embeddings.append(embeddings)


corpus_embeddings = torch.cat(corpus_embeddings).detach().cpu().numpy()

index = faiss.IndexFlatL2(corpus_embeddings.shape[1])
index.add(corpus_embeddings)


def search(query):
    inputs = tokenizer(query, return_tensors='pt', truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        query_embedding = model(**inputs).pooler_output.detach().cpu().numpy()
    

    D, I = index.search(query_embedding, k=5) 
    return [corpus[i] for i in I[0]]