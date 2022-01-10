from constraintsearch import *

region = ['A', 'B', 'C', 'D', 'E']
colors = ['red', 'blue', 'green', 'yellow', 'white']

dict = {'A':'BED', 'B':'AEC', 'C':'BED', 'D':'AEC', 'E':'ABCD'}

def constrain(p1, c1, p2, c2):
    return c1 !=  c2
    

def make_constraint_graph(region, dict):
    return { (X,Y):constrain for X in region for Y in dict[X]}    

def make_domains(region):
    return { r:colors for r in region}

cs = ConstraintSearch(make_domains(region), make_constraint_graph(region, dict))

print(cs.search())
