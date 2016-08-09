__author__ = 'fsiavash'

import sys, getopt
import xml.etree.ElementTree as ET
import random
import os
import os.path
import copy
from copy import deepcopy
import subprocess
from subprocess import call
import re
import shutil


# nameoffile= 'timed-gate.xml'
# tree = ET.parse(nameoffile)
# root = tree.getroot()

# FileNeme = nameoffile[:-4]


 # current path
currpath= os.getcwd()
print currpath
# with open('myverify.txt', 'a') as file:
#     file.write('verifyta -t0 -f tracefile')
# print Address_Invalid_Mut, Address_Valid_Mut

def main(argv):
    inputfile = ''
    templatename = ''
    queryfile = ''
    try:
      opts, args = getopt.getopt(argv,"hi:t:q:",["ifile=","tfile=","qfile="])
    except getopt.GetoptError:
      print 'test.py -i <inputfile> -t <templatename> -q <queryfile>'
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <inputfile> -t <templatename> -q <queryfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-t","--tfile"):
         templatename = arg
      elif opt in ("-q", "--qfile"):
         queryfile = arg
    print 'Input file is "', inputfile
    print 'template is "',templatename
    print 'Query file is "', queryfile
    global Address_Invalid_Mut, Address_Valid_Mut
    Address_Valid_Mut= '/Mutants_'+inputfile[:-4]+'_Valid/'
    Address_Invalid_Mut = '/Mutants_'+inputfile[:-4]+'_INValid/'
    # MakeTree (inputfile)
    global tree, root
    tree= ET.parse(inputfile)
    root = tree.getroot()
    print root.tag
    NewDir (inputfile)
    CN(inputfile[:-4],templatename,queryfile)
    CS(inputfile[:-4], templatename,queryfile)
    CT(inputfile[:-4], templatename,queryfile)
    CG(inputfile[:-4], templatename,queryfile)
    NG(inputfile[:-4],templatename,queryfile)
    C_I(inputfile[:-4],templatename,queryfile)
    # IR(inputfile[:-4],templatename,queryfile)


def NewDir(i):
    print 'in NewDir'
    if not os.path.exists('Mutants_'+i[:-4]+'_Valid'):
         os.makedirs('Mutants_'+i[:-4]+'_Valid')

    if not os.path.exists('Mutants_'+i[:-4]+'_INvalid'):
         os.makedirs('Mutants_'+i[:-4]+'_INvalid')

def Change_dir(MyMy,answer):
    dist_inv = str(os.getcwd())+Address_Invalid_Mut+str(MyMy)
    dist_val = str(os.getcwd())+Address_Valid_Mut+str(MyMy)
    src=str(os.getcwd())+'\\'+str(MyMy)
    if answer=='yes':
        shutil.move(MyMy,dist_val)
        print 'moved to valid folder'
    if answer=='no':
        shutil.move(MyMy,dist_inv)
        print 'moved to invalid folder'

def CS(inp,tem,que):#change Source of transition
    print 'in cc'
    for t in root.findall('template'):
        r =  [loc.attrib['id'] for loc in t.findall('location')]
        r2 = [loc.find('label') for loc in t.findall('transition')]
        print 'number of transitions:', len(r),r, len(r2), r2
        print 'main temp', t.find('name').text
        if t.find('name').text==tem:
            for ii in range(len(r)):
                for k in range(len(r2)):
                    strin = 'transition['+str(k)+']'
                    MyName =inp+'MUT_CS'+str(k)+'_'+str(ii)+'.xml'
                    tree.write(MyName)
                    treex = ET.parse(MyName)
                    rootx = treex.getroot()
                    for t in rootx.findall('template'):
                        print 'inside temp', t.find('name').text
                        if t.find('name').text==tem:
                            print strin
                            strin = 'transition['+str(k)+']'
                            tra = t.find(strin)
                            print 'in Template and transition is',tra.find('label').text
                            for s in tra.iter('source'):
                                    print 'with source location',s.attrib,'candidate location is : ',r[ii]
                                    before= s.attrib['ref']
                                    if before != r[ii]:
                                        s.attrib['ref']=r[ii]
                                        print 'location',before,'changes to', s.attrib
                                        os.path
                                        treex.write(MyName)
                                        # addme= 'MUT_CS'+str(k)+'_'+str(ii)+'.xml'
                                        print 'new tree is made'
                                        if CheckQuery(MyName):
                                            Change_dir(MyName,'yes')
                                        else:
                                            Change_dir(MyName,'no')
                                    else:
                                        os.remove(MyName)
                                        print 'it is deleted'

def CT(inp, tem,que):#change Target of transition
    for t in root.findall('template'):
        r =  [loc.attrib['id'] for loc in t.findall('location')]
        r2 = [loc.find('label') for loc in t.findall('transition')]
        print 'number of transitions:', len(r),r, len(r2), r2
        print 'main temp', t.find('name').text
        if t.find('name').text==tem:
            for ii in range(len(r)):
                for k in range(len(r2)):
                    strin = 'transition['+str(k)+']'
                    MyName=inp+'MUT_CT'+str(k)+'_'+str(ii)+'.xml'
                    tree.write(MyName)
                    treex = ET.parse(MyName)
                    rootx = treex.getroot()
                    for t in rootx.findall('template'):
                        print 'inside temp', t.find('name').text
                        if t.find('name').text==tem:
                            print strin
                            strin = 'transition['+str(k)+']'
                            tra = t.find(strin)
                            print 'in Template and transition is',tra.find('label').text
                            for s in tra.iter('target'):
                                    print 'with source location',s.attrib,'candidate location is : ',r[ii]
                                    before= s.attrib['ref']
                                    if before != r[ii]:
                                        s.attrib['ref']=r[ii]
                                        print 'location',before,'changes to', s.attrib
                                        treex.write(MyName)
                                        print 'new tree is made'
                                        if CheckQuery(MyName):
                                            Change_dir(MyName,'yes')
                                        else:
                                            Change_dir(MyName,'no')
                                    else:
                                        os.remove(MyName)
                                        print 'it is deleted'

def CN(inp,tem,que): # change output transition
    i=0
    j=0
    for temp in root.findall('template'):
        if temp.find('name').text==tem:
            r= []
            for loc in temp.findall('transition'):
                sync =loc.find("label[@kind='synchronisation']")
                if sync!= None:
                    r.append(sync.text)
                else:
                    r.append(None)
            print r
            # r[loc] = [loc.find("label[@kind='synchronisation']").text for loc in temp.findall('transition')]
            print 'main temp', temp.find('name').text
            # print 'all transitions are',r
            for output_selection in range(len(r)):
                check= r[output_selection]
                print check
                if check!= None and check[-1:]!= '!':
                    r[output_selection]=None
                else: j+=1 # counting the number of output transitions
            # print 'all output transitions ',r, j
            for ii in range(len(r)):
                for k in range(len(r)):
                    strin = 'transition['+str(k)+']'
                    MyName=inp+'MUT_CN'+str(k)+'_'+str(ii)+'.xml'
                    tree.write(MyName)
                    treex = ET.parse(MyName)
                    rootx = treex.getroot()
                    for t in rootx.findall('template'):
                        if t.find('name').text==tem:
                            # print strin
                            strin = 'transition['+str(k)+']'
                            tra = t.find(strin)
                            s= tra.find("label[@kind='synchronisation']")
                            if s != None:
                                print 'transition is ',s.text
                                ss = s.text
                                if ss[-1:]=='!':
                                    # print 'inside '
                                    if ss != r[ii] and r[ii]!= None:
                                        s.text=r[ii]
                                        print 'tarn name ',ss,'changes to', s.text
                                        treex.write(inp+'MUT_CN'+str(k)+'_'+str(ii)+'.xml')
                                        i+=1
                                        print MyName,'new tree is made for transitions',s.text
                                        if CheckQuery(MyName):
                                            Change_dir(MyName,'yes')
                                        else:
                                            Change_dir(MyName,'no')
                                    else:
                                        os.remove(inp+'MUT_CN'+str(k)+'_'+str(ii)+'.xml')
                                        # print MyName,'it is deleted'
                                else:
                                    os.remove(inp+'MUT_CN'+str(k)+'_'+str(ii)+'.xml')

                            else:
                                print 'remove the unsync channels'
                                os.remove(MyName)
                                print MyName,'it is deleted'
    print 'i is :', i

def CheckQuery(MyName):
    try:
        print 'The name of the model: ', MyName
        output = subprocess.check_output('verifyta -t0 -f mytrace '+MyName+' query.q',shell=False)
        print 'output is ',output
        result_sat = re.search(r'\bProperty is satisfied',str(output))
        result_not_sat = re.search(r'\bProperty is NOT satisfied.',str(output))
        print 'result of regex:', result_sat, result_not_sat
        if result_sat!=None:
            return True
        if result_not_sat!=None:
            return False
    except subprocess.CalledProcessError:
        print 'here is an error'
        return False

#Change Guard
def CG(inp,tem,que):
    for t in root.findall('template'):
            r =  [loc.attrib['id'] for loc in t.findall('location')]
            h=0
            for loc in t.findall('transition'):
                x=loc.find("label[@kind='guard']")
                if x!= None: h+=1

            print 'number of gurads:',h
            #print 'main temp', t.find('name').text
            if t.find('name').text==tem:
                # for ii in range(len(r)):
                    for k in range(h):
                        strin = 'transition['+str(k)+']'
                        MyName =inp+'MUT_CG'+str(k)+'_'+str(h)+'.xml'
                        tree.write(MyName)
                        treex = ET.parse(MyName)
                        rootx = treex.getroot()
                        for t in rootx.findall('template'):
                            #print 'inside temp', t.find('name').text
                            if t.find('name').text=='Template':
                                #print strin
                                strin = 'transition['+str(k)+']'
                                tra = t.find(strin)
                                #print 'in Template and transition is',tra.find('label').tag
                                x=tra.find("label[@kind='guard']")
                                if x != None:
                                    print x.text
                                    x.text='cl<=5'
                                    treex.write(MyName)
                                    if CheckQuery(MyName):
                                            Change_dir(MyName,'yes')
                                    else:
                                            Change_dir(MyName,'no')
                                else:
                                    os.remove(MyName)

#Negate Gurad
def NG(inp,tem,que):
    for t in root.findall('template'):
            r =  [loc.attrib['id'] for loc in t.findall('location')]
            h=0
            for loc in t.findall('transition'):
                x=loc.find("label[@kind='guard']")
                if x!= None: h+=1
            print 'number of gurads:',h
            print 'main temp', t.find('name').text
            if t.find('name').text==tem:
                  for ii in range(h):
                    for k in range(len(r)):
                        strin = 'transition['+str(k)+']'
                        MyName=inp+'MUT_NG'+str(k)+'_'+str(h)+'.xml'
                        tree.write(MyName)
                        treex = ET.parse(MyName)
                        rootx = treex.getroot()
                        for t in rootx.findall('template'):
                            #print 'inside temp', t.find('name').text
                            if t.find('name').text==tem:
                                print strin
                                strin = 'transition['+str(k)+']'
                                tra = t.find(strin)
                                x=tra.find("label[@kind='guard']")
                                print 'x is',x
                                if x != None:
                                    print 'and text is ', x.text
                                    x.text=str('not('+x.text+')')
                                    treex.write(MyName)
                                    if CheckQuery(MyName):
                                            Change_dir(MyName,'yes')
                                    else:
                                            Change_dir(MyName,'no')

                                else:
                                    os.remove(MyName)

#Change invarient
def C_I(inp,tem,que):
    print 'here i am'
    for t in root.findall('template'):
            r =  [loc.attrib['id'] for loc in t.findall('location')]
            h=0
            for loc in t.findall('location'):
                x=loc.find("label[@kind='invariant']")
                if x!= None: h+=1
            print 'number of inv:',h
            print 'main temp', t.find('name').text
            if t.find('name').text==tem:
                  for ii in range(h):
                    for k in range(len(r)):
                        strin = 'location['+str(k)+']'
                        MyName= inp+ 'MUT_CI_'+str(k)+'_'+str(h)+'.xml'
                        tree.write(MyName)
                        treex = ET.parse(MyName)
                        rootx = treex.getroot()
                        for t in rootx.findall('template'):
                            #print 'inside temp', t.find('name').text
                            if t.find('name').text==tem:
                                print strin
                                strin = 'location['+str(k)+']'
                                tra = t.find(strin)
                                x=tra.find("label[@kind='invariant']")
                                print 'x is',x
                                if x != None:
                                    print 'and text is ', x.text
                                    x.text=x.text+'+1'
                                    treex.write(MyName)
                                    print 'created'
                                    if CheckQuery(MyName):
                                            Change_dir(MyName,'yes')
                                    else:
                                            Change_dir(MyName,'no')
                                else:
                                    os.remove(MyName)
                                print 'removed'
#Sink location
def SL(): # has problem
    for t in root.findall('template'):
            r =  [loc.attrib['id'] for loc in t.findall('transition')]
            # for loc in t.findall('transition'):
            #     x=loc.find("label[@kind='guard']")
            #     if x!= None: h+=1
            print 'number of trans:',len(r)
            print 'main temp', t.find('name').text
            if t.find('name').text==tem:
                  for ii in range(len(r)):
                    for k in range(len(r)):
                        strin = 'transition['+str(k)+']'
                        MyName=inp+'MUT_SL_'+str(k)+'_'+str(ii)+'.xml'
                        tree.write(MyName)
                        treex = ET.parse(MyName)
                        rootx = treex.getroot()
                        for t in rootx.findall('template'):
                            #print 'inside temp', t.find('name').text
                            if t.find('name').text==tem:
                                print strin
                                strin = 'transition['+str(k)+']'
                                tra = t.find(strin)
                                x=tra.find("label[@kind='target']") #find traget of a transition
                                print 'target of '+tra+ ' is',x
                                x.text='id_new'
                                treex.write(MyName)
                                if CheckQuery(MyName):
                                        Change_dir(MyName,'yes')
                                else:
                                        Change_dir(MyName,'no')




#Invert reset
def IR(inp,tem,que):
        for t in root.findall('template'):
            r =  [loc.attrib['id'] for loc in t.findall('location')]
            h=0
            for loc in t.findall('transition'):
                x=loc.find("label[@kind='assignment']")
                if x== None: h+=1
            print 'number of transitions without assignment:',h
            print 'main temp', t.find('name').text
            if t.find('name').text==tem:
                   for k in range(len(r)):
                        strin = 'transition['+str(k)+']'
                        MyName=inp+'MUT_IR_'+str(k)+'_'+str(h)+'.xml'
                        tree.write(MyName)
                        treex = ET.parse(MyName)
                        rootx = treex.getroot()
                        for t in rootx.findall('template'):
                            #print 'inside temp', t.find('name').text
                            if t.find('name').text==tem:
                                print strin
                                strin = 'transition['+str(k)+']'
                                tra = t.find(strin)
                                x=tra.find("label[@kind='assignment']")
                                copyfromme =tra.find("label[@kind='target']")
                                print 'x is',x
                                print 'copy line is:', copyfromme
                                # if x == None:
                                #     print 'and text is ', x.text
                                #
                                #     treex.write(MyName)
                                #     if CheckQuery(MyName):
                                #             Change_dir(MyName,'yes')
                                #     else:
                                #             Change_dir(MyName,'no')
                                #
                                # else:
                                #     os.remove(MyName)

# NewDir()
# CN()
# CS()
# CT()
# CG()
# NG()
# CI()
# SL()
# IR()
# CheckQuery()

# current_path='\FSDT\Mutation_UPTA\mut_locations'
# ChangeDIR()


if __name__ == "__main__":
   main(sys.argv[1:])