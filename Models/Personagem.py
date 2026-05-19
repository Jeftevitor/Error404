class Personagem:
    def __init__(self, x, y, nome, sprite):
        self.x = x
        self.y = y
        self.nome = nome
        self.sprite = sprite

    def desenhar(self, tela):
        tela.blit(self.sprite, (self.x, self.y))
        