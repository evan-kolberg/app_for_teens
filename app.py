from flask import Flask, request, render_template
from bs4 import BeautifulSoup
import requests
import re

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form.get('query')
        response = requests.get(f'http://google.com/search?q=wikihow+steps+to+recycle+{query}')
        response2 = requests.get(f'https://images.search.yahoo.com/search/images?p=${query}+pullute')
        
        soup = BeautifulSoup(response.text, 'html.parser')
        soup2 = BeautifulSoup(response2.text, 'html.parser')
            
        text = soup.get_text()

        steps = re.findall(r'(\bStep\s+\d[^.]*\.)', text, flags=re.I)
        first_step_index = next((i for i, s in enumerate(steps) if 'step 1' in s.lower()), None)
        if first_step_index is not None: steps = steps[first_step_index:]
        result = '<br>'.join(steps)
        result = re.sub(r'(<br>.*?)(Step\s+\d+)', r'\1<br>\2', result)

        images = soup2.find_all('img')
        all_image_links = [img.get('src') for img in images if img.get('src') is not None]
        https_image_links = [link for link in all_image_links if link.startswith('https')]
        image_links = https_image_links[:5]


        if result != None:
            return render_template('index.html', after=result, image_links=image_links)
        else:
            return render_template('index.html', result="Please edit your search. Try 'plastic' instead")
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True, port=8080)


