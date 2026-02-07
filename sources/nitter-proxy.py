#!/usr/bin/env python3
from flask import Flask, request, Response
import requests
import re

app = Flask(__name__)

@app.route('/proxy')
def proxy():
    username = request.args.get('username', '')
    
    if not username:
        return 'Username required', 400
    
    # Sanitize username
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return 'Invalid username', 400
    
    url = f'https://nitter.net/{username}'
    
    try:
        response = requests.get(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
            timeout=30
        )
        
        return Response(
            response.content,
            status=response.status_code,
            headers={
                'Content-Type': 'text/html; charset=utf-8',
                'Access-Control-Allow-Origin': '*'
            }
        )
    except Exception as e:
        return f'Error: {str(e)}', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
