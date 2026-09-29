# 🎓 College RAG Assistant

An AI-powered **Document Question Answering System** built using
**Retrieval-Augmented Generation (RAG)**.

The application allows users to upload a PDF document and ask questions
about its content in natural language. Instead of relying only on the
LLM's general knowledge, the system retrieves relevant information from
the uploaded document and uses that information to generate a
document-grounded answer.

## 🚀 Live Demo

👉 **Try the application here:**

https://college-rag-mljxn5gfprym8qft3nebzb.streamlit.app/

---

## 📌 Project Overview

College RAG Assistant is designed to make it easier to interact with
college-related documents such as:

- 📚 College rules and regulations
- 📝 Examination rules
- 🎓 Academic documents
- 📅 Attendance policies
- 🏠 Hostel guidelines
- 📄 Student handbooks
- 📑 Notes and study materials
- 📋 Other text-based PDF documents

Instead of manually searching through a long PDF, users can simply
upload the document and ask questions.

### Example

**User uploads:**

`College_Rules.pdf`

**User asks:**

> What is the minimum attendance requirement?

The system searches the uploaded document, retrieves the most relevant
sections, and generates an answer based on that retrieved information.

---

# 🧠 What is RAG?

**RAG stands for Retrieval-Augmented Generation.**

It combines two important concepts:

### Retrieval

The system searches the uploaded document and finds the pieces of
information most relevant to the user's question.

### Generation

The retrieved information is provided to a Large Language Model (LLM),
which generates a clear natural-language answer.

Therefore, instead of asking the LLM to answer from general knowledge,
the system first retrieves relevant information from the user's document.

---

# 🏗️ System Architecture

```text
                    ┌─────────────────┐
                    │   Upload PDF    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   PDF Loader    │
                    │     pypdf       │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    Chunking     │
                    │  500 characters │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Embeddings    │
                    │ MiniLM-L6-v2    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  FAISS Index    │
                    │ Vector Search   │
                    └────────┬────────┘
                             │
                             │
              ┌──────────────┘
              │
              ▼
       ┌─────────────────┐
       │  User Question  │
       └────────┬────────┘
                │
                ▼
       ┌─────────────────┐
       │ Query Embedding │
       └────────┬────────┘
                │
                ▼
       ┌─────────────────┐
       │ FAISS Similarity│
       │     Search      │
       └────────┬────────┘
                │
                ▼
       ┌─────────────────┐
       │ Top-K Relevant  │
       │     Chunks      │
       └────────┬────────┘
                │
                ▼
       ┌─────────────────┐
       │  Gemini LLM     │
       │ Context + Query │
       └────────┬────────┘
                │
                ▼
       ┌─────────────────┐
       │ Final Answer    │
       └─────────────────┘
