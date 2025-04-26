from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/count', methods=['GET'])
def get_count():
    CHANNEL_ID = "UCaDpCyQiDfjLJ5jTmzZz7ZA"
    youtube_api_url = f"https://api.socialcounts.org/youtube-live-subscriber-count/{CHANNEL_ID}"

    try:
        response = requests.get(youtube_api_url)
        data = response.json()
        subscriber_count = int(data.get("est_sub", 0))
        avarage_count = subscriber_count - 1019000
        print(f"Abone Sayisi: {avarage_count}")
    except Exception as e:
        print(f"Hata: {e}")
        avarage_count = 0

    return jsonify({"count": avarage_count})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print("Flask sunucusu calisiyor...")
    app.run(host='0.0.0.0', port=port)