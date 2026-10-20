"""
Configurable Website Customer Service Agent
==========================================
This script builds a customer service agent using `smolagents` and the Tavily
Search API. It searches public pages within a configured website domain and uses
the returned results to answer customer support questions.

Author: Alaa Abou Ahmad
License: MIT
"""

import os
import json
from dotenv import load_dotenv
from smolagents import OpenAIModel, CodeAgent, tool
from tavily import TavilyClient
import gradio as gr

# Load environment variables from a .env file if present
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY environment variable is missing.")
if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY environment variable is missing.")

# Target website configuration
TARGET_WEBSITE_DOMAIN = os.getenv("TARGET_WEBSITE_DOMAIN")
TARGET_WEBSITE_NAME = os.getenv("TARGET_WEBSITE_NAME")

if not TARGET_WEBSITE_DOMAIN:
    raise ValueError("TARGET_WEBSITE_DOMAIN environment variable is missing.")
if not TARGET_WEBSITE_NAME:
    raise ValueError("TARGET_WEBSITE_NAME environment variable is missing.")

tavily = TavilyClient(api_key=TAVILY_API_KEY)

# Website search tool
@tool
def search_website_docs(query: str) -> str:
    """
    Search the target website domain for public information, documentation, and support guides.

    Args:
        query: Specific customer question or keywords to search for on the website.

    Returns:
        A JSON-formatted string containing matching page titles, URLs,
        relevance scores, and textual content snippets.
    """
    # Ask Tavily to limit search results to the configured domain.
    results = tavily.search(
        query=query,
        include_domains=[TARGET_WEBSITE_DOMAIN],
        max_results=5,
    )

    formatted_results = []
    for i, item in enumerate(results.get("results", []), start=1):
        formatted_results.append(
            {
                "number": i,
                "title": item.get("title", "Untitled Page"),
                "url": item.get("url", ""),
                "relevance": round(item.get("score", 0), 3),
                "snippet": item.get("content", "")[:600],
            }
        )

    if not formatted_results:
        return f"No relevant public pages were found on {TARGET_WEBSITE_DOMAIN} for this query."

    return json.dumps(
        formatted_results,
        ensure_ascii=False,
        indent=2,
    )


# Model configuration
model = OpenAIModel(
    model_id="openrouter/free",
    api_base="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    max_tokens=2048,
    temperature=0.2,
)

# Customer service agent
customer_service_agent = CodeAgent(
    model=model,
    tools=[search_website_docs],
    max_steps=8,
    verbosity_level=1,
    instructions=f"""
                  You are a professional, polite, and helpful customer service agent for {TARGET_WEBSITE_NAME} ({TARGET_WEBSITE_DOMAIN}).

                  When responding to a customer's inquiry:
                  1. Search the official website pages using the search_website_docs tool.
                  2. Read and carefully interpret the returned snippet results.
                  3. Never return raw Python lists, dictionaries, or JSON to the user.
                  4. Present helpful answers structured clearly with references.

                  Use this response structure:

                  ## Support Answer

                  Provide a clear, direct answer to the customer's question based on the documentation found.

                  ## Relevant References / Links
                  - **Title:** [Clickable Markdown Link to the source page]
                  - **Summary:** Brief detail of how this link answers or supports the query.

                  Important Guidelines:
                  - Only use information directly supported by the search results.
                  - If the information is missing or insufficient, politely explain that the current public documentation doesn't cover it and suggest contacting human support.
                  - Do not invent policies, pricing, URLs, or features.
                  - Do not print tool outputs directly as the final text response.
                  """,
)

# Gradio interface
def chat_with_customer_agent(message, history):
    """Generate a customer support response for a Gradio chat message.

    Args:
        message: The customer's current message.
        history: Previous Gradio chat messages. Currently unused by the agent.

    Returns:
        The agent's response as text, or an error message if processing fails.
    """
    try:
        response = customer_service_agent.run(message)
        return str(response)
    except Exception as exc:
        return f"An error occurred while processing your request: {exc}"


demo = gr.ChatInterface(
    fn=chat_with_customer_agent,
    title=f"{TARGET_WEBSITE_NAME} Customer Support Assistant",
    description=(
        f"Ask any questions about {TARGET_WEBSITE_NAME} "
        f"({TARGET_WEBSITE_DOMAIN}). "
        "My answers depend on the indexed website pages,"
        "I'll do my best to give you the last updated answers"
    ),
    examples=[
        "What is this website about?",
        "Can you guide me?",
        "Can you help me troubleshoot an issue?",
    ],
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
