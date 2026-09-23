import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle
import os

class VectorStore:
    def __init__(self, model_name='all-MiniLM-L6-v2', index_path='data/faiss_index.bin', metadata_path='data/metadata.pkl'):
        self.encoder = SentenceTransformer(model_name)
        self.embedding_size = self.encoder.get_sentence_embedding_dimension()
        
        self.index_path = index_path
        self.metadata_path = metadata_path
        
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        
        if os.path.exists(self.index_path) and os.path.exists(self.metadata_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.metadata_path, 'rb') as f:
                self.metadata = pickle.load(f)
        else:
            self.index = faiss.IndexFlatL2(self.embedding_size)
            self.metadata = [] 

    def add_texts(self, texts, metadatas):
        if not texts:
            return
        embeddings = self.encoder.encode(texts)
        self.index.add(np.array(embeddings).astype('float32'))
        self.metadata.extend(metadatas)
        self.save()

    def search(self, query: str, k: int = 5):
        if self.index.ntotal == 0:
            return []
            
        query_vector = self.encoder.encode([query])
        distances, indices = self.index.search(np.array(query_vector).astype('float32'), k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1:
                results.append({
                    "metadata": self.metadata[idx],
                    "distance": float(distances[0][i])
                })
        return results
        
    def save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, 'wb') as f:
            pickle.dump(self.metadata, f)
            
    def get_all_embeddings(self):
        if self.index.ntotal == 0:
            return np.array([]), []
            
        vectors = np.zeros((self.index.ntotal, self.embedding_size), dtype=np.float32)
        for i in range(self.index.ntotal):
            vectors[i] = self.index.reconstruct(i)
            
        return vectors, self.metadata
