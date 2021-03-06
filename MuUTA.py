__author__ = 'fsiavash'

import sys, getopt
import xml.etree.ElementTree as ET
#from lxml import etree
import random
import os
import os.path
import copy
from copy import deepcopy
import subprocess
from subprocess import call
import re
import shutil
import datetime
import logging

logger= logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler('MuUTA.log')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)
#logger.info('*****************************Generator has started.****************************************')
# nameoffile= 'timed-gate.xml'
# tree = ET.parse(nameoffile)
# root = tree.getroot()

# FileNeme = nameoffile[:-4]


# current path
currpath= os.getcwd()
#print("now ",currpath)
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

    NewDir (inputfile[:-4])
    #CN(inputfile[:-4],templatename)
    #CS(inputfile[:-4], templatename)
    #CT(inputfile[:-4], templatename)
    #CG(inputfile[:-4], templatename)
    #NG(inputfile[:-4],templatename,queryfile)
    #C_I(inputfile[:-4],templatename,queryfile)
    #IR(inputfile[:-4],templatename,queryfile)
    #RG(inputfile[:-4],templatename)
    CGL(inputfile[:-4],templatename)
    CGV(inputfile[:-4],templatename)
#--------------------------- HOM ----------------------------#
    #STS(inputfile[:-4], templatename)
    #CTN(inputfile[:-4], templatename)
    #CSN(inputfile[:-4], templatename)
    #RA(inputfile[:-4], templatename)
    #DA(inputfile[:-4], templatename)
    #EIG(inputfile[:-4], templatename)

def NewDir(i):
    #print('in NewDir')
    if not os.path.exists('Mutants_'+i+'_Valid'):
        os.makedirs('Mutants_'+i+'_Valid')

    if not os.path.exists('Mutants_'+i+'_INvalid'):
        os.makedirs('Mutants_'+i+'_INvalid')

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

def CS(inp,tem):#change Source of transition
    #print('in cc')
    timerStart=datetime.datetime.now()
    logger.info('CS for '+str(inp)+' '+str(tem)+' started.')
    for t in root.findall('template'):
        locations =  [loc for loc in t.findall('location')]
        transitions = [tran for tran in t.findall('transition')]
        print('number of transitions:', locations, transitions)
        print('main temp', t.find('name').text)
        i=0
        if t.find('name').text==tem: # check if the template is the selected template to mutate
            for tr in range(len(transitions)): #for each transition
                #print "tr is", transitions[tr].find('source').attrib['ref']
                source=transitions[tr].find('source').attrib['ref']
                nameofSource=transitions[tr].find('label').text
                print 'name of source',nameofSource
                for lo in locations:
                    newsource =lo.attrib['id']
                    if source!=newsource:
                        #print "source and new source are not the same", source, newsource
                #       make a new copy of the tree, find the source and change it
                        myMutation = inp+'Mut_CS_'+source+'_'+newsource+'_'+str(i)+'.xml'

                        tree.write(myMutation)
                        tree2= ET.parse(myMutation)
                        root2= tree2.getroot()
                        tem2=root2.findall('template')
                        for template2 in tem2:
                            if template2.find('name').text == str(tem):
                                i = i + 1
                               # print "template is found ", template2.find('name').text
                                transitionstest= template2.findall('transition')
                                selectedTransition = transitionstest[tr]
                                trann= transitionstest[tr].find('source').attrib['ref']
                                print"source ", trann,
                                transitionstest[tr].find('source').attrib['ref']=lo.attrib['id']
                                print 'changes to',transitionstest[tr].find('source').attrib['ref']
                                print "new file is craated", myMutation
                                # reachability settings
                                assignment = transitionstest[tr].find("label[@kind='assignment']")
                                if assignment != None:
                                    assignment.text += ',\ntrap=true'
                                    # print "in the assignment setting- if"
                                else:
                                    #ele = selectedTransition.find("transition[" + str(tr) + "]")
                                    assignmentAttrib = {"kind": "assignment", "x": "-20", "y": "-20"}
                                    item = ET.Element("label")
                                    item.text = "trap=true"
                                    item.attrib = assignmentAttrib
                                    selectedTransition.insert(3, item)

                                tree2.write(myMutation)
                                if os.name == 'nt':
                                    if CheckQuery(True, myMutation):

                                        Change_dir(myMutation, 'yes')
                                    else:
                                        Change_dir(myMutation, 'no')
    timerStop=datetime.datetime.now()
    te= timerStop-timerStart
    logger.info('CS finnished.')
    logger.info(te)

                            #else: # if the
                            #    os.remove(myMutation)

def CT(inp, tem):#change Target of transition
    #print('in cc')
    timerStart=datetime.datetime.now()
    logger.info('CT for '+str(inp)+' '+str(tem)+' started.')
    for t in root.findall('template'):
        locations =  [loc for loc in t.findall('location')]
        transitions = [tran for tran in t.findall('transition')]
        print('number of transitions:', locations, transitions)
        print('main temp', t.find('name').text)
        i=0
        if t.find('name').text==tem: # check if the template is the selected template to mutate
            for tr in range(len(transitions)): #for each transition
                #print "tr is", transitions[tr].find('source').attrib['ref']
                source=transitions[tr].find('target').attrib['ref']
                nameofSource=transitions[tr].find('label').text
                print 'name of source',nameofSource
                for lo in locations:
                    newsource =lo.attrib['id']

                    if source!=newsource:
                        #print "source and new source are not the same", source, newsource
                #       make a new copy of the tree, find the source and change it
                        myMutation = inp+'_Mut_CT_'+source+'_'+newsource+'_'+str(i)+'.xml'

                        tree.write(myMutation)
                        tree2= ET.parse(myMutation)
                        root2= tree2.getroot()
                        tem2=root2.findall('template')
                        for template2 in tem2:
                            if template2.find('name').text == str(tem):
                                i = i + 1
                               # print "template is found ", template2.find('name').text
                                transitionstest= template2.findall('transition')
                                selectedTransition = transitionstest[tr]
                                trann= transitionstest[tr].find('target').attrib['ref']
                                print"target ", trann,
                                transitionstest[tr].find('target').attrib['ref']=lo.attrib['id']
                                print 'changes to',transitionstest[tr].find('target').attrib['ref']
                                print "new file is craated", myMutation
                                # reachability settings
                                assignment = transitionstest[tr].find("label[@kind='assignment']")
                                if assignment != None:
                                    assignment.text += ',\ntrap=true'
                                    # print "in the assignment setting- if"
                                else:
                                    #ele = selectedTransition.find("transition[" + str(tr) + "]")
                                    assignmentAttrib = {"kind": "assignment", "x": "-20", "y": "-20"}
                                    item = ET.Element("label")
                                    item.text = "trap=true"
                                    item.attrib = assignmentAttrib
                                    selectedTransition.insert(3, item)

                                tree2.write(myMutation)
                                if os.name == 'nt':
                                    if CheckQuery(True, myMutation):

                                        Change_dir(myMutation, 'yes')
                                    else:
                                        Change_dir(myMutation, 'no')
    timerStop=datetime.datetime.now()
    te= timerStop-timerStart
    logger.info('CT finnished.')
    logger.info(te)

def CN(inp, tem):
    timerStart=datetime.datetime.now()
    logger.info('CN for '+str(inp)+' '+str(tem)+' started.')
    i=0
    j=0
    for temp in root.findall('template'):
        if temp.find('name').text==tem:
            allTransitions = [tran for tran in temp.findall("transition")]
            print 'list of channels', allTransitions
            for action in range(len(allTransitions)): # to cover all possible mutations, we neet to have 2 for loops
                for action2 in range(len(allTransitions)):
                    # check whether the action is not Null and their name are not the same.
                    i=i+1
                    if allTransitions[action].find("label[@kind='synchronisation']") !=None and allTransitions[action2].find("label[@kind='synchronisation']") != None:
                        oldAction = allTransitions[action].find("label[@kind='synchronisation']").text
                        newAction = allTransitions[action2].find("label[@kind='synchronisation']").text
                        if oldAction != newAction:
                            print'not same ', oldAction, newAction
                            j=j+1
                            MyName = inp + 'MUT_CN' + str(oldAction[:-1])+str(i) + '_' + str(newAction[:-1]) + '.xml'
                            print(MyName, ' is made.')
                            tree.write(MyName)
                            treex = ET.parse(MyName)
                            rootx = treex.getroot()
                            for tx in rootx.findall('template'):
                                if tx.find('name').text==tem:
                                    transitionsListx = tx.findall("transition")
                                    print('selected action in the copy ',transitionsListx[action].find("label[@kind='synchronisation']").text)
                                    transitionsListx[action].find("label[@kind='synchronisation']").text= transitionsListx[action2].find("label[@kind='synchronisation']").text
                                    transxx = transitionsListx[action]
                                    print 'difference ',transxx, transitionsListx[action]
                                    assignment =transxx.find("label[@kind='assignment']")
                                    #print 'assignment is', assignment.text
                                    if assignment != None:
                                        assignment.text += ',\ntrap=true'
                                    else:
                                        # ele = selectedTransition.find("transition[" + str(tr) + "]")
                                        assignmentAttrib = {"kind": "assignment", "x": "-20", "y": "-20"}
                                        item = ET.Element("label")
                                        item.text = "trap=true"
                                        item.attrib = assignmentAttrib
                                        transxx.insert(3, item)
                                    treex.write(MyName)
                                    if os.name == 'nt':
                                        if CheckQuery(True, MyName):

                                            Change_dir(MyName, 'yes')
                                        else:
                                            Change_dir(MyName, 'no')

                    print '# of mutants will be', j
    timerStop = datetime.datetime.now()
    te = timerStop - timerStart
    logger.info('CN finnished.')
    logger.info(te)

def CheckQuery(reachability, MyName):
    try:
        if reachability: # if reachability variable is true, then check reachability and deadlockfreeness,

            #print 'The name of the model: ', MyName
            output = subprocess.check_output('verifyta -t0 -f mytrace '+MyName+' query1.q', shell=False)
            #print 'output is ',output
            result_sat = re.search(r'\bProperty is satisfied',str(output))
            #result_not_sat = re.search(r'\bProperty is NOT satisfied.',str(output))
            output2 = subprocess.check_output('verifyta -t0 -f mytrace '+MyName+' query2.q', shell=False)

            result_sat2 = re.search(r'\bProperty is satisfied', str(output2))
            #result_not_sat2 = re.search(r'\bProperty is NOT satisfied.', str(output2))
            #print 'result of regex:', result_sat, result_not_sat
            if result_sat2!= None and result_sat != None:
                return True
            else:
                return False
        else: # otherwise we only check the deadlockfreeness
            output = subprocess.check_output('verifyta -t0 -f mytrace ' + MyName + ' query1.q', shell=False)
            # print 'output is ',output
            result_sat = re.search(r'\bProperty is satisfied', str(output))

            if result_sat!=None :
                return True
            else:
                return False

    except subprocess.CalledProcessError:
        # print 'here is an error'
        return False

# Remove Guard
def RG(inp, tem):
    timerStart = datetime.datetime.now()
    logger.info('RG for '+str(inp)+' '+str(tem)+' started.')
    for t in root.findall('template'):  # find all templates
        if t.find('name').text == tem:  # find the template that we want
            locations = [loc.attrib['id'] for loc in t.findall('location')]  # get the locations of the template
            transitions = [tran for tran in t.findall('transition')]
            print 'transitions', transitions
            h = 0
            #guardsList = t.findall("transition/label[@kind='guard']")
            for k in range(len(transitions)):  # for each guard make a mutant and increase the value guard by +1
                MyName = inp + 'MUT_RG' + str(k) + '_' + str(h) + '.xml'
                tree.write(MyName)
                treex = ET.parse(MyName)
                rootx = treex.getroot()
                for txx in rootx.findall('template'):
                    if txx.find('name').text == tem:
                        trn = txx.find("transition["+str(k)+"]")
                        #guards = txx.findall("transition/label[@kind='guard']")
                        #print 'guards:', guards
                        # change the guard
                        #guards[k].text += str('+1')
                        g=trn.find("label[@kind='guard']")
                        #element_guard=txx.find(".//label[@kind='guard']")
                        if g!=None:
                            print 'element',g
                            trn.remove(g)
                            print 'removed'
                            #   reachability settings
                            assignment = trn.find("label[@kind='assignment']")
                            if assignment != None:
                                assignment.text += ',\ntrap=true'
                                # print "in the assignment setting- if"
                            else:
                                # ele = selectedTransition.find("transition[" + str(tr) + "]")
                                assignmentAttrib = {"kind": "assignment", "x": "-20", "y": "-20"}
                                item = ET.Element("label")
                                item.text = "trap=true"
                                item.attrib = assignmentAttrib
                                trn.insert(3, item)
                            treex.write(MyName)
                            if CheckQuery(True,MyName):
                                Change_dir(MyName,'yes')
                            else:
                                Change_dir(MyName,'no')
                        else:
                            os.remove(MyName)
    timerStop = datetime.datetime.now()
    te = timerStop - timerStart
    logger.info('RG finnished.')
    logger.info(te)

#Change Guard logical Operators
def CGL(inp,tem):
    timerStart = datetime.datetime.now()
    logger.info('CGL started.')
    for t in root.findall('template'): # find all templates
        if t.find('name').text==tem: # find the template that we want
            locations = [loc.attrib['id'] for loc in t.findall('location')] # get the locations of the template
            print 'locations', locations
            h=0
            guardsList= t.findall("transition/label[@kind='guard']")
            for k in range(len(guardsList)): # for each guard make a mutant
                for j in ['==','!=','>','<','=<','>=']:
                    for j2 in ['==','!=','>','<','=<','>=']:
                        MyName =inp+'MUT_CGL'+str(k)+'_'+str(h)+'.xml'
                        tree.write(MyName)
                        treex = ET.parse(MyName)
                        rootx = treex.getroot()
                        for txx in rootx.findall('template'):
                            if txx.find('name').text==tem:
                                guards=txx.findall("transition/label[@kind='guard']")
                                #print 'guards:', guards
                                # change the guard
                               # print 'guard is:', guards[k].text
                                s= guards[k].text
                                if re.search(j,s) and j!=j2:
                                    print 'it is a j', j, 'j2 is', j2
                                    replaced= re.sub(j,j2,s)
                                    guards[k].text= replaced
                                    print 'repl is  ',guards[k].text, MyName
                                    h=h+1
                                    # reachability settings
                                    # assignment = txx.find[tr].find("label[@kind='assignment']")
                                    # if assignment != None:
                                    #     assignment.text += ',\ntrap=true'
                                    #     # print "in the assignment setting- if"
                                    # else:
                                    #     # ele = selectedTransition.find("transition[" + str(tr) + "]")
                                    #     assignmentAttrib = {"kind": "assignment", "x": "-20", "y": "-20"}
                                    #     item = ET.Element("label")
                                    #     item.text = "trap=true"
                                    #     item.attrib = assignmentAttrib
                                    #     selectedTransition.insert(3, item)
                                    treex.write(MyName)
                                    if CheckQuery(False,MyName):
                                        Change_dir(MyName,'yes')
                                    else:
                                        Change_dir(MyName,'no')
    timerStop = datetime.datetime.now()
    te = timerStop - timerStart
    logger.info('CGL finnished.')
    logger.info(te)

#Change Guard Values
def CGV(inp,tem):
    timerStart = datetime.datetime.now()
    logger.info('CGV started.')
    for t in root.findall('template'): # find all templates
        if t.find('name').text==tem: # find the template that we want
            locations = [loc.attrib['id'] for loc in t.findall('location')] # get the locations of the template
            print 'locations', locations
            h=0
            guardsList= t.findall("transition/label[@kind='guard']")
            for k in range(len(guardsList)): # for each guard make a mutant
                for j in ['0','[a]','[com]','[u]','[sa]','[su]','[max_art]']:
                    for j2 in ['+1','-1','0','[a]','[com]','[u]','[su]','[sa]','[max_art]']:
                        MyName =inp+'MUT_CGV'+str(k)+'_'+str(h)+'.xml'
                        tree.write(MyName)
                        treex = ET.parse(MyName)
                        rootx = treex.getroot()
                        for txx in rootx.findall('template'):
                            if txx.find('name').text==tem:
                                guards=txx.findall("transition/label[@kind='guard']")
                                #print 'guards:', guards
                                # change the guard
                               # print 'guard is:', guards[k].text
                                s= guards[k].text
                                if re.search(j,s) and j!=j2:
                                    print 'it is a j', j, 'j2 is', j2
                                    replaced= re.sub(j,j2,s)
                                    guards[k].text= replaced
                                    print 'repl is  ',guards[k].text, MyName
                                    h=h+1
                                    # reachability settings
                                    # assignment = txx.find[tr].find("label[@kind='assignment']")
                                    # if assignment != None:
                                    #     assignment.text += ',\ntrap=true'
                                    #     # print "in the assignment setting- if"
                                    # else:
                                    #     # ele = selectedTransition.find("transition[" + str(tr) + "]")
                                    #     assignmentAttrib = {"kind": "assignment", "x": "-20", "y": "-20"}
                                    #     item = ET.Element("label")
                                    #     item.text = "trap=true"
                                    #     item.attrib = assignmentAttrib
                                    #     selectedTransition.insert(3, item)
                                    treex.write(MyName)
                                    if CheckQuery(False,MyName):
                                        Change_dir(MyName,'yes')
                                    else:
                                        Change_dir(MyName,'no')
    timerStop = datetime.datetime.now()
    te = timerStop - timerStart
    logger.info('CGV finnished.')
    logger.info(te)

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

# Invert reset
def IR(inp, tem, que):
    for t in root.findall('template'):
        r = [loc.attrib['id'] for loc in t.findall('location')]
        h = 0
        for loc in t.findall('transition'):
            x = loc.find("label[@kind='assignment']")
            if x == None: h += 1
        # print 'number of transitions without assignment:',h
        # print 'main temp', t.find('name').text
        if t.find('name').text == tem:
            for k in range(len(r)):
                strin = 'transition[' + str(k) + ']'
                MyName = inp + 'MUT_IR_' + str(k) + '_' + str(h) + '.xml'
                tree.write(MyName)
                treex = ET.parse(MyName)
                rootx = treex.getroot()
                for t in rootx.findall('template'):
                    ##print 'inside temp', t.find('name').text
                    if t.find('name').text == tem:
                        # print strin
                        strin = 'transition[' + str(k) + ']'
                        tra = t.find(strin)
                        x = tra.find("label[@kind='assignment']")
                        copyfromme = tra.find("label[@kind='target']")
                        # print 'x is',x
                        # print 'copy line is:', copyfromme
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


####################################  Higher-Order Mutation Generators ######################################



def STS(inp, tem):
    print '-------------------------------------------------------------------------'
    print 'Mutation Operator STS (Switch Target and Source) is started.'
    #dec= root.find('declaration')
    #dec.text += '\nbool trap= false;
    #  // reachability of the mutation canbe checked by this boolean variable'
    t = root.find(".//template[name='" + str(tem) + "']")
    #listoflocations = [loc.attrib['id'] for loc in t.findall('location')]
    listoftransitions =  t.findall('transition')
    #print 'tran', listoftransitions
    synch= []
    for tt in listoftransitions:
        if tt.find("label[@kind='synchronisation']")!= None:
            synch.append(tt)
    #print 'list of transitions', synch
    for transition in range(len(synch)):
        #print 'current transition', synch[transition]
        MyName=inp+'MUT_STS'+str(transition)+'.xml'
        tree.write(MyName)
        treex = ET.parse(MyName)
        rootx = treex.getroot()
        t2= rootx.find(".//template[name='" + str(tem) + "']")

        # add trap in the declaration
        #dec = rootx.find('declaration')
        #dec.text += '\nbool trap= false;'
        currTarget = t2.find("transition[" + str(transition) + "]/target")
        currentSource = t2.find("transition[" + str(transition) + "]/source")
        currTran = t2.find("transition[" + str(transition) + "]/label[@kind='synchronisation']")

        #print 'in ',MyName,'old target and old source :',currTarget.attrib['ref'], currentSource.attrib['ref']
        #if it is a loop then target and source are the same
        if currentSource.attrib['ref'] != currTarget.attrib['ref']:
            #swap between the target and source
            temporary = currentSource.attrib['ref']
            currentSource.attrib['ref']= currTarget.attrib['ref']
            currTarget.attrib['ref']= temporary
            #print 'in ',MyName,' is mutating with new target and new source :',currTarget.attrib['ref'], currentSource.attrib['ref']
            assignment = t2.find("transition[" + str(transition) + "]/label[@kind='assignment']")
            # print assignment.index('kind')
            #print 'the assign is:', assignment
            if assignment != None:
                assignment.text += ',\ntrap=true'
               # print 'new ass', t2.find("transition[" + str(transition) + "]/label[@kind='assignment']").text
            else:
                ele = t2.find("transition[" + str(transition) + "]")
                assignmentAttrib = {"kind": "assignment", "x": "-20", "y": "-20"}
                item = ET.Element("label")
                item.text = "trap=true"
                item.attrib = assignmentAttrib
                ele.insert(3, item)
                # ET.tostring(rootx)
              #  print el
             #   print "in the assignment setting - else"
            treex.write(MyName)
            print 'Mutant', str(MyName),'is generated.'

            if os.name == 'nt':
                if CheckQuery(True, MyName):
                    Change_dir(MyName,'yes')
                else:
                    Change_dir(MyName,'no')
        else:
            #print 'the loop edge, and no mutation is generated'
            os.remove(MyName)



# it has still problem on generating two mutants that are equivalent to eachother
def CTN(inp, tem): # change target and change name
    print '-------------------------------------------------------------------------'

    print 'Mutation operator Change Target and name (CTN) is started.'
    #dec= root.find('declaration')
    #dec.text += '\nbool trap= false; // reachability of the mutation canbe checked by this boolean variable'
    t = root.find(".//template[name='"+str(tem)+"']")
    listoflocations =  [loc.attrib['id'] for loc in t.findall('location')]
    listoftransitions = [loc.find("label[@kind='synchronisation']") for loc in t.findall('transition')]

    for l in range(len(listoflocations)):
        #print 'num', len(listoflocations), len(listoftransitions), len(listoflocations)
        for transition in range(len(listoftransitions)):
            i =0
            for target in listoflocations:
                currTarget = t.find("transition["+str(transition)+"]/target")
                currTran =t.find("transition["+str(transition)+"]/label[@kind='synchronisation']")
                if currTran != None: # we check if the transition is actually a synchronisation

                    if currTarget.attrib['ref'] != target and currTran.text != listoftransitions[transition]:
                        #print 'not the same'
                        #print 'candidate transition:',listoftransitions[transition].text,'current transition: ', currTran.text
                        #print 'candidare target:', target, 'current target', currTarget.attrib['ref']

                        #create new file
                        MyName=inp+'MUT_CTN'+str(transition)+str(l)+str(i)+'.xml'
                        tree.write(MyName)
                        treex= ET.parse(MyName)
                        rootx = treex.getroot()
                        i = i + 1
                        tx = rootx.find(".//template[name='"+str(tem)+"']")

                        # mutation on target
                        tx.find("transition["+str(transition)+"]/target").attrib['ref']= target
                        #mutation on transition's name
                        tx.find("transition["+str(transition)+"]/label[@kind='synchronisation']").text = listoftransitions[transition].text

                        print 'new transition is', tx.find("transition["+str(transition)+"]/label[@kind='synchronisation']").text
                        print 'new target is', tx.find("transition["+str(transition)+"]/target").attrib['ref']
                        #reachability settings
                        assignment = tx.find("transition["+str(transition)+"]/label[@kind='assignment']")
                        if assignment != None:
                            assignment.text += ',\ntrap=true'
                            #print "in the assignment setting- if"
                        else:

                            ele = tx.find("transition["+str(transition)+"]")
                            assignmentAttrib = {"kind": "assignment", "x": "-20", "y": "-20"}
                            item = ET.Element("label")
                            item.text = "trap=true"
                            item.attrib= assignmentAttrib
                            ele.insert(3,item)

                            #ET.tostring(rootx)
                            #print el
                            #print "in the assignment setting - else"


                        #check if they are correctly mutated
                        #print 'mutated transition name is:', tx.find("transition["+str(transition)+"]/label[@kind='synchronisation']").text
                        #print 'mutated target is :', tx.find("transition["+str(transition)+"]/target").attrib['ref']

                        treex.write(MyName)
                        print 'Mutant', str(MyName),'is generated.'

                    #apply the verification by calling verifyta
                        if os.name == 'nt':
                            if CheckQuery(True, MyName):
                                Change_dir(MyName,'yes')
                            else:
                                Change_dir(MyName,'no')

                        else:
                            os.remove(MyName)



# ChangeSourceandName
def CSN(inp, tem):  # change source and  name
    print '-------------------------------------------------------------------------'

    print 'Mutation operator Change Source and Name (CSN) is started.'
    #dec = root.find('declaration')
    #dec.text += '\nbool trap= false; // reachability of the mutation canbe checked by this boolean variable'
    t = root.find(".//template[name='" + str(tem) + "']")
    listoflocations = [loc.attrib['id'] for loc in t.findall('location')]
    listoftransitions = [loc.find("label[@kind='synchronisation']") for loc in
                         t.findall('transition')]

    for l in range(len(listoflocations)):
        for transition in range(len(listoftransitions)):
            i = 0
            for source in listoflocations:

                # print 'l, trans, target', l, transition, source
                currSource = t.find("transition[" + str(transition) + "]/source")
                # print 'curtrans',currTrans.attrib['ref']
                currTran = t.find(
                    "transition[" + str(transition) + "]/label[@kind='synchronisation']")
                if currTran != None:  # we check if the transition is actually a synchronisation

                    if currSource.attrib['ref'] != source and currTran.text != listoftransitions[
                        transition]:
                        #print 'not the same'
                        #print 'candidate transition:', listoftransitions[
                          #  transition], 'current transition: ', currTran.text
                        #print 'candidare source:', source, 'current source', currSource.attrib[
                         #   'ref']

                        # create new file
                        MyName = inp + 'MUT_CSN' + str(transition) + str(l) + str(
                            i) + '.xml'
                        tree.write(MyName)
                        treex = ET.parse(MyName)
                        rootx = treex.getroot()
                        tx = rootx.find(".//template[name='" + str(tem) + "']")

                        # mutation on target
                        tx.find("transition[" + str(transition) + "]/source").attrib['ref'] = source
                        # mutation on transition's name
                        tx.find("transition[" + str(
                            transition) + "]/label[@kind='synchronisation']").text = \
                        listoftransitions[transition]

                        # reachability settings
                        assignment = tx.find(
                            "transition[" + str(transition) + "]/label[@kind='assignment']")
                        if assignment != None:
                            assignment.text += ',\ntrap=true'
                            #print "in the assignment setting- if"
                        else:
                            ele = tx.find("transition["+str(transition)+"]")
                            assignmentAttrib = {"kind": "assignment", "x": "-20", "y": "-20"}
                            item = ET.Element("label")
                            item.text = "trap=true"
                            item.attrib= assignmentAttrib
                            ele.insert(3,item)
                            # ET.tostring(rootx)
                            #print el
                            #print "in the assignment setting - else"

                        # check if they are correctly mutated
                        #print 'mutated transition name is:', tx.find("transition[" + str(
                         #   transition) + "]/label[@kind='synchronisation']").text
                        #print 'mutated source is :', tx.find("transition[" + str(transition) + "]/source").attrib['ref']

                        treex.write(MyName)
                        print 'Mutant', str(MyName),'is generated.'


                        # apply the verification by calling verifyta
                        if os.name == 'nt':
                            if CheckQuery(True, MyName): # true means that we have to check both queries: reachability and deadlock

                                Change_dir(MyName,'yes')
                            else:
                                Change_dir(MyName,'no')
                        i = i + 1

#remove actions
def RA(inp, tem):
    print '-------------------------------------------------------------------------'
    print 'Mutation operator Remove Actions (RA) is started.'
    timerStart=datetime.datetime.now()
    logger.info('RA for '+str(inp)+' '+str(tem)+' started.')
    #dec = root.find('declaration')
    #dec.text += '\nbool trap= false; // reachability of the mutation canbe checked by this boolean variable'
    t = root.find(".//template[name='" + str(tem) + "']")
    #listoflocations = [loc.attrib['id'] for loc in t.findall('location')]
    listoftransitions = [loc.find("label[@kind='synchronisation']") for loc in t.findall('transition')]
    #for l in range(len(listoflocations)):
    for transition in range(len(listoftransitions)):
                    # print 'l, trans, target', l, transition, source
        currTran = t.find(
            "transition[" + str(transition) + "]/label[@kind='synchronisation']")
        # create new file
        MyName = inp + 'MUT_RT' + str(transition) + '.xml'
        tree.write(MyName)
        treex = ET.parse(MyName)
        rootx = treex.getroot()
        tx = rootx.find(".//template[name='" + str(tem) + "']")

        # delete transition
        el=tx.find("transition[" + str(
            transition) + "]")
        tx.remove(el)

        # check if they are correctly mutated
        #print 'mutated transition name is:', tx.find("transition[" + str(
        #    transition) + "]/label[@kind='synchronisation']").text

        treex.write(MyName)
        print 'Mutant', str(MyName),'is generated.'

    # apply the verification by calling verifyta
        if os.name == 'nt':
            if CheckQuery(False,MyName):
                Change_dir(MyName, 'yes')
            else:
                Change_dir(MyName, 'no')
    timerStop = datetime.datetime.now()
    te = timerStop - timerStart
    logger.info('RA finnished.')
    logger.info(te)


# duplicate actions
def DA(inp, tem):
    print '-------------------------------------------------------------------------'

    print 'Mutation operator Duplicate Actions (DA) is started.'
    timerStart=datetime.datetime.now()
    logger.info('DA for '+str(inp)+' '+str(tem)+' started.')
    #dec = root.find('declaration')
    #dec.text += '\nbool trap= false; // reachability of the mutation canbe checked by this boolean variable'
    t = root.find(".//template[name='" + str(tem) + "']")
    listoflocations = [loc.attrib['id'] for loc in t.findall('location')]
    listoftransitions = [loc.find("label[@kind='synchronisation']") for loc in
                         t.findall('transition')]

    for transi in range(len(listoftransitions)):
        for newSource in range(len(listoflocations)):
            #i = 0
            for newtarget in range(len(listoflocations)):

                #print 'transi, listof transit', transi, listoftransitions[transi]
                currSource = t.find("transition[" + str(transi) + "]/source")
                # print 'curtrans',currTrans.attrib['ref']
                currtarget = t.find("transition[" + str(transi) + "]/target")
                currTran = t.find(
                    "transition[" + str(transi) + "]/label[@kind='synchronisation']")
                #print "current transition", currTran.text
                #print "transi, newsource and newtarget", transi, newSource, newtarget
                #print "cursource and cu target", currSource.attrib['ref'], currtarget.attrib['ref']
                if currTran != None:  # we check if the transition is actually a synchronisation

                    #print 'candidate transition:', transi, 'current transition: ', currTran.text
                    #print currSource.attrib['ref'], "to" ,currtarget.attrib['ref'], 'will change to', \
                     #   listoflocations[newSource],"to", listoflocations[newtarget]

                    # create new file
                    MyName = inp + 'DT' +'_tran'+ str(transi)+'_fromloc' + str(
                        newtarget) +'to_loc'+ str(newSource) + '.xml'
                    tree.write(MyName)
                    treex = ET.parse(MyName)
                    rootx = treex.getroot()
                    tx = rootx.find(".//template[name='" + str(tem) + "']")

                    # make a new transition

                    newTransition = tx.find(
                        "transition[" + str(transi) + "]")
                    copyelem = copy.deepcopy(newTransition)
                    #print 'copy element', copyelem
                    #mutate the copied element
                    tx.append(copyelem)
                    print "copy element target is: ", copyelem.find("target").attrib['ref']
                    copyelem.find("target").attrib['ref']= listoflocations[newtarget]
                    print"copy element traget is mutated to", copyelem.find("target").attrib['ref']

                    print "copy element source is: ", copyelem.find("source").attrib['ref']
                    copyelem.find("source").attrib['ref'] = listoflocations[newSource]
                    print"copy element source is mutated to", copyelem.find("source").attrib['ref']

                    # reachability settings
                    assignment = copyelem.find("label[@kind='assignment']")
                    #print 'assignment', assignment
                    if assignment != None:
                        assignment.text += ',\ntrap=true'
                     #   print "in the assignment setting- if"
                    else:

                        #ele = tx.find("transition[" + str(transi) + "]")
                        assignmentAttrib = {"kind": "assignment", "x": "-20", "y": "-20"}
                        item = ET.Element("label")
                        item.text = "trap=true"
                        item.attrib = assignmentAttrib
                        copyelem.insert(3, item)
                    print"copy element source is mutated to", copyelem.find("source").attrib['ref']
                    print"copy element traget is mutated to", copyelem.find("target").attrib['ref']
                        # ET.tostring(rootx)
                      #  print el
                       # print "in the assignment setting - else"


                    treex.write(MyName)
                    print 'Mutant', str(MyName), 'is made.'
                    # apply the verification by calling verifyta
                    # true means that we have to check both queries: reachability and deadlock
                    if os.name == 'nt':
                        if CheckQuery(True, MyName):

                            Change_dir(MyName,'yes')
                        else:
                            Change_dir(MyName,'no')
    timerStop = datetime.datetime.now()
    te = timerStop - timerStart
    logger.info('DA finnished.')
    logger.info(te)


 # exchange invariant and guard

#exchange invariant and guard
def EIG(inp, tem):
    print '-------------------------------------------------------------------------'

    print 'Mutation operator Exchange Invariant and Guard (EIG) is started.'
    t = root.find(".//template[name='" + str(tem) + "']")
    listoflocations = [loc.attrib['id'] for loc in t.findall('location')]
    listoftransitions = [loc.find("label[@kind='synchronisation']") for loc in
                         t.findall('transition')]
    #for each location, check whether it has an invariant
    for l in range(len(listoflocations)):
        i = 0
        locationObject = t.find("location["+str(l)+"]")#/label[@kind='invariant']")
        if locationObject.find("label[@kind='invariant']") != None:
            #print 'location has an inv', locationObject
            locName = locationObject.attrib['id']
            locInv = locationObject.find("label[@kind='invariant']").text
            #print 'the name is', locName
            # find all transitions which are emitted from this location

            for alltran in range(len(listoftransitions)):
                print 'all', alltran, range(len(listoftransitions)-1), len(listoftransitions)
                if listoftransitions[alltran] != None:
                    if t.find("transition["+str(alltran)+"]/source").attrib['ref']==locName:
                        #print 'here we are'

                        #create new file
                        MyName = inp + 'MUT_EIG' + str(l) + str(i) + '.xml'
                        i=i+1
                        tree.write(MyName)
                        treex = ET.parse(MyName)
                        rootx = treex.getroot()

                        txx = rootx.find(".//template[name='" + str(tem) + "']")
                        # check if the transition has a guard
                        #print 'check if ', locName
                        currentSource = txx.find("transition["+str(alltran)+"]/source").attrib['ref']
                        currentGuard = txx.find("transition["+str(alltran)+"]/label[@kind='guard']")
                        # if a transition is from the current location and it has guard
                        if currentSource == locName and currentGuard != None:

                            #print 'before inv and guard:', locInv, currentGuard
                            txx.find("location[" + str(l) + "]/label[@kind='invariant']").text = currentGuard.text
                            #print 'new invariant is', txx.find("location[" + str(l) + "]/label[@kind='invariant']").text
                            currentGuard.text = locInv
                            #print 'new guard is:', txx.find("transition["+str(alltran)+"]/label[@kind='guard']").text

                            # reachability settings
                            assignment = txx.find(
                                "transition[" + str(alltran) + "]/label[@kind='assignment']")
                            if assignment != None:
                                assignment.text += ',\ntrap=true'
                                #print "in the assignment setting- if"
                            else:
                                ele = txx.find("transition[" + str(alltran) + "]")
                                assignmentAttrib = {"kind": "assignment", "x": "-20", "y": "-20"}
                                el = ET.SubElement(ele, "label", attrib=assignmentAttrib)
                                el.text = "trap=true"
                                # ET.tostring(rootx)
                                #print el
                                #print "in the assignment setting - else"
                            treex.write(MyName)
                            print 'Mutant', str(MyName),'is generated.'
                            # check the reachability and deadlockfree
                            if os.name == 'nt':
                                if CheckQuery(True, MyName):

                                    Change_dir(MyName, 'yes')
                                else:
                                    Change_dir(MyName, 'no')
                        else:
                            os.remove(MyName)





if __name__ == "__main__":
    main(sys.argv[1:])
