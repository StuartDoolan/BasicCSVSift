import sys
#open router file
f = open(sys.argv[1], 'r') 

#read in data from file
filecontents = f.readlines()
f.close()

#remove blank lines (I'm assuming this means empty fields)
#probably not very pythonic way to do it, but does work!
counter = len(filecontents)
i=0
while i<counter:
    if filecontents[i] == ',,,,\r\n':
        filecontents.remove(filecontents[i])
        counter-=1    
    else:
        i+=1

#skip header
filestart = 0
if 'Hostname' in str(filecontents[filestart]):
    filestart += 1

Nentries = len(filecontents)

#initialises nD list for data
routerdata = [[0 for x in range(5)] for y in range(Nentries-1)]

for i in range(Nentries-1):
    thisline = []
    lines = filecontents[filestart+i].split(',')
    for entry in lines:
            thisline.append(entry.strip())
    routerdata[i] = thisline

#transposes matrix
routerdataT=zip(*routerdata)

#name variables, make lowercase to catch duplicates/NOs
Hostname = [x.lower() for x in routerdataT[0]]
IP = list(routerdataT[1])
Patched = [x.lower() for x in routerdataT[2]]
OS = routerdataT[3]

label = ' [invalid] '
#Check IP valid, adapted from stack exchange...
for i in range(Nentries-1):
    #splits IP about dots
    a = IP[i].split('.')
    #if a has more/less than 4 elements, label invalid and skip to next
    if len(a) != 4:
        IP[i] = str(IP[i] + label)
        continue
    for x in a:
        #checks if all elements in a are digits
        if not x.isdigit():
            IP[i] = str(IP[i] + label)
            continue
        #converts to integer and checks elements in a are between 0 and 255
        j = int(x)
        if i < 0 or i > 255:
            IP[i] = str(IP[i] + label)
            continue

##check hostname valid, also adapted from stack exchange...
#just rough check on length and characters as I'm guessing this is an extra
allowed = '0123456789abcdefghijklmnopqrstuvwxyz-'
for i in range(Nentries-1):
    #splits Hostname about dots
    a = Hostname[i].split('.')
    #if Hostname is longer than 255 characters, label invalif
    if len(Hostname[i]) >255:
        Hostname[i] = str(Hostname[i] + label)
        continue
    #checks all characters in Hostname permitted, pretty slow 
    for c in a:
        for d in c:
            
            if  d not in allowed:
                Hostname[i] = str(Hostname[i] + label)
                break
            
        


# initialise list to keep track of non patched
Patchedpass=[]
#test patched
for i in range(Nentries-1):   
    if Patched[i] == 'no':
        Patchedpass.append(i)

##OS Test
OSpass=[]
for i in range(Nentries-1):
    #tests entry can be floated, labels invalid if not
    try:
        float(OS[i])
    except ValueError:
        OS[i].join(label)
        continue
    #If can be floated and is >= 12 then assigned to list
    if float(OS[i]) >= 12:
        OSpass.append(i)

##IP Test
# Checks for duplicate IPs, adds index of non dupes to IPpass
IPpass = []                
for i in range(Nentries-1):
    Test= True
    for j in range(Nentries-1):
        if i == j:
            continue
        elif IP[i]==IP[j]:
            Test = False
            continue
    if Test == True:
        IPpass.append(i)
    
#Hostname test
Hpass=[]
for i in range(Nentries-1):
    Test= True
    for j in range(Nentries-1):
        if i == j:
            continue
        elif Hostname[i]==Hostname[j]:
            Test = False
            continue
    if Test == True:
        Hpass.append(i)

#finds intersection of 'pass' lists using set funtions then sorting
final = sorted(set(range(Nentries-1)).intersection(Hpass, IPpass, OSpass, Patchedpass))

for i in final:
    #jam [] around nonempty Notes entries to be printed
    if routerdata[i][4] != '':
        routerdata[i][4] =' ['+routerdata[i][4]+']'
    print(Hostname[i]+ ' ('+IP[i]+'), OS Version '+ routerdata[i][3] + ' '+routerdata[i][4])
