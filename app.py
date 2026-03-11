import os
import re
from flask import Flask, render_template, request, jsonify, send_file
from textblob import TextBlob
import tweepy
import pandas as pd
from wordcloud import WordCloud
from io import BytesIO
from dotenv import load_dotenv

# load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Twitter API credentials should be set in environment variables
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET')

# Initialize tweepy client
auth = tweepy.OAuth1UserHandler(
    TWITTER_API_KEY, TWITTER_API_SECRET,
    TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET
)
api = tweepy.API(auth)


def clean_tweet(text):
    """Remove URLs, mentions, hashtags and non-alphanumeric chars"""
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"@\S+", "", text)
    text = re.sub(r"#", "", text)
    text = re.sub(r"[^A-Za-z0-9 ]+", "", text)
    return text.strip()


def analyze_sentiment(tweet):
    blob = TextBlob(tweet)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return "positive"
    elif polarity < 0:
        return "negative"
    else:
        return "neutral"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    keyword = request.form.get('keyword')
    count = int(request.form.get('count', 100))
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    location = request.form.get('location')  # optional

    # build query; location handling is limited in the standard API
    query = keyword + ' -filter:retweets'
    if location:
        query += f' near:{location}'

    tweets = []
    dates = []
    for status in tweepy.Cursor(api.search_tweets, q=query, tweet_mode='extended', lang='en', since=start_date, until=end_date).items(count):
        text = status.full_text
        tweets.append(text)
        dates.append(status.created_at.date())

    cleaned = [clean_tweet(t) for t in tweets]
    sentiments = [analyze_sentiment(t) for t in cleaned]

    df = pd.DataFrame({'tweet': cleaned, 'sentiment': sentiments, 'date': dates})

    # statistics
    stats = df['sentiment'].value_counts().to_dict()

    # trend by date
    trend = df.groupby(['date', 'sentiment']).size().unstack(fill_value=0).to_dict()

    # prepare records for download
    records = df.to_dict(orient='records')

    # word cloud
    all_text = ' '.join(cleaned)
    wc = WordCloud(width=800, height=400).generate(all_text)
    buf = BytesIO()
    wc.to_image().save(buf, format='PNG')
    buf.seek(0)
    import base64
    wc_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')

    return jsonify({
        'stats': stats,
        'total': len(df),
        'trend': trend,
        'wordcloud': wc_b64,
        'records': records,
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
