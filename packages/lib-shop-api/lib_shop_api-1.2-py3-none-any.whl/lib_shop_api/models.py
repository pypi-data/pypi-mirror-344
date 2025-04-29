class Product():
	def __init__(self, title:str, image:str, price:str, description:str, catalog:str):
		self.title = title.strip()
		self.image = image.strip()
		self.price = price.strip()
		self.description = description.strip()
		self.catalog = catalog.strip()
	def __str__(self):
		return f"{self.title, self.image, self.price, self.description}"
        
