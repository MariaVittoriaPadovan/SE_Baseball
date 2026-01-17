import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model


    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        # TODO
        try:
            year= int(self._view.dd_anno.value)
        except Exception:
            self._view.show_alert("Anno non valido")
            return

        self._model.build_graph(year)

    def handle_dettagli(self, e):
        """ Handler per gestire i dettagli """""
        # TODO
        team_id= int(self._view.dd_squadra.value)

        self._view.txt_risultato.controls.clear()
        for n, w in self._model.get_neighbors(self._model.team_map[team_id]):
            self._view.txt_risultato.controls.append(
                ft.Text(f"{n} - peso {w}")
            )
        self._view.update()

    def handle_percorso(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del percorso """""
        # TODO
        team_id = self._view.dd_squadra.value
        start= next(t for t in self._model.teams if t.id == int(team_id))
        '''
        cerca nella lista self._model.teams (lista di tutti gli oggetti Team) l’oggetto Team con id == team_id
        next(...) restituisce il primo che trova
        ora start è un nodo del grafo
        '''
        path, weight = self._model.compute_best_path(start)

        self._view.txt_risultato.controls.clear()
        for i in range(len(path) - 1):
            #scorre il cammino a coppie consecutive: path[0] → path[1], path[1] → path[2]
            w= self._model.G[path[i]][path[i+1]]['weight']
            self._view.txt_risultato.controls.append(
                ft.Text(f"{path[i]} -> {path[i+1]} (peso {w})")
            )
        self._view.txt_risultato.controls.append(
            ft.Text(f"Peso totale: {weight}")
        )
        self._view.update()

    """ Altri possibili metodi per gestire di dd_anno """""
    # TODO
    def get_years(self):
        return self._model.get_years()


    def handle_year_change(self, e):
        '''Handler per gestire on_change del dropdown dd_anno'''
        year= int(self._view.dd_anno.value)
        teams= self._model.load_teams(year)

        self._view.txt_out_squadre.controls.clear()
        self._view.txt_out_squadre.controls.append(
            ft.Text(f"Numero squadre: {len(teams)}")
        )
        for t in teams:
            self._view.txt_out_squadre.controls.append(ft.Text(t))

        self._view.dd_squadra.options= [ft.dropdown.Option(key=str(t.id), text= t) for t in teams]

        self._view.update()
