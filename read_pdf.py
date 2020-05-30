# importing all the required modules

from os import listdir
from os.path import isfile, join
import PyPDF2
import glob, os

import requests
from getpass import getpass
from bs4 import BeautifulSoup

import urllib.request # download files

OUTPUT = "output/archivos_Tarea_1/"

def read_pdf(file_pdf):
	PDFFile = open(file_pdf,'rb')
	PDF = PyPDF2.PdfFileReader(PDFFile)
	pages = PDF.getNumPages()
	key = '/Annots'
	uri = '/URI'
	ank = '/A'

	file_error = []
	url = ""
	for page in range(pages):
		#print("Current Page: {}".format(page))
		pageSliced = PDF.getPage(page)
		pageObject = pageSliced.getObject()
		if key in pageObject.keys():
			ann = pageObject[key]
			for a in ann:
				try:
					u = a.getObject() # se cae por algo pero no cacho
				except:
					file_error.append(file_pdf)
					next
				else:
					if uri in u[ank].keys():
						url = u[ank][uri]
						path_cc3002 = "/CC3002-Metodologias/99-7-citric-liquid"
						if path_cc3002 in url:
							#print(url)
							break
	return [url, file_error]

github_links = {}
directories = [f for f in listdir(OUTPUT)]
for student_dir in directories:
	full_path = f"{OUTPUT}{student_dir}/"
	for file in listdir(full_path):
		if(file.endswith(".pdf")):
			path_pdf = f"{OUTPUT}{student_dir}/{file}"
			link, errors_file = read_pdf(path_pdf)
			if (link!=""):
				github_links[full_path] = link

headers = {
 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

login_data = {
	'commit': 'Sign in',
	'utf8': '%E2%9C%93',
	'login': input('Username: '),
	'password': getpass()
}
url = 'https://github.com/session'
session = requests.Session()
response = session.get(url, headers=headers)

soup = BeautifulSoup(response.text, 'html5lib')
login_data['authenticity_token'] = soup.find('input', attrs={'name': 'authenticity_token'})['value']
response = session.post(url, data=login_data, headers=headers)
#print(response.status_code)
response = session.get('https://github.com', headers=headers)
#print(response.text)

contador = 0
for full_path, link in github_links.items():
	#print(link)
	#print(f"{link}/archive/master.zip")
	response = session.get(f"{link}/archive/master.zip", allow_redirects=True)
	#print(response.status_code)
	if (response.status_code==200):
		open(f'{full_path}master_project.zip', 'wb').write(response.content)
		print(f"file {contador+1} downloaded")
		contador+=1
