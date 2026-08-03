# RAFT Mental Health Chatbot

This project implements a Retrieval-Augmented Fine-Tuning (RAFT) approach for a specialized mental health chatbot. The system combines the knowledge retrieval of a RAG (Retrieval-Augmented Generation) system with the specialized behavior of a fine-tuned LLM.

## Architecture Components

- **Web App:** Flask-based web application with RESTful API endpoints, utilizing JavaScript to handle dynamic interfaces.

![Web App Architecture](https://github.com/user-attachments/assets/c2211641-f47d-4fc4-b7c9-aae4a2210753)

- **Chatbot Engine:**
  The core operational unit responsible for knowledge indexing, context retrieval, and fine-tuning dataset generation.

![Chatbot Engine Architecture](https://github.com/user-attachments/assets/eb403254-4e81-4c3e-9fb8-8a27af355338)

  - **a. Vectorstore Builder:** Handles domain knowledge ingestion. It cleans raw mental health literature, chunks documents into optimal token lengths, generates dense vector embeddings, and indexes them into PostgreSQL using `pgvector` for similarity matching.

  ![Vector Store Data Flow](https://github.com/user-attachments/assets/93d70fb6-25fb-40e6-bb3d-22c94c4b4eb0)

  - **b. Retriever:** Fetches contextual knowledge in real time. It converts incoming user queries into vector embeddings, performs hybrid similarity search against the PostgreSQL store, and selects the top-$k$ relevant domain documents to construct context-aware prompts for the LLM.
  - **c. RAFT Preparation Pipeline:** Prepares synthetic fine-tuning datasets designed to teach the model how to ignore irrelevant context (distractor documents) and answer strictly using verified domain knowledge.

  ![Fine Tuning Preparation Data Flow](https://github.com/user-attachments/assets/84ed8fa3-90e3-4a8b-bcbc-3a57512a6909)

- **Cloud Architecture:**

![Cloud Architecture](https://github.com/user-attachments/assets/0dc6343c-65ad-4e29-82c4-6aa39618a8c2)

---

## Database ERD & Tech Stack

- **Languages:** Python 3.12 & JavaScript
- **Web Framework:** Flask
- **Databases:** PostgreSQL (knowledge retrieval system) & MongoDB (users and chats data)

![Entity Relationship Diagram](https://github.com/user-attachments/assets/07125779-1ecf-41a9-9c29-a49d0c5da504)

---

## Guide
### 1. Running the web app
To launch the user interface and API services for deployment or local testing:
`python main.py run-web app`

### 2. Building the vectorstore (domain knowledge)
To process your documents and build the semantic search index:
`python main.py run-engine vectorstore-builder`

### 3. Running the RAFT Pipeline
You can run the entire 5-phase data preparation sequence or target a specific phase using the --phase flag:
- Full Pipeline: `python main.py run-engine raft-preparation-pipeline`

- Specific Phase: `python main.py run-engine raft-preparation-pipeline --phase 4` (e.g., for CoT Augmentation)

### 4. Maintenance & Cleanup
To reset local data or clear cached outputs:
- Clear prepared data: `python main.py clean raft-data`
