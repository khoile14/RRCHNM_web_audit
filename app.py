from flask import Flask, render_template, request, jsonify
import requests
import urllib.parse

app = Flask(__name__)


def check_links(links):
    headers = {
        'User-Agent': 'curl/7.55.1'
    }
    results = []
    for link in links:
        try:
            response = requests.get(link.strip(),headers= headers, allow_redirects=True)
            if response.status_code <= 399:
                results.append({"link": link, "status": "Working"})
                print("test")
            else:
                results.append(
                    {"link": link, "status": f"Status Code: {response.status_code}"})
        except requests.exceptions.RequestException as e:
            results.append({"link": link, "status": f"Error: {e}"})
    return results


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        links = request.form.get('text').split('\n')
        results = check_links(links)
        return jsonify(results)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

