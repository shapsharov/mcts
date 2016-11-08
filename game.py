class NimState:
    """ Игровое поля для Ним. В Ним, игроки поочередно берут 1, 2 или 3 доли,
        победителем считается тот, кто взял последним.
        Любая начальная позиция соответствующая 4n+k, где k = 1,2,3 является выигрышной для игрока 1.
        Любая начальная позиция соответствующая 4n - выйгрышна для игрока 2.
    """
    def __init__(self, ch):
        self.playerJustMoved = 2  # At the root pretend the player just moved is p2 - p1 has the first move
        self.chips = ch

    def Clone(self):
        """ Создание копии игрового поля.
        """
        st = NimState(self.chips)
        st.playerJustMoved = self.playerJustMoved
        return st

    def DoMove(self, move):
        """ Обновление игрового поля (совершение хода).
            Обязательно нужно передать ход оппоненту.
        """
        assert move >= 1 and move <= 3 and move == int(move)
        self.chips -= move
        self.playerJustMoved = 3 - self.playerJustMoved

    def GetMoves(self):
        """ Получить все возможные ходы для данного состояния.
        """
        return list(range(1, min([4, self.chips + 1])))

    def GetResult(self, playerjm):
        """ Получить результат игры с точки зрения текущего игрока.
        """
        assert self.chips == 0
        if self.playerJustMoved == playerjm:
            return 1.0  # текущий игрок берет последнюю долю и побеждает
        else:
            return 0.0  # следующий игрок беред последнюю долю и побеждает

    def __repr__(self):
        s = "Chips:" + str(self.chips) + " JustPlayed:" + str(self.playerJustMoved)
        return s
