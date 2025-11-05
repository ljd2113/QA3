# QA3
# QA3

# 🧠 AI-Powered News Newsletter Generator

A Python project that automates the process of collecting, summarizing, and delivering news related to a topic of interest. It integrates the **News API** for data collection and the **OpenAI Large Language Model (LLM)** for efficient summarization.

## Project Goals

* **Fetch Data:** Automatically retrieve the latest articles on a specific topic.
* **Summarize with AI:** Use an LLM (GPT-3.5-Turbo) to condense lengthy articles into concise, email-friendly bullet points.
* **Deliver:** Send the formatted digest via a secure email connection (SMTP).

---

## 🛠️ Setup and Configuration

### Prerequisites
* Python installed.
* Required libraries installed: `pip install requests openai`
* **API Keys and App Password** (set as Environment Variables below).

### Environment Variables (Credentials)
This script reads all sensitive credentials securely from your system's environment variables.

| Environment Variable | Purpose |
| :--- | :--- |
| `NEWS_API_KEY` | Key for retrieving news articles. |
| `OPENAI_API_KEY` | Key for accessing the LLM. |
| `SENDER_APP_PASSWORD` | The Gmail **App Password** for secure email login. |
| `SENDER_EMAIL` | The email address sending the newsletter. |
| `RECIPIENT_EMAIL` | The email address receiving the newsletter. |

---

## 💻 Code Structure: What Each Part Does

### 1. Initial Setup and Tools

| Code Section | Simple Comment | Purpose Explained |
| :--- | :--- | :--- |
| `import requests...` | `#LOAD_NECESSARY_TOOLS 🛠️` | **Brings in all the essential Python libraries** (tools) needed for data fetching, AI communication, and email sending. |
| `Configuration variables (...)` | `#CUSTOM_CONFIG_VARIABLES` | Defines all the **settings, search terms, and security credentials** needed for the script to run (read securely from environment variables). |

### 2. Step 1: Article Fetching

| Code Section | Simple Comment | Purpose Explained |
| :--- | :--- | :--- |
| `def fetch_articles(...)` | `#NEWS_API_CONNECTOR 📰` | **Initiates the data collection** by preparing parameters (topic, API key, date range) and making the request to the News API. |
| `try: response = requests.get(...)` | `#HANDLE_DATA_RESPONSE ✅` | **Executes the API call**, converts the raw data to JSON, and checks if the response status was successful (e.g., uses `raise_for_status()` for immediate error detection). |
| `except requests.exceptions.RequestException as e:` | `#FAILURE_CATCHER 🚨` | **Safety net for network issues** (like internet connection loss). It gracefully catches the error, alerts the user, and prevents the script from crashing. |

### 3. Step 2: AI Summarization

| Code Section | Simple Comment | Purpose Explained |
| :--- | :--- | :--- |
| `def summarize_article(...)` | `#AI_SUMMARIZER_LLM 🤖` | **Core function that communicates with the OpenAI LLM** to process raw article content and generate the summary. |
| `prompt = f"""You are a professional news editor..."""` | `#PROMPT_ENGINEERING_INSTRUCTIONS 📝` | **Defines the exact rules for the AI** (role, length, and format) to ensure a high-quality, concise summary. |
| `except Exception as e:` | `#LLM_SAFETY_CATCHER 🛡️` | **Error handling for the AI API**. Catches issues like invalid API keys or rate limits and returns a simple "Summarization failed" message. |

### 4. Step 3: Email Delivery

| Code Section | Simple Comment | Purpose Explained |
| :--- | :--- | :--- |
| `def send_newsletter(...)` | `#EMAIL_DELIVERER ✉️` | The **final function** responsible for formatting and sending the newsletter to the recipient. |
| `html_body = f"""<html>..."""` | `#EMAIL_HTML_TEMPLATE 🎨` | **Designs the look of the email** using HTML and CSS (`<style>`) to ensure a professional layout. |
| `try: with smtplib.SMTP(...)` | `#SMTP_DELIVERY_PROTOCOL 🔒` | **Handles the secure transmission**. It connects to the mail server, uses `server.starttls()` for **encryption**, and `server.login()` for **authentication** before delivering the final message. |

### 5. Main Execution

| Code Section | Simple Comment | Purpose Explained |
| :--- | :--- | :--- |
| `if __name__ == "__main__":` | `#ORCHESTRATOR_STARTUP 🎬` | The **control center** that ensures the functions are called in the correct order: Fetch $\rightarrow$ Summarize $\rightarrow$ Send. |
| `for item in newsletter_items: item['summary'] = summarize_article(...)` | `#SUMMARIZATION_LOOP_TESTING 🤖` | The loop that **calls the AI for every article**, updates the data structure, and includes a test print to verify the summary before the email is sent. |

---

## ▶️ How to Run the Script

1.  **Set Environment Variables** in your terminal (using the `Set-Item -Path Env:VARIABLE_NAME -Value "VALUE"` commands).
2.  Run the script using the Python launcher:
    ```bash
    py script.py
    ```

    ![alt text](image.png)
