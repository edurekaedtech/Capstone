# retrieval.py - LlamaIndex and query retrieval module

import os
import asyncio
from dotenv import load_dotenv
from llama_index.core import Document, VectorStoreIndex
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from data import load_csv
import logging

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger("capstone_retrieval")

query_engine = None
index_initialized = False

def build_index():
    """Build and cache vector index with error handling"""
    global query_engine, index_initialized
    try:
        logger.info("Starting vector index build...")
        df = load_csv()
        docs = [Document(text=row["text"]) for _, row in df.iterrows()]
        logger.info(f"Creating embeddings for {len(docs)} documents...")
        index = VectorStoreIndex.from_documents(docs)
        logger.info("Vector index built successfully")
        
        # Initialize LLM and query engine
        llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)
        embed_model = OpenAIEmbedding(model="text-embedding-3-small")
        query_engine = index.as_query_engine(llm=llm, similarity_top_k=2)
        index_initialized = True
        
        return query_engine
    except Exception as e:
        logger.error(f"Error building index: {str(e)}")
        index_initialized = False
        return None


def initialize_retrieval():
    """Initialize retrieval system on startup"""
    global query_engine, index_initialized
    try:
        logger.info("Initializing retrieval system...")
        query_engine = build_index()
        if query_engine:
            logger.info("Retrieval system initialized successfully")
        else:
            logger.warning("Retrieval system initialization failed - queries may fail")
            index_initialized = False
    except Exception as e:
        logger.error(f"Failed to initialize retrieval: {str(e)}")
        index_initialized = False


def execute_query(question: str) -> str:
    """Execute a query using the query engine"""
    if query_engine is None:
        raise Exception("Query engine not initialized")
    
    try:
        response = query_engine.query(question)
        return str(response)
    except Exception as e:
        logger.error(f"Error executing query: {str(e)}")
        raise
