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
    """Test endpoint to check final attempts and simulation"""
    CHANNEL_ID = "UCaDpCyQiDfjLJ5jTmzZz7ZA"
    
    # Final attempts test
    final_attempts = [
        {
            "name": "Alternative URL",
            "url": f"https://socialcounts.org/youtube-subscriber-count/{CHANNEL_ID}",
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
            }
        },
        {
            "name": "Mobile Safari",
            "url": f"https://socialcounts.org/youtube-live-subscriber-count/{CHANNEL_ID}",
            "headers": {
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
            }
        }
    ]
    
    results = []
    
    # Final attempts test
    for i, attempt in enumerate(final_attempts):
        try:
            with httpx.Client(headers=attempt["headers"], timeout=15.0, follow_redirects=True) as client:
                response = client.get(attempt["url"])
                results.append({
                    "attempt": i+1,
                    "name": attempt["name"],
                    "url": attempt["url"],
                    "status": "success",
                    "status_code": response.status_code,
                    "content_length": len(response.text),
                    "content_preview": response.text[:500]
                })
        except httpx.HTTPStatusError as e:
            results.append({
                "attempt": i+1,
                "name": attempt["name"],
                "url": attempt["url"],
                "status": "http_error",
                "status_code": e.response.status_code,
                "error": str(e),
                "response_text": e.response.text[:200]
            })
        except Exception as e:
            results.append({
                "attempt": i+1,
                "name": attempt["name"],
                "url": attempt["url"],
                "status": "error",
                "error": str(e)
            })
    
    # Simülasyon test
    try:
        import random
        import time
        
        base_count = 1000000
        current_time = int(time.time())
        hour = (current_time // 3600) % 24
        day_of_week = (current_time // 86400) % 7
        
        hourly_multiplier = 1.0
        if 9 <= hour <= 22:
            hourly_multiplier = 1.2
        elif 6 <= hour <= 8:
            hourly_multiplier = 0.8
        else:
            hourly_multiplier = 0.5
            
        if day_of_week in [5, 6]:
            hourly_multiplier *= 1.3
            
        random.seed(current_time // 300)
        base_increase = random.randint(50, 200) * hourly_multiplier
        trend_factor = 1 + (current_time % 86400) / 86400 * 0.1
        
        subscriber_count = int(base_count + base_increase * trend_factor)
        avarage_count = subscriber_count - 1001000
        
        simulation_result = {
            "attempt": "simulation",
            "name": "Realistic Simulation",
            "status": "success",
            "subscriber_count": subscriber_count,
            "average_count": avarage_count,
            "details": {
                "hour": hour,
                "day_of_week": day_of_week,
                "hourly_multiplier": round(hourly_multiplier, 2),
                "trend_factor": round(trend_factor, 2)
            }
        }
        
        results.append(simulation_result)
        
    except Exception as e:
        results.append({
            "attempt": "simulation",
            "name": "Realistic Simulation",
            "status": "error",
            "error": str(e)
        })
    
    return jsonify({
        "test_results": results,
        "total_attempts": len(final_attempts) + 1,
        "channel_id": CHANNEL_ID
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Vercel"""
    return jsonify({
        "status": "healthy",
        "message": "Server is running"
    })

@app.route('/number', methods=['GET'])
def get_number():
    """Simple endpoint that returns only the number for Smiirl"""
    count_data = get_subscriber_count()
    
    if count_data.get("status") == "success":
        return jsonify({"number": count_data.get("count", 0)})
    else:
        return jsonify({"number": 0, "error": count_data.get("error", "Unknown error")})

def get_subscriber_count():
    CHANNEL_ID = "UCaDpCyQiDfjLJ5jTmzZz7ZA"
    
    # Daha agresif yaklaşım - gerçek veriyi almak için
    aggressive_attempts = [
        # Deneme 1: Farklı endpoint
        {
            "name": "API Endpoint",
            "url": f"https://api.socialcounts.org/youtube-live-subscriber-count/{CHANNEL_ID}",
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Referer": "https://socialcounts.org/",
                "Origin": "https://socialcounts.org",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache"
            }
        },
        # Deneme 2: Web scraping
        {
            "name": "Web Scraping",
            "url": f"https://socialcounts.org/youtube-live-subscriber-count/{CHANNEL_ID}",
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Upgrade-Insecure-Requests": "1"
            }
        },
        # Deneme 3: Farklı User-Agent
        {
            "name": "Mobile Safari",
            "url": f"https://api.socialcounts.org/youtube-live-subscriber-count/{CHANNEL_ID}",
            "headers": {
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
                "Accept": "application/json",
                "Accept-Language": "en-US,en;q=0.9"
            }
        },
        # Deneme 4: Minimal headers
        {
            "name": "Minimal Headers",
            "url": f"https://api.socialcounts.org/youtube-live-subscriber-count/{CHANNEL_ID}",
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        },
        # Deneme 5: Farklı endpoint
        {
            "name": "Alternative Endpoint",
            "url": f"https://socialcounts.org/api/youtube-live-subscriber-count/{CHANNEL_ID}",
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "application/json"
            }
        }
    ]
    
    for i, attempt in enumerate(aggressive_attempts):
        try:
            logger.info(f"Aggressive attempt {i+1}: {attempt['name']}")
            
            with httpx.Client(headers=attempt["headers"], timeout=20.0, follow_redirects=True) as client:
                response = client.get(attempt["url"])
                response.raise_for_status()
                
                # JSON response kontrolü
                if attempt["name"] == "API Endpoint" or attempt["name"] == "Mobile Safari" or attempt["name"] == "Minimal Headers" or attempt["name"] == "Alternative Endpoint":
                    try:
                        data = response.json()
                        logger.info(f"JSON Response: {data}")
                        
                        subscriber_count = int(data.get("est_sub", 0))
                        if subscriber_count > 0:
                            avarage_count = subscriber_count - 1001000
                            
                            logger.info(f"Found real data from {attempt['name']}: {subscriber_count:,} | Average: {avarage_count:,}")
                            
                            return {
                                "count": avarage_count,
                                "raw_count": subscriber_count,
                                "status": "success",
                                "method": attempt["name"],
                                "source": "real API data"
                            }
                    except:
                        pass
                
                # HTML response kontrolü
                html_content = response.text
                logger.info(f"HTML Content length: {len(html_content)}")
                
                # HTML'den abone sayısını çıkaralım
                import re
                
                patterns = [
                    r'"est_sub":\s*(\d+)',
                    r'"subscriber_count":\s*(\d+)',
                    r'"count":\s*(\d+)',
                    r'(\d{1,3}(?:,\d{3})*)\s*subscribers',
                    r'(\d{1,3}(?:,\d{3})*)\s*abone',
                    r'(\d{1,3}(?:,\d{3})*)\s*followers',
                    r'(\d{1,3}(?:,\d{3})*)\s*subscriber'
                ]
                
                for pattern in patterns:
                    match = re.search(pattern, html_content, re.IGNORECASE)
                    if match:
                        subscriber_count = int(match.group(1).replace(',', ''))
                        if subscriber_count > 0:
                            avarage_count = subscriber_count - 1001000
                            
                            logger.info(f"Found real data from {attempt['name']}: {subscriber_count:,} | Average: {avarage_count:,}")
                            
                            return {
                                "count": avarage_count,
                                "raw_count": subscriber_count,
                                "status": "success",
                                "method": attempt["name"],
                                "source": "real HTML data"
                            }
                
                logger.warning(f"No valid data found in {attempt['name']}")
                
        except Exception as e:
            logger.error(f"Aggressive attempt {i+1} failed: {e}")
            continue
    
    # Tüm denemeler başarısız olursa hata döndür
    logger.error("All attempts failed - no real data available")
    return {
        "count": 0,
        "raw_count": 0,
        "status": "error",
        "method": "all attempts failed",
        "error": "Socialcounts API is blocking all requests. No real data available.",
        "source": "blocked"
    }

# Vercel için export
app.debug = True
