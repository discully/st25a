from argparse import ArgumentParser
from pathlib import Path
from ST25A import Index


def printEntry(entry):
	print(entry["name"])
	if len(entry["entries"]) > 1:
		for subentry in entry["entries"]:
			printSubentry(subentry)


def printSubentry(subentry):
	print(" |- {:<12}    {}".format(subentry["name"], subentry["offset"]))


def main():
	parser = ArgumentParser()
	parser.add_argument("-d", "--dir", required=True, type=Path, help="Path to directory of game install")
	parser.add_argument("-s", "--search", required=False,type=str, help="String to match file names against. Prints all entries if not used.")
	args = parser.parse_args()

	if args.search is None:
		index = Index.get(args.dir)
		for entry in index:
			printEntry(entry)
	else:
		search = args.search.upper()
		names = Index.names(args.dir)
		for name in names:
			if name.find(search) != -1:
				printSubentry(names[name])


if __name__ == "__main__":
	main()
