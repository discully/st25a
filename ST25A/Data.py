from ST25A import Index


def readKEY(dir, entry):
	data = Index.getData(dir, entry)
	text = "".join([chr(x) for x in data]).splitlines()
	key = {}
	for txt in text:
		if txt[0] == '$':
			break
		file_name = txt[0:7] + ".DB"
		topic = txt[8:].rstrip()
		key[file_name] = topic
	return key


def readDB(dir, entry):
	text = Index.getData(dir, entry)
	text = "".join([chr(x) for x in text])
	text = text.replace("$\r\0", "")
	text = text.rstrip()
	text = text.split("\r\n")

	title = text[0]
	location = text[1].replace("#", "")
	lines = "\n".join(text[2:])
	
	return {
		"title": title,
		"folder": location,
		"text": lines
	}


def readTXT(dir, entry):
	text = Index.getData(dir, entry)
	text = "".join([chr(x) for x in text])
	text = text.replace("$\r\0", "")
	text = text.rstrip()
	text = text.split("\0")
	#text = text.split("\r\n")
	
	print(text)
	#text = text.replace("\0", "\n")
	#text = text.replace("\r", "")

