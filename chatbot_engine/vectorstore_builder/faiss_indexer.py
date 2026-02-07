import logging
import os
import json
import faiss
import tqdm
from sentence_transformers import SentenceTransformer


class FAISSIndexer:
    def __init__(self):
        self.chunked_files_dir = "./chunked_files"
        self.vectorstore_dir = "../vectorstore"
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

        os.makedirs(self.vectorstore_dir, exist_ok=True)

    def build_index(self):
        json_files = [
            f for f in os.listdir(self.chunked_files_dir)
            if f.endswith(".json")
        ]

        for filename in tqdm.tqdm(json_files, desc="Building FAISS indices"):
            aspect = filename.replace(".json", "")
            json_path = os.path.join(self.chunked_files_dir, filename)

            with open(json_path, "r", encoding="utf-8") as f:
                chunks = json.load(f)

            texts = self._extract_texts(chunks)

            logging.info(f"[{aspect}] Embedding {len(texts)} chunks...")
            embeddings = self._embed_chunks(texts)

            dim = embeddings.shape[1]
            index = faiss.IndexFlatL2(dim)
            index.add(embeddings)

            out_path = os.path.join(self.vectorstore_dir, f"{aspect}.faiss")
            faiss.write_index(index, out_path)

            logging.info(f"[{aspect}] Saved FAISS index → {out_path}")

    def _extract_texts(self, chunks):
        if isinstance(chunks[0], str):
            return chunks
        return [chunk["text"] for chunk in chunks if "text" in chunk]

    def _embed_chunks(self, texts):
        embeddings = self.embedding_model.encode(
            texts,
            batch_size=32,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return embeddings.astype("float32")
