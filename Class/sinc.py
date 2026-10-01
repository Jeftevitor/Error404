class Sinc:
    def __init__(self, jogo):
        self.jogo = jogo

    def verificar_sinc(self, setas):
        setas[:] = [seta for seta in setas if seta.y <= self.jogo.altura + 200]
