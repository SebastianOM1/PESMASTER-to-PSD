import requests
from bs4 import BeautifulSoup
import json

def get(url):
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')
  json_script = soup.find_all('script')[2].text
  first_trim = json_script[json_script.find('const player'):] # Up to player cons declaration
  second_trim = first_trim[first_trim.find('{'):] # Up to '{'
  data = second_trim[:second_trim.find(';')]
  return json.loads(data)