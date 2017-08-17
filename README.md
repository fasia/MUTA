# MUTA
Mutation generator from Uppaal Timed Automata
MuUTA is a tool for generating mutations from Uppaal timed automata. It contains different mutation operators which manipulate a given UTA model and create various versions of the model with slight changes in each version. 
The tool validates the generated mutants based on two main verification properties: deadlockfree and reachability

A valid mutant model is the one which passes:
1- deadlockfree rule in TCTL
2- and reahability property

the tool divides the generated mutants into two groups: invalid and valid. Valid mutants are suitable for model-based test generation, and the invalid mutants will be discarded.
********************************
Implemented Mutation Operators in Version 1.0:
(first order mutants)
CN : Change Name of a transition
CS: Change Source location of a transition
CT: Change Traget location of a transition
CG: Change Guard
NG: Negate Guard
CI: Change Invariant

********************************
Implemented Mutation Operators in Version 1.1:
(higher-order mutants)
STS : Switch Target and Source of a transition
CTN: Change Target and name of a transition
CSN : change Source and name of a transition
DT : duplicate a transition
RT : Remove a Transition
EIG : Exchange Invariant and Guard 

*********************************
To run MUTTA tool:

- open cmd in MUTTA folder
- write mut_opt.py -i <inputfile.xml> -t <name of the template for mutation> -q <query.q>

it will make two folders one for valid models and one for invalid models. 

********************************
example:MuUTA.py -i LightContr.xml -t Interface -q query.q

********************************

Faezeh Siavashi 17.08.2017
