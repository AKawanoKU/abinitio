#!/usr/bin/python
import sys,subprocess
# curl version
list = ['' for i in range(10000)]
list_file = 'cod_list.txt' # cod_ist, change here
try: # text file open
	fin = open(list_file,'r')
except IOError, (errno, msg): # file not found
	print list_file + ' is missing.'
	exit()
contents = fin.readlines() # read all lines in cif file to contents
fin.close() # close file

print "Search by 1:mineral; 2:formula; Other: exit"
input_no = input('>>> ')
if (input_no != 1) and (input_no != 2):
	exit()
if input_no == 1:
	while True: # exit by input
		print "Provide mineral name for search. (0 to stop)"
		input_mineral = raw_input('>>> ')
		if input_mineral == '0':
			exit()
		# check input
		find = 0
		for line in contents: # simple search
			tmp = line.strip()
			# list contents... 1:cif f.name, 2:formula, 3:H-M, 4:cheminfo, 5:mineral
			llist = tmp.split(",")
			check = llist[4]
			if input_mineral in check:
				find = find + 1
				list[find] = llist[0]
				print str(find) + ':' + llist[4] + '  ' + llist[1] + '  ' + llist[2] + '  ' + llist[3]
		if find > 0:
			print "Select by number? (0 to skip)"
			input_no = input('>>> ')
			if (input_no <= 0) or (input_no > find):
				pass
			else:
				fname = list[input_no]
				cmd = "curl -s -o" + " " + fname + " " + "http://www.crystallography.net/cod/" + fname
				subprocess.call(cmd.split(" ")) # Get specified cif file from the COD site by curl   
				cmd = "open -a VESTA" + " " + fname
				subprocess.call(cmd.split(" ")) # open VESTA using a downloaded cif file  
		else:
			print "Not found!"			
if input_no == 2:
	while True: # exit by input
		print "Provide elements for search (0 to stop)"
		print "Example: O4 Mg2 Si"
		input_formula = raw_input('>>> ')
		if input_formula == '0':
			exit()
		chem_list = input_formula.split(' ')
		n = len(chem_list)
		# check input
		find = 0
		for line in contents: # simple search
			tmp = line.strip()
			# line contents... 1:cif f.name, 2:formula, 3:H-M, 4:cheminfo, 5:mineral
			llist = tmp.split(",")
			clist = llist[1].split(' ')
			point = 0
			for i in range(1,n+1):
				if chem_list[i-1] in clist:
					point = point + 1
#			if (point == n) and (len(clist) == n): # exact match
			if point == n: # not exact match (including, not identical)
				find = find + 1
				list[find] = llist[0]
				print str(find) + ':' + llist[1] + '  ' + llist[4] + '  ' + llist[2] + '  ' + llist[3]
		if find > 0:
			print "Select by number? (0 to skip)"
			input_no = input('>>> ')
			if (input_no <= 0) or (input_no > find):
				pass
			else:
				fname = list[input_no]
				cmd = "curl -s -o" + " " + fname + " " + "http://www.crystallography.net/cod/" + fname
				subprocess.call(cmd.split(" ")) # Get specified cif file from the COD site by curl   
				cmd = "open -a VESTA" + " " + fname
				subprocess.call(cmd.split(" ")) # open VESTA using a downloaded cif file  
		else:
			print "Not found!"

# for local file
# base = '/Users/masami/cod/cif/' # cif base directory, change here
#dir = base + fname[0] + '/' + fname[1:3] + '/' + fname[3:5] + '/' + fname
#cmd = "open -a VESTA " + dir
#subprocess.call(cmd.split(" ")) # open VESTA using a specified cif file  
