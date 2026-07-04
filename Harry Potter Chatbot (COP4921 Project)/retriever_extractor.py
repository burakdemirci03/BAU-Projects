import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain_core.documents import Document


class RetrieverExtractor:
    embedding_model = "intfloat/multilingual-e5-base"
    model = SentenceTransformer(embedding_model)

    # ---------- EMBEDDING ---------- #
    # Embedding texts into vector representations
    def embed_text(self, texts):
        embeddings = []

        for text in texts:
            embedding = self.model.encode(text)
            embeddings.append(embedding.tolist())

        return embeddings


    # Adding texts and their embeddings to a JSON file
    def add_json(self, texts):
        if isinstance(texts, str):
            texts = [texts]
            
        embeddings = self.embed_text(texts)

        with open("storage/embeddings.json", "w+") as emb_file:
            try:
                file_data = json.load(emb_file)
            except (json.JSONDecodeError, FileNotFoundError):
                file_data = []

            for text, emb in zip(texts, embeddings):
                json_obj = {
                    "text": text,
                    "embedding": emb
                }
                file_data.append(json_obj)

            emb_file.seek(0)
            json.dump(file_data, emb_file, indent=2)


    # Reading documents and their embeddings from the JSON file
    def read_json(self):
        documents = []
        with open("storage/embeddings.json", "r") as emb_file:
            json_data = json.load(emb_file)
            for data in json_data:
                doc = Document(
                        page_content=data["text"],
                        metadata={
                            "embedding": data["embedding"]
                            }
                    )
                documents.append(doc)
            
        return documents


    # ---------- RETRIEVAL ---------- #
    # Similarity search to retrieve top-k relevant documents for a query
    def similarity_search(self, query, k=4):
        documents = self.read_json()
        if not documents:
            return []
        
        embeddings_list = [doc.metadata["embedding"] for doc in documents]
        dataset = np.array(embeddings_list).astype("float32")

        dimension = dataset.shape[1] 
        if not hasattr(self, 'index') or self.index == None:
            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(dataset)

        query_embedding = self.model.encode([query])
        query_embedding = np.array(query_embedding).astype("float32")

        distances, indices = self.index.search(query_embedding, k)

        results = []
        for idx in indices[0]:
            if idx != -1:
                results.append(documents[idx].page_content)

        return results
    

    # ---------- HISTORY MANAGEMENT ---------- #
    # Adding question-asnwer pairs to chat history
    def add_history(self, query, response, session_id):
        hst_obj = {
            "user": query,
            "assistant": response,
            "id": session_id
        }
        with open("storage/history.jsonl", "a") as hst_file:
            json.dump(hst_obj, hst_file)
            hst_file.write("\n")


    # Reading the last n entries from chat history
    def read_history(self, n=None):
        history = []
        if n == 0:
            return []
        
        try:
            with open("storage/history.jsonl", "r") as hst_file:
                for line in hst_file:
                    hst_obj = json.loads(line)
                    history.append(hst_obj)
        except FileNotFoundError:
            return history

        if n is not None:
            return history[-n:]
        else:
            return history
    

    # Clearing the entire chat history
    def clear_history(self):
        open("storage/history.jsonl", "w").close()


    # ---------- EXTRACTION ---------- #
    # Extracting text from uploaded file and adding to database
    def extract_txt(self, file):
        try:
            content = file.read().decode("utf-8").splitlines()
            contents = [line.strip() for line in content if line.strip()]
            self.add_json(contents)
            self.index = None
        except Exception as e:
            print(f"Error reading text file: {e}")
        