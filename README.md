# sup_bot

### Getting Start

##### Setup

Following are steps to setup this application before run locally:

1. Clone the repo:

```py
git clone git@github.com:jdl15/sup_bot.git
```

2. Creating a vector store on the OpenAI platform and obtain the vectore store id for later use. To create the vector store, see [OpenAI Storage](https://platform.openai.com/storage)
3. Creating an **`.env`** and pass in your OpenAI API Key and the vector store id you obtain from the previous step as follow:
   ```py
    OPENAI_API_KEY=<your key>
    VECTOR_STORE_ID=<your id>
   ```
4. Creating a virtual environment using `python -m venv venv` and activate by `source venv/bin/activate`

##### Running the application

If you don't want to run using Docker, download the requirements in requirements.txt by `pip install -r requirements.txt` and run `python main.py` in your virtual environment.
<br>
To run with docker, build: `docker build -t main.py:latest .` and run `docker run --env-file .env main.py`.

### About the Application

- Scraping support articles using Zendesk API and converting them into clean Markdown.

- Uploading the articles to OpenAI Vector Store, where the content is automatically split into manageable. The application use the vector store default chunking strategy which the token size is 800 for each chunk and overlap 400 tokens. User can create an OpenAI Assistant that answers user questions using only the uploaded documentation.

- Automating daily updates: the scraper runs daily in digital ocean, detecting new or updated articles and uploading only the changes. Log added, updated, and skipped articles. Access the Log using [Open Search Dashboard](db-opensearch-nyc3-68715-do-user-24863894-0.j.db.ondigitalocean.com)
  <br>
  This application ensures that OptiBot always has access to the latest support content, providing accurate, concise, and cited answers to customer questions without requiring manual updates. Here is some of the example output:
