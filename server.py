from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Sayaç API çalışıyor."})

@app.route('/count', methods=['GET'])
def get_count():
    CHANNEL_ID = "UCaDpCyQiDfjLJ5jTmzZz7ZA"
    youtube_api_url = f"https://api.socialcounts.org/youtube-live-subscriber-count/{CHANNEL_ID}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://socialcounts.org/",
        "Origin": "https://socialcounts.org",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        response = requests.get(youtube_api_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        subscriber_count = int(data.get("est_sub", 0))
        avarage_count = subscriber_count - 1001000
        print(f"Abone Sayısı: {subscriber_count} | Ortalama: {avarage_count}")
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Hatası: {errh}")
        avarage_count = 0
    except Exception as e:
        print(f"Genel Hata: {e}")
        avarage_count = 0

    return jsonify({"count": avarage_count})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print("Flask sunucusu çalışıyor...")
    app.run(host='0.0.0.0', port=port)
