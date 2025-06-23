from langchain.chains.router import multi_prompt
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from typing import List
from langchain_core.documents import Document
import os
from langchain.prompts import ChatPromptTemplate as LCPT
from chroma_utils import vectorstore
from langchain.load import dumps, loads
from typing import List, Tuple, Dict, Any
from pydantic import ConfigDict
from langchain.schema import BaseRetriever
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check for Google API key
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY environment variable is not set. Please set it with your Google API key.")

# Define retriever
retriever = vectorstore.as_retriever()

# String output parser for LLM output
output_parser = StrOutputParser()

# Initialize Google Gemini 2.0 Flash model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.4,
    max_tokens=500,
    google_api_key=google_api_key,
)

# Set up prompts
multi_query_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a search query specialist designed to enhance the accuracy of a RAG chatbot. Your job is to generate multiple search queries.

STEP 1 - Context Understanding:
If there is chat history, understand what pronouns (he/she/it/this/that) refer to.

STEP 2 - Query Generation:
Generate EXACTLY 3 different search queries that will find relevant information.
Each query should approach the topic from a different angle.

Rules:
- Keep queries concise (5-8 words/characters)
- Replace vague references with specific terms
- Cover different aspects of the question
- Output ONLY a numbered list, no explanations
- The generated queries should be in the same language as the question

Example:
User: "Tell me about it"
Chat History: "User asked about task decomposition"
Output:
1. task decomposition methods
2. breaking down complex tasks
3. task decomposition examples"""),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}")
])

# Main LLM prompt
main_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant with access to retrieved documents. Provide accurate, well-structured answers based on the context provided.

Guidelines:
- Use the provided context to answer questions
- If context is insufficient, say so clearly
- Structure responses with clear paragraphs
- Use markdown formatting when appropriate
- Always respond using the same language as the question
- The response should ONLY contain your answer and nothing else
- Do NOT say "Based on the context provided"
- Don't be concise, COVER as much information as possible"""),
    ("system", "Context: {context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

#simpler fusion prompt if there is no chat history

simple_fusion_prompt = """SYSTEM: You are a  search query generation specialist tasked with creating diverse and effective search queries from a user question.

YOUR TASK:
1. Analyze the user's question to identify the core information need
2. Generate EXACTLY 3 distinct search queries that approach the question from different angles
3. Each query should:
   - Be concise (5-8 words)
   - Use different keywords and phrasings
   - Cover various aspects of the question
   - Be formatted for vector searches (no special operators unless specifically needed)
4. Format output as a numbered list with ONLY the queries, no explanations

Input question: {input}

Output (3 queries only):
1. 
2. 
3. """

fusion_prompt = LCPT.from_template(simple_fusion_prompt)

# Combined function to generate multiple queries
def generate_search_queries(input_dict):
    if not input_dict.get("chat_history"):
        #if a chat history was not found in the prompt, just use the simpler query
        simple_prompt = fusion_prompt
        response = llm.invoke(simple_prompt.format(input = input_dict["input"]))
    else:
        #else the more complicated one
        response = llm.invoke(multi_query_prompt.format_messages(**input_dict))

    #extract the queries from response
    queries = []
    content = response.content if hasattr(response, "content") else str(response)

    for line in content.split("\n"):
        line = line.strip()
        #look for the numbered items
        if line and len(line) > 2 and line[0].isdigit() and line[1] in ".":
            query = line.split(line[1], 1)[1].strip()
            if query:
                queries.append(query)

    #include the original query as a fallback
    #if input_dict["input"] not in queries:
        #queries.append(input_dict["input"])

    return queries[:3] #limit to 3 queries


# Reciprocal Rank Fusion Algorithm
def reciprocal_rank_fusion(results: List[List[Document]], k=60) -> List[Document]:
    fused_scores = {}
    for docs_list in results:
        for rank, doc in enumerate(docs_list):
            key = dumps(doc)
            fused_scores[key] = fused_scores.get(key, 0) + 1 / (rank + k)

    top = sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
    return [loads(key) for key, score in top[:5]]


def enhanced_retrieval(input_dict):
    #generate three queries
    queries = generate_search_queries(input_dict)

    #retrive documents
    results = []
    for query in queries:
        docs = retriever.get_relevant_documents(query)
        if docs:
            results.append(docs)

    #Fuse results using RRF
    if results:
        return reciprocal_rank_fusion(results)
    else:
        return retriever.get_relevant_documents(input_dict["input"])

def slice_output(output: str) -> str:
    if 'AI:' in output:
        idx = output.find('AI:')
        response = output[idx + 3:].strip()
    else:
        response = output.strip()       
    return response

def get_rag_chain(model="Gemini"):
    qa_chain = create_stuff_documents_chain(
        llm = llm,
        prompt = main_prompt,
        document_variable_name="context"
    )

    from langchain_core.runnables import RunnableLambda

    rag_chain = create_retrieval_chain(
        retriever = RunnableLambda(enhanced_retrieval),
        combine_docs_chain=qa_chain
    )

    return rag_chain
