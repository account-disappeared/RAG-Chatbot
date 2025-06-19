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
    max_tokens=500,  # Gemini uses max_tokens instead of max_new_tokens
    google_api_key=google_api_key,
)

# Set up prompts
contextualize_q_system_prompt = (
    """
    SYSTEM ROLE: You are a query reformulation system with ONE purpose only: to convert conversational queries into standalone, vector-search-friendly questions.

    INPUT: A chat history and the user's most recent question that may reference context from that history.

    YOUR TASK: 
    1. ONLY output a standalone question that could be understood without any chat history
    2. NEVER answer the question or provide information
    3. NEVER add explanations or commentary
    4. For pronouns like "he/she/it/they/this/that" in the user's question, replace with specific nouns from context
    5. If the question is already standalone, return it unchanged
    6. Format your response as "[your reformulated question]"
    """
)

context_prompt = ChatPromptTemplate.from_messages([
    ("system", contextualize_q_system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

#main llm prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert assistant for question-answering tasks with access to retrieved information. Your goal is to provide accurate, helpful, and well-structured answers in Markdown.

    CONTEXT INSTRUCTIONS:
    - The context below contains relevant information to answer the user's question
    - If the context is insufficient, acknowledge the limitations of your response
    - If you don't know the answer, clearly state that you don't have enough information

    RESPONSE GUIDELINES:
    1. Primarily use the provided context to formulate your answer
    2. Structure your response with clear paragraphs and logical flow
    3. For factual information, cite which part of the context you're using at the end of the response
    4. Use markdown formatting to improve readability when appropriate
    5. Start your response with "AI: " followed by your answer
    6. Keep your response concise but complete"""),
    ("system", "Context: {context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

fusion_prompt = """SYSTEM: You are a search query generation specialist tasked with creating diverse and effective search queries from a user question.

YOUR TASK:
1. Analyze the user's question to identify the core information need
2. Generate EXACTLY 5 distinct search queries that approach the question from different angles
3. Each query should:
   - Be concise (3-8 words)
   - Use different keywords and phrasings
   - Cover various aspects of the question
   - Be formatted for vector searches (no special operators unless specifically needed)
4. Format output as a numbered list with ONLY the queries, no explanations

Input question: {question}

Output (5 queries only):
1. 
2. 
3. 
4. 
5. """
prompt_rag_fusion = LCPT.from_template(fusion_prompt)

#generate RAG fusion queries
generate_queries = (
    prompt_rag_fusion
    | LCHF(llm=llm)
    | StrOutputParser()
    | (lambda x: x.split("\n"))
)

#Reciprocal Rank Fusion Algorithim
def reciprocal_rank_fusion(results: list[list], k=60, top_n=8):
    fused_scores = {}
    for docs in results:
        for rank, doc in enumerate(docs):
            key = dumps(doc)
            fused_scores[key] = fused_scores.get(key, 0) + 1 / (rank + k)
    top = sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return [(loads(d), score) for d, score in top]

#slicing output
def slice_output(output: str) -> str:
    idx = output.find('AI:')
    if idx != -1:
        response = output[idx + 3:]
    else:
        response = output  # if no newline found, leave string unchanged
    return response


#Fusion Retriever

class FusionRetriever(BaseRetriever):
    # 1) Tell Pydantic to accept any Python object as a field
    model_config = ConfigDict(arbitrary_types_allowed=True)

    # 2) Declare exactly the fields you’ll pass in:
    base: BaseRetriever
    qgen: Any
    rrf: Any

    # 3) Implement the new abstract method:
    def _get_relevant_documents(self, query: str) -> List[Document]:
        # generate sub‑queries
        sub_queries = self.qgen.invoke({"question": query})
        # fetch and fuse
        lists = [self.base.get_relevant_documents(q) for q in sub_queries]
        fused = self.rrf(lists)
        # return just the docs
        return [doc for doc, _ in fused]

#initiate Fusion Retriever
fusion_retriever = FusionRetriever(
    base=retriever,
    qgen=generate_queries,
    rrf=reciprocal_rank_fusion,
)

#final
def get_rag_chain(model="Gemini"):
    chat_model = ChatHuggingFace(llm=llm)
    history_aware_retriever = create_history_aware_retriever(
        llm=llm,
        retriever=fusion_retriever,
        prompt=context_prompt,
    )
    qa_chain = create_stuff_documents_chain(
        llm=llm,
        prompt=prompt,
        document_variable_name="context",
    )
    rag_chain = create_retrieval_chain(
        retriever=history_aware_retriever,
        combine_docs_chain=qa_chain
    )
    return rag_chain
