## 🚀 Live Demo: [Try the chatbot](https://atharva-portfolio-chatbot.streamlit.app/)
# Personal Portfolio Chatbot (RAG)

An interactive chatbot embedded on my portfolio website that answers questions
about my background, projects, and skills — built using Retrieval-Augmented
Generation (RAG) rather than a hardcoded FAQ or static prompt.

## Why RAG instead of a static prompt?
Hardcoding my bio into a system prompt doesn't scale — every update means
touching the LLM logic. This project instead treats my personal context as
a separate knowledge base: I write about myself in plain text, the pipeline
chunks and embeds it, and the chatbot retrieves only the relevant pieces
per question. Updating my bio is just editing a text file and re-running
the indexer — no code changes needed.

## Features
- **Retrieval-Augmented Generation** — LangChain + FAISS vector store,
  Gemini for embeddings and generation.
- **Source citations** — every answer shows which chunks of context it was
  grounded in, so answers are traceable rather than opaque.
- **Hallucination guardrail** — the model is explicitly instructed to say
  when it doesn't have enough context, with a graceful fallback message,
  instead of guessing.
- **Evaluation set** — a small fixed test suite (`eval_set.py`) of
  questions with expected keywords, including negative test cases that
  should trigger the fallback, used to validate retrieval quality after
  every change to the knowledge base.

## Tech Stack
Python, LangChain, FAISS, Gemini API, Streamlit

## How it works
1. Personal context (bio, projects, skills) is written in `context.txt`.
2. `build_index.py` chunks the text and embeds it into a local FAISS
   vector index.
3. On each user question, the top-k most relevant chunks are retrieved
   and passed to Gemini along with the question.
4. The model answers strictly from the retrieved context, citing sources,
   or returns a fallback message if the context is insufficient.
