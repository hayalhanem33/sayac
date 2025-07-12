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

    try:
        response = requests.get(youtube_api_url)
        response.raise_for_status()  # Hatalı istekleri otomatik yakala
        data = response.json()

        subscriber_count = int(data.get("est_sub", 0))
        avarage_count = subscriber_count - 1001000

        print(f"API'den Gelen: {subscriber_count} | Ortalama: {avarage_count}")
    except Exception as e:
        print(f"Hata: {e}")
        avarage_count = 0

    return jsonify({"count": avarage_count})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print("Flask sunucusu çalışıyor...")
    app.run(host='0.0.0.0', port=port)
