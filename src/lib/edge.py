class Edge(object):
    def __init__(self, id, start, end, bidirectional):
        self.title = ""
        self.color = [0, 0, 0]
        self.width = 1
        self.id = id
        self.start = start
        self.end = end
        self.bidirectional = bidirectional

        start.touching_edges.append(self)
        end.touching_edges.append(self)

        start.add_edge(self)

        if self.bidirectional:
            end.add_edge(self)

    def touches(self, vertex):
        return vertex == self.start or vertex == self.end
