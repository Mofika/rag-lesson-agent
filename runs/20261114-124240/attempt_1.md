## What you will learn

You will learn what RAG is and how it helps computers answer questions. You will also learn why this method is useful for a career in AI.

## The problem

A Large Language Model (LLM) is an AI program trained on a large amount of text. Think of it as a student who read every library book up to a certain year. 

After that training, the student's knowledge is fixed and frozen in time. The AI does not know your private company files. It also does not know recent news that happened yesterday. 

When the AI does not know an answer, it can still sound very confident. It will make up a false answer instead of saying it does not know. This bad habit is called hallucination. 

## What is RAG?

RAG stands for Retrieval-Augmented Generation. 

In simple words, RAG is a method that lets an AI search through documents first, and then use those documents to write a correct answer. 

Think of an open-book exam. The student does not memorize every single page. Instead, the student searches the book for the right page and writes the answer using only that page.

## Why it matters

RAG matters because it solves the big problems of AI models. 

First, it gives the AI fresh knowledge without training the AI again. 

Second, it lets the AI read your private documents safely. 

Third, it reduces false, made-up answers because the AI reads real text before writing. 

Fourth, RAG can show its sources so you can check the facts yourself.

## How it works (step by step)

RAG does not retrain the model and does not change the model's internal numbers. It gives the model extra text at question time. 

Here are the exact steps:

### Step 1: Prepare documents
First, you collect all your text documents into a knowledge base. You split these large texts into smaller pieces called chunks. 

### Step 2: Make embeddings
You convert each chunk into a list of numbers called an embedding. An embedding represents the true meaning of a piece of text. Texts with similar meanings get similar embeddings. 

### Step 3: Store in a database
You store all these embeddings inside a special vector database or index for fast searching. 

### Step 4: The question arrives
When a user asks a question, you convert the question into an embedding too. 

### Step 5: Retrieve
The system searches the database and finds the text chunks that are most similar to the question. This is the retrieval step.

### Step 6: Augment
You add those retrieved text chunks into the prompt along with the original question. The prompt usually tells the model to answer using only the given text. 

### Step 7: Generate
Finally, the generator, which is the language model, reads the prompt and writes the final answer. 

## A full example

Let us follow one real question through the RAG system.

Imagine you work at a college in India. A student asks a question about library rules.

* **The Question:** "Can I keep a reference book for two weeks?"
* **Step 1 and 2 (Prepare and Embed):** The college has a digital rulebook. The system chopped the rulebook into chunks and turned them into embeddings stored in a database.
* **Step 5 (Retrieve):** The system takes the student's question, searches the database, and pulls out Chunk 42. Chunk 42 says: "Reference books must be returned within one day. Normal books can be kept for two weeks."
* **Step 6 (Augment):** The system creates a prompt. It combines the student's question with Chunk 42. It tells the AI: "Answer the question using only the provided text."
* **Step 7 (Generate):** The language model reads the prompt and writes the answer: "No, you cannot keep a reference book for two weeks. Reference books must be returned within one day according to the rules."

## Where it can go wrong

RAG is very useful, but it has limits:

* If the retrieval step brings back the wrong text, the AI will give a bad answer.
* If your stored documents are wrong or outdated, the answers will also be wrong.
* RAG can reduce hallucinations, but it cannot remove them completely. 
* Reading too much text at once is hard because models have a limited context window, which is the maximum amount of text a model can read at one time.
* Extra database searches add a small delay and extra cost.

## Words to know

* **Retrieval-Augmented Generation (RAG):** A method that combines searching for documents with a language model that writes the answer.
* **Large Language Model (LLM):** An AI model trained on a large amount of text.
* **Hallucination:** When an AI produces a confident but false or made-up answer.
* **Chunk:** A small piece of a larger document.
* **Embedding:** A list of numbers that represents the meaning of a piece of text.
* **Vector Database:** A special database used to store and search embeddings.
* **Context Window:** The limit on how much text a model can read at one time.
* **Fine-tuning:** Training a model further on extra data, which is a different approach from RAG.

## Check yourself

1. What do the letters R-A-G stand for?
2. Why is an LLM prone to hallucinations when asked about private data?
3. True or False: RAG changes the internal weights of the language model during the process.
4. What is the role of an embedding in a RAG system?
5. Name two limits of using RAG.