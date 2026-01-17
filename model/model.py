import copy

import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):

        self.teams= []

        self.G = nx.Graph()
        self.salary_map = {}
        self.team_map = {}

        self.best_path = []
        self.best_weight = 0
        self.K= 3

    def get_years(self):
        return DAO.get_years_from_1980()

    def load_teams(self, year):
        self.teams= DAO.get_teams_by_year(year)
        return self.teams #lista di oggetti Team

    def build_graph(self, year):
        self.G.clear()

        self.salary_map = DAO.get_team_salary(year) # dizionario team_id : salario totale

        for i, t1 in enumerate(self.teams):
            for t2 in self.teams[i+1:]: #considero tutte le coppie di squadre senza ripetizioni, evita (t1, t1)
                w= self.salary_map.get(t1.id, 0) + self.salary_map.get(t2.id, 0) #se una squadra non ha salario uso 0
                self.G.add_edge(t1, t2, weight=w)

        #mappa id -> Team
        for t in self.teams: #t è un oggetto Team
            self.team_map[t.id] = t

    def get_neighbors(self, team):
        neighbors = []
        for n in self.G.neighbors(team):
            w= self.G[team][n]['weight']
            neighbors.append((n, w)) #[(nodo1, peso_arco1), (nodo2, peso_arco2), ...]
        return sorted(neighbors, key=lambda x: x[1], reverse=True)

    def compute_best_path(self, start):
        self.best_path = []
        self.best_weight = 0
        self._ricorsione([start], 0, float("inf"))
        return self.best_path, self.best_weight

    def _ricorsione(self, path, weight, last_edge_weight):
        last= path[-1] #ultimo nodo del cammino da cui provo ad estendermi

        # condizione di terminazione
        if weight > self.best_weight:
            self.best_weight = weight
            self.best_path = copy.deepcopy(path)

        vicini= self.get_neighbors(last)
        neighbors = [] #lista dei vicini che rispettano i vincoli
        counter= 0

        #vincoli
        for node, edge_w in vicini:
            if node in path: #non torno su un nodo già visitato
                continue
            if edge_w <= last_edge_weight: #cammino con pesi degli archi decrescenti
                neighbors.append((node, edge_w))
                counter += 1
                if counter == self.K:
                    break

        #ciclo di ricorsione
        for node, edge_w in neighbors:
                path.append(node)
                self._ricorsione(path, weight + edge_w, edge_w)
                path.pop()

