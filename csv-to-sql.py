# CSV to SQL Insert Program
#
# a program to convert a csv data file into sql insert statements. This requires the csv file to be prepared to contain the same headers
# as the columns they will be entered into in their respective sql table.
# 
# Arguments:
#   - path to csv file
#   - path to sql export file
#   - sql table name
#   - column headers (as many as you want)
#

import sys, csv;

# Validate command line arguments
def validateArguments(args):
	if(len(args) < 5):
		return False;

	return True;


# Parse column headers from cmd line arguments
def parseColumnHeaders(args):
	headers = [];
	for i in range(4, len(args)):
		headers.append(args[i]);
	return headers;

# Match headers from arguments to headers from csv
def getHeaderIndexFromCSV(csv, headers):
	indecies = [];

	for i in range(0, len(csv[0])):
		if csv[0][i] in headers:
			indecies.append(i);

	return indecies;

# Import CSV
def importCSV(fn):
	with open(fn, 'rb') as f:
	    reader = csv.reader(f);
	    your_list = list(reader);

	return your_list;

# Create SQL
def createSQL(csv, table, indecies, headers):
	# INSERT INTO table (h1, h2, ..., hn) VALUES (v1, v2, ..., vn);

	sql = "";

	# Create the base str
	base_str = "INSERT INTO "+str(table)+" (";
	for i in range(0, len(headers)):
		if(i < len(headers) - 1):
			base_str += str(headers[i]) + ", ";
		else:
			base_str += str(headers[i]) + ") VALUES (";

	# Create sql statements
	cur_str = "";
	for i in range(1, len(csv)):
		cur_str += base_str;
		for j in range(0, len(indecies)):
			if(j < len(indecies) - 1):
				cur_str += "'"+ str(csv[i][indecies[j]]) + "', ";
			else:
				cur_str += "'"+ str(csv[i][indecies[j]]) + "');";
		sql += str(cur_str) + '\n';
		cur_str = "";

	return sql;


# Export SQL

# Test argument print
def testArgPrint(csv, sql, table, headers):
	header_str = "";
	
	for h in headers:
		header_str += str(h) + ", ";

	print("CSV: "+ str(csv));
	print("SQL: "+ str(sql));
	print("Table: "+ str(table));
	print("Headers: " + str(header_str));


# Test Main
def testMain(args):

	if (not validateArguments(args)):
		print("Invalid command line arguments.");
		return;

	csv_filename = args[1];
	sql_filename = args[2];
	table_name   = args[3];
	col_headers  = parseColumnHeaders(args);

	testArgPrint(csv_filename, sql_filename, table_name, col_headers);

	csv = importCSV(csv_filename);

	indecies = getHeaderIndexFromCSV(csv, col_headers);

	if(len(indecies) == 0):
		print("No column headers match csv headers");
		return;

	sql_content = createSQL(csv, table_name, indecies, col_headers);

	print(sql_content);


	



testMain(sys.argv);