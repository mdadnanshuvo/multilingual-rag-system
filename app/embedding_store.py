from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import pickle

class VectorStore:
    def __init__(self, model_name='paraphrase-multilingual-MiniLM-L12-v2') -> None:
        """
        Initializes the embedding store with a specified SentenceTransformer model.

        Args:
            model_name (str): Name of the pre-trained SentenceTransformer model to use. Defaults to 'paraphrase-multilingual-MiniLM-L12-v2'.

        Returns:
            None
        """
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.chunks = []

    def build_index(self, chunks) -> None:
        """
        Builds a FAISS index from a list of text chunks by encoding them into embeddings.
        Args:
            chunks (List[str]): List of text chunks to be indexed.
        Returns:
            None
        """
        self.chunks = chunks
        embeddings = self.model.encode(chunks, show_progress_bar=True)

        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings))

    def save(self, folder_path='vector_store') -> None:
        """
        Saves the FAISS index and associated data chunks to the specified folder.
        Args:
            folder_path (str): Path to the folder where the index and chunks will be saved. Defaults to 'vector_store'.
        Returns:
            None
        """
        os.makedirs(folder_path, exist_ok=True)
        faiss.write_index(self.index, os.path.join(folder_path, 'faiss_index.bin'))

        with open(os.path.join(folder_path, 'chunks.pkl'), 'wb') as f:
            pickle.dump(self.chunks, f)

    def add_texts(self, new_chunks) -> None:
        """
        Adds new text chunks to the embedding index.
        Args:
            new_chunks (List[str]): List of text chunks to be embedded and added.
        Returns:
            None
        """
        embeddings = self.model.encode(new_chunks, show_progress_bar=False)

        if self.index is None:
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)

        self.index.add(np.array(embeddings))
        self.chunks.extend(new_chunks)

    def load(self, folder_path='vector_store') -> None:
        """
        Loads the FAISS index and associated text chunks from the specified folder.

        Args:
            folder_path (str): Path to the folder containing 'faiss_index.bin' and 'chunks.pkl'. Defaults to 'vector_store'.

        Returns:
            None
        """
        self.index = faiss.read_index(os.path.join(folder_path, 'faiss_index.bin'))
        with open(os.path.join(folder_path, 'chunks.pkl'), 'rb') as f:
            self.chunks = pickle.load(f)

    def query(self, question, top_k=3) -> list[str]:
        """
        Queries the embedding index with a given question and retrieves the top_k most similar text chunks.

        Args:
            question (str): The input question to search for similar chunks.
            top_k (int, optional): The number of top similar results to return. Defaults to 3.

        Returns:
            List[str]: A list of the most similar text chunks.
        """
        q_emb = self.model.encode([question])
        distances, indices = self.index.search(np.array(q_emb), top_k)
        results = [self.chunks[i] for i in indices[0]]
        return results
