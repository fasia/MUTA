The tool MUTTA is for generating mutation models form Uppaal model. It also optimizes the number of mutation models by dividing them into two groups of Valid and Invalid mutant models. 
A valid mutant model is the one which passes:
1- deadlockfree rule in TCTL
2- The mutant part is accessible (not implemented yet)
********************************
Implemented Mutation Operators :

CN : Change Name of a transition
CS: Change Source location of a transition
CT: Change Traget location of a transition
CG: Change Guard
NG: Negate Guard
C_I: Change Invariant

********************************
To run MUTTA tool:

- open cmd in MUTTA folder
- write mut_opt.py -i <inputfile.xml> -t <name of the template for mutation> -q <query.q>

it will make two folders one for valid models and one for invalid models. 

********************************
example:mut_opt.py -i LightContr.xml -t Interface -q query.q

********************************

Faezeh Siavashi 11.09.2015