import csv
import sys
FILE_NAME = "data/diamonds.csv"


# This is a test of te existence of the csv file
# Get a name and relativ path to the file
# Return an adress of the csv file That was founded
def file_exist_test(file):
    try:
        print("Try to find a csv file")
        csvfile = open(FILE_NAME)
    except OSError as err:
        print("OS error: {0}: Pleas check if the csv file exist".format(err))
    else:
        print("The file is founded")
        return +1


# Read the first line from the csv file
# Get "IO bufer" and an empty list "key"
# Return the "key" as list of all the headers from th "csv file"
def get_keys(io_buffer, keys):
    csv.reader(io_buffer, delimiter=',')
    head_line = io_buffer.readline().strip("\n")
    head_line = head_line.replace('"', '')
    tup = head_line.split(",")
    tup[0] = "num"
    keys += tup


# Read values from some Line, accept the first one
# Get a Line from CSV file and Values: an empty list
# Change the Values: put values from this Line
def get_values(line, values):
#    line = line.strip("\n")
    line = line.replace('"', '')
    my_list = line.split(",")
    values += my_list


# Help to preper the Keys: names of the colunbs
# Get a CSV file with first line contain the Keys: names of columns,
#   comma seprated (",")
def preper_keys(csv_file, keys):
    io_buffer = open(csv_file)
    get_keys(io_buffer, keys)


# Help to preper the values from the CSV flie
# Get a Strim and Values: empty list
# Goes line by line and pass it to "Get-Values"
def preper_values(s, values):
    for line in s:
        get_values(line, values)


# This is the *main* part.
# The wanted result is a string like this one:
#
#   "INSERT INTO `diamonds` "
#   "(`carat`, `cut`, `color`, `clarity`,"
#   " `depth`, `table1 `, `x`, `y`, `z`) "
#   "VALUES (4.2, 'Good', 'D', 'IF', 4.2,"
#   " 3.87, 2.4, 4.54, 7.87)")


csv_file = FILE_NAME
k = []  # For keyes
v = []  # For values
if file_exist_test(csv_file):
    preper_keys(csv_file, k)
    i = 0
    with open(csv_file, newline='') as file:
        diamond_reader = csv.reader(file, delimiter=' ')
        for line in diamond_reader:
#            get_values(line, v)
            if i > 0:
                print(type(line[0]))
                print("***", i, "***")
                v = line[0].replace('"', '')
                print (v)
                v = v.split(',')
                print(v)
                sql = ("INSERT INTO `diamonds` (`"
                         "{}`,`{}`,`{}`,`{}`,`{}`,`{}`"
                         ",`{}`,`{}`,`{}`,`{}`)"
                         .format(k[0], k[1], k[2], k[3], k[4],
                         k[5], k[6], k[7], k[8], k[9]))
                sql += (" VALUES (`{}`,`{}`,`{}`,`{}`,`{}`,"
                          "`{}`,`{}`,`{}`,`{}`,`{}`)"
                          .format(v[0], v[1], v[2], v[3], v[4],
                          v[5], v[6], v[7], v[8], v[9]))
                print(sql)
            i = i + 1
