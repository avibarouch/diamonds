import csv
import sys
csv_file = "data/diamonds.csv"


# This is a test of te existence of a file
# Get a name and relativ path to the file
# Return 1 if the file was found
def file_exist_test(file):
    try:
        print("Try to find a csv file")
        open(csv_file)
    except OSError as err:
        print("OS error: {0}: Pleas check if the csv file exist".format(err))
    else:
        print("The file is founded")
        return +1


# This is the *main* part.
# The wanted result is a string like this one:
#
#   "INSERT INTO `diamonds` "
#   "(`carat`, `cut`, `color`, `clarity`,"
#   " `depth`, `table1 `, `x`, `y`, `z`) "
#   "VALUES (4.2, 'Good', 'D', 'IF', 4.2,"
#   " 3.87, 2.4, 4.54, 7.87)")
i = 0
with open(csv_file, newline='') as file:
    diamond_reader = csv.reader(file)
    for line in diamond_reader:
        if i >= 1:
            v = line  # For values
            sql = "INSERT INTO `diamonds` (`num`,`carat`,`cut`,`color`,`clarity`,`depth`,`table1`,`price`,`x`,`y`,`z`)"
            sql += " VALUES (`{}`,`{}`,`{}`,`{}`,`{}`, `{}`,`{}`,`{}`,`{}`,`{}`,`{}`)".format(v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7], v[8], v[9], v[10])
            print(sql)
        i += 1
