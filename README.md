# Configurable Website Customer Service Agent

An open-source core for businesses that want to add an AI customer service assistant to their website.

The agent searches a configured public website and answers customer questions using its published content. It is designed to be easy to configure, extend, and deploy.

## Features

- Works with any configured public website
- Answers using information found on that website
- Provides relevant source links
- Includes a simple Gradio chat interface
- Uses OpenRouter for AI responses
- Uses Tavily for website search
- Can be customized for different businesses

## Project Status

This project is an open-source foundation and demonstration. It can be adapted into a production customer service system by adding authentication, rate limiting, monitoring, persistent conversations, and human-support escalation.

## Setup

Requires Python 3.10 or newer.

```bash
git clone <repository-url>
cd website-customer-service-agent
pip install -r requirements.txt
cp .env.example .env
```

Configure `.env`:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
TAVILY_API_KEY=your_tavily_api_key
TARGET_WEBSITE_DOMAIN=www.example.com
TARGET_WEBSITE_NAME=Example Business
```

Never commit your `.env` file or API keys.

## Run

```bash
python app.py
```

Then open `http://127.0.0.1:7860`.

## How It Works

1. A customer submits a question.
2. The agent searches the configured website.
3. It analyzes the available public content.
4. It returns an answer with relevant source links.

## Privacy and Deployment

Customer questions are sent to OpenRouter and Tavily. Review their privacy policies before using this project with sensitive information.

The default application is intended for development and demonstration. Add authentication, usage limits, secure hosting, logging controls, and isolated agent execution before deploying it publicly.

## Limitations

- Answers depend on publicly indexed website content.
- The agent may not find recently published or unindexed pages.
- Conversation history is not currently used.
- Human support is still recommended for sensitive or complex requests.

## Customization

You can extend the project with:

- A website chat widget
- Custom branding
- Private documentation
- Conversation storage
- Support-ticket creation
- Human-agent escalation
- Analytics and monitoring
- Additional tools and integrations

## Contributing

Contributions, bug reports, and feature suggestions are welcome.

## License

MIT License. See `LICENSE` for details.
