from PIL import Image as PIL_Image
from ST25A import Data,Index


_TRANSPARENT = (1,1,1)

_PALETTES = {
	"BRIDGE.BMP": "BRIDGE.PAL",
	"GOLDLOGO.BMP": "GOLD.PAL",
}


class Image:
	
	def __init__(self, width, height):
		self.blank = _TRANSPARENT
		self.width = width
		self.height = height
		self.pixels = [ [self.blank for x in range(height)] for x in range(width) ]
		self.name = None
	
	
	def __getitem__(self, x):
		if( x < 0 or x >= self.width ):
			raise IndexError( "Image x-index {0} out of range [0,{1})".format(x, self.width) )
		return self.pixels[x]
	
	
	def __len__(self):
		return self.nPixels()
	
	
	def __str__(self):
		if self.name:
			return self.name
		else:
			return "Image (width={0}, height={1})".format(self.width, self.height)
	
	
	def nPixels(self):
		return self.width * self.height
	
	
	def set(self, colour, coord1, coord2 = None):
		
		if( coord2 == None ):
			if( coord1 >= len(self) ):
				raise IndexError( "Attempt to set nth pixel {0} which is out of range (0,{1}]".format( coord1, len(self) ) )
			x,y = ( coord1%self.width, coord1//self.width )
		else:
			x,y = (coord1,coord2)
		
		if( x < 0 or x >= self.width or y < 0 or y >= self.height ):
			raise IndexError( "Attempt to set pixel {0} which is out of image {1}".format( (x,y), (self.width,self.height) ) )
		
		
		self[x][y] = colour

	
	def export(self, name):
		class PILImage:
			
			def __init__(self, img):
				
				self.transparent = img.blank
				
				self.image = PIL_Image.new("RGBA", (img.width, img.height))
				self.pixels = self.image.load()
				
				for x in range(img.width):
					for y in range(img.height):
						self.set(x, y, img[x][y])
			
			def get(self, row, column):
				return self.pixels[row, column]
			
			def save(self, file_name):
				self.image.save(file_name, "PNG")
			
			def set(self, row, column, colour):
				if len(colour) == 3:
					if colour == self.transparent:
						colour = (0, 0, 0, 0)
					else:
						colour = (colour[0], colour[1], colour[2], 255)  # convert rgb to rgba
				elif len(colour) != 4:
					raise ValueError("Invalid colour: {0}".format(colour))
				
				self.pixels[row, column] = colour
		
		png_image = PILImage(self)
		png_image.save(name)


def readBMP(dir, entry):
	data = Index.getDataFile(dir, entry)
	x_offset = data.readUInt16()
	y_offset = data.readUInt16()
	width = data.readUInt16()
	height = data.readUInt16()
	raw_image = [[0 for y in range(0xff)] for x in range(width)]
	for y in range(height):
		for x in range(width):
			raw_image[x][y] = data.readUInt8()

	return {
		"name": entry["name"],
		"offset": (x_offset, y_offset),
		"width": width,
		"height": height,
		"raw_image": raw_image,
	}


def _bmpAddImage(bmp, pal):
	image = Image(bmp["width"], bmp["height"])
	for x in range(bmp["width"]):
		for y in range(bmp["height"]):
			image.set(pal[ bmp["raw_image"][x][y] ], x, y)
	bmp["image"] = image
	bmp.pop("raw_image")


def readPAL(dir, entry):
	data = Index.getDataFile(dir, entry)
	pal = []
	while not data.eof():
		r = data.readUInt8() << 2
		g = data.readUInt8() << 2
		b = data.readUInt8() << 2
		if len(pal) == 0:
			pal.append( _TRANSPARENT ) # Ignore first entry, it's supposed to be interpreted as transparent
		else:
			pal.append( (r,g,b) )
	return pal


def readBitmap(dir, entry):
	bmp = readBMP(dir, entry)

	pal_name = _PALETTES.get(entry["name"], "PALETTE.PAL")
	pal_entry = Index.getEntry(dir, pal_name)
	pal = readPAL(dir, pal_entry)

	_bmpAddImage(bmp, pal)

	return bmp
