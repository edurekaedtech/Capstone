# Capstone Project Overview 

This capstone project demonstrates how to build, optimize, and deploy a modern AI-powered data pipeline using FastAPI, LlamaIndex, and Docker. The project has been restructured into modular components for better maintainability, scalability, and clarity.

## Project Structure

The application follows a clean, modular architecture with separated concerns:

capstone/
├── main.py              # Main FastAPI application and endpoints
├── auth.py              # Authentication and authorization logic
├── data.py              # Data loading and management
├── retrieval.py         # LlamaIndex and query retrieval
├── models.py            # Pydantic request/response models
├── analytics.py         # Monitoring and analytics tracking
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker containerization
├── README.md            # This file
└── .github/
    └── workflows/
        └── ci-cd.yml    # GitHub Actions CI/CD pipeline
```

## Module Descriptions

### `auth.py` - Authentication & Authorization
Handles all authentication-related functionality:
- JWT token creation and verification
- User database management with role-based access control
- Admin and regular user roles
- Token expiration handling
- Secure password validation

Users can be admin or regular users, with admin users having access to additional statistics endpoints.

### `data.py` - Data Management
Manages data sourcing and loading:
- CSV data loading with in-memory caching
- Data validation and error handling
- Data summary and statistics
- Extensible for multiple data sources (APIs, databases, etc.)

The `@lru_cache` decorator ensures data is loaded only once and reused for performance.

### `retrieval.py` - Context Retrieval
Implements semantic search and query handling:
- Vector index building with LlamaIndex
- OpenAI embeddings and LLM integration
- Query execution with context retrieval
- Error handling and logging
- Initialize retrieval system on application startup

This module bridges your data with the LLM for intelligent query responses.

### `models.py` - Data Models
Defines Pydantic models for request/response validation:
- `QueryRequest`: User query input
- `QueryResponse`: Query response with metadata
- `TokenResponse`: Authentication token response
- `HealthResponse`: Health check response
- `DashboardResponse`: Monitoring metrics
- `HistoryResponse`: User query history

These models ensure type safety and automatic API documentation.

### `analytics.py` - Monitoring & Analytics
Tracks and manages application analytics:
- Request tracking per user
- Query result caching with timestamps
- User query history management
- Analytics summary generation
- Cache cleanup for old entries
- Performance metrics collection

This module provides insights into usage patterns and performance.

### `main.py` - FastAPI Application
The main application file that ties everything together:
- FastAPI app initialization
- Startup and shutdown events
- All API endpoints
- Request routing and handling
- Error handling and logging

## API Endpoints

### Authentication
- `POST /token` - Obtain JWT token (username/password)
  - Request: `{"username": "user", "password": "pass"}`
  - Response: `{"access_token": "...", "token_type": "bearer", "role": "user"}`

### Query & Interaction
- `POST /ask` - Query the pipeline (requires auth)
  - Request: `{"question": "Your question here"}`
  - Response: Query result with cached status and response time
  
- `GET /history` - View your query history (requires auth)
  - Response: Last 10 queries with timestamps and response times

### Monitoring
- `GET /health` - Health check endpoint
  - Response: Application status and statistics
  
- `GET /dashboard` - Monitoring dashboard (requires auth)
  - Response: Detailed metrics including query count, users, cache info
  
- `GET /admin/stats` - Admin statistics (admin only)
  - Response: Comprehensive system statistics

### Information
- `GET /` - Landing page with API documentation
  - Response: Features, version, and available endpoints

## Key Features

### Security
- JWT authentication with configurable expiration
- Role-based access control (admin/user)
- Secure password handling
- Protected endpoints requiring authentication

### Performance
- In-memory query result caching
- Automatic cache invalidation (TTL-based)
- Semantic search with vector embeddings
- Response time tracking

### Monitoring
- Real-time analytics dashboard
- User query history tracking
- Performance metrics (response times, cache hits)
- Comprehensive logging
- Admin-only statistics endpoint

### Scalability
- Modular architecture for easy extension
- Docker containerization for deployment
- CI/CD automation with GitHub Actions
- Horizontal scaling support

## Setup & Usage

### Local Development

1. **Install dependencies:**
   pip install -r requirements.txt 

2. **Configure environment variables:**
     OPENAI_API_KEY=your-actual-openai-key-here
     SECRET_KEY=your-secure-secret-key
     ALGORITHM=HS256
     ACCESS_TOKEN_EXPIRE_MINUTES=30
   
3. **Run the application:**
   uvicorn main:app --reload
   

4. **Access the API:**
   - Open browser: http://127.0.0.1:8000/
   - API docs: http://127.0.0.1:8000/docs
   - Interactive testing: http://127.0.0.1:8000/docs 

### Docker Deployment

1. **Build the Docker image:**
   docker build -t capstone-ai-pipeline 

2. **Run the container:**
   docker run -d -p 80:8000 -e OPENAI_API_KEY="your-key" capstone-ai-pipeline

3. **Access the application:**
   - http://localhost/8000

### Cloud Deployment (Azure VM)

1. **Transfer files to VM via SCP:**
   scp -i your-key.pem -r ./capstone ubuntu@your-vm-ip:/home/ubuntu

2. **On the VM, build and run:**
   cd /home/ubuntu/capstone
   sudo docker build -t capstone-ai-pipeline .
   sudo docker run -d -p 80:8000 capstone-ai-pipeline

3. **Configure firewall:**
   - Open port 80 in Azure VM's inbound rules

4. **Access your application:**
   - http://your-vm-public-ip/

## Testing the API

This script tests:
-  Health check endpoint
-  Token generation and authentication
-  Query endpoint with and without authentication
-  History retrieval
-  Dashboard metrics
-  Admin statistics (permission denied test)

### Example: Get Token and Query

import requests

# 1. Get token
token_response = requests.post(
    "http://127.0.0.1:8000/token",
    data={"username": "user", "password": "pass"}
)
token = token_response.json()["access_token"]

# 2. Ask a question
headers = {"Authorization": f"Bearer {token}"}
query_response = requests.post(
    "http://127.0.0.1:8000/ask",
    json={"question": "What is LlamaIndex?"},
    headers=headers
)
print(query_response.json())

# 3. View dashboard
dashboard = requests.get("http://127.0.0.1:8000/dashboard", headers=headers)
print(dashboard.json())

## Advanced Demonstrations

### 1. Pipeline Optimization and Caching
Demonstrated in `analytics.py` with query caching and performance tracking. Cached queries return instantly with minimal overhead.

### 2. Data Integration
Shown in `data.py` with multiple data source support. Easily extendable to connect APIs, databases, and other sources.

### 3. Context Retrieval
Implemented in `retrieval.py` using LlamaIndex and OpenAI embeddings for semantic search over indexed documents.

### 4. FastAPI Service with Auth
Demonstrated in `main.py` with JWT authentication, role-based access, and protected endpoints.

### 5. Dockerization & Cloud Deployment
Enabled through `Dockerfile` and deployment instructions for local, cloud, and CI/CD environments.

### 6. Monitoring & CI/CD
Provided through `analytics.py` for monitoring and `.github/workflows/ci-cd.yml` for automated deployment.

## Best Practices

- **Modularity**: Each module has a single responsibility
- **Security**: Secrets are managed via environment variables
- **Performance**: Query results are cached for faster responses
- **Logging**: Comprehensive logging for debugging and monitoring
- **Error Handling**: Graceful error handling with meaningful messages
- **Testing**: CI/CD pipeline includes automated tests
- **Deployment**: Docker ensures consistency across environments

## Configuration

### Environment Variables

The application uses a `.env` file to manage configuration and secrets. Here are the available variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key for embeddings and LLM | Required |
| `SECRET_KEY` | Secret key for JWT token signing | `your-secret-key` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time in minutes | `30` |


**Example `.env` file:**
OPENAI_API_KEY=sk-proj-xxx...
SECRET_KEY=your-very-secure-secret-key-at-least-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Set environment variables for production:

## Dependencies

See `requirements.txt` for all dependencies. Key packages:
- FastAPI: Web framework
- LlamaIndex: Data framework and semantic search
- OpenAI: LLM and embeddings
- Pydantic: Data validation
- python-jose: JWT handling
