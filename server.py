import httpx
from flask import Flask, jsonify, render_template_string
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    # Get the count and display it on the main page
    count_data = get_subscriber_count()
    return jsonify({
        "message": "Sayaç API çalışıyor.",
        "subscriber_count": count_data
    })

@app.route('/html', methods=['GET'])
def html_view():
    count_data = get_subscriber_count()
    
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>YouTube Abone Sayacı</title>
        <meta charset="UTF-8">
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                margin: 0;
                padding: 50px;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
            }
            .container {
                background: rgba(255, 255, 255, 0.1);
                padding: 40px;
                border-radius: 20px;
                backdrop-filter: blur(10px);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            }
            h1 {
                font-size: 2.5em;
                margin-bottom: 20px;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            }
            .count {
                font-size: 4em;
                font-weight: bold;
                margin: 20px 0;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            }
            .status {
                font-size: 1.2em;
                margin: 10px 0;
            }
            .error {
                color: #ff6b6b;
                background: rgba(255, 107, 107, 0.2);
                padding: 10px;
                border-radius: 10px;
                margin: 10px 0;
            }
            .refresh-btn {
                background: rgba(255, 255, 255, 0.2);
                border: none;
                color: white;
                padding: 15px 30px;
                border-radius: 25px;
                font-size: 1.1em;
                cursor: pointer;
                margin-top: 20px;
                transition: all 0.3s ease;
            }
            .refresh-btn:hover {
                background: rgba(255, 255, 255, 0.3);
                transform: translateY(-2px);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📺 YouTube Abone Sayacı</h1>
            <div class="status">
                {% if count_data.status == "success" %}
                    <div class="count">{{ count_data.count | default(0) }}</div>
                    <p>Ham Sayı: {{ count_data.raw_count | default(0) }}</p>
                {% else %}
                    <div class="count">❌</div>
                    <div class="error">{{ count_data.error | default("Bilinmeyen hata") }}</div>
                {% endif %}
            </div>
            <button class="refresh-btn" onclick="location.reload()">🔄 Yenile</button>
        </div>
    </body>
    </html>
    """
    
    return render_template_string(html_template, count_data=count_data)

@app.route('/count', methods=['GET'])
def get_count():
    count_data = get_subscriber_count()
    return jsonify(count_data)

@app.route('/test', methods=['GET'])
def test_api():
    """Test endpoint to check if the external API is working"""
    CHANNEL_ID = "UCaDpCyQiDfjLJ5jTmzZz7ZA"
    youtube_api_url = f"https://api.socialcounts.org/youtube-live-subscriber-count/{CHANNEL_ID}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://socialcounts.org/",
        "Origin": "https://socialcounts.org"
    }
    
    try:
        with httpx.Client(headers=headers, timeout=10.0) as client:
            response = client.get(youtube_api_url)
            return jsonify({
                "status": "success",
                "status_code": response.status_code,
                "response_headers": dict(response.headers),
                "response_text": response.text[:500]  # First 500 chars
            })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Render"""
    return jsonify({
        "status": "healthy",
        "message": "Server is running"
    })

def get_subscriber_count():
    CHANNEL_ID = "UCaDpCyQiDfjLJ5jTmzZz7ZA"
    youtube_api_url = f"https://api.socialcounts.org/youtube-live-subscriber-count/{CHANNEL_ID}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://socialcounts.org/",
        "Origin": "https://socialcounts.org"
    }

    try:
        logger.info(f"Fetching subscriber count from: {youtube_api_url}")
        with httpx.Client(headers=headers, timeout=15.0) as client:
            response = client.get(youtube_api_url)
            response.raise_for_status()
            data = response.json()
            
            logger.info(f"API Response: {data}")
            
            subscriber_count = int(data.get("est_sub", 0))
            avarage_count = subscriber_count - 1001000
            
            logger.info(f"Abone Sayısı: {subscriber_count} | Ortalama: {avarage_count}")
            
            return {
                "count": avarage_count,
                "raw_count": subscriber_count,
                "status": "success"
            }
            
    except httpx.RequestError as e:
        logger.error(f"Request error: {e}")
        return {
            "count": 0,
            "error": f"Request failed: {str(e)}",
            "status": "error"
        }
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error: {e.response.status_code} - {e}")
        return {
            "count": 0,
            "error": f"HTTP error: {e.response.status_code}",
            "status": "error"
        }
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {
            "count": 0,
            "error": f"Unexpected error: {str(e)}",
            "status": "error"
        }

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Flask sunucusu çalışıyor... Port: {port}")
    app.run(host='0.0.0.0', port=port)
