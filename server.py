from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/count', methods=['GET'])
def get_count():
    CHANNEL_ID = "UCaDpCyQiDfjLJ5jTmzZz7ZA"
    youtube_api_url = f"https://api.socialcounts.org/youtube-live-subscriber-count/{CHANNEL_ID}"

    try:
        response = requests.get(youtube_api_url)
        data = response.json()
        subscriber_count = int(data.get("est_sub", 0))
        youtube_count = int(data.get("API_sub"))
        #avarage_count = ((40*subscriber_count + 60*youtube_count)/100)+1500
        avarage_count = subscriber_count-1019000
        #rounded_count = int(round(avarage_count))
        print(f"Abone Sayisi: {avarage_count}")  # Terminale yazdırma
    except Exception as e:
        print(f"Hata: {e}")
        subscriber_count = 0

    return jsonify({"count": avarage_count})

if __name__ == '__main__':
    print("Flask sunucusu calisiyor...")  # Başlangıç mesajı
    app.run(host='0.0.0.0', port=5000)
