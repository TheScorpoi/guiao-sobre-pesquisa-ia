from constraintsearch import *

amigos = ["Andre", "Bernardo", "Claudio"]   

def constraint(a1, t1, a2, t2):
    b1, c1 = t1
    b2, c2 = t2
    
    if b1 == b2 or c1 == c2:
        return False
    
    if "Bernardo" in [b1, b2]:
        if ("Bernardo", "Claudio") in [t1, t2]:
            return False
        else:    
            return True
    return True

def make_constraint_graph():
    return {(A,B):constraint for A in amigos for B in amigos if A != B}

def make_domain(amigos):
    return {A : [(B,C) for B in amigos for C in amigos if A not in [B, C] and B != C ]for A in amigos}
cs = ConstraintSearch(make_domain(amigos), make_constraint_graph())

print(cs.search())
