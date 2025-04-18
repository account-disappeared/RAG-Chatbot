# RAG Chatbot example🤖
###### Contains 3 different RAG examples of a RAG chatbot

---

### Base RAG.ipynb
Simple RAG chatbot with nothing to increase its accuracy

---

### Multi Query.ipynb
RAG chatbot with query transformation, the steps include:
1. prompting the LLM to generate 3 different queries based on the user's questions
2. Perform retrival based on each generated question.
3. Combine all retrieved documents
4. feed it to the LLM with the user's original question
5. Generate answer

---

### RAG Fusion.ipynb
RAG chatbot with more query transformation, based on Multi-Query but adds a re-ranking step:
1. prompting the LLM to generate 3 different queries based on the user's questions
2. Perform retrival based on each generated question.
3. 👨‍🏫Use a Re-Ranking algorithim to rank the retrieved documents based on relevance to the user's question
3. Combine all retrieved & Re-Ranked documents
4. feed it to the LLM with the user's original question
5. Generate answer

---

### RAG Fusion with 8 files.ipynb
All the same thing as RAG-Fusion but adds optimization:
1. prompting the LLM to generate 3 different queries based on the user's questions
2. Perform retrival based on each generated question.
3. 👨‍🏫Use a Re-Ranking algorithim to rank the retrieved documents based on relevance to the user's question
4. Only take the top 8 most relevant documents
3. Combine all retrieved & Re-Ranked documents
4. feed it to the LLM with the user's original question
5. Generate answer
