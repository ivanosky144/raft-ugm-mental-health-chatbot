import faiss
import os
import numpy as np
import logging
import pickle

from sentence_transformers import SentenceTransformer

class Retriever:
    def __init__(self):
        self.vectorstore_dir = "./vectorstore"
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.logger = logging.getLogger("Retriever")

        self.indices = {}
        self.texts = {}
        self._load_all()
    
    def _load_all(self):
        section_meta_path = os.path.join(self.vectorstore_dir, "section_data.pkl")

        if not os.path.exists(section_meta_path):
            raise FileNotFoundError("Missing `section_data.pkl`. Vector store incomplete")
        
        with open(section_meta_path, "rb") as f:
            section_data = pickle.load(f)
        
        for aspect, data in section_data.items():
            index_path = os.path.join(self.vectorstore_dir, f"{aspect}.index")

            if not os.path.exists(index_path):
                self.logger.warning(f"Missing FAISS index for aspect: {aspect}")
                continue

            self.indices[aspect] = faiss.read_index(index_path)
            self.texts[aspect] = data["texts"]

    def run(self, query, aspect, top_k = 5):
        if aspect not in self.indices:
            return ValueError(f"Aspect {aspect} index not found")
        
        index = self.indices[aspect]
        texts = self.texts[aspect]

        query_vector = self.embedding_model.encode([query]).astype("float32")

        distances, indices = index.search(query_vector, top_k)

        results = []
        for rank, idx in enumerate(indices[0]):
            if idx < 0 or idx >= len(texts):
                continue

            results.append({
                "rank": rank + 1,
                "score": float(distances[0][rank]),
                "chunk": texts[idx]
            })
        
        return results