from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    person_name = request.form['person']
    wiki_url = f'https://en.wikipedia.org/wiki/{person_name.replace(" ", "_")}'

    try:
        response = requests.get(wiki_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the infobox where the "Born" information is typically located
        infobox = soup.find('table', class_='infobox')
        born_info = "Born information not found."

        if infobox:
            rows = infobox.find_all('tr')
            for row in rows:
                header = row.find('th')
                if header and 'Born' in header.text:
                    born_info = row.find('td').text
                    break

    except Exception as e:
        born_info = f"Error fetching data: {str(e)}"

    return render_template('result.html', person_name=person_name, bio_info=born_info)

if __name__ == '__main__':
    app.run(debug=True)
