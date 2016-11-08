import tree
import random
from game import *

def UCT(rootstate, itermax, verbose = False):
    """ Производит UCT поиск не более заданного числа итераций (itermax),
        начиная с заданного положения (rootstate)
        Возвращает лучший ход среди потомков rootstate
        Предполагает наличие двух противоборствующих игроков (игрок 1 начинает).
        Результатом игры могут быть значения из [0.0, 1.0]
    """

    rootnode = tree.Node(state=rootstate)

    for i in range(itermax):
        node = rootnode
        state = rootstate.Clone()

        #if (verbose):
           # print ("\tSelect stage")

        # Выбор (Select)
        while node.untriedMoves == [] and node.childNodes != []:  # узел полностью изучен и не лист (терминальный)
            node = node.UCTSelectChild()
            state.DoMove(node.move)

        #if (verbose):
         #   print ("\tExpand stage")

        # Расширение (Expand)
        if node.untriedMoves != []:  # можем расширять (т.е. есть допустимые ходы)
            m = random.choice(node.untriedMoves)
            state.DoMove(m)
            node = node.AddChild(m, state)  # добавить потомка в поддерево

        #if (verbose):
            #print ("\tRollout stage")

        # Симуляция (Rollout)
        while state.GetMoves() != []:  # пока есть допустимые ходы
            state.DoMove(random.choice(state.GetMoves()))

        #if (verbose):
         #   print ("\tBackpropagate stage")

        # Обратное распространиение (Backpropagate)
        while node != None:  # обратное распространиение от добавленного узла до корня дерева
            node.Update(state.GetResult(node.playerJustMoved))  # получаем результат симуляции
            node = node.parentNode

    sortedChildren = sorted(rootnode.childNodes, key=lambda c: c.visits)  # сортируем по посещениям

    # При возвращении дерева некотороая информация может быть опущена
    if (verbose):
        print(rootnode.TreeToString(0))
    else:
        print(rootnode.ChildrenToString())

    return sortedChildren[-1].move  # возвращщение хода, который был посещен

def UCTPlayGame():
    """ Разыгрывание простой игры между двумя UCT игроками, у которых задано разное количество итераций.
    """
    state = NimState(12)

    while (state.GetMoves() != []):
        print(str(state))
        if state.playerJustMoved == 1:
            m = UCT(rootstate=state, itermax=10, verbose=True)  # play with values for itermax and verbose = True
        else:
            m = int(input('Enter value\n'))
        print("Best Move: " + str(m) + "\n")
        state.DoMove(m)
    if state.GetResult(state.playerJustMoved) == 1.0:
        print("Player " + str(state.playerJustMoved) + " wins!")
        return state.playerJustMoved
    elif state.GetResult(state.playerJustMoved) == 0.0:
        print("Player " + str(3 - state.playerJustMoved) + " wins!")
        return 3 - state.playerJustMoved
    else:
        print("Nobody wins!")
        return 0
