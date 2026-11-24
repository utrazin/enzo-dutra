from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        pilha = [initial]
        melhor_prof = {initial.tiles: initial.cost}
        n_expandidos, n_gerados, tam_max = 0, 1, 1

        while len(pilha) > 0:
            no = pilha.pop()

            if melhor_prof[no.tiles] < no.cost:
                continue

            if no.is_goal:
                return SearchResult(no, n_expandidos, n_gerados, tam_max, no.cost)

            if no.cost == self.depth_limit:
                continue

            n_expandidos += 1
            for vizinho in no.neighbors():
                prof_vista = melhor_prof.get(vizinho.tiles)
                if prof_vista is not None and prof_vista <= vizinho.cost:
                    continue
                melhor_prof[vizinho.tiles] = vizinho.cost
                pilha.append(vizinho)
                n_gerados += 1

            if len(pilha) > tam_max:
                tam_max = len(pilha)

        return SearchResult(None, n_expandidos, n_gerados, tam_max)
