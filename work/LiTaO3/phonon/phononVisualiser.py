import numpy as np
import os
import copy

#edfname = 'phonon5.out' # File name which includes eigen displacements
#vestafname = 'LiTaO3_mp-3666_primitive.vesta'
#phfname = 'trf2_1.out'
print('Name of the vesta file like "LiTaO3_mp-3666_primitive.vesta"')
vestafname = raw_input('>> ')

print('Name of the output file of phonon calculation like "phonon.out"')
phfname = raw_input('>> ')

print('Name of the file including eigen displacements like "phonon5.out"')
edfname = raw_input('>> ')

f1 = open(edfname)
eddata = f1.readlines()
f1.close()

f2 = open(vestafname)
vestadata = f2.readlines()
f2.close()

f3 = open(phfname)
phdata = f3.readlines()
f3.close()

print('Type the number of atoms in the primitive cell')
atomNum = int(raw_input('>> '))

for line in vestadata:
    vestaLineNums = [i for i, line in enumerate(vestadata) if 'STRUC' in line]

vestaLineNum = vestaLineNums[0] + 1

atomListVesta = [[float(vestadata[vestaLineNum + 2*i].split()[4]), float(vestadata[vestaLineNum + 2*i].split()[5]), float(vestadata[vestaLineNum + 2*i].split()[6])] for i in range(atomNum)]

for line in phdata:
    phLineNums = [i for i, line in enumerate(phdata) if 'xred' in line]

phLineNum = phLineNums[0] + 1

atomListPh = [[float(phdata[phLineNum + i].split()[0]), float(phdata[phLineNum + i].split()[1]), float(phdata[phLineNum + i].split()[2])] for i in range(atomNum - 1)]
xred0 = [float(phdata[phLineNums[0]].split()[i+1]) for i in range(3)]
atomListPh.insert(0, xred0)

phToVesta = []
for i in range(atomNum):
    phAtom = atomListPh[i]
    for j in range(atomNum):
        vestaAtom = atomListVesta[j]
        if phAtom == vestaAtom:
            phToVesta.append(j)
            break

for line in phdata:
    RecipLineNums = [i for i, line in enumerate(phdata) if 'Recip(G)' in line]

RecipLineNum = RecipLineNums[0] + 1

RecipVecList = [[float(phdata[RecipLineNum + i].split()[5]), float(phdata[RecipLineNum + i].split()[6]), float(phdata[RecipLineNum + i].split()[7])] for i in range(3)]
RecipVecNp = np.array(RecipVecList)

print('Which modes? Type mode numbers(>3) like >> 7 8 10')
modeNumsIn = raw_input('>> ')

modeNums = modeNumsIn.split(" ")

for k in range(len(modeNums)):
    modeNum = modeNums[k]
    
    for line in eddata:
        phLineNums = [i for i, line in enumerate(eddata) if 'Phonon frequencies in cm-1' in line] 

    phLineNum = phLineNums[0] + 1
    phLineNum = phLineNum + ((int(modeNum)-1) // 5)
    phFreq = float(eddata[phLineNum].split()[((int(modeNum)-1) % 5) +1])

    print('Making ' + modeNum + '_mode(' + str(phFreq) + ' cm^-1)_' + vestafname + '...')
    
    for line in eddata:
        lineNums = [i for i, line in enumerate(eddata) if 'Mode number' in line and ' '+modeNum+' ' in line] 

    lineNum = lineNums[0] + 1
    edList = [[float(eddata[lineNum + 2*i].split()[2]), float(eddata[lineNum + 2*i].split()[3]), float(eddata[lineNum + 2*i].split()[4])] for i in range(atomNum)] 

    edListToVesta = [[] for i in range(atomNum)]
    for i in range(atomNum):
        edListToVesta[phToVesta[i]] = edList[i]

    edListReduced = [RecipVecNp.dot(edListToVesta[i]) for i in range(atomNum)]

    edListOut = [[str(i+1), str(edListReduced[i][0]), str(edListReduced[i][1]), str(edListReduced[i][2]), '1\n'] for i in range(atomNum)]

    for line in vestadata:
        vestaLineNums = [i for i, line in enumerate(vestadata) if 'VECTR' in line]
    vestaLineNum = vestaLineNums[0] + 1

    vestadataOut = copy.deepcopy(vestadata)
    
    for i in range(atomNum):
        vestadataOut.insert(vestaLineNum + 3*i, ' '.join(edListOut[i]))
        vestadataOut.insert(vestaLineNum + 3*i + 1, ' '+str(i+1)+' 0 0 0 0 \n')
        vestadataOut.insert(vestaLineNum + 3*i + 2, ' 0 0 0 0 0 \n')


    for line in vestadataOut:
        vestaLineNums = [i for i, line in enumerate(vestadataOut) if 'VECTT' in line]
    vestaLineNum = vestaLineNums[0] + 1

    for i in range(atomNum):
        vestadataOut.insert(vestaLineNum + i, str(i+1)+' 0.5 255  0 0 0 \n')

    for line in vestadataOut:
        vestaLineNums = [i for i, line in enumerate(vestadataOut) if 'VECTS' in line]
    vestaLineNum = vestaLineNums[0]

    vestadataOut.pop(vestaLineNum)
    vestadataOut.insert(vestaLineNum, 'VECTS 10000 \n')

    outPath = './output_visualise/'
    if not os.path.exists(outPath):
        os.makedirs(outPath)
    with open(outPath + modeNum + '_mode(' + str(phFreq) + ' cm^-1)_' + vestafname, mode='w') as f:
        f.writelines(vestadataOut)

