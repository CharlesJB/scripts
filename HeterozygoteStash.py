#!/usr/bin/env python
# encoding: utf-8

"""
usage:

HeterozygoteStash.py phasedData

phasedData: phased data file from hapmap.
Note: script is for gene on chromosome 4

"""

class HeterozygoteStash:
	def __init__(self):
		self.clear()

	def clear(self):
		self.individuals = []
		self.rsList = []
		self.positionList = []
	
	def printAll(self):
		for i in range(0, len(self.individuals)):
			bedname = self.individuals[i] + ".bed"
			bed = open(bedname, 'a')
			filename = open(self.individuals[i], 'a')
			for j in range(0, len(self.rsList[i])):
				bed.write("chr4\t")
				pos = int(self.positionList[i][j]) + 1
				bed.write(str(pos) + '\t')
				bed.write(str(pos + 1) + '\n')
				filename.write(self.rsList[i][j] + '\n')

	def addEntry(self, name):
		self.individuals.append(name)
		self.rsList.append([])
		self.positionList.append([])

	def addRS(self, index, name):
		self.rsList[index].append(name)

	def addPosition(self, index, position):
		self.positionList[index].append(position)

	def getName(self, position):
		return self.individuals[position]

class Parser:
	def __init__(self):
		self.clear()
		self.firstLine = False

	def clear(self):
		self.heterozygoteStash = HeterozygoteStash()
		self.count = 0

	def parseHeader(self, header):
		tokens = header.split()
		for i in range(2, len(tokens)):
			if i % 2 == 0:
				name = tokens[i][:-2]
				self.heterozygoteStash.addEntry(name)

	def parseRS(self, line):
		tokens=line.split()
		rsNumber=tokens[0]
		position=tokens[1]
		for i in range(2, len(tokens)-1):
			if i % 2 == 0:
				allele1 = tokens[i]
			else:
				allele2 = tokens[i]
				if allele1 != allele2:
#					print "parseRS: i:" + str(i)
					print "allele1: " + allele1
					print "allele2: " + allele2
					index = ((i-1)/2)-1
					self.heterozygoteStash.addRS(index, rsNumber)
					self.heterozygoteStash.addPosition(index, position)

	def parseFile(self, filename):
		for line in open(filename):
			if self.firstLine == False:
				self.parseHeader(line)
				self.firstLine = True
			else:
				self.parseRS(line)

#			self.count = self.count + 1
#			if self.count == 1000:
#				self.printAll()
#				self.clear()

	def printAll(self):
		self.heterozygoteStash.printAll()
				

import sys

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print __doc__
		sys.exit(1)

	parser = Parser()

	filename = sys.argv[1]

	parser.parseFile(filename)
	parser.printAll()
