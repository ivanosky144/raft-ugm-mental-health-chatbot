import logging
import tqdm
import os
import faiss
import json
from sentence_transformers import SentenceTransformer


class FAISSIndexer:
    def __init__(self):
        self.chunked_files_dir = "./chunked_files"
        self.vectorstore_dir = "../vectorstore"
        self.embedding_model = "text-embedding-3-small"
    
    def build_index(self):
        json_files = [f for f in self.chunked_files_dir if f.endswith(".json")]

        for filename in tqdm(json_files, desc="Building FAISS indices"):
            aspect = filename.replace(".json", "")
            json_path = os.path.join(self.chunked_files_dir, filename)
            with open(json_path, "r", encoding="utf-8") as f:
                chunks = json.load(f)

            logging.info(f"[{aspect}] Embedding {len(chunks)} chunks...")
            embeddings = self._embed_chunks(chunks)

            dim = embeddings.shape[1]
            index = faiss.IndexFlatL2(dim)
            index.add(embeddings)

            out_path = os.path.join(self.index_dir, f"{aspect}.faiss")
            faiss.write_index(index, out_path)

            logging.info(f"[{aspect}] Saved FAISS index → {out_path}")

    def _embed_chunks(self, chunks):
        embeddings = self.embedding_model.encode(
            chunks,
            batch_size=32,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True  
        )

        return embeddings.astype("float32")