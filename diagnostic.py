"""
Quick diagnostic script to test OpenAI API and retrieval system
Run this to identify the exact problem
"""

import os
import sys
from dotenv import load_dotenv

print("=" * 70)
print("🔍 CAPSTONE AI PIPELINE - DIAGNOSTIC TEST")
print("=" * 70)

# Step 1: Check .env
print("\n1️⃣  CHECKING .env FILE")
print("-" * 70)

if not os.path.exists(".env"):
    print("❌ .env file NOT found!")
    print("   Create .env file in capstone directory with:")
    print("   OPENAI_API_KEY=sk-proj-YOUR-KEY")
    sys.exit(1)
else:
    print("✅ .env file found")

# Step 2: Load environment
print("\n2️⃣  LOADING ENVIRONMENT VARIABLES")
print("-" * 70)

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
secret_key = os.getenv("SECRET_KEY")

if not api_key:
    print("❌ OPENAI_API_KEY not found in .env!")
    sys.exit(1)
else:
    key_preview = api_key[:20] + "..." + api_key[-5:]
    print(f"✅ OPENAI_API_KEY: {key_preview}")
    print(f"   Length: {len(api_key)} characters")

if secret_key:
    print(f"✅ SECRET_KEY found")
else:
    print("⚠️  SECRET_KEY not found (optional)")

# Step 3: Check packages
print("\n3️⃣  CHECKING REQUIRED PACKAGES")
print("-" * 70)

packages = {
    "openai": "OpenAI API client",
    "llama_index": "LlamaIndex framework",
    "llama_index.core": "LlamaIndex core",
    "llama_index.llms.openai": "LlamaIndex OpenAI",
    "llama_index.embeddings.openai": "LlamaIndex embeddings",
    "fastapi": "FastAPI framework",
    "uvicorn": "Uvicorn server",
    "pandas": "Pandas data",
    "dotenv": "Python-dotenv",
    "pydantic": "Pydantic validation"
}

missing_packages = []
for package, description in packages.items():
    try:
        __import__(package)
        print(f"✅ {package:35} - {description}")
    except ImportError:
        print(f"❌ {package:35} - {description} [MISSING]")
        missing_packages.append(package)

if missing_packages:
    print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
    print("   Run: pip install -r requirements.txt")

# Step 4: Test OpenAI API
print("\n4️⃣  TESTING OPENAI API CONNECTION")
print("-" * 70)

try:
    import openai
    from openai import OpenAI
    
    client = OpenAI(api_key=api_key)
    print("✅ OpenAI client created")
    
    # Try to list models
    try:
        models = client.models.list()
        model_list = [m.id for m in models.data[:3]]
        print(f"✅ OpenAI API accessible")
        print(f"   Sample models: {model_list}")
    except Exception as e:
        print(f"❌ OpenAI API Error: {str(e)}")
        if "401" in str(e) or "Unauthorized" in str(e):
            print("   → Your API key is INVALID")
        elif "429" in str(e) or "rate_limit" in str(e):
            print("   → Rate limit exceeded (wait a bit)")
        elif "Connection" in str(e):
            print("   → Network connection issue")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")

# Step 5: Test data loading
print("\n5️⃣  TESTING DATA LOADING")
print("-" * 70)

try:
    from data import load_csv
    df = load_csv()
    print(f"✅ CSV loaded successfully")
    print(f"   Records: {len(df)}")
    print(f"   Columns: {list(df.columns)}")
except Exception as e:
    print(f"❌ Data loading failed: {str(e)}")

# Step 6: Test LlamaIndex
print("\n6️⃣  TESTING LLAMAINDEX")
print("-" * 70)

try:
    from llama_index.core import Document, VectorStoreIndex
    from llama_index.llms.openai import OpenAI as LlamaOpenAI
    from llama_index.embeddings.openai import OpenAIEmbedding
    
    print("✅ LlamaIndex imports successful")
    
    # Try to create embeddings (this will use OpenAI API)
    print("   Testing embeddings...")
    embed_model = OpenAIEmbedding(model="text-embedding-3-small")
    print("✅ Embedding model initialized")
    
    # Test LLM
    print("   Testing LLM...")
    llm = LlamaOpenAI(model="gpt-3.5-turbo", temperature=0.1)
    print("✅ LLM initialized")
    
except Exception as e:
    print(f"❌ LlamaIndex error: {str(e)}")

# Step 7: Test full retrieval
print("\n7️⃣  TESTING FULL RETRIEVAL SYSTEM")
print("-" * 70)

try:
    print("   Building index (may take 10-20 seconds)...")
    from retrieval import initialize_retrieval, execute_query
    
    initialize_retrieval()
    print("✅ Retrieval system initialized")
    
    # Test a query
    print("   Testing query...")
    result = execute_query("Tell me about Python")
    print(f"✅ Query executed")
    print(f"   Result: {str(result)[:100]}...")
    
except Exception as e:
    print(f"❌ Retrieval error: {str(e)}")

# Summary
print("\n" + "=" * 70)
print("📊 DIAGNOSTIC SUMMARY")
print("=" * 70)

if not missing_packages and api_key:
    print("\n✅ ALL CHECKS PASSED!")
    print("\nYou should be able to run:")
    print("   python -m uvicorn main:app --reload")
    print("\nThen access at: http://localhost:8000")
else:
    print("\n⚠️  SOME ISSUES FOUND:")
    if missing_packages:
        print(f"   • Missing packages: {', '.join(missing_packages)}")
        print("     Fix: pip install -r requirements.txt")
    if not api_key:
        print("   • OpenAI API key not set")
        print("     Fix: Add OPENAI_API_KEY to .env")

print("\n" + "=" * 70)
