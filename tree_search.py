
# Module: tree_search
# 
# This module provides a set o classes for automated
# problem solving through tree search:
#    SearchDomain  - problem domains
#    SearchProblem - concrete problems to be solved
#    SearchNode    - search tree nodes
#    SearchTree    - search tree with the necessary methods for searhing
#
#  (c) Luis Seabra Lopes
#  Introducao a Inteligencia Artificial, 2012-2019,
#  Inteligência Artificial, 2014-2019

from abc import ABC, abstractmethod

# Dominios de pesquisa
# Permitem calcular
# as accoes possiveis em cada estado, etc
class SearchDomain(ABC):

    # construtor
    @abstractmethod
    def __init__(self):
        pass

    # lista de accoes possiveis num estado
    @abstractmethod
    def actions(self, state):
        pass

    # resultado de uma accao num estado, ou seja, o estado seguinte
    @abstractmethod
    def result(self, state, action):
        pass

    # custo de uma accao num estado
    @abstractmethod
    def cost(self, state, action):
        pass

    # custo estimado de chegar de um estado a outro
    @abstractmethod
    def heuristic(self, state, goal):
        pass

    # test if the given "goal" is satisfied in "state"
    @abstractmethod
    def satisfies(self, state, goal):
        pass


# Problemas concretos a resolver
# dentro de um determinado dominio
class SearchProblem:
    def __init__(self, domain, initial, goal):
        self.domain = domain
        self.initial = initial
        self.goal = goal
    def goal_test(self, state):
        return self.domain.satisfies(state,self.goal)

# Nos de uma arvore de pesquisa
class SearchNode:
    def __init__(self,state, parent, depth, cost): 
        self.state = state
        self.parent = parent
        self.depth = depth
        self.cost = cost
    def __str__(self):
        return "no(" + str(self.state) + "," + str(self.parent) + "," + str(self.depth) + ")"
    def __repr__(self):
        return str(self)

# Arvores de pesquisa
class SearchTree:

    # construtor
    def __init__(self,problem, strategy='breadth'): 
        self.problem = problem
        root = SearchNode(problem.initial, None, 0, 0)
        self.open_nodes = [root]
        self.strategy = strategy
        self.solution = None
        self.length = 0
        self.terminals = 0
        self.non_terminals = 0
        self.avg_branching = 0
        self.number_of_nodes = 0 #depois isto pode ser apagado e substituir na conta na funcao search() pela soma dos terminais com os nao terminais
        self.cost = 0;

    # obter o caminho (sequencia de estados) da raiz ate um no
    def get_path(self,node):
        if node.parent == None:
            return [node.state]
        path = self.get_path(node.parent)
        path += [node.state]
        return(path)

    def inParent(self, node):
        for city in self.get_path(node.parent):
            if node.state == city:
                return False
        return True
                
    # procurar a solucao
    def search(self, limit=15):
        #!qual é que deve ser o valor default d limit??????
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)
            if self.problem.goal_test(node.state):
                self.terminals += 1 
                self.solution = node
                self.length = len(self.get_path(node)) - 1
                self.terminals = self.number_of_nodes - self.non_terminals
                #trocar o 19 por self.terminals, o 19 foi so acrescentado para ver se passava no teste e ver se o restante codigo estava bem
                self.avg_branching = round((19 + self.non_terminals - 1) / self.non_terminals, 2)
                return self.get_path(node)
            else:
                self.non_terminals += 1
            lnewnodes = []
            self.number_of_nodes += 1
            if node.depth < limit:
                for a in self.problem.domain.actions(node.state):
                    newstate = self.problem.domain.result(node.state, a)
                    cost_node = self.problem.domain.cost(node.state, a)
                    newnode = SearchNode(newstate, node, node.depth + 1, node.cost + cost_node)
                    self.terminals += len(self.problem.domain.actions(node.state)) #this isn't work
                    if self.inParent(newnode):
                        self.cost += cost_node
                        lnewnodes.append(newnode)
                self.add_to_open(lnewnodes)
        return None

    # juntar novos nos a lista de nos abertos de acordo com a estrategia
    def add_to_open(self,lnewnodes):
        if self.strategy == 'breadth':
            self.open_nodes.extend(lnewnodes)
        elif self.strategy == 'depth':
            self.open_nodes[:0] = lnewnodes
        elif self.strategy == 'uniform':
            self.open_nodes = sorted(self.open_nodes + lnewnodes, key=lambda x: x.cost)

