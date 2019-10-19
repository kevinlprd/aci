import sys
filename = 'port_list.txt'
infile = open(filename, 'r')
infile.readline() # skip the first line
#epg = []
#path = []
#port = []
for line in infile:
    words = line.split()
     # words[0]: epg, words[1]: path, works[2]: port
    epg=(words[0])
    path=(words[1])
    port=(words[2])
    print(epg)
    print(path)
    print(port)
infile.close()
