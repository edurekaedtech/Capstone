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
        logger.info("🔨 Starting vector index build...")
        
        # Check if OpenAI API key exists
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("❌ OPENAI_API_KEY not found in .env file!")
            raise ValueError("OPENAI_API_KEY is required")
        
        logger.info("✅ OpenAI API key found")
        
        # Load data
        logger.info("📚 Loading CSV data...")
        df = load_csv()
        logger.info(f"✅ Loaded {len(df)} documents")
        
        # Create documents
        docs = [Document(text=row["text"]) for _, row in df.iterrows()]
        logger.info(f"📄 Created {len(docs)} document objects")
        
        # Build index with embeddings
        logger.info("🔗 Creating vector embeddings (this may take 10-20 seconds)...")
        index = VectorStoreIndex.from_documents(docs)
        logger.info("✅ Vector index built successfully")
        
        # Initialize LLM and query engine
        logger.info("🤖 Initializing GPT-3.5-turbo model...")
        llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)
        embed_model = OpenAIEmbedding(model="text-embedding-3-small")
        query_engine = index.as_query_engine(llm=llm, similarity_top_k=2)
        logger.info("✅ Query engine created successfully")
        
        index_initialized = True
        return query_engine
        
    except ValueError as e:
        logger.error(f"❌ Configuration Error: {str(e)}")
        index_initialized = False
        return None
    except Exception as e:
        logger.error(f"❌ Error building index: {type(e).__name__}: {str(e)}")
        logger.error("This usually means: OpenAI API key invalid, network issue, or API quota exceeded")
        index_initialized = False
        return None


def initialize_retrieval():
    """Initialize retrieval system on startup"""
    global query_engine, index_initialized
    logger.info("=" * 60)
    logger.info("🚀 INITIALIZING RETRIEVAL SYSTEM")
    logger.info("=" * 60)
    
    try:
        query_engine = build_index()
        
        if query_engine:
            logger.info("✅ RETRIEVAL SYSTEM READY!")
            logger.info("=" * 60)
        else:
            logger.error("⚠️  Retrieval system initialization FAILED")
            logger.error("Possible causes:")
            logger.error("  1. Invalid OPENAI_API_KEY in .env")
            logger.error("  2. Network connection issue")
            logger.error("  3. OpenAI API quota exceeded")
            logger.error("  4. LlamaIndex installation issue")
            logger.error("=" * 60)
            index_initialized = False
            
    except Exception as e:
        logger.error(f"❌ Unexpected error: {type(e).__name__}: {str(e)}")
        index_initialized = False


def execute_query(question: str) -> str:
    """Execute a query using the query engine"""
    if query_engine is None:
        error_msg = (
            "Query engine not initialized. "
            "Check logs for initialization errors. "
            "Common cause: Invalid OPENAI_API_KEY"
        )
        logger.error(f"❌ {error_msg}")
        raise Exception(error_msg)
    
    if not index_initialized:
        error_msg = "Query engine not ready. Initialization failed."
        logger.error(f"❌ {error_msg}")
        raise Exception(error_msg)
    
    try:
        logger.info(f"🔍 Executing query: {question[:50]}...")
        response = query_engine.query(question)
        logger.info(f"✅ Query executed successfully")
        return str(response)
    except Exception as e:
        logger.error(f"❌ Error executing query: {type(e).__name__}: {str(e)}")
        raise
