# CSV to SQL Insert Program
#
# a program to convert a csv data file into sql insert statements. This requires the csv file to be prepared to contain the same headers
# as the columns they will be entered into in their respective sql table.
# 
# Arguments:
#   - path to csv file
#   - [-t]  -> sql table name
#   - [-ch] -> column headers (as many as you want) NOTE: Headers cannot start with '-'
#
# Optional Arguments:
#   - [-o]  -> output file name
#   - [-sh] -> sql headers. if headers from csv to sql arent consistant
#              this use this list of headers for the sql output 


import sys, csv;

# Validate command line arguments
def validateArguments(args):

	if(args['in_fn'][-4:] != '.csv' and args['in_fn'][-4:] != '.CSV'):
		print("Invalid input filename. Must end in '.csv' or '.CSV'.");
		return False;

	# Output filename validation
	if 'out_fn' in args:
		if(args['out_fn'][-4:] != '.sql' and args['out_fn'][-4:] != '.SQL'):
			print("Invalid output filename. Must end in '.sql' or '.SQL'.");
			return False;

	# Table name validation
	if 'table' not in args:
		print("Invalid arguments. No table name provided.");
		return False;
	else:
		if(args['table'] == ""):
			print("Invalid arguments. Empty table name provided.");
			return False;

	# csv header validation
	if 'csv_headers' not in args:
		print("Invalid arguments. No CSV headers provided.");
		return False;

	# sql header validation
	if 'sql_headers' in args:
		if(len(args['csv_headers']) != len(args['sql_headers'])):
			print(args['csv_headers']);
			print(args['sql_headers']);

			print("Invalid arguments. Number of input headers is not equal to number of output headers.");
			return False;


	return True;

# Parse column headers from cmd line arguments
def parseArguments(args):

	params = {};

	params['in_fn'] = args[1];

	for i in range(0,len(args)):
		if(args[i] == "-o"):
			params['out_fn'] = args[i+1];
		elif(args[i] == '-t'):
			params['table'] = args[i+1];
		elif(args[i] == '-ch'):
			j = 1;
			csv_head_arr = [];
			csv_cur_arg = args[i+j];
			while(csv_cur_arg[0] != '-'):
				csv_head_arr.append(csv_cur_arg);
				j += 1;
				csv_cur_arg = args[i+j];
			params['csv_headers'] = csv_head_arr;
		elif(args[i] == '-sh'):
			k = 1;
			sql_head_arr = [];
			sql_cur_arg = args[i+k];
			while(sql_cur_arg[0] != '-'):
				sql_head_arr.append(sql_cur_arg);
				k += 1;
				if(i + k < len(args)):
					sql_cur_arg = args[i+k];
				else:
					break;
			params['sql_headers'] = sql_head_arr;

	return params;

# Match headers from arguments to headers from csv
def getHeaderIndexFromCSV(csv, headers):
	indecies = [];

	for i in range(0, len(headers)):
		indecies.append(-1);

	for i in range(0, len(csv[0])):
		if csv[0][i] in headers:
			cur_header = csv[0][i];
			ind = headers.index(cur_header)
			indecies[ind] = i;

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
def testArgPrint(csv, sql, table, headers, sql_headers, ind):
	header_str     = "";
	ind_str        = "";
	sql_header_str = "";

	for h in headers:
		header_str += str(h) + ", ";

	for i in ind:
		ind_str += str(i) + ", ";

	for sh in sql_headers:
		sql_header_str += str(sh) + ", ";

	print("CSV: "+ str(csv));
	print("SQL: "+ str(sql));
	print("Table: "+ str(table));
	print("Indecies: "+ str(ind_str));
	print("CSV Headers: " + str(header_str));
	print("SQL Headers: "+ str(sql_header_str));


# Test Main
def testMain(args):

	params = parseArguments(args);

	if not validateArguments(params): return;
	
	is_sql_headers = False;
	is_out_file    = False;

	csv_filename = params['in_fn'];
	table_name   = params['table'];
	csv_headers  = params['csv_headers'];
	sql_filename = "";
	sql_headers  = [];


	if 'out_fn' in params:
		is_out_file = True;
		sql_filename = params['out_fn'];
	if 'sql_headers' in params:
		is_sql_headers = True;
		sql_headers = params['sql_headers'];

	csv = importCSV(csv_filename);

	indecies = getHeaderIndexFromCSV(csv, csv_headers);

	if(len(indecies) == 0):
		print("No column headers match csv headers");
		return;

	sql_content = "";

	if is_sql_headers:
		sql_content = createSQL(csv, table_name, indecies, sql_headers);
	else:
		sql_content = createSQL(csv, table_name, indecies, csv_headers);

	print(sql_content);

	testArgPrint(csv_filename, sql_filename, table_name, csv_headers, sql_headers, indecies);



	



testMain(sys.argv);