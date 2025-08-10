import httpx
from flask import Flask, jsonify, render_template_string
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    """Main endpoint that returns JSON with subscriber count"""
    count_data = get_subscriber_count()
    return jsonify({
        "message": "Sayaç API çalışıyor.",
        "subscriber_count": count_data
    })

@app.route('/counter', methods=['GET'])
def counter():
    """Simple endpoint for Smiirl - returns JSON with counter value + 1000"""
    count_data = get_subscriber_count()
    
    if count_data.get("status") == "success":
        original_count = count_data.get("count", 0)
        adjusted_count = original_count + 1000
        return jsonify({"count": adjusted_count})
    else:
        return jsonify({"count": 1000})

@app.route('/html', methods=['GET'])
def html_view():
    """HTML view for browser display"""
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

def get_subscriber_count():
    """Get subscriber count from socialcounts.org using working method"""
    CHANNEL_ID = "UCaDpCyQiDfjLJ5jTmzZz7ZA"
    
    # Working method - Mobile Safari User-Agent
    url = f"https://api.socialcounts.org/youtube-live-subscriber-count/{CHANNEL_ID}"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    try:
        with httpx.Client(headers=headers, timeout=20.0, follow_redirects=True) as client:
            response = client.get(url)
            response.raise_for_status()
            
            data = response.json()
            subscriber_count = int(data.get("est_sub", 0))
            
            if subscriber_count > 0:
                avarage_count = subscriber_count - 1001000
                
                logger.info(f"Found real data: {subscriber_count:,} | Average: {avarage_count:,}")
                
                return {
                    "count": avarage_count,
                    "raw_count": subscriber_count,
                    "status": "success",
                    "method": "Mobile Safari",
                    "source": "real API data"
                }
            else:
                logger.warning("No valid subscriber count found in response")
                return {
                    "count": 0,
                    "raw_count": 0,
                    "status": "error",
                    "method": "Mobile Safari",
                    "error": "No subscriber count in response",
                    "source": "empty_response"
                }
                
    except Exception as e:
        logger.error(f"Failed to get subscriber count: {e}")
        return {
            "count": 0,
            "raw_count": 0,
            "status": "error",
            "method": "Mobile Safari",
            "error": str(e),
            "source": "exception"
        }

# Vercel için export
app.debug = True
