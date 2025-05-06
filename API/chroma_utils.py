from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from typing import List
from langchain_core.documents import Document
import os

#Default Text Splitter
text_splitter = RecursiveCharacterTextSplitter(
    separators=[
        "\n\n",
        "\n",
        " ",
        ".",
        ",",
        "\u200b",  # Zero-width space
        "\uff0c",  # Fullwidth comma
        "\u3001",  # Ideographic comma
        "\uff0e",  # Fullwidth full stop
        "\u3002",  # Ideographic full stop
        "",
    ],
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len)

embedding_function = HuggingFaceEmbeddings(
    model_name="jinaai/jina-embeddings-v3",
    model_kwargs={"trust_remote_code": True, "device": "cpu"}, #"cpu" can be replaced with other hardwares ("cuda")
    encode_kwargs={
        "batch_size": 32,
        "normalize_embeddings": True,
    },
)

vectorstore = Chroma(
    collection_name="my_collection",
    persist_directory="./chroma_db",
    embedding_function=embedding_function
)

def get_dynamic_chunk_size(file_path: str) -> int:
    file_size_bytes = os.path.getsize(file_path)

    #count characters for text files for precision
    if file_path.endswith(".txt"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                char_count = len(content)
                #dynamic chunk sizes
                if char_count < 10000:
                    return 500
                elif char_count < 100000:
                    return 1000
                elif char_count < 1000000:
                    return 2000
                else:
                    return 3000
        except Exception as e:
            print(f"Error reading file for size calculation: {e}")

    #non-text files--pdfs
    if file_size_bytes < 50000:  # < 50KB
        return 500
    elif file_size_bytes < 500000:  # < 500KB
        return 1000
    elif file_size_bytes < 5000000:  # < 5MB
        return 2000
    else:  # >= 5MB
        return 3000


def load_and_split_document(file_path: str) -> List[Document]:
    if file_path.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith('.docx'):
        loader = Docx2txtLoader(file_path)
    elif file_path.endswith('.txt'):
        loader = TextLoader(file_path, encoding="utf-8")
    else:
        raise ValueError(f"Unsupported file type: {file_path}")

    #get dynamic chunk size
    chunk_size = get_dynamic_chunk_size(file_path)
    dynamic_text_splitter = RecursiveCharacterTextSplitter(
        separators=[
            "\n\n",
            "\n",
            " ",
            ".",
            ",",
            "\u200b",  # Zero-width space
            "\uff0c",  # Fullwidth comma
            "\u3001",  # Ideographic comma
            "\uff0e",  # Fullwidth full stop
            "\u3002",  # Ideographic full stop
            "",
        ],
        chunk_size=chunk_size,
        chunk_overlap=min(200, int(chunk_size * 0.2)),  # Dynamic overlap (20% of chunk size, max 200)
        length_function=len
    )

    documents = loader.load()
    return dynamic_text_splitter.split_documents(documents)

def index_document_to_chroma(file_path: str, file_id: int) -> bool:
    try:
        splits = load_and_split_document(file_path)

        # Add metadata to each split
        for split in splits:
            split.metadata['file_id'] = file_id

        vectorstore.add_documents(splits)
        #   vectorstore.persist()
        return True
    except Exception as e:
        print(f"Error indexing document: {e}")
        return False

def delete_doc_from_chroma(file_id: int):
    try:
        docs = vectorstore.get(where={"file_id": file_id})
        print(f"Found {len(docs['ids'])} document chunks for file_id {file_id}")

        vectorstore._collection.delete(where={"file_id": file_id})
        print(f"Deleted all documents with file_id {file_id}")

        return True
    except Exception as e:
        print(f"Error deleting document with file_id {file_id} from Chroma: {str(e)}")
        return False
