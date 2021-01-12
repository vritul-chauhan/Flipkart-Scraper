#Importing required libraries
from bs4 import BeautifulSoup
import requests
import csv

#Opening CSV file and writing to it
csv_file = open("smartphone.csv","w", newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Brand", "Model_name", "Model_colour", "RAM(GB)","ROM(GB)" , "Display", "Processor", "Current_price","Original_price","Discount(%)", "Rating"])

#looping through all pages
for n in range(1,11):
	url = "https://www.flipkart.com/search?q=Smartphones&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&sort=popularity&page="+str(n)
	source = requests.get(url).text
	soup = BeautifulSoup(source, 'lxml')
	containers = soup.find_all("div", class_="_2kHMtA")
	for container in containers:
		model_detail = container.a.find("div", class_='_3pLy-c row')
		model = model_detail.div.div.text
		
		#Model name and Brand 
		model_name = model.split("(")[0]
		brand = model_name.split(" ")[0]

		#Colour
		model_colour = model.split("(")[1].split(",")[0]

		##Specifications
		specs = model_detail.find("div", class_='fMghEO').ul

		#Storage: RAM and ROM
		storage = specs.li.text.split("|")
		model_ram = None #default
		model_rom = None #default
		for s in storage:
			if 'RAM' in s:
				model_ram = s.strip(" ").split("G")[0]
				model_ram = int(model_ram)
			elif 'ROM' in s:
				model_rom = s.strip(" ").split("G")[0]
				model_rom = int(model_rom)

		if model_ram is None:
			if model_rom == 32:
				model_ram = 3
			else:
				model_ram = 4

		#Display and Processor		
		display = None #Default
		proc = 'Not Specified' #Default
		specs_list = specs.find_all("li")
		for s in specs_list:
			if "Display" in s.text:
				display = s.text
			if "Processor" in s.text:
				proc = s.text

		#Price
		model_price = model_detail.find("div",class_="col col-5-12 nlI3QM").div.div
		current_price = model_price.div.text[1:]
		s1 = int(current_price.split(',')[0])*1000
		s2 = int(current_price.split(',')[1])
		current_price = s1+s2
		try:
			original_price = model_price.find("div",class_="_3I9_wc _27UcVY").text[1:]
			s1 = int(original_price.split(',')[0])*1000
			s2 = int(original_price.split(',')[1])
			original_price = s1+s2
		except AttributeError as e:
			original_price = current_price
		try:
			discount = model_price.find("div", class_='_3Ay6Sb').span.text.split("%")[0]
		except AttributeError as e:
			discount = 0

		#Rating and Reviews
		try:
			review = float(model_detail.div.find("div",class_='gUuXy-').span.div.text)
		except AttributeError as e:
			review = 4.0
		#Adding row for each new entry
		csv_writer.writerow([brand, model_name, model_colour,model_ram, model_rom, display, proc, current_price,original_price, discount, review])

csv_file.close()