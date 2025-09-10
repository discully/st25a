from argparse import ArgumentParser
from pathlib import Path
from struct import pack
from ST25A import Index


def dump(args, entry):
	data = Index.getData(args.dir, entry)
	output_path = args.output.joinpath(entry["name"])
	output_file = open(output_path, "wb")
	for i in data:
		output_file.write(pack("B", i))
	output_file.close()


def main():
	parser = ArgumentParser()
	parser.add_argument("-d", "--dir", type=Path, required=True, help="Path of directory of game install")
	parser.add_argument("-f", "--file", type=str, required=True, help="Name of file to be extracted")
	parser.add_argument("-o", "--output", type=str, default=Path("."), help="Path of directory output will be saved to")
	args = parser.parse_args()

	entry = Index.getEntry(args.dir, args.file.upper())
	print(entry["name"])
	dump(args, entry)


if __name__ == "__main__":
	main()
