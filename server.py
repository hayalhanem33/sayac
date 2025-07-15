import subprocess
import json
from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Sayaç API çalışıyor."})

@app.route('/count', methods=['GET'])
def get_count():
    CHANNEL_ID = "UCaDpCyQiDfjLJ5jTmzZz7ZA"
    url = f"https://api.socialcounts.org/youtube-live-subscriber-count/{CHANNEL_ID}"

    try:
        result = subprocess.run(
            ['curl', '-s', '-A', 'Mozilla/5.0', url],
            stdout=subprocess.PIPE,
            check=True
        )
        data = json.loads(result.stdout)
        subscriber_count = int(data.get("est_sub", 0))
        avarage_count = subscriber_count - 1001000
        print(f"Abone Sayısı: {subscriber_count} | Ortalama: {avarage_count}")
    except Exception as e:
        print(f"Hata: {e}")
        avarage_count = 0

    return jsonify({"count": avarage_count})

if __name__ == '__main__':
