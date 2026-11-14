## What you will learn

You will learn about a helpful tool in artificial intelligence called RAG. 
You will see how computers can read your private documents to answer questions. 
This lesson is made for beginners who want to start an artificial intelligence career.

## The problem

A Large Language Model, which is an artificial intelligence program trained on a large amount of text, has a big limit. 
The knowledge of a Large Language Model is fixed at training time, which means it cannot know new events after its training. 
It also does not know private documents unless you show them. 
Sometimes, a Large Language Model can produce confident but false or made-up answers, and this bad habit is called hallucination. 
Fixing a model by training it again takes too much time and money.

## What is Retrieval-Augmented Generation?

Retrieval-Augmented Generation, which is called RAG for short, is a method that connects a search tool to a text generator. 
The idea of RAG was introduced in a famous research paper by Lewis and other writers in the year 2020. 
RAG does not retrain the model and does not change the model's internal numbers, which are called weights. 
Instead, RAG gives the model extra text at the exact time you ask your question.

Think of an open-book exam at your college. 
If the teacher asks a question about a new rule, your memory might fail you. 
If you guess the answer blindly, you might tell a lie, which is like a hallucination. 
Instead, you open your study notes, find the exact page, and read the answer to the teacher. 
RAG is like giving your study notes to the artificial intelligence right when it needs them.

## Why it matters

RAG is very important for modern computer systems for four main reasons.
First, it gives the model fresh knowledge without changing the base program. 
Second, it lets the model read your private documents safely. 
Third, it helps stop the model from making up false facts. 
Fourth, RAG can show its sources, so a person can check if the answer is correct.

## How it works (step by step)

Building a RAG system happens in two main parts: preparation and question time.

### Part 1: Preparation
1. You collect your files into a central place, which is called a knowledge base.
2. You split large files into smaller pieces, and each piece is called a chunk.
3. You convert each chunk into a list of numbers that represents the meaning of the text, and this list is called an embedding.
4. You store these embeddings in a special search folder, which is called a vector database.

### Part 2: Question Time
1. A user types a question into the system.
2. The system turns the user question into an embedding.
3. The system searches the vector database to find the text chunks with the most similar meaning, which is the retrieval step.
4. The system adds those text chunks to the question in a container text, which is called a prompt. This is the augmentation step.
5. The language model reads the prompt and writes the final answer, which is the generation step.

## A full example

Let us follow one single question through the RAG system.

Question: "What is the fee for the library card?"

**Step 1: Document preparation (made up for this example)**
You have a private college rulebook. 
You split the rulebook into smaller text chunks. 
One chunk says: "Students can get a library card for free by showing their college ID."

**Step 2: Embedding and storing**
The system turns that chunk into an embedding, which is a list of numbers representing the meaning. 
The system stores this embedding in a vector database.

**Step 3: User asks a question**
A new student types the question: "What is the fee for the library card?"

**Step 4: Retrieval**
The system turns the question into an embedding and searches the vector database. 
It finds the matching text chunk about the free library card.

**Step 5: Augmentation**
The system puts the matching text chunk and the user question into a prompt. 
The prompt usually tells the model to answer using only the given text and to say when the answer is not in it.

**Step 6: Generation**
The Large Language Model reads the prompt and writes the final answer: "The library card is free if you show your college ID."

## Where it can go wrong

Even though RAG is very powerful, it can still fail in a few ways. 
If the search tool finds bad documents, the model will give a bad answer. 
If your documents are outdated, the model will use old facts. 
The chunk size matters a lot because too little text misses the point, and too much text confuses the model. 
A model can only read a limited amount of text at one time, which is called its context window. 
Also, RAG can reduce hallucinations, but it cannot remove them completely. 
Finally, searching extra databases adds a small delay and cost to the system.

## Words to know

- **LLM**: Short for Large Language Model, which is an artificial intelligence trained on lots of text.
- **Large Language Model**: An artificial intelligence program trained on a large amount of text.
- **Hallucination**: When an artificial intelligence produces a confident but false or made-up answer.
- **RAG**: Short for Retrieval-Augmented Generation, a method that joins search and text generation.
- **Retrieval-Augmented Generation**: A system that finds relevant text and gives it to a language model to write an answer.
- **Embedding**: A list of numbers that represents the meaning of a piece of text.
- **Vector database**: A special place to store and search embeddings.
- **Chunk**: A small piece of a larger document.
- **Prompt**: The text container given to the language model with instructions and data.
- **Knowledge base**: A collection of documents used to store information.
- **Training**: Teaching a model by showing it text data so it learns patterns.
- **Fine-tuning**: Training a model further on extra data, which is a different approach from RAG.

## Check yourself

1. What does the acronym RAG stand for in artificial intelligence?
2. What is the name of the problem when a language model makes up false answers?
3. What do you call a small piece of a larger document?
4. What is a list of numbers that represents the meaning of text called?
5. Where do you store the embeddings for fast searching?
6. Does RAG retrain the model weights during the question time?
7. What is the term for training a model further on extra data?