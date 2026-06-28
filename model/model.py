import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._idMapO = {}
        self._grafo = nx.DiGraph()

    def getAllStores(self):
        return DAO.getAllStores()

    def getAllOrdini(self,store):
        return DAO.getAllOrdini(store)

    def creaGrafo(self, store, k):
        self._grafo.clear()
        self._ordini = DAO.getAllOrdini(store)

        for o in self._ordini:
            self._idMapO[o.order_id] = o

        self._grafo.add_nodes_from(self._ordini)

        allEdges = DAO.getAllArchi(store, k, self._idMapO)
        for e in allEdges:
            self._grafo.add_edge(e.o1, e.o2, peso=e.peso)

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getTop5archi(self):
        return sorted(self._grafo.edges(data=True), key=lambda x: x[2]['peso'], reverse=True)[:5]

    def getCammino(self, sourceStr):
        source = self._idMap[int(sourceStr)]
        lp = []

        # for source in self._graph.nodes:
        tree = nx.dfs_tree(self._grafo, source)
        nodi = list(tree.nodes())

        for node in nodi:
            tmp = [node]

            while tmp[0] != source:
                pred = nx.predecessor(tree, source, tmp[0])
                tmp.insert(0, pred[0])

            if len(tmp) > len(lp):
                lp = copy.deepcopy(tmp)

        return lp
