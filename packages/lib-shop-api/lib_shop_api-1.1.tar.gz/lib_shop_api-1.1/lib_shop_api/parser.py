import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from lib_shop_api import models
from lib_shop_api import urls

class Parser():
	def __init__(self) -> None:	
		self._user_agent = UserAgent().random
		self._headers = {'User-Agent':self._user_agent}	
		self._cookies = {}
		self._default_number_page = 1
		self._suffix_url_page = "?PAGEN_1="

	def _build_url(self, category:str, number_page:int) -> str:
		url = urls.URLS[category]
		return f"{url}{self._suffix_url_page}{number_page}"
	
	def _get_soup(self, url:str) -> BeautifulSoup:
		response = requests.get(url, headers=self._headers, cookies=self._cookies)
		soup = BeautifulSoup(response.text, 'html.parser')
		return soup

	def get_count_pages(self, category:str) -> int:
		url = self._build_url(category, self._default_number_page)
		soup = self._get_soup(url)
		try:
			num = soup.find("div",class_="bx-pagination-container").find_all("span")[-2].text
		except AttributeError:
			num = soup.find("div",class_="catalog__all-goods catalog__all-goods_bottom").text
			num = num.replace("Всего", "").replace("товаров", "").strip()
		return int(num)		
	
	def get_count_products(self, category:str) -> int:
		url = self._build_url(category, self._default_number_page)
		soup = self._get_soup(url)
		num = soup.find("div",class_="catalog__all-goods catalog__all-goods_bottom").text.replace("Всего", "").replace("товаров", "").strip()
		return int(num)		

	def get_products(self, category:str, number_page:int) -> list[ models.Product ]:
		url = self._build_url(category,number_page)
		soup = self._get_soup(url)
		temp_array_products = []
		for div in soup.find_all("div", class_="product-card-item"):
			title = div.find("a", class_="product-card-item__link link").text
			price = str(div.find("div", class_="product-card-item__prices").find("p").text.replace("₽","").strip().replace(u"\xa0",u"")).encode('utf-8')
			image = urls.URL_PREFIX_IMAGE + div.find("a",class_="product-card-item__image").find("img").get("src")
			description = div.find("p", class_="product-card-item__description").text
			temp_array_products.append(models.Product(title, image, price, description))
		return temp_array_products

	def get_products_iterator(self, category:str, max_products:int=1) -> list[ models.Product ]:
		'''if max=-1 : run loop with ended
		default max=1'''
		counter_iter = 0
		for num_page in range(self.get_count_pages(category)):
			url = self._build_url(category,num_page)
			soup = self._get_soup(url)
			for div in soup.find_all("div", class_="product-card-item"):
				if counter_iter == max_products:
					return
				title = div.find("a", class_="product-card-item__link link").text
				price = str(div.find("div", class_="product-card-item__prices").find("p").text.replace("₽","").strip().replace(u"\xa0",u"")).encode('utf-8')
				image = urls.URL_PREFIX_IMAGE + div.find("a",class_="product-card-item__image").find("img").get("src")
				description = div.find("p", class_="product-card-item__description").text
				product = models.Product(title, image, price, description)
				counter_iter += 1
				yield product
				