from bs4 import BeautifulSoup
import requests


url = "https://www.healthline.com/health/pregnancy/dos-and-donts"

response = requests.get(url=url)

soup = BeautifulSoup(response.content, 'html.parser')

data = []

for content in soup.find_all(['h1', 'h2', 'h3', 'p']):
    data.append(content.get_text())

# print(data)


with open(file='pregnancy_precautions.txt', mode='w') as f:
    for line in data:
        f.write(line + '\n')

print('data has been extracted and saved')
