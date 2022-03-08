from bs4 import BeautifulSoup
import sys
import requests
import jieba

def translate(argv):

	hex_q = (repr(argv[0].encode('utf-8'))[2:-1].replace("\\","%").replace("x","").upper())
	url = f'https://www.youdao.com/result?word={hex_q}&lang=en'
	print(url)
	result = requests.get(url)
	a = (BeautifulSoup(result.content,"html5lib"))
	b = [div.get_text() for div in a.find_all('div') if len(div.find_all('b')) > 0 and len(div.find_all('div')) == 0]
	for i in range(len(b)):
		c = b[i]
		if len(c.split("\xa0")) == 1:
			c = jieba.lcut(c)
		else: 
			c = c.split("\xa0")[1]
			c = c.split([char for char in c if char > u'\u4e00' and char <u'\u9fff'][0])[0]
		print(c)


def add_to_anki(translation,examples):
	data = {}
	data["action"] = "addNote"
	data["version"] = 6
	params = {}
	note = {}
	params["note"] = note
	note["deckName"] = "中文"
	note["modelName"] = "Basic (and reversed card) with pin yin"
	data["params"] = "Basic"
	data["action"] = "addNote"
	data["action"] = "addNote"
	data["action"] = "addNote"
	data["action"] = "addNote"
	data["action"] = "addNote"
	data["action"] = "addNote"
	

if __name__ == '__main__':
	translate(sys.argv[1:])

