from flask import Flask, render_template, request
import requests

app = Flask(__name__)


def check_links(links):
    results = []
    for link in links:
        try:
            response = requests.get(link)
            if response.status_code <= 399:
                results.append(f"{link} - Working")
            else:
                results.append(f"The link {link} returned a status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            results.append(f"An error occurred while checking the link {link}: {e}")
    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        links = request.form.get('links').split('\n')
        results = check_links(links)
        return render_template('index.html', results=results)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)