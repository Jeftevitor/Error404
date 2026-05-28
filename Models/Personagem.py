class Personagem:
    def __init__(self, x, y, nome, seta):
        self.x = x
        self.y = y
        self.nome = nome
        self.seta = seta

    def direcao(self):
        if self.seta == 'esquerda':
            return 'esquerda'

        elif self.seta == 'direita':
            return 'direita'

        elif self.seta == 'baixo':
            return 'baixo'

        elif self.seta == 'cima':
            return 'cima'