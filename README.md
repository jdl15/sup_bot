# sup_bot

### Getting Start

##### Setup

Following are steps to setup this application before run locally:

1. Clone the repo:

```py
git clone git@github.com:jdl15/sup_bot.git
```

2. Creating a vector store on the OpenAI platform and obtain the vectore store id for later use. To create the vector store, see [OpenAI Storage](https://platform.openai.com/storage).
3. Creating an **`.env`** and pass in your OpenAI API Key and the vector store id you obtain from the previous step as follow:
   ```py
    OPENAI_API_KEY=<your key>
    VECTOR_STORE_ID=<your id>
   ```
4. Creating a virtual environment using `python -m venv venv` and activate by `source venv/bin/activate`.

##### Running the application

If you don't want to run using Docker, download the requirements in requirements.txt by `pip install -r requirements.txt` and run `python main.py` in your virtual environment.
<br>
To run with docker, build: `docker build -t main.py:latest .` and run `docker run --env-file .env main.py`.

### About the Application

- Scraping support articles using Zendesk API and converting them into clean Markdown.

- Uploading the articles to OpenAI Vector Store, where the content is automatically split into manageable. The application use the following chunking strategy: the token size is 700 for each chunk and overlap 300 tokens. User can create an OpenAI Assistant that answers user questions using only the uploaded documentation.

- Automating daily updates: the scraper runs daily in digital ocean, detecting new or updated articles and uploading only the changes. Log added, updated, and skipped articles. You can access the log data through [OpenSearch](db-opensearch-nyc3-68715-do-user-24863894-0.j.db.ondigitalocean.com).
  <br>
  This application ensures that OptiBot always has access to the latest support content, providing accurate, concise, and cited answers to customer questions without requiring manual updates. Here is some of the example output:
  #### Q: What payment methods do you accept?
  <img width="1233" height="754" alt="Screenshot 2025-09-03 at 9 10 23 PM" src="https://github.com/user-attachments/assets/0a345587-5fd2-4552-a44f-269b17001ebd" />


  #### Q: How do I add a YouTube video?
  <img width="1214" height="762" alt="Screenshot 2025-09-03 at 9 09 04 PM" src="https://github.com/user-attachments/assets/2e078913-29db-4061-a02e-41452f3ba8f3" />


  #### Q: What's in your free plan?
  <img width="1232" height="750" alt="Screenshot 2025-09-03 at 9 12 37 PM" src="https://github.com/user-attachments/assets/f889bcc2-6375-4652-b338-422bb5ceb633" />

  
### Side Note
This newest commit prechunk the markdown file before upload to the vector store so the assisant can site the exact url. 
<br> 
The old version upload the entire markdown to the vector store and let the OpenAI handle chunking internally. You view it by [version 1](https://github.com/jdl15/sup_bot/tree/7d047f71ef2233a98a09cdaff5597e23ff05a4f3).


