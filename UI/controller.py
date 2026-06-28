import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillddStore(self):
        stores = self._model.getAllStores()

        storesDD = list(
            map(lambda x: ft.dropdown.Option(data=x, key=x.store_name, on_click=self._storeScelto), stores))
        self._view._ddStore.options = storesDD
        self._view.update_page()

    def _storeScelto(self, e):
        # salva in una variabile di classe la scelta dell'utente
        self._storeValue = e.control.data



    def fillddNodi(self,e):
        nodi = list(self._model._grafo.nodes)

        ordiniDD = list(
            map(lambda x: ft.dropdown.Option(data=x, key=str(x.order_id),text=f"Ordine #{x.order_id}", on_click=self._ordineScelto), nodi))
        self._view._ddNode.options = ordiniDD
        self._view.update_page()

    def _ordineScelto(self, e):
        # salva in una variabile di classe la scelta dell'utente
        self._ordineValue = e.control.data

    def handleCreaGrafo(self, e):
        store = self._storeValue
        k = self._view._txtIntK.value


        if store is None:
            self._view.txt_result.clean()
            self._view.txt_result.controls.append(ft.Text("selezionare uno store"))
            self._view.update_page()
            return

        self._model.creaGrafo(store, k)

        n, m = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"grafo correttamnete creato, è formato da {n} nodi e {m} archi"))
        self.handleDettagli(e)
        self.fillddNodi(e)
        self._view.update_page()


    def handleCerca(self, e):
        if self._view._ddNode.value is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Selezionare nodo di partenza."))
            self._view.update_page()
            return
        nodes = self._model.getCammino(self._view._ddNode.value)

        self._view.txt_result.controls.append(ft.Text(f"Nodo di partenza : {self._view._ddNode.value}"))
        for n in nodes:
            self._view.txt_result.controls.append(ft.Text(n))
        self._view.update_page()


    def handleRicorsione(self, e):
        pass

    def handleDettagli(self, e):
        top5 = self._model.getTop5archi()
        self._view.txt_result.controls.append(ft.Text(f"i 5 archi di peso maggiore:"))
        for arco in top5:
            self._view.txt_result.controls.append(ft.Text(f"{arco[0]} --> {arco[1]} ( {arco[2]["peso"]})"))
