from flask import Flask, render_template, request, redirect, url_for
import requests
import json

app = Flask(__name__)

def check_links(links):
    results = []
    for link in links:
        try:
            response = requests.get(link)
            if response.status_code <= 399:
                results.append({"link": link, "status": "Working"})
            else:
                results.append({"link": link, "status": f"Status Code: {response.status_code}"})
        except requests.exceptions.RequestException as e:
            results.append({"link": link, "status": f"Error: {e}"})
    return results

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        links = request.form.get('text').split('\n')
        results = check_links(links)
        serialized_results = json.dumps(results)  # Serialize the results to JSON
        return redirect(url_for('show_results', results=serialized_results))
    else:
        return render_template('index.html')

@app.route('/results')
def show_results():
    serialized_results = request.args.get('results')
    results = json.loads(serialized_results) if serialized_results else None  # Deserialize the results from JSON
    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
