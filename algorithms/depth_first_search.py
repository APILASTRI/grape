# coding=utf-8

from lib.algorithm import Algorithm

class DepthFirstSearch(Algorithm):
    def __init__(self, graph):
        Algorithm.__init__(self, graph)

    def run(self):
        first = self.vertex_list[0] # consideremos o primeiro vértice criado como origem, por enquanto
        goal = self.vertex_list[-1]  # consideremos o último vértice criado como origem, por enquanto

        stack = [] # utlizaremos uma pilha para nossa busca em profundidade

        # adicionamos nosso inicio na pilha
        stack.append((first, None)) # uma tupla (vertice, aresta). Como este é o inicio não utilizamos nenhuma aresta para alcançá-lo

		# marcamos todos os vértices como não visitados
        for e in self.edge_list:
            self.set_attribute(e, 'visited', False)

        while len(stack) > 0:
            pop = True
            print stack

            node = stack[-1]
            if node[1]:
                self.set_attribute(node[1], 'visited', True)
            self.check(node[0])
            self.check(node[1])
            self.show()

            if node[0].id == goal.id:
                rtn = node[0]
                break
            else:
                pop_it = True
                for edge in node[0].edge_list:
                    if self.get_attribute(edge, 'visited') == 'False':
                        pop_it = False
                        break

                if pop_it:
                    self.uncheck(node[0])
                    self.uncheck(node[1])
                    stack.pop()

            for edge in node[0].edge_list:
                if self.get_attribute(edge, 'visited') == 'False':
                    if edge.start == node[0]:
                        print "app1"
                        stack.append((edge.end, edge))
                    else:
                        print "app2"
                        stack.append((edge.start,edge))

