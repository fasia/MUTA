__author__ = 'fsiavash'

import sys, getopt
import xml.etree.ElementTree as ET
import os.path
import copy
from copy import deepcopy
import subprocess
from subprocess import call
import re
import shutil


# make different folders for each MO
currpath= os.getcwd()
print("now ",currpath)

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

    make_folders(inputfile[:-4])

    # define a global var for the tree and its root
    global root, tree
    tree = ET.parse(inputfile)
    root = tree. getroot()

    # get all transitions in the given template
    get_transitions(inputfile[:-4], templatename)


def make_folders(inp):
    global Address_Invalid_Mut, Address_Valid_Mut
    Address_Valid_Mut= '/Mutants_'+inp+'_Valid/'
    Address_Invalid_Mut = '/Mutants_'+inp+'_INValid/'

def get_transitions(inp, template):
    r = root.find("template[@name="]")
    print 'template is:', r

if __name__ == "__main__":
    main(sys.argv[1:])