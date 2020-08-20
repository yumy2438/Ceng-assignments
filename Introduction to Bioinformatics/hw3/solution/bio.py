
from math import sqrt
basepath = "pdbfiles/"
filename = "6lac.pdb"

def distanceOkay(x1,x2,y1,y2,z1,z2):
	distance = sqrt((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)
	return (distance < 8.0)

chain1 = []
chain2 = []
with open(basepath+filename,"r") as file:
	line = file.readline()
	while(line):
		if(len(line)>4):
			if(line[0]=="A" and line[1]=="T" and line[2]=="O" and line[3]=="M"):
				atomname = line[12:16].strip()
				aa = line[17:20].strip()
				chainID = line[21]
				resSeq = line[22:26].strip()#aa name(resseq)
				x = float(line[30:38].strip())
				y = float(line[38:46].strip())
				z = float(line[46:54].strip())
				if(aa == "GLY" and atomname == "CA"):
					if(chainID == "A"):
						chain1.append((atomname,aa,resSeq,x,y,z))
					else:
						chain2.append((atomname,aa,resSeq,x,y,z))
				elif(atomname == "CB"):
					if(chainID == "A"):
						chain1.append((atomname,aa,resSeq,x,y,z))
					else:
						chain2.append((atomname,aa,resSeq,x,y,z))
		line = file.readline()
# interacted ids hold the id of the interacted ones. as like: first in chain1 second in chain2
interactedids = []
c0 = 0
for aa1 in chain1:
	(_,_,_,x1,y1,z1) = aa1
	c1 = 0
	for aa2 in chain2:
		(_,_,_,x2,y2,z2) = aa2
		if(distanceOkay(x1,x2,y1,y2,z1,z2)):
			interactedids.append((c0,c1))
		c1+=1
	c0+=1
print("There are " + str(len(interactedids)) + " interacting pairs.")
counter1 = 0
groups = []
for (c1_1,c2_1) in interactedids:
	(c1_atomname1,c1_aa1,c1_resSeq1,c1_x1,c1_y1,c1_z1) = chain1[c1_1]
	(c2_atomname1,c2_aa1,c2_resSeq1,c2_x1,c2_y1,c2_z1) = chain2[c2_1]
	counter2 = counter1+1
	for (c1_2,c2_2) in interactedids[counter2:]:
		(c1_atomname2,c1_aa2,c1_resSeq2,c1_x2,c1_y2,c1_z2) = chain1[c1_2]
		(c2_atomname2,c2_aa2,c2_resSeq2,c2_x2,c2_y2,c2_z2) = chain2[c2_2]
		if(distanceOkay(c1_x1,c1_x2,c1_y1,c1_y2,c1_z1,c1_z2) 
			or distanceOkay(c1_x1,c2_x2,c1_y1,c2_y2,c1_z1,c2_z2) 
			or distanceOkay(c1_x2,c2_x1,c1_y2,c2_y1,c1_z2,c2_z1)
			or distanceOkay(c2_x1,c2_x2,c2_y1,c2_y2,c2_z1,c2_z2)):
			isAppended = False
			for groupcounter in range(len(groups)):
				if counter1 in groups[groupcounter] and (not counter2 in groups[groupcounter]):
					isAppended = True
					groups[groupcounter] = groups[groupcounter] + (counter2,)
				elif counter2 in groups[groupcounter] and (not counter1 in groups[groupcounter]):
					isAppended = True
					groups[groupcounter] = groups[groupcounter] + (counter1,)
				elif counter1 in groups[groupcounter] and counter2 in groups[groupcounter]:
					isAppended = True
			if(not isAppended):
				groups.append((counter1,counter2,))
		counter2+=1
	counter1+=1
	if(counter1 == len(interactedids)):
		break
# rearrange it for duplicates
def indexesOfBelongedTo(g):
	c = 0
	indexes = []
	for group in groups:
		if g in group:
			indexes.append(c)
		c+=1
	return indexes

def addIfNotExist(index,original):
	group = groups[index]
	for g in group:
		if(not g in groups[original]):
			groups[original] = groups[original] + (g,) 
for group in groups:
	for g in group:
		indexes = indexesOfBelongedTo(g)
		if(len(indexes) == 1):
			continue
		else:
			original = indexes[0]
			for index in indexes[1:]:
				addIfNotExist(index,original)
				del groups[index]

def isInAnyGroup(counter):
	for group in groups:
		if counter in group:
			return True
	return False

for counter in range(len(interactedids)):
	if not isInAnyGroup(counter): 
		groups.append((counter,))

groupID = 1
for group in groups:
	for g in group:
		(c1,c2) = interactedids[g]
		(_,aa1,resSeq1,_,_,_) = chain1[c1]
		(_,aa2,resSeq2,_,_,_)= chain2[c2]
		print("Group "+str(groupID)+": "+ aa1 + "(" + resSeq1 + ")" + "-" + aa2 + "(" + resSeq2 + ")")
	groupID+=1
print("Number of groups = "+str(len(groups)))



