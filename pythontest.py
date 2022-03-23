from ast import Str
import time 

# named_tuple = time.localtime() # get struct_time
# time_string = time.strftime("%Y-%m-%d-%H-%M-%S", named_tuple)

# filename = time_string+".txt"
# print(filename)
# folder = "scrapedJsons\\"
# f = open(folder + "manylines.txt", "a")
# f.write("file opened and written in \n")
# f.close()

# from datetime import datetime, timedelta 
# # print(datetime.now())
# time_str = "2020-01-01 22:00:00"
# format_str = "%Y-%m-%d %H:%M:%S"
# datetime_obj = datetime.strptime(time_str, format_str)
# print((datetime_obj + timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"))
# print(datetime_obj)
# #remaking into string
# str_time = datetime.strftime(datetime_obj, format_str)
# print(type(str_time))

a = "apples "
b = "oranges"
print(a + b)