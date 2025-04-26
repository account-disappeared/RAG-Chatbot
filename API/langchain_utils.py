from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from typing import List
from langchain_core.documents import Document
import os
from langchain.prompts import ChatPromptTemplate as LCPT
from langchain_huggingface import ChatHuggingFace as LCHF
from chroma_utils import vectorstore
from langchain.load import dumps, loads
from typing import List, Tuple, Dict, Any
from pydantic import ConfigDict
from langchain.schema import BaseRetriever
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

#load enviroment variables
load_dotenv()

# Check for HuggingFace API token
hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
if not hf_token:
    raise ValueError("HUGGINGFACEHUB_API_TOKEN environment variable is not set. Please set it with your HuggingFace API token.")

#define retriever
retriever = vectorstore.as_retriever()

#string out parser for LLM output
output_parser = StrOutputParser()

#LLM model
llm = HuggingFaceEndpoint(
    endpoint_url="",
    huggingfacehub_api_token=hf_token,
    task="text-generation",
    max_new_tokens=50000,
    do_sample=False,
    repetition_penalty=1.03,
)

# Set up prompts
contextualize_q_system_prompt = (
    """
    Given a chat history and the most recent user question (which may reference context from the chat history), output a standalone question that can be understood without the chat history.
    Do not answer the question, only rephrase it if necessary, otherwise return it as is:
    """
)

context_prompt = ChatPromptTemplate.from_messages([
    ("system", contextualize_q_system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are the assistant of the question-answering task. Use the following retrieved context to answer the question. If you don't know the answer, just say you don't know. Only include the answer in your answer, and don't include other irrelevant content, such as 'text', 'AI':"),
    ("system", "Context: {context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

fusion_prompt = """You are a helpful assistant that generates 5 search queries from a single user question, and only contains 5 search queries in the answer:
{question}
Output(5 queries):"""
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

#Fusion Retriever

class FusionRetriever(BaseRetriever):
    # 1) Tell Pydantic to accept any Python object as a field
    model_config = ConfigDict(arbitrary_types_allowed=True)

    # 2) Declare exactly the fields:
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
def get_rag_chain(model="Gemma3"):
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
