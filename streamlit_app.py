"""
Streamlit Application for Capstone AI Pipeline
Deploys the FastAPI application as an interactive Streamlit web app
"""

import streamlit as st
import os
import json
from datetime import datetime
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Configure Streamlit
st.set_page_config(
    page_title="Capstone AI Pipeline",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-weight: bold;
        font-size: 16px;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.access_token = None
    st.session_state.user_role = None

if "query_history" not in st.session_state:
    st.session_state.query_history = []

if "cached_results" not in st.session_state:
    st.session_state.cached_results = {}


# --- API Configuration ---
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def check_api_health():
    """Check if FastAPI backend is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except Exception as e:
        st.error(f"⚠️ Backend not responding: {str(e)}")
        return False


def login_user(username, password):
    """Authenticate user with FastAPI backend"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/token",
            json={"username": username, "password": password}
        )
        if response.status_code == 200:
            data = response.json()
            st.session_state.access_token = data["access_token"]
            st.session_state.username = username
            st.session_state.user_role = data.get("role", "user")
            st.session_state.logged_in = True
            st.success(f"✅ Welcome, {username}!")
            return True
        else:
            st.error("❌ Invalid credentials")
            return False
    except Exception as e:
        st.error(f"❌ Login failed: {str(e)}")
        return False


def ask_question(question):
    """Send query to FastAPI backend"""
    if not st.session_state.access_token:
        st.error("❌ Please login first")
        return None

    try:
        headers = {
            "Authorization": f"Bearer {st.session_state.access_token}"
        }
        response = requests.post(
            f"{API_BASE_URL}/ask",
            json={"question": question},
            headers=headers,
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            # Cache result
            st.session_state.cached_results[question] = data
            # Add to history
            st.session_state.query_history.append({
                "timestamp": datetime.now().isoformat(),
                "query": question,
                "response": data.get("answer", "No response")
            })
            return data
        elif response.status_code == 429:
            st.warning("⏱️ Rate limit exceeded. Wait a moment and try again.")
            return None
        else:
            st.error(f"❌ Error: {response.text}")
            return None
    except Exception as e:
        st.error(f"❌ Query failed: {str(e)}")
        return None


def get_dashboard_stats():
    """Get analytics from FastAPI backend"""
    if not st.session_state.access_token:
        return None

    try:
        headers = {
            "Authorization": f"Bearer {st.session_state.access_token}"
        }
        response = requests.get(
            f"{API_BASE_URL}/dashboard",
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.warning(f"Could not fetch dashboard stats: {str(e)}")
    return None


def get_admin_stats():
    """Get admin statistics"""
    if not st.session_state.access_token or st.session_state.user_role != "admin":
        st.error("❌ Admin access required")
        return None

    try:
        headers = {
            "Authorization": f"Bearer {st.session_state.access_token}"
        }
        response = requests.get(
            f"{API_BASE_URL}/admin/stats",
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.warning(f"Could not fetch admin stats: {str(e)}")
    return None


# --- Main Layout ---
st.title("🚀 Capstone AI Pipeline")
st.markdown("Advanced AI Data Pipeline with Authentication & Monitoring")

# Check API health
if not check_api_health():
    st.error("""
    ❌ **Backend Not Available**
    
    Make sure your FastAPI application is running:
    ```bash
    uvicorn main:app --reload
    ```
    """)
    st.stop()

# Sidebar
with st.sidebar:
    st.header("🔐 Authentication")

    if not st.session_state.logged_in:
        st.markdown("### Login")
        tab1, tab2 = st.tabs(["Login", "Demo Users"])

        with tab1:
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login", use_container_width=True):
                login_user(username, password)

        with tab2:
            st.markdown("""
            **Demo Credentials:**
            - Username: `user1`
            - Password: `pass1`
            - Role: User

            OR

            - Username: `admin`
            - Password: `admin123`
            - Role: Admin
            """)

    else:
        st.markdown(f"### 👤 Logged in as")
        st.info(f"**{st.session_state.username}** ({st.session_state.user_role})")

        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.access_token = None
            st.session_state.username = None
            st.session_state.user_role = None
            st.session_state.query_history = []
            st.rerun()

        st.divider()
        st.markdown("### 📊 Quick Stats")
        stats = get_dashboard_stats()
        if stats:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Queries", stats.get("total_queries", 0))
            with col2:
                st.metric("Cached", stats.get("cached_queries", 0))

# Main content
if not st.session_state.logged_in:
    st.markdown("""
    # 👋 Welcome!

    Please **login on the left sidebar** to get started.

    ### Features:
    - 🤖 AI-powered query engine
    - 💾 Smart caching system
    - 📊 Analytics & monitoring
    - 🔐 Role-based access control
    - ⚡ Rate limiting for fair usage

    ### Demo Credentials:
    - **User Account**: user1 / pass1
    - **Admin Account**: admin / admin123
    """)

else:
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(
        ["🎯 Query", "📜 History", "📊 Dashboard", "⚙️ Admin"]
    )

    with tab1:
        st.markdown("## 🤖 Ask the AI")
        st.markdown("""
        Enter your question and the AI will search through the data
        to provide intelligent answers.
        """)

        # Query input
        col1, col2 = st.columns([4, 1])
        with col1:
            question = st.text_input(
                "Your Question:",
                placeholder="Ask me anything about the data...",
                label_visibility="collapsed"
            )
        with col2:
            search_button = st.button("🔍 Search", use_container_width=True)

        if search_button and question:
            with st.spinner("🔄 Searching..."):
                result = ask_question(question)

            if result:
                st.success("✅ Query completed!")

                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown("### Answer:")
                    st.markdown(result.get("answer", "No answer available"))
                with col2:
                    st.metric(
                        "Response Time",
                        f"{result.get('response_time', 0):.2f}s"
                    )

                # Show metadata
                with st.expander("📋 Query Details"):
                    st.json({
                        "query": question,
                        "cached": result.get("cached", False),
                        "timestamp": datetime.now().isoformat(),
                        "execution_time": result.get("response_time", 0)
                    })

    with tab2:
        st.markdown("## 📜 Query History")

        if st.session_state.query_history:
            for i, item in enumerate(reversed(st.session_state.query_history)):
                with st.expander(f"Query {len(st.session_state.query_history) - i}"):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**Q:** {item['query']}")
                        st.markdown(f"**A:** {item['response']}")
                    with col2:
                        st.caption(item['timestamp'])

            if st.button("🗑️ Clear History", use_container_width=True):
                st.session_state.query_history = []
                st.rerun()
        else:
            st.info("No queries yet. Go to the Query tab to start!")

    with tab3:
        st.markdown("## 📊 Dashboard & Analytics")

        stats = get_dashboard_stats()
        if stats:
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Total Queries",
                    stats.get("total_queries", 0),
                    delta="Today"
                )

            with col2:
                st.metric(
                    "Cached Queries",
                    stats.get("cached_queries", 0),
                    delta=f"{stats.get('cache_hit_rate', 0):.1%}",
                    delta_color="off"
                )

            with col3:
                st.metric(
                    "Avg Response Time",
                    f"{stats.get('avg_response_time', 0):.2f}s"
                )

            with col4:
                st.metric(
                    "Active Users",
                    stats.get("active_users", 0)
                )

            st.divider()

            # Query trends
            st.markdown("### Recent Activity")
            activity_data = stats.get("recent_activity", [])
            if activity_data:
                st.write(activity_data)
            else:
                st.info("No activity data available yet")

    with tab4:
        st.markdown("## ⚙️ Admin Panel")

        if st.session_state.user_role != "admin":
            st.warning("⚠️ This section is for administrators only")
        else:
            admin_stats = get_admin_stats()

            if admin_stats:
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Total Users",
                        admin_stats.get("total_users", 0)
                    )

                with col2:
                    st.metric(
                        "Rate Limit Violations",
                        admin_stats.get("rate_limit_violations", 0)
                    )

                with col3:
                    st.metric(
                        "System Uptime",
                        f"{admin_stats.get('uptime_hours', 0):.1f}h"
                    )

                st.divider()

                # System health
                st.markdown("### System Health")
                health = admin_stats.get("health", {})
                st.json(health)

                # User management
                st.markdown("### User Management")
                users = admin_stats.get("users", [])
                st.dataframe(users)

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: gray; font-size: 12px;'>
    Capstone AI Pipeline | Powered by Streamlit & FastAPI
    </div>
    """, unsafe_allow_html=True)
