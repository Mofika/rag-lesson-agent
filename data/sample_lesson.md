# Introduction to RAG: Teach an AI to Look Things Up

## What you will learn
After this lesson, you will be able to:
- Say what RAG is in one simple sentence.
- Explain why people use it.
- Describe the steps RAG follows to answer a question.

You do not need any AI knowledge. We explain every new word when it first appears.

## 1. The problem: AI can sound sure but be wrong
Tools like ChatGPT are built on a Large Language Model, or LLM. An LLM is a computer program that reads and writes text. It learned this skill by reading a huge amount of text from books and websites.

An LLM has two big limits.

First, it only knows what it saw during training. Training is the learning period before the model is released. After that, the model does not learn new facts by itself. So it may not know last week's news. It also does not know your college's rules or your company's private files.

Second, it can make mistakes and say them in a confident voice. This is called a hallucination. A hallucination is an answer that sounds correct but is false or made up.

Think about a student in an exam hall. The student studied hard, but the book is closed. If a question is about something the student never studied, the student may guess. The guess may sound good, but it can be wrong.

## 2. What is RAG?
RAG stands for Retrieval-Augmented Generation. Let us break the name into three parts.
- Retrieval means finding. The system finds useful information.
- Augmented means added to. The system adds that information to your question.
- Generation means writing. The LLM writes the answer.

So, in simple words: RAG lets an AI look up facts first, and then write its answer using those facts.

Go back to the exam hall. Now it is an "open book" exam. The student can open the book, find the right page, and then write the answer. RAG gives the AI an open book.

## 3. Why RAG matters
- Fresh answers. You can change the documents at any time. The AI can use new facts without more training. Training again is slow and costs a lot of money.
- Fewer made-up answers. The AI reads real text before it answers, so it guesses less.
- Private knowledge. A company can let the AI use its own files, such as a help guide. These files were never part of the AI's training.
- Easy to check. The system can show which document it used. A person can open that document and check the answer.

Another way to teach an AI new things is fine-tuning. Fine-tuning means training the model some more on new data. RAG is often easier to update, because you only change the documents. The model itself stays the same.

## 4. How RAG works
RAG has two stages. First, we prepare the documents one time. Then, we answer questions.

### Stage A: Prepare the documents
1. Collect the documents. These can be PDF files, web pages, or help guides. Together they are called a knowledge base. A knowledge base is the set of documents the AI is allowed to use.
2. Split the documents into chunks. A chunk is a small piece of a document, such as a few lines or one short paragraph. Small pieces are easier to search.
3. Turn each chunk into numbers. A program called an embedding model reads each chunk and makes a list of numbers for it. This list of numbers is called an embedding. Chunks with similar meaning get similar numbers. For example, "refund" and "money back" get numbers that are close.
4. Store the numbers. They go into a vector database. A vector database is a storage system that can quickly find the chunks whose numbers are closest to the numbers of a question. A vector is just a list of numbers.

### Stage B: Answer a question
1. Retrieve. The user asks a question. The system turns the question into numbers in the same way. Then it finds the chunks with the closest numbers. These are the best matches.
2. Augment. The system builds a new prompt. A prompt is the text we send to the LLM. The new prompt has the user's question, the chunks that were found, and a rule such as: "Answer only from these chunks. If the answer is not here, say you do not know."
3. Generate. The LLM reads the prompt and writes the answer. The system can also show the name of the source document.

Here is the full path in one line:

```
Question -> Find best chunks -> Add them to the prompt -> LLM writes answer
```

Important: RAG does not retrain the LLM. The LLM does not change. It just receives extra text each time.

## 5. A full example
This example is made up. The college, the course and the dates are not real.

Asha is a Class 12 student. She uses the chat box on a college website. She asks: "What is the last date to apply for the B.Com course?"

**Without RAG.** The LLM has never seen this college's notice. It may guess a date, such as "31 May". The answer sounds sure, but it is wrong. This is a hallucination.

**With RAG.** The college has already prepared its documents.
- Prepare: The college uploaded its admission notice. The system split it into chunks, made embeddings, and stored them.
- Retrieve: The system finds this chunk: "Applications for B.Com close on 15 June. Apply on the college website."
- Augment: The system makes a prompt. It contains Asha's question, the chunk above, and the rule "Answer only from this text."
- Generate: The LLM answers: "The last date to apply for B.Com is 15 June." It also shows the name of the admission notice.

Asha can now open the notice and check the date herself.

Now a second, shorter example. An employee asks the company chat tool: "How many days of leave do I get?" The system finds the leave policy chunk, adds it to the prompt, and the LLM answers from that policy.

## 6. Where RAG can still go wrong
RAG is helpful, but it is not perfect.
- Bad search. If the system finds the wrong chunk, the answer will be wrong.
- Wrong or old documents. If the documents are old or wrong, the answer will be wrong too.
- Bad chunk size. If chunks are too small or too big, they can lose their meaning.
- Limited reading space. The LLM can only read a limited amount of text at one time.
- Hallucination can still happen. RAG reduces it, but it does not remove it. So teams must test their systems.

## Words to know
- LLM: a computer program that reads and writes text.
- Hallucination: an answer that sounds correct but is false or made up.
- RAG: a method where an AI finds facts first and then writes the answer using them.
- Knowledge base: the set of documents the AI is allowed to use.
- Chunk: a small piece of a document.
- Embedding: a list of numbers that shows the meaning of a text.
- Vector database: a storage system that finds chunks with similar numbers.
- Prompt: the text we send to an LLM.
- Fine-tuning: training a model some more on new data.

## Check yourself
1. What do the three words in "Retrieval-Augmented Generation" mean?
2. Why can an LLM give a wrong answer in a confident voice?
3. What happens in the "augment" step?
4. Why do we split documents into chunks?
5. Give one reason why RAG can still fail.

Try to answer in your own words before you look back at the lesson.
