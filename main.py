import requests
from bs4 import BeautifulSoup

url = 'https://www.decathlon.fr/browse/c0-tous-les-sports/c1-velo-tout-chemin-vtc/c3-velos-gravel-homme/_/N-1xp9wy3'
headers = {
  'User-Agent':
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}

import requests
from bs4 import BeautifulSoup

url = 'https://www.decathlon.fr/browse/c0-tous-les-sports/c1-velo-tout-chemin-vtc/c3-velos-gravel-homme/_/N-1xp9wy3'
headers = {
  'User-Agent':
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}


class BikeData:
  def __init__(self, n, i, d, p, l):
    self.name = n
    self.img = i
    self.dispo = d
    self.price = p
    self.link = l

  def __str__(self):
        return str(self.name) + ": " + 'Img: ' + str(self.img) + 'Dispo: ' + str(self.dispo) + ' Price :' + str(self.price) + ' Link : ' + str(self.link)
        

def getData():
  result = requests.get(url, headers=headers)

  # print(result.content.decode())
  # print(result.status_code)

  soup = BeautifulSoup(result.content, "html.parser")
  #print(soup.prettify())


  bikes = soup.find_all('div', {'class': 'vtmn-flex vtmn-flex-col vtmn-items-center vtmn-relative vtmn-overflow-hidden vtmn-text-center vtmn-z-0 dpb-bottom-btn-padding dpb-holder--is-light svelte-1xziusa'})
  print("Nombre de résultats :",len(bikes))

  allBikeData = []

  for bike in bikes: 
    bikeData = BikeData(None, None, None, None, None)
    bikeData.name = bike.h2.get_text()
    bikeData.img = bike.img['src']

    price = bike.find_all('div', {'class': 'price-content'})
    if(price):
      bikeData.price = price[0].get_text().strip()

    
    # print(bike)
    # return
    link = bike.find_all('a', {'class': 'dpb-product-model-link'})
    if(link):
      bikeData.link = 'https://www.decathlon.fr/' + link[0]['href']

    # print(bike.h2.get_text())
    # print(bike.img['src'])

    status = bike.find_all('div', {'class': 'dpb-leadtime'}) #dispo
    if(status):
      bikeData.dispo = status[0].get_text()
      # print(status[0].get_text())
    else:
      status = bike.find_all('div', {'class': 'dpb-unavailable'}) #indispo
      if(status):
        bikeData.dispo = status[0].get_text().strip()
        # print(status[0].get_text().strip())
      else:
        compagnie_name = bike.find_all('a', {'class': 'seller-link'}) #indispo
        if(compagnie_name):
          bikeData.dispo = 'Vendu et expédié par' + compagnie_name[0].get_text().strip()
          # print('Vendu et expédié par', compagnie_name[0].get_text().strip())
        else:
          bikeData.dispo = 'Disponible pour certaines tailles'

    allBikeData.append(bikeData)

  for bike in allBikeData:
    print(bike)
  
  return allBikeData


data = getData()

for bike in data:
  print(bike)

from flask import Flask
from flask import render_template

app = Flask('app')


@app.route("/")
def home():
  data = getData()
  return render_template('home.html', data=data)


app.run(host='0.0.0.0', port=8080)
