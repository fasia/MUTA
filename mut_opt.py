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
print("now ",currpath)
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
        print('Mut_opt.py -i <inputfile> -t <templatename> -q <queryfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('mut_opt.py -i <inputfile> -t <templatename> -q <queryfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-t","--tfile"):
            templatename = arg
        elif opt in ("-q", "--qfile"):
            queryfile = arg
    #print('Input file is "', inputfile)
    #print('template is "',templatename)
    #print('Query file is "', queryfile)
    global Address_Invalid_Mut, Address_Valid_Mut
    Address_Valid_Mut= '/Mutants_'+inputfile[:-4]+'_Valid/'
    Address_Invalid_Mut = '/Mutants_'+inputfile[:-4]+'_INValid/'
    # MakeTree (inputfile)
    global tree, root
    tree= ET.parse(inputfile)
    root= tree.getroot()
    #print 'my test', [t.find(templatename) for t in root.findall(".//name")]
    #print(root.tag)
    #NewDir (inputfile[:-4])
#CN(inputfile[:-4],templatename,queryfile)
#CS(inputfile[:-4], templatename,queryfile)
    #CT(inputfile[:-4], templatename,queryfile)
#CG(inputfile[:-4], templatename,queryfile)
#NG(inputfile[:-4],templatename,queryfile)
#C_I(inputfile[:-4],templatename,queryfile)
# IR(inputfile[:-4],templatename,queryfile)



#--------------------------- HOM ----------------------------#
    #STS(inputfile[:-4], templatename)
    CTCN(inputfile[:-4], templatename)
def NewDir(i):
    print('in NewDir')
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
        print('moved to valid folder')
    if answer=='no':
        shutil.move(MyMy,dist_inv)
        print('moved to invalid folder')

def CS(inp,tem,que):#change Source of transition
    print('in cc')
    for t in root.findall('template'):
        r =  [loc.attrib['id'] for loc in t.findall('location')]
        r2 = [loc.find('label') for loc in t.findall('transition')]
        print('number of transitions:', len(r),r, len(r2), r2)
        print('main temp', t.find('name').text)
        if t.find('name').text==tem:
            for ii in range(len(r)):
                for k in range(len(r2)):
                    strin = 'transition['+str(k)+']'
                    MyName =inp+'MUT_CS'+str(k)+'_'+str(ii)+'.xml'
                    tree.write(MyName)
                    treex = ET.parse(MyName)
                    rootx = treex.getroot()
                    for t in rootx.findall('template'):
                        print('inside temp', t.find('name').text)
                        if t.find('name').text==tem:
                            print(strin)
                            strin = 'transition['+str(k)+']'
                            tra = t.find(strin)
                            #print 'in Template and transition is',tra.find('label').text
                            for s in tra.iter('source'):
                                #  print 'with source location',s.attrib,'candidate location is : ',r[ii]
                                before= s.attrib['ref']
                                if before != r[ii]:
                                    s.attrib['ref']=r[ii]
                                    # print 'location',before,'changes to', s.attrib
                                    # os.path
                                    treex.write(MyName)
                                    # addme= 'MUT_CS'+str(k)+'_'+str(ii)+'.xml'
                                    # print 'new tree is made'
                                    if CheckQuery(MyName):
                                        Change_dir(MyName,'yes')
                                    else:
                                        Change_dir(MyName,'no')
                                else:
                                    os.remove(MyName)
                                #print 'it is deleted'

def CT(inp, tem,que):#change Target of transition
    for t in root.findall('template'):
        r =  [loc.attrib['id'] for loc in t.findall('location')]
        r2 = [loc.find('label') for loc in t.findall('transition')]
        #print 'number of transitions:', len(r),r, len(r2), r2
        #print 'main temp', t.find('name').text
        if t.find('name').text==tem:
            for ii in range(len(r)):
                for k in range(len(r2)):
                    strin = 'transition['+str(k)+']'
                    MyName=inp+'MUT_CT'+str(k)+'_'+str(ii)+'.xml'
                    tree.write(MyName)
                    treex = ET.parse(MyName)
                    rootx = treex.getroot()
                    for t in rootx.findall('template'):
                        #print 'inside temp', t.find('name').text
                        if t.find('name').text==tem:
                            #print strin
                            strin = 'transition['+str(k)+']'
                            tra = t.find(strin)
                            #print 'in Template and transition is',tra.find('label').text
                            for s in tra.iter('target'):
                                print('with source location',s.attrib,'candidate location is : ',r[ii])
                                before= s.attrib['ref']
                                if before != r[ii]:
                                    s.attrib['ref']=r[ii]
                                    #print 'location',before,'changes to', s.attrib
                                    treex.write(MyName)
                                    #print 'new tree is made'
                                    if CheckQuery(MyName):
                                        Change_dir(MyName,'yes')
                                    else:
                                        Change_dir(MyName,'no')
                                else:
                                    os.remove(MyName)
                                #print 'it is deleted'

def CN(inp,tem,que): # change output transition name
    i=0
    j=0
    # get the transitions in the target template
    for temp in root.findall('template'):
        if temp.find('name').text==tem:
            listOfTransitions= []
            for tran in temp.findall('transition'):
                sync =tran.find("label[@kind='synchronisation']") # gets all synchronizations
                if sync!= None:
                    listOfTransitions.append(sync.text)
                # else:
                #     listOfTransitions.append(None)
            print("listOfTransitions", listOfTransitions)
            # r[loc] = [loc.find("label[@kind='synchronisation']").text for loc in temp.findall('transition')]
            #print 'main temp', temp.find('name').text
            # #print 'all transitions are',r
            for output_selection in range(len(listOfTransitions)):
                check= listOfTransitions[output_selection]
                #print check
                if check[-1:]!= '!':
                    listOfTransitions[output_selection]=None # remove output synch
                else: j+=1 # counting the number of output transitions
            print('all output transitions ',listOfTransitions)
            for ii in range(len(listOfTransitions)):
                for k in range(len(listOfTransitions)):
                    strin = 'transition['+str(k)+']'
                    #print("stin", strin)
                    MyName=inp+'MUT_CN'+str(k)+'_'+str(ii)+'.xml'
                    print('tree', MyName, ' is made.')
                    tree.write(MyName)
                    treex = ET.parse(MyName)
                    rootx = treex.getroot()
                    # for all templates in the model it looks for the target template and changes the names one by one
                    for t in rootx.findall('template'):
                        if t.find('name').text==tem:
                            #print('t ',t.findall("label[@kind='synchronisation']"))
                            #print("strin",strin)
                            #strin = 'transition['+str(k)+']'
                            transitionsList = t.findall("./transition/label[@kind='synchronisation']")
                            print(transitionsList[k].text)
                            transitionText= transitionsList[k].text
                            if transitionText[-1:]=='!':
                                print("inside if", 'transition is', transitionText)
                                if transitionText != listOfTransitions[ii] and listOfTransitions[ii]!= None: # checks whether the transition name is different that selected transition
                                    print(t.find("./transition/label[@kind='synchronisation']").text)#=listOfTransitions[ii]
                                    print ('tree is :',inp+'MUT_CN'+str(k)+'_'+str(ii)+'.xml')
                                    treex.write(inp+'MUT_CN'+str(k)+'_'+str(ii)+'.xml')
                                    i+=1
                                #print MyName,'new tree is made for transitions',s.text
                                #if CheckQuery(MyName):
                                #    Change_dir(MyName,'yes')
                                #else:
                                #    Change_dir(MyName,'no')
                                else:
                                    os.remove(MyName)
                                # #print MyName,'it is deleted'
                            else:
                                os.remove(MyName)

                            # else:
                            #     #print 'remove the unsync channels'
                            #     os.remove(MyName)
                            #print MyName,'it is deleted'
                            #print 'i is :', i

def CheckQuery(MyName):
    try:
        #print 'The name of the model: ', MyName
        output = subprocess.check_output('verifyta -t0 -f mytrace '+MyName+' query.q',shell=False)
        #print 'output is ',output
        result_sat = re.search(r'\bProperty is satisfied',str(output))
        result_not_sat = re.search(r'\bProperty is NOT satisfied.',str(output))
        #print 'result of regex:', result_sat, result_not_sat
        if result_sat!=None:
            return True
        if result_not_sat!=None:
            return False
    except subprocess.CalledProcessError:
        #print 'here is an error'
        return False

#Change Guard
def CG(inp,tem,que):
    for t in root.findall('template'):
        r =  [loc.attrib['id'] for loc in t.findall('location')]
        h=0
        for loc in t.findall('transition'):
            x=loc.find("label[@kind='guard']")
            if x!= None: h+=1

        #print 'number of gurads:',h
        ##print 'main temp', t.find('name').text
        if t.find('name').text==tem:
            # for ii in range(len(r)):
            for k in range(h):
                strin = 'transition['+str(k)+']'
                MyName =inp+'MUT_CG'+str(k)+'_'+str(h)+'.xml'
                tree.write(MyName)
                treex = ET.parse(MyName)
                rootx = treex.getroot()
                for t in rootx.findall('template'):
                    ##print 'inside temp', t.find('name').text
                    if t.find('name').text=='Template':
                        ##print strin
                        strin = 'transition['+str(k)+']'
                        tra = t.find(strin)
                        ##print 'in Template and transition is',tra.find('label').tag
                        x=tra.find("label[@kind='guard']")
                        if x != None:
                            #print x.text
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
        #print 'number of gurads:',h
        #print 'main temp', t.find('name').text
        if t.find('name').text==tem:
            for ii in range(h):
                for k in range(len(r)):
                    strin = 'transition['+str(k)+']'
                    MyName=inp+'MUT_NG'+str(k)+'_'+str(h)+'.xml'
                    tree.write(MyName)
                    treex = ET.parse(MyName)
                    rootx = treex.getroot()
                    for t in rootx.findall('template'):
                        ##print 'inside temp', t.find('name').text
                        if t.find('name').text==tem:
                            #print strin
                            strin = 'transition['+str(k)+']'
                            tra = t.find(strin)
                            x=tra.find("label[@kind='guard']")
                            #print 'x is',x
                            if x != None:
                                #print 'and text is ', x.text
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
    #print 'here i am'
    for t in root.findall('template'):
        r =  [loc.attrib['id'] for loc in t.findall('location')]
        h=0
        for loc in t.findall('location'):
            x=loc.find("label[@kind='invariant']")
            if x!= None: h+=1
        #print 'number of inv:',h
        #print 'main temp', t.find('name').text
        if t.find('name').text==tem:
            for ii in range(h):
                for k in range(len(r)):
                    strin = 'location['+str(k)+']'
                    MyName= inp+ 'MUT_CI_'+str(k)+'_'+str(h)+'.xml'
                    tree.write(MyName)
                    treex = ET.parse(MyName)
                    rootx = treex.getroot()
                    for t in rootx.findall('template'):
                        ##print 'inside temp', t.find('name').text
                        if t.find('name').text==tem:
                            #print strin
                            strin = 'location['+str(k)+']'
                            tra = t.find(strin)
                            x=tra.find("label[@kind='invariant']")
                            #print 'x is',x
                            if x != None:
                                #print 'and text is ', x.text
                                x.text=x.text+'+1'
                                treex.write(MyName)
                                #print 'created'
                                if CheckQuery(MyName):
                                    Change_dir(MyName,'yes')
                                else:
                                    Change_dir(MyName,'no')
                            else:
                                os.remove(MyName)
                            #print 'removed'
#Sink location
def SL(inp, tem): # has problem
    for t in root.findall('template'):
        r =  [loc.attrib['id'] for loc in t.findall('transition')]
        # for loc in t.findall('transition'):
        #     x=loc.find("label[@kind='guard']")
        #     if x!= None: h+=1
        #print 'number of trans:',len(r)
        #print 'main temp', t.find('name').text
        if t.find('name').text==tem:
            for ii in range(len(r)):
                for k in range(len(r)):
                    strin = 'transition['+str(k)+']'
                    MyName=inp+'MUT_SL_'+str(k)+'_'+str(ii)+'.xml'
                    tree.write(MyName)
                    treex = ET.parse(MyName)
                    rootx = treex.getroot()
                    for t in rootx.findall('template'):
                        ##print 'inside temp', t.find('name').text
                        if t.find('name').text==tem:
                            #print strin
                            strin = 'transition['+str(k)+']'
                            tra = t.find(strin)
                            x=tra.find("label[@kind='target']") #find traget of a transition
                            #print 'target of '+tra+ ' is',x
                            x.text='id_new'
                            treex.write(MyName)
                            # if CheckQuery(MyName):
                            #     Change_dir(MyName,'yes')
                            # else:
                            #     Change_dir(MyName,'no')

# def declare_Trap(inp):
#     dec= root.find('declaration')
#     print 'dec is', dec.text
#     dec.text += '\nbool trap= false;'
#     print root.find('declaration').text
#     tree.write(inp)

#################################### switch Target and Source######################################



def STS(inp, tem):
    dec= root.find('declaration')
    dec.text += '\nbool trap= false; // reachability of the mutation canbe checked by this boolean variable'
    for t in root.findall('template'):
        r =  [loc.attrib['id'] for loc in t.findall('location')]
        r2 = [loc.find('label') for loc in t.findall('transition')]
        print 'transitions:',  r2
        #print 'main temp', t.find('name').text
        if t.find('name').text==tem:
            for ii in range(len(r)):
                for k in range(len(r2)):
                    strin = 'transition['+str(k)+']'
                    MyName=inp+'MUT_STS'+str(k)+'_'+str(ii)+'.xml'
                    tree.write(MyName)
                    treex = ET.parse(MyName)
                    rootx = treex.getroot()
                    for t in rootx.findall('template'):
                        #print 'inside temp', t.find('name').text
                        if t.find('name').text==tem:
                            #print strin
                            strin = 'transition['+str(k)+']'
                            tra = t.find(strin)
                            assignment =  tra.find("label[@kind='assignment']")
                            #print assignment.index('kind')
                            print 'the assign is:', assignment
                            if assignment != None:
                                assignment.text += ', \ntrap=true'
                                print 'new ass', tra.find("label[@kind='assignment']").text
                            oldTarget = tra.find('target')
                            oldSource= tra.find('source')
                            print 'in ',MyName,'old target and old source :',oldTarget.attrib['ref'], oldSource.attrib['ref']
                            #if it is a loop then target and source are the same
                            if oldSource.attrib['ref'] != oldTarget.attrib['ref']:
                                #swap between the target and source
                                temporary = oldSource.attrib['ref']
                                oldSource.attrib['ref']= oldTarget.attrib['ref']
                                oldTarget.attrib['ref']= temporary
                                print 'in ',MyName,' is mutating with new target and new source :',oldTarget.attrib['ref'], oldSource.attrib['ref']
                                print '----------------------------------------'
                                treex.write(MyName)
                                # if CheckQuery(MyName):
                                #     Change_dir(MyName,'yes')
                                # else:
                                #     Change_dir(MyName,'no')
                            else:
                                print 'the loop edge, and no mutation is generated'
                                os.remove(MyName)


# it has still problem on generating two mutants that are equivalent to eachother
def CTCN(inp, tem): # change target and change name
    #for each mutated name of a transition:
        # for each mutated target of a transition:
            # generate a new file
            # add the reachability
            # check the reachabilty
            #if it is reachable and deadlockfree:
                #save the file as a valid mutant

    dec= root.find('declaration')
    dec.text += '\nbool trap= false; // reachability of the mutation canbe checked by this boolean variable'
    t = root.find(".//template[name='"+str(tem)+"']")
    listoflocations =  [loc.attrib['id'] for loc in t.findall('location')]
    listoftransitions = [loc.find("label[@kind='synchronisation']").text for loc in t.findall('transition')]

    for l in range(len(listoflocations)):
        for transition in range(len(listoftransitions)):
            i =0
            for target in listoflocations:

                #print 'l, trans, target', l, transition, target
                currTarget = t.find("transition["+str(transition)+"]/target")
                #print 'curtrans',currTrans.attrib['ref']
                currTran =t.find("transition["+str(transition)+"]/label[@kind='synchronisation']").text

                if currTarget.attrib['ref'] != target and currTran != listoftransitions[transition]:
                    print 'not the same'
                    print 'candidate transition:',listoftransitions[transition],'current transition: ', currTran
                    print 'candidare target:', target, 'current target', currTarget.attrib['ref']
                    #create new file
                    MyName=inp+'MUT_CTCN_'+str(transition)+'_'+str(l)+str(i)+'.xml'
                    tree.write(MyName)
                    treex= ET.parse(MyName)
                    rootx = treex.getroot()
                    tx = rootx.find(".//template[name='"+str(tem)+"']")
                    # mutation on target
                    tx.find("transition["+str(transition)+"]/target").attrib['ref']= target
                    #mutation on transition's name
                    tx.find("transition["+str(transition)+"]/label[@kind='synchronisation']").text = listoftransitions[transition]

                    #check if they are correctly mutated
                    print 'mutated transition name is:', tx.find("transition["+str(transition)+"]/label[@kind='synchronisation']").text
                    print 'mutated target is :', tx.find("transition["+str(transition)+"]/target").attrib['ref']

                    treex.write(MyName)
                    i =i+1






#Invert reset
def IR(inp,tem,que):
    for t in root.findall('template'):
        r =  [loc.attrib['id'] for loc in t.findall('location')]
        h=0
        for loc in t.findall('transition'):
            x=loc.find("label[@kind='assignment']")
            if x== None: h+=1
        #print 'number of transitions without assignment:',h
        #print 'main temp', t.find('name').text
        if t.find('name').text==tem:
            for k in range(len(r)):
                strin = 'transition['+str(k)+']'
                MyName=inp+'MUT_IR_'+str(k)+'_'+str(h)+'.xml'
                tree.write(MyName)
                treex = ET.parse(MyName)
                rootx = treex.getroot()
                for t in rootx.findall('template'):
                    ##print 'inside temp', t.find('name').text
                    if t.find('name').text==tem:
                        #print strin
                        strin = 'transition['+str(k)+']'
                        tra = t.find(strin)
                        x=tra.find("label[@kind='assignment']")
                        copyfromme =tra.find("label[@kind='target']")
                    #print 'x is',x
                    #print 'copy line is:', copyfromme
                    # if x == None:
                    #     #print 'and text is ', x.text
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

