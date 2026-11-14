# GROUNDING FACTS (the judge checks the lesson against ONLY this file)

Source basis: Lewis et al., 2020, "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"
(Facebook AI Research, UCL, NYU) and widely documented RAG practice. Review and edit before use.

## Facts
- F1. RAG stands for Retrieval-Augmented Generation. The idea was introduced in a 2020 research paper by Lewis et al.
- F2. RAG combines two parts: a retriever that finds relevant text, and a generator (a language model) that writes the answer.
- F3. A Large Language Model (LLM) is trained on a large amount of text. Its knowledge is fixed at training time.
- F4. An LLM can produce confident but false or made-up answers. This is called hallucination.
- F5. An LLM does not know private documents or events after its training unless they are given to it.
- F6. RAG does NOT retrain the model and does NOT change the model's weights. It gives the model extra text at question time.
- F7. Typical RAG preparation: collect documents (knowledge base), split them into chunks, convert each chunk into an embedding, store embeddings in a vector database or index.
- F8. An embedding is a list of numbers (a vector) that represents the meaning of a piece of text. Texts with similar meaning get similar embeddings.
- F9. At question time: embed the question, search for the most similar chunks (retrieve), add them to the prompt with the question (augment), and the LLM writes the answer (generate).
- F10. The prompt usually tells the model to answer using the given text and to say when the answer is not in it.
- F11. RAG can reduce hallucinations but cannot remove them completely.
- F12. To update what the system knows, you update the documents/index; no model retraining is needed. This is usually cheaper and faster than retraining or fine-tuning.
- F13. RAG can show its sources, so a person can check the answer.
- F14. Limitations: bad retrieval gives bad answers; wrong or outdated documents give wrong answers; chunk size matters; the model can only read a limited amount of text at once (context window); extra search adds some delay and cost.
- F15. Fine-tuning means training a model further on extra data. It is a different approach from RAG.

## MUST_COVER
1. What RAG is, in one simple sentence, and what the name means.
2. The problem it solves (knowledge frozen at training, no private data, hallucination).
3. Why it matters (fresh knowledge, private data, fewer made-up answers, checkable sources).
4. How it works: prepare documents (chunk, embed, store), then retrieve, augment, generate.
5. At least one worked example.
6. Limits: RAG can still fail (bad retrieval, bad documents, hallucination possible).
