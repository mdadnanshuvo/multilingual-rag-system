from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import pickle

class VectorStore:
    def __init__(self, model_name='paraphrase-multilingual-MiniLM-L12-v2'):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.chunks = []

    def build_index(self, chunks):
        self.chunks = chunks
        embeddings = self.model.encode(chunks, show_progress_bar=True)

        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings))

    def save(self, folder_path='vector_store'):
        os.makedirs(folder_path, exist_ok=True)
        faiss.write_index(self.index, os.path.join(folder_path, 'faiss_index.bin'))

        with open(os.path.join(folder_path, 'chunks.pkl'), 'wb') as f:
            pickle.dump(self.chunks, f)

    def add_texts(self, new_chunks):
        embeddings = self.model.encode(new_chunks, show_progress_bar=False)

        if self.index is None:
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)

        self.index.add(np.array(embeddings))
        self.chunks.extend(new_chunks)

    def load(self, folder_path='vector_store'):
        self.index = faiss.read_index(os.path.join(folder_path, 'faiss_index.bin'))
        with open(os.path.join(folder_path, 'chunks.pkl'), 'rb') as f:
            self.chunks = pickle.load(f)

    def query(self, question, top_k=3):
        q_emb = self.model.encode([question])
        distances, indices = self.index.search(np.array(q_emb), top_k)
        results = [self.chunks[i] for i in indices[0]]
        return results
