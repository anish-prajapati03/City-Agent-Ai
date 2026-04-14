# 🌍 AI City Assistant Agent

An intelligent AI-powered city assistant built using **LangChain Agents**, **Mistral AI**, **OpenWeather API**, **Tavily Search**, and **Streamlit**.

This project demonstrates the implementation of a **tool-calling AI agent** capable of dynamically selecting external tools to answer user queries related to **weather** and **latest city news**.

---

## 🚀 Live Demo

https://cityassistantanix.streamlit.app/

---

## 📌 Project Overview

Traditional chatbots respond only based on model knowledge, which may be outdated or lack real-time information.

To solve this, I built an **AI Agent** that can:

- Understand natural language user queries  
- Decide which tool/API to call  
- Retrieve live external data  
- Return contextual, real-time responses  

This project showcases practical implementation of **LLM Agents + Tool Calling**, an important GenAI engineering pattern.

---

## ✨ Features

- 🌦️ Real-Time Weather Retrieval  
- 📰 Latest News Fetching  
- 🤖 LangChain Tool Calling Agent  
- 💬 Interactive Streamlit Chat UI  
- 🔐 Secure API Key Handling with Streamlit Secrets  
- 🧠 Dynamic Agent Reasoning for Tool Selection  

---

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|---------|
| Python | Core Programming Language |
| LangChain | Agent Framework / Tool Calling |
| Mistral AI | Large Language Model |
| OpenWeather API | Live Weather Data |
| Tavily Search API | Real-Time News Search |
| Streamlit | Frontend UI / Deployment |
| dotenv / Secrets | Environment Variable Management |

---

## 🧠 How It Works

### Agent Workflow

1. User enters a query in the Streamlit UI  
2. LangChain Agent analyzes user intent  
3. Agent decides which tool to call:
   - `get_weather()` → for weather-related queries  
   - `get_news()` → for news-related queries  
4. Tool fetches real-time data from external APIs  
5. Agent formats and returns final response to user  

---

## 🏗️ Architecture

```text
User Input
   ↓
Streamlit UI
   ↓
LangChain Agent
   ↓
Tool Selection Logic
   ↓
-----------------------------
| Weather Tool | News Tool |
-----------------------------
   ↓               ↓
OpenWeather API   Tavily API
   ↓               ↓
Processed Response
   ↓
User Output
