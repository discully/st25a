from pathlib import Path
from argparse import ArgumentParser
from json import JSONEncoder,dump
from ST25A import Animation,Data,Image,Index


def exportImage(args, name, img):
	print(name)
	if args.scale:
		scaleImage(img)
	output_path = args.output.joinpath(name)
	img["image"].export(output_path)


def scaleImage(image, scale=4):
	img0 = image["image"]
	img1 = Image.Image(img0.width * scale, img0.height * scale)
	for x0 in range(img0.width):
		for y0 in range(img0.height):
			for sx in range(scale):
				for sy in range(scale):
					x1 = x0*scale + sx
					y1 = y0*scale + sy
					img1.set(img0[x0][y0], x1, y1)
	image["image"] = img1


def exportPalette(args, entry):
	palette = Image.readPAL(args.dir, entry)
	# palette has 256 colours, image is 640x480px
	# draw 16x16 squares, each 40x30px
	image = Image.Image(640,480)
	for i,colour in enumerate(palette):
		row = i % 16
		col = i // 16
		for dx in range(40):
			for dy in range(30):
				x = (row * 40) + dx
				y = (col * 30) + dy
				image.set(colour, x, y)
	output_name = entry["name"] + ".png"
	image.export(args.dir.joinpath(output_name))


def exportText(args, entry):
	data = Index.getData(args.dir, entry)
	data = [chr(x) for x in data]
	text = "".join(data)
	text = text.replace("\0", "\n")
	text = text.replace("\r", "")
	
	path = args.output.joinpath("{}.txt".format(entry["name"]))
	print(path.name)
	f = open(path, "w")
	f.write(text)
	f.close()


class Encoder (JSONEncoder):
	def default(self, obj):
		#if isinstance(obj, Enum):
		#	return obj.name
		if isinstance(obj, Image.Image):
			return str(obj)
		# Let the base class default method raise the TypeError
		return JSONEncoder.default(self, obj)


def exportJson(args, entry, data):
	output_path = args.output.joinpath(entry["name"] + ".json")
	print(output_path.name)
	dump(data, open(output_path, "w"), indent="\t", cls=Encoder)


def exportFile(args, entry):
	
	ext = entry["name"].split(".")[1]

	if ext == "ANM":
		animation = Animation.readAnimation(args.dir, entry)
		for image_name,image in animation["images"].items():
			output_name = "{}.{}.png".format(entry["name"], image_name)
			exportImage(args, output_name, image)
		exportJson(args, entry, animation)
	elif ext == "BMP":
		bmp = Image.readBitmap(args.dir, entry)
		exportImage(args, entry["name"] + ".png", bmp)
	elif ext == "DB":
		db = Data.readDB(args.dir, entry)
		exportJson(args, entry, db)
	elif ext == "KEY":
		key = Data.readDBKey(args.dir, entry)
		exportJson(args, entry, key)
	elif ext == "PAL":
		exportPalette(args, entry)
	elif ext == "TXT":
		Data.readTXT(args.dir, entry)
		#exportText(args, entry)
	else:
		print("Unsupported file type: {}".format(ext))


def main():
	parser = ArgumentParser()
	parser.add_argument("-d", "--dir", type=Path, required=True, help="Path of directory of game install")
	parser.add_argument("-f", "--file", type=str, required=True, help="Name of file to be extracted")
	parser.add_argument("-o", "--output", type=Path, default=Path("."), help="Path of directory output will be saved to")
	parser.add_argument("-s", "--scale", action="store_true", help="If file is an image, will increase the size")
	args = parser.parse_args()

	entry = Index.getEntry(args.dir, args.file.upper())

	exportFile(args, entry)


if __name__ == "__main__":
	main()
