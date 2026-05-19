class Seta:

    def __init__(self, x, y, direcao, velocidade=5):

        self.x = x
        self.y = y
        self.direcao = direcao
        self.velocidade = velocidade

        self.acertada = False

    def mover(self):
        self.y += self.velocidade