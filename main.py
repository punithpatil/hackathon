import sys
import os
import link_extractor
import summary

def main():
	
	print("Enter search query")
	query = raw_input()
	q = link_extractor.main(query)
	print "HTML data extracted"
	summary.main(query)

if __name__ == '__main__':
	main()
