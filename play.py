import mcts

if __name__ == "__main__":
    """ Доигрывает игру между двумя ИИ до конца.
    """

    results = [0, 0, 0]

    for i in range(1):
        winner = mcts.UCTPlayGame()
        results[winner] += 1

    print("results " + str(results))
