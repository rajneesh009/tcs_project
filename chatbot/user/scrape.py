import requests
from bs4 import BeautifulSoup


def cricket_score():
	result = {}
	url = "http://static.cricinfo.com/rss/livescores.xml"
	r = requests.get(url)
	while r.status_code is not 200:
        	r = requests.get(url)
	soup = BeautifulSoup(r.text,"lxml")
	data = soup.find_all("description")
	result['title'] = data[0].text
	result['match3'] = data[1].text
	result['match2'] = data[2].text
	result['match1'] = data[3].text
	return result

def football_score():
	result = {}
	url = "http://www.livefootball.com/"
	r = requests.get(url)
	while r.status_code is not 200:
        	r = requests.get(url)
	soup = BeautifulSoup(r.text,"lxml")
	data = soup.find_all("dd")
	result['0'] = data[0].text
	result['1'] = data[1].text
	result['2'] = data[2].text
	result['3'] = data[3].text
	result['4'] = data[4].text
	result['5'] = data[5].text
	result['6'] = data[6].text
	result['7'] = data[7].text
	return result

def weather():
	import requests
	from bs4 import BeautifulSoup
	url = "https://www.wunderground.com/q/zmw:00000.56.42182"
	r = requests.get(url)
	while r.status_code is not 200:
        	r = requests.get(url)
	soup = BeautifulSoup(r.text,"lxml")
	data = soup.find(id="curTemp")
	data2 = soup.find(id="curCond")
	result = {}
	result['temp'] = data.text.splitlines()[2];
	result['unit'] = data.text.splitlines()[3];
	result['Condition'] = data2.text;
	for span in soup.find_all("span", attrs={"data-variable": "humidity"}):
		result['Humidity'] = span.text.splitlines()[1]
	return result

def stock():
	import requests
	from bs4 import BeautifulSoup
	url = "http://economictimes.indiatimes.com/indices/nifty_50_companies"
	r = requests.get(url)
	result = {}
	while r.status_code is not 200:
	        r = requests.get(url)
	soup = BeautifulSoup(r.text,"lxml")
	data2 = soup.find("div", attrs={"id": "ltp"})
	result['nifty'] = data2.text

	url = "http://economictimes.indiatimes.com/indices/sensex_30_companies"
	r = requests.get(url)
	while r.status_code is not 200:
	        r = requests.get(url)
	soup = BeautifulSoup(r.text,"lxml")
	data2 = soup.find("div", attrs={"id": "ltp"})
	result['sensex'] = data2.text

	url = "http://economictimes.indiatimes.com/commoditysummary/symbol-GOLD.cms"
	r = requests.get(url)
	while r.status_code is not 200:
	        r = requests.get(url)
	soup = BeautifulSoup(r.text,"lxml")
	data2 = soup.find("span", attrs={"class": "commodityPrice"})
	result['gold'] = data2.text


	url = "http://economictimes.indiatimes.com/commoditysummary/symbol-SILVER.cms"
	r = requests.get(url)
	while r.status_code is not 200:
	        r = requests.get(url)
	soup = BeautifulSoup(r.text,"lxml")
	data2 = soup.find("span", attrs={"class": "commodityPrice"})
	result['silver'] = data2.text
	return result

def petrol():
	import requests
	from bs4 import BeautifulSoup
	url = "http://www.mypetrolprice.com/2/Diesel-price-in-Delhi"
	r = requests.get(url)
	while r.status_code is not 200:
	        r = requests.get(url)
	soup = BeautifulSoup(r.text,"lxml")
	data2 = soup.find("span", attrs={"id": "CPH1_lblCurrent"})
	result = {}
	result['diesel'] = data2.text

	url = "http://www.mypetrolprice.com/2/Petrol-price-in-Delhi"
	r = requests.get(url)
	while r.status_code is not 200:
	        r = requests.get(url)
	soup = BeautifulSoup(r.text,"lxml")
	data2 = soup.find("span", attrs={"id": "CPH1_lblCurrent"})
	result['petrol'] = data2.text

	url = "http://www.mypetrolprice.com/2/CNG-price-in-Delhi"
	r = requests.get(url)
	while r.status_code is not 200:
	        r = requests.get(url)
	soup = BeautifulSoup(r.text,"lxml")
	data2 = soup.find("span", attrs={"id": "CPH1_lblCurrent"})
	result['cng'] = data2.text
	return result

	

if __name__ == '__main__':
	cricket_score()
	football_score()
	weather()
	stock()
	petrol()
