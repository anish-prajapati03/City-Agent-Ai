import os
import requests
import streamlit as st

from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from tavily import TavilyClient
from langchain.agents import create_agent

# =========================
# LOCAL DEV SUPPORT
# =========================
load_dotenv()

def get_secret(key: str):
    return st.secrets[key] if key in st.secrets else os.getenv(key)


# =========================
# STREAMLIT PAGE CONFIG
# =========================
st.set_page_config(
    page_title="City Agent",
    page_icon="🌍",
    layout="centered"
)


# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>
    .main {
        background-color: #0E1117;
    }
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)


# =========================
# WEATHER TOOL
# =========================
@tool
def get_weather(city: str) -> str:
    """Get current weather of a city"""

    api_key = get_secret("OPENWEATHER_API_KEY")

    url = (
        f"http://api.openweathermap.org/data/2.5/weather?"
        f"q={city},IN&appid={api_key}&units=metric"
    )

    response = requests.get(url)
    data = response.json()

    if str(data.get("cod")) != "200":
        return f"Error: {data.get('message', 'Could not fetch weather')}"

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]

    return f"🌦️ Weather in {city}: {desc}, {temp}°C"


# =========================
# NEWS TOOL
# =========================
tavily_client = TavilyClient(
    api_key=get_secret("TAVILY_API_KEY")
)


@tool
def get_news(city: str) -> str:
    """Get latest news about a city"""

    response = tavily_client.search(
        query=f"latest news in {city}",
        search_depth="basic",
        max_results=3
    )

    results = response.get("results", [])

    if not results:
        return f"No news found for {city}"

    news_list = []

    for r in results:
        title = r.get("title", "No title")
        url = r.get("url", "")
        snippet = r.get("content", "")

        news_list.append(
            f"### {title}\n"
            f"🔗 {url}\n\n"
            f"{snippet[:150]}..."
        )

    return f"📰 Latest News in {city}:\n\n" + "\n\n---\n\n".join(news_list)


# =========================
# LLM SETUP
# =========================
os.environ["MISTRAL_API_KEY"] = get_secret("MISTRAL_API_KEY")

llm = ChatMistralAI(
    model="mistral-small-2506"
)


# =========================
# AGENT CREATION
# =========================
agent = create_agent(
    llm,
    tools=[get_weather, get_news],
    system_prompt="""
You are a helpful city assistant.

You can:
- Provide weather updates
- Provide latest city news

Respond professionally and clearly.
"""
)


# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.title("🌍 City Agent")
    st.markdown("""
### Features
- 🌦️ Real-Time Weather  
- 📰 Latest News  

### Tech Stack
- LangChain  
- Mistral AI  
- Tavily API  
- OpenWeather API  
- Streamlit  
""")


# =========================
# MAIN HEADER
# =========================
st.title("🌍 AI City Assistant")
st.caption("Ask weather or latest news about any city")


# =========================
# CHAT HISTORY
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# =========================
# USER INPUT
# =========================
prompt = st.chat_input("Ask something like: Weather in Delhi")

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            result = agent.invoke({
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            })

            response = result["messages"][-1].content

            st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })