# Twitter-tweet-analysis-
Twitter sentiment analysis is an NLP-based technique used to determine whether a tweet expresses positive, negative, or neutral sentiment towards a specific topic or entity. It involves cleaning text, removing URLs and stopwords, and applying machine learning models like Random Forest or Logistic Regression to analyze public opinion.

## Project Overview
This repository contains a simple web application that allows users to perform sentiment analysis on tweets related to a keyword, hashtag, or topic. The application:

- Fetches tweets automatically using the Twitter API
- Cleans tweet text by removing URLs, mentions, hashtags, and special characters
- Analyzes sentiment as **positive**, **negative**, or **neutral** using TextBlob
- Displays results through pie charts and summary statistics
- Supports filtering by date range
- Generates a word cloud of frequently used words

### Features
- **Keyword/Hashtag search**
- **Date filtering**
- **Location filtering** (optional)
- **Chart visualizations** (pie chart for sentiment distribution and trends over time)
- **Word cloud** of the most common words
- **Downloadable CSV reports** with individual tweets and sentiment labels
- **Extensible dashboard** for additional statistics

### Getting Started
1. Copy `.env.example` to `.env` and populate your Twitter API credentials.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Visit `http://localhost:5000` in your browser.

### Containerized Deployment
You can also build a Docker image and run it locally or on any container host:

```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
CMD ["flask", "run"]
```

Build and run:

```bash
docker build -t twitter-sentiment .
docker run -p 5000:5000 --env-file .env twitter-sentiment
```

The web UI will again be available at `http://localhost:5000`.

### Automatic deployment via GitHub Actions
You can push this repository to GitHub and use the provided workflow (`.github/workflows/deploy.yml`) to deploy to Heroku automatically when `main` is updated.

1. **Create a Heroku app** (using the web UI or CLI):
   ```bash
   heroku create your-app-name
   ```
2. **Add the required secrets** to your GitHub repo (`Settings > Secrets > Actions`):
   - `HEROKU_API_KEY` – your Heroku API key (`heroku auth:token`)
   - `HEROKU_APP_NAME` – name of the Heroku app you created
   - `HEROKU_EMAIL` – email address associated with your Heroku account
3. When you push to `main`, GitHub Actions will install dependencies and deploy the app to Heroku. The workflow uses `akhileshns/heroku-deploy` action.

> After deployment you will have a live website at `https://your-app-name.herokuapp.com` (or your custom domain if configured).

> This repo has everything required to run or deploy the service; there is no pre‑existing hosted instance I can hand you, but the above steps will get it running under your GitHub account and Heroku.  If you prefer a different host, adjust the workflow accordingly.

### Future Enhancements
- Real-time tweet streaming and analysis
- Location-based filtering
- Exportable reports (PDF/CSV)
- More advanced sentiment classification models (e.g., fine-tuned transformers)
- Trend graphs over time
- User authentication for recurring queries

This setup is intended for businesses, researchers, or students to monitor public opinion and trends on social media.
