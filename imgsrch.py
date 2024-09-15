import requests
import json
import jinja2
from jinja2 import Template
import os
import subprocess

latex_jinja_env = jinja2.Environment(
	block_start_string = '\BLOCK{',
	block_end_string = '}',
	variable_start_string = '\VAR{',
	variable_end_string = '}',
	comment_start_string = '\#{',
	comment_end_string = '}',
	line_statement_prefix = '%%',
	line_comment_prefix = '%#',
	trim_blocks = True,
	autoescape = False,
	loader = jinja2.FileSystemLoader(os.path.abspath('.'))
)
url = 'https://api.unsplash.com/search/photos/?query='
print('Enter a keyword:')
inpt = input()
access = 'client_id=A8ewNFg43RPgI8BaTZZStQiVqX-mxVKwHEt4efs1fr4'
url = url +inpt.rstrip()+'&'+access
r = requests.get(url)
js = json.loads(r.text)
js = js["results"]
counter = 1
ids = list()
for item in js:
    image = requests.get(item["urls"]["regular"])
    file = open("image"+str(counter)+'.png', 'wb')
    file.write(image.content)
    file.close()
    counter+=1
    ids.append(item['id'])

d_ids = dict()
for item in ids:
	url1 = 'https://api.unsplash.com/photos/' + item +'?'+ access
	r1 = requests.get(url1)
	js = json.loads(r1.text)
	if js['exif'] == 'None':
		break
	d_ids[item] = js['exif']

f_list =list()
counter = 1 
for item in d_ids:
	im = 'image' + str(counter)
	f_list.append([im,d_ids[item]['make'],d_ids[item]['model'],d_ids[item]['exposure_time'],d_ids[item]['aperture']])
	counter+=1
template = latex_jinja_env.get_template('imgview.tex')
kinstarva = template.render(data = f_list,inpt =inpt.capitalize())

s = open('final.tex', 'w')
s.write(kinstarva)
s.close()
s = subprocess.Popen(['pdflatex','final.tex'])
