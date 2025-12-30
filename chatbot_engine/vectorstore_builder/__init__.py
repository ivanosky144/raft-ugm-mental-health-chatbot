import logging
from .ocr_converter import OCRConverter
from .data_chunker import DataChunker
from .faiss_indexer import FAISSIndexer

class VectorStoreBuilder:
    def __init__(self):
        self.ocr_converter = OCRConverter()
        self.data_chunker = DataChunker()
        self.faiss_indexer = FAISSIndexer()

    def run(self):
        logging.info("-- Running OCR Conversion")
        self.ocr_converter.convert_all_pdfs()

        logging.info("-- Chunking Text Files")
        self.data_chunker.chunk_all_files()

        logging.info("-- Building FAISS Index")
        self.faiss_indexer.build_index()

        logging.info("-- Vector Store Building Process is completed")