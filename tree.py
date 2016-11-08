from math import sqrt, log
class Node:
    """ Узел дерева игры. NB: победа всегда считается с точки зрания текущего игрока (playerJustMoved).
        Ломается, если не указано состояние (игра).
    """
    def __init__(self, move=None, parent=None, state=None):
        self.move = move  # ход приведщий к этому узлу. "None" - для корня
        self.parentNode = parent  # "None" - для корня
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.GetMoves()  # потенциальные потомки
        self.playerJustMoved = state.playerJustMoved  # единственное свойство, которое будем вызывать извне

    def UCTSelectChild(self):
        """ Используется формула UCB1 для выбора потомка.
        """
        s = sorted(self.childNodes, key=lambda c: c.wins/c.visits + sqrt(2*log(self.visits)/c.visits))[-1]
        return s

    def AddChild(self, m, s):
        """ Переносим m из untriedMoves в нового потомка.
            Возвращаем новый узел (добавленный потомок)
        """
        n = Node(move=m, parent=self, state=s)
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n

    def Update(self, result):
        """ Обновляем информацию об узле: обновляем счетчик посещений и результат.
            Результат должен быть представлен с точки зрения текущего игрока.
        """
        self.visits += 1
        self.wins += result

    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/" + str(self.visits) + " U:" + str(self.untriedMoves) + "]"

    def TreeToString(self, indent):
        s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
             s += c.TreeToString(indent+1)
        return s

    def IndentString(self, indent):
        s = "\n"
        for i in range(1, indent+1):
            s += "| "
        return s

    def ChildrenToString(self):
        s = ""
        for c in self.childNodes:
             s += str(c) + "\n"
        return s