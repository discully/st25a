from ST25A.File import File,DataFile
from ST25A.LZSS import decode


def _dirFile(dir):
	return File( dir.joinpath("DATA.DIR") )


def _runFile(dir):
	return File( dir.joinpath("DATA.RUN") )


def _dataFile(dir):
	return File( dir.joinpath("DATA.001") )


def _readRunOffsets(f, offset, count):
	f.setPosition(offset)
	offsets = []
	for i in range(count):
		if i == 0:
			x = [f.readUInt8() for i in range(3)]
			offsets.append( x[0] + (x[1] << 8) + (x[2] << 16) )
		else:
			offsets.append( offsets[-1] + f.readUInt16())
	return offsets


def _readDirEntry(f):
	offset = f.pos()
	base = f.readStringBuffer(8)
	ext = f.readStringBuffer(3)
	x = [f.readUInt8() for i in range(3)]

	if x[2] & 0x80:
		count = x[2] & 0x7F
		addr = x[0] + (x[1] << 8)
	else:
		count = 1
		addr = x[0] + (x[1] << 8) + (x[2] << 16)

	assert(count > 0 and count <= 10)

	return {
		"offset": offset,
		"name": "{}.{}".format(base, ext),
		"entries": [],
		"_count": count,
		"_addr": addr
	}


def get(dir):
	f_index = _dirFile(dir)
	f_run = _runFile(dir)
	index = []
	while not f_index.eof():
		entry = _readDirEntry(f_index)
		if entry["_count"] == 1:
			entry["entries"].append({
				"name": entry["name"],
				"offset": entry["_addr"],
			})
		else:
			base,ext = entry["name"].split(".")
			offsets = _readRunOffsets(f_run, entry["_addr"], entry["_count"])
			for i,offset in enumerate(offsets):
				entry["entries"].append({
					"name": "{}{}.{}".format(base[:-1], i, ext),
					"offset": offset,
				})
		entry.pop("_count")
		entry.pop("_addr")
		index.append(entry)
	return index


def names(dir):
	full_index = get(dir)
	name_index = {}
	for entry in full_index:
		for subentry in entry["entries"]:
			name_index[subentry["name"]] = subentry
	return name_index
	

def getEntry(dir, name, number=None):
	index = names(dir)
	if number is None:
		if name in index:
			return index[name]
	if not number is None:
		base,ext = name.split(".")
		number_name = "{}{}.{}".format(base[:-1], number, ext)
		if number_name in index:
			return index[number_name]
		raise ValueError("Could not find {}[{}] = {} in index".format(name, number, number_name))
	if name in index:
		return index[name]
	raise ValueError("Could not find {} in index".format(name))


def getData(dir, entry):
	f = _dataFile(dir)
	f.setPosition(entry["offset"])
	size_uncompressed = f.readUInt16()
	size_compressed = f.readUInt16()
	return decode(f, size_compressed, size_uncompressed)


def getDataFile(dir, entry):
	data = getData(dir, entry)
	return DataFile(data)
