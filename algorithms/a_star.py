import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        total = 0
        for i in range(9):
            peca = state.tiles[i]
            if peca != 0:
                destino = peca - 1
                total += abs(i // 3 - destino // 3) + abs(i % 3 - destino % 3)
        return total

    def search(self, initial: State) -> SearchResult:
        ordem = 0
        heap = []
        heapq.heappush(heap, (self.heuristic(initial), ordem, initial))
        g = {initial.tiles: initial.cost}
        n_expandidos, n_gerados, tam_max = 0, 1, 1

        while len(heap) > 0:
            f, _, no = heapq.heappop(heap)

            if no.cost > g[no.tiles]:
                continue

            if no.is_goal:
                return SearchResult(no, n_expandidos, n_gerados, tam_max, no.cost)

            n_expandidos += 1
            for vizinho in no.neighbors():
                if vizinho.tiles in g and g[vizinho.tiles] <= vizinho.cost:
                    continue
                g[vizinho.tiles] = vizinho.cost
                ordem += 1
                heapq.heappush(heap, (vizinho.cost + self.heuristic(vizinho), ordem, vizinho))
                n_gerados += 1

            if len(heap) > tam_max:
                tam_max = len(heap)

        return SearchResult(None, n_expandidos, n_gerados, tam_max)
