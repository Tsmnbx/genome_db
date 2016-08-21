list_file = open("list", 'r')

list_array = list_file.readlines()

for item in list_array:
    item = item.strip()
    print (item)

a = "GCA_001693595.1_ASM169359v1"

if any(a in y for y in list_array):
    print ("fuck ya")
