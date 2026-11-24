from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):

    def search(self, initial: State) -> SearchResult:
        fronteira = deque()
        fronteira.append(initial)
        alcancados = set()
        alcancados.add(initial.tiles)
        n_expandidos, n_gerados, tam_max = 0, 1, 1

        while len(fronteira) > 0:
            no = fronteira.popleft()

            if no.is_goal:
                return SearchResult(no, n_expandidos, n_gerados, tam_max, no.cost)

            n_expandidos += 1
            for vizinho in no.neighbors():
                if vizinho.tiles in alcancados:
                    continue
                alcancados.add(vizinho.tiles)
                fronteira.append(vizinho)
                n_gerados += 1

            if len(fronteira) > tam_max:
                tam_max = len(fronteira)

        return SearchResult(None, n_expandidos, n_gerados, tam_max)
