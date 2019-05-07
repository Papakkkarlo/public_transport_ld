import pandas as pd
import geocoder

fields = ['district', 'street', 'house', 'flats', 'lat', 'lng']
#with open('flatsSpb.csv','a+', encoding="utf-8") as f:
#		f.write("{}\n".format('\t'.join(str(field) for field in fields)))
file = pd.read_csv('spbFlats.csv', sep='\t')
for i in range(11810, len(file['street'])):
	add = file['district'][i]+', '+file['street'][i]+', '+file['house'][i]
	g = geocoder.yandex(add)
	data = { 'district':file['district'][i],
			'street':file['street'][i],
			'house':file['house'][i],
			'flats':file['flats'][i],
			'lat': g.json['lat'],
			'lng': g.json['lng']}
	print(data)
	with open('flatsSpb.csv','a+', encoding="utf-8") as f:
		f.write("{}\n".format('\t'.join(str(data[field]) for field in fields)))