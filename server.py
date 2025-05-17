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
        if response.status_code == 200:
            data = response.json()
            subscriber_count = int(data.get("est_sub", 0))
            avarage_count = subscriber_count - 1009000
            print(f"Abone Sayısı: {avarage_count}")
        else:
            print(f"API hata kodu: {response.status_code}")
            avarage_count = 0
    except Exception as e:
        print(f"Hata: {e}")
        avarage_count = 0

    return jsonify({"count": avarage_count})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print("Flask sunucusu çalışıyor...")
    app.run(host='0.0.0.0', port=port)
