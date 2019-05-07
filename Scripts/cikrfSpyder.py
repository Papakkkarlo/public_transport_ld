import scrapy
import json

# scrapy runspider

class cikrfSpyder(scrapy.Spider):
	name = 'cikrfSpyder'
	start_urls = ['http://www.cikrf.ru/services/lk_tree?id=9524391943']
	streets_url = 'http://www.cikrf.ru/services/lk_tree?ret=0&id='
	houses_url = 'http://www.cikrf.ru/services/lk_tree?id='
	flats_url = 'http://www.cikrf.ru/services/lk_tree?id='

	fields = ['district', 'street', 'house', 'flats']

	def __init__(self):
		with open('spbFlats.csv','a+', encoding="utf-8") as f:
			f.write("{}\n".format('\t'.join(str(field) for field in self.fields)))

	def parse(self, response):
		for resp in json.loads(response.body_as_unicode()):
			dist = resp["text"]
			dist_id = resp["id"]
			yield scrapy.Request(self.streets_url+dist_id, meta={'dist': dist}, callback=self.streets)

	def streets(self, response):
		for resp in json.loads(response.body_as_unicode()):
			street = resp["text"]
			street_id = resp["id"]
			yield scrapy.Request(self.houses_url+street_id, meta={'dist': response.meta.get('dist'), 'street': street}, callback=self.houses)

	def houses(self, response):
		for resp in json.loads(response.body_as_unicode()):
			house = resp["text"]
			house_id = resp["id"]
			yield scrapy.Request(self.flats_url+house_id, meta={'house': house ,'dist': response.meta.get('dist'), 'street': response.meta.get('street')}, callback=self.flats)

	def flats(self, response):
		try:
			flats = json.loads(response.body_as_unicode())[-1]["text"]
		except:
			flats = ''
		if flats == '1':
			flats = ''

		data = { 'district':response.meta.get('dist'),
			'street':response.meta.get('street'),
			'house':response.meta.get('house'),
			'flats':flats}
		print(data)
		with open('spbFlats.csv','a+', encoding="utf-8") as f:
			f.write("{}\n".format('\t'.join(str(data[field]) for field in self.fields)))