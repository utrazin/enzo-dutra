from __future__ import annotations
from typing import List, Optional, Tuple


GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)


class State:
    """Representa um estado do 8-puzzle como tupla imutável de 9 inteiros (0 = espaço vazio)."""

    def __init__(self, tiles: Tuple[int, ...], parent: Optional["State"] = None, action: Optional[str] = None, cost: int = 0):
        if len(tiles) != 9 or set(tiles) != set(range(9)):
            raise ValueError("Estado inválido: deve conter exatamente os valores 0-8.")
        self.tiles = tiles
        self.parent = parent
        self.action = action
        self.cost = cost

    @property
    def is_goal(self) -> bool:
        return self.tiles == GOAL_STATE

    @property
    def blank_index(self) -> int:
        return self.tiles.index(0)

    def neighbors(self) -> List["State"]:
        """Retorna os estados filhos válidos a partir deste estado."""
        pos_vazio = self.blank_index
        lin, col = divmod(pos_vazio, 3)
        direcoes = (("cima", -1, 0), ("baixo", 1, 0), ("esquerda", 0, -1), ("direita", 0, 1))

        resultado = []
        for nome, d_lin, d_col in direcoes:
            l, c = lin + d_lin, col + d_col
            if l < 0 or l > 2 or c < 0 or c > 2:
                continue
            destino = 3 * l + c
            novo = list(self.tiles)
            novo[pos_vazio] = novo[destino]
            novo[destino] = 0
            resultado.append(State(tuple(novo), parent=self, action=nome, cost=self.cost + 1))
        return resultado

    def path(self) -> List["State"]:
        """Retorna a sequência de estados do estado inicial até este."""
        sequencia = []
        no = self
        while no:
            sequencia.insert(0, no)
            no = no.parent
        return sequencia

    def actions(self) -> List[str]:
        """Retorna a sequência de ações do estado inicial até este."""
        return [no.action for no in self.path() if no.parent is not None]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, State) and self.tiles == other.tiles

    def __hash__(self) -> int:
        return hash(self.tiles)

    def __lt__(self, other: "State") -> bool:
        return self.cost < other.cost

    def __repr__(self) -> str:
        t = self.tiles
        return (
            f"+-------+\n"
            f"| {t[0]} {t[1]} {t[2]} |\n"
            f"| {t[3]} {t[4]} {t[5]} |\n"
            f"| {t[6]} {t[7]} {t[8]} |\n"
            f"+-------+"
        ).replace("0", " ")
