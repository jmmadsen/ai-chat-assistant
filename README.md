# ai-chat-assistant
Leveraging Langchain to create a quantitative and qualitative GenAI chatbot

## Overview
This project shows how you can use ChatGPT to query documents for qualitative information, as well as querying databases for quantitative information. Users can interact with a chatbot using natural language to find the information they need.

The bot in this project has been "trained" on a library of documents about the 2023 MLB season to learn qualitative information (MVP, etc.). It can also translate quantitative questions from users into SQL, querying the Postgresql database about batting averages to provide analysis.

## How Does It Work?
ai-chat-assistant leverages the [Langchain library](https://www.langchain.com) to interact with ChatGPT. To answer qualitative questions, it loads various files (PDF, JSON, etc.) from a local directory. It then chunks and embeds these into a Vector Store database to optimize training and response performance.
![Screenshot vector store sharding](https://python.langchain.com/assets/images/vector_stores-125d1675d58cfb46ce9054c9019fea72.jpg)

Obviously, this simple use case is only for the 2023 MLB season - but it can be easily extended on your own using whatever relevant documents you want to provide.

To answer quantitative questions, ai-chat-assistant interprets the user's questions into SQL based on its understanding of select MLB stat tables in Postgres. It then interprets the responses to its queries to provide natural-language analysis based on the user's prompt.
![Screenshot of LLM to SQL](https://python.langchain.com/assets/images/sql_usecase-d432701261f05ab69b38576093718cf3.png)

## Technical Overview
This repository uses a Flask API in order to interact with the OpenAI API. It uses a React app for the user interface and chatbot, and a local Postgres container for the database. The API, UI, and DB are all containerized with Docker, and orchestrated via docker-compose.

The goal of this project is to show how it can be extended for more practical use cases. The UI can be replaced with an integration to Slack or Teams for a chatbot, and the local DB would be replaced with one used for business needs.

Functions to interact with Langchain and the LLM are stored in the `langchain_functions` folder. Utility functions for connecting to Postgresql and logging errors are stored in the `utils` folder. MLB information documents are stored in the `training_scripts` folder. The Postgresql datbase is seeded on start with batting average data, and the table needed for logging ChatGPT messages.

## How Do I Run This?
### Docker
1. Clone the repository onto your local machine
2. From the root directory, run `docker compose up`
3. Navigate to `localhost` in your browser URL to access the chatbot

### Local