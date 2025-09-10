
def decode(indata, compressedSize, uncompressedSize):
	end = indata.pos() + compressedSize
	N = 0x1000
	histbuff = [0] * N
	outstreampos = 0
	bufpos = 0
	outLzssBufData = [0] * uncompressedSize

	while True:
		flagbyte = indata.readUInt8()

		if indata.pos() >= end:
			break

		for i in range(8):
			if (flagbyte & (1 << i)) == 0:
				offsetlen = indata.readUInt16()
				if indata.pos() == end:
					break

				length = (offsetlen & 0xF) + 3
				offset = (bufpos - (offsetlen >> 4)) & (N-1)
				for j in range(length):
					tempa = histbuff[(offset + j) & (N-1)]
					outLzssBufData[outstreampos] = tempa
					outstreampos += 1
					histbuff[bufpos] = tempa
					bufpos = (bufpos + 1) & (N - 1)
			
			else:
				tempa = indata.readUInt8()

				if indata.pos() >= end:
					break

				outLzssBufData[outstreampos] = tempa
				outstreampos += 1
				histbuff[bufpos] = tempa
				bufpos = (bufpos + 1) & (N - 1)
	
	return outLzssBufData
