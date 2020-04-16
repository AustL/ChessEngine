class StartGame(Exception):
    pass


class EndGame(Exception):
    def __init__(self, result):
        self.result = result


class ShowMenu(Exception):
    pass
