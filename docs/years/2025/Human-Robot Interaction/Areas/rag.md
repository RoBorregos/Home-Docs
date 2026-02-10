# RAG

## Overview

`RAGService` integrates a knowledge base with large language model (LLM) reasoning to answer natural language questions. The system retrieves relevant context from multiple knowledge bases, uses embeddings and similarity metrics for relevance scoring, and generates coherent answers via an LLM.

---

## What is RAG?

**Retrieval-Augmented Generation (RAG)** combines:
- **Retrieval**: Searching a knowledge base or document collection for relevant information related to a query.
- **Augmented Generation**: Conditioning a generative language model on retrieved context to produce precise, informative answers.

RAG improves LLM accuracy by grounding responses in specific, relevant documents instead of relying solely on model parameters.

---

## Use Case

The `RAGService` is designed to provide a conversational AI interface for answering questions based on curated knowledge bases. This is useful for:

- Fetch previous command history
- On grpc answer any question asked by the host with some context

---

## Architecture and Implementation

### Components

- **ROS 2 Node (`RAGService`)**: Implements the service that listens for question requests and responds with generated answers.
- **ChromaAdapter**: Interface to vector search over knowledge bases, handling embedding queries and document retrieval.
- **OpenAI LLM Client**: Connects to an LLM API for question cleaning and answer generation.
- **Dialogs module (`clean_question_rag` & `get_answer_question_dialog`)**: Prepares prompts and context for the LLM.

### Key Functionalities

| Feature                      | Description                                                                                         |
|------------------------------|-------------------------------------------------------------------------------------------------|
| **Initialization**           | Reads ROS parameters; sets up `ChromaAdapter`, `OpenAI` client, and `AnswerQuestion` service.    |
| **Cosine Similarity**        | Computes similarity between two embedding vectors, safely handling zero vectors.                  |
| **Recursive Comparison**     | Recursively compares objects (dicts, lists, primitives) using embeddings for text similarity.    |
| **Question Cleaning**        | Preprocesses and cleans questions with LLM before retrieval to improve query quality.             |
| **Answer Callback**          | Handles question requests; (commented) performs retrieval; currently uses hardcoded context; generates and returns LLM answer. |

---

## Knowledge Bases

The system uses 3 main knowledge bases stored as JSON files and accessed via `ChromaAdapter`:

1. **frida_knowledge.json**  
2. **roborregos_knowledge.json**  
3. **tec_knowledge.json**  

These contain curated domain-specific information such as team background, projects, events, and technical documentation relevant to the robotics community and smart assistant (FRIDA).

---

## Dialogs Module

| Function                      | Purpose                                                                                                 |
|-------------------------------|-------------------------------------------------------------------------------------------------------|
| `clean_question_rag(question)` | Creates a prompt that instructs the LLM to determine relevant information to fetch for answering.     |
| `get_answer_question_dialog(contexts, question)` | Builds a prompt combining retrieved contexts with the question, adding system instructions for FRIDA's concise, friendly, and context-aware answers. |


---

## Areas for Improvement

- **Enable Dynamic Retrieval:** The current callback uses a fixed context list instead of querying the vector DB via `ChromaAdapter`. Restoring and debugging the retrieval code would improve real-time relevance.
- **Expand Embedding Models:** Supporting multiple embedding models for recursive similarity calculations could improve matching accuracy.
- **Error Handling:** Improve robustness in embedding calls and LLM responses, including fallback mechanisms.
- **Parameterization:** Expose more parameters for tuning retrieval thresholds, top-k results, and model temperature dynamically.
- **Logging and Monitoring:** Enhance logging for debugging retrieval and generation steps.
- **Context Management:** Implement context caching or session handling for multi-turn dialogues.
