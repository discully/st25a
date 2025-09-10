from ST25A import Image,Index


KIRK = 'K'
MCCOY = 'M'
SPOCK = 'S'
REDSHIRT = 'R'

_colourShift = {
	KIRK: 8,
	MCCOY: 0,
	SPOCK: 0,
	REDSHIRT: -8,
}

_colourBase = 0xa8


def _bmpApplyShift(bmp, shift, base):
	if shift == 0:
		return
	for x in range(bmp["width"]):
		for y in range(bmp["height"]):
			pixel = bmp["raw_image"][x][y]
			if pixel >= base and pixel < base + 8:
				bmp["raw_image"][x][y] += shift


def _bmpApplyXor(bmp, xor):
	x0,y0 = xor["offset"]
	for x in range(xor["width"]):
		for y in range(xor["height"]):
			bmp["raw_image"][x0+x][y0+y] ^= xor[x][y]


def readXOR(dir, entry):
	data = Index.getDataFile(dir, entry)
	x_offset = data.readUInt8()
	y_offset = data.readUInt8()
	width = data.readUInt8()
	height = data.readUInt8()

	xor = [[0 for y in range(height)] for x in range(width)]
	for y in range(height):
		for x in range(width):
			xor[x][y]= data.readUInt8()
	
	return {
		"offset": (x_offset, y_offset),
		"width": width,
		"height": height,
		"xor": xor,
	}


def readANM(dir, entry):
	data = Index.getDataFile(dir, entry)
	anm = []
	while not data.eof():
		image = data.readStringBuffer(10).rstrip() # There are two 'space' characters at the end for some reason?
		x_offset = data.readUInt16()
		y_offset = data.readUInt16()
		z_value = data.readUInt16()
		frames = data.readUInt16() # Number of frames to show this image for
		next = [data.readUInt8() for i in range(4)] # Choose the next image from one of these at random
		anm.append({
			"image_name": image.upper(),
			"offset": (x_offset, y_offset),
			"z": z_value,
			"frames": frames,
			"next": next,
		})
	return anm


def readAnimation(dir, entry):
	# todo: this is a temporary bodge while migrating from Data to Index
	entry = Index.getEntry(dir, entry["name"])

	animation = {
		"name": entry["name"],
		"entries": readANM(dir, entry),
	}

	animation["images"] = {}
	for image_name in set([a["image_name"] for a in animation["entries"]]):

		xor_entry = None
		try:
			bmp_entry = Index.getEntry(dir, image_name + ".BMP")
		except ValueError:
			xor_entry = Index.getEntry(dir, image_name + ".XOR")
			bmp_entry = Index.getEntry(dir, MCCOY + image_name[1:] + ".BMP")
		
		bmp = Image.readBMP(dir, bmp_entry)

		if not xor_entry is None:
			xor = readXOR(dir, xor_entry)
			_bmpApplyXor(bmp, xor)
			_bmpApplyShift(bmp, _colourShift[image_name[0]], _colourBase)
		
		pal_name = Image._PALETTES.get(bmp_entry["name"], "PALETTE.PAL")
		pal_entry = Index.getEntry(dir, pal_name)
		pal = Image.readPAL(dir, pal_entry)

		Image._bmpAddImage(bmp, pal)

		animation["images"][image_name] = bmp
	
	return animation
