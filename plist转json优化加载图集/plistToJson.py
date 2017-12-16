
import re
import json
from xml.etree import ElementTree as ET
per=ET.parse('bibirole.plist')
p=per.findall('./dict/dict')
pp = per.findall('./dict/dict/dict');

frame = p[1]
data = p[0]
if len(p[0]) > len(p[1]):
	frame = p[0]
	data  = p[1]

result = {}
frames = []
name = ""
i = 0
for m in frame:
	item = {}
	if m.tag == "key":
		name = m.text
	item['name'] = name
	if m.tag == "dict":
		length = len(pp[i])
		for n in range(length):
			temp = pp[i][n]
			if temp.text == "frame":
				count = n+1
				rtp = pp[i][count]
				v = re.sub('{','',rtp.text)
				v = re.sub('}','',v)
				a = v.split(',')
				rect ={"x":int(a[0]),"y":int(a[1]),"width":int(a[2]),"height":int(a[3])}
				item['rect'] = rect
			if temp.text == "offset":
				count = n+1
				rtp = pp[i][count]
				v = re.sub('{','',rtp.text)
				v = re.sub('}','',v)
				a = v.split(',')
				offset = {"x":int(a[0]),"y":int(a[1])}
				item['offset'] = offset
			if temp.text == "rotated":
				count = n+1
				rtp = pp[i][count]
				rotated = rtp.tag
				item['rotated'] = rotated == 'true'
		frames.append(item)
		i = i+1
print ('--------frames---------')
result['frames'] = frames
print frames
length = len(data)
print 'data.length=> ',length
for m in range(length):
	temp = data[m]
	count = m+1
	if temp.text == 'size':
		rtp = data[count]
		v = re.sub('{','',rtp.text)
		v = re.sub('}','',v)
		a = v.split(',')
		size = {"width":int(a[0]),"height":int(a[1])}
		result['sourceSize'] = size
print result

fo = open("bibirole.json", "wt")
jsonStr = json.dumps(result)
fo.write(jsonStr)