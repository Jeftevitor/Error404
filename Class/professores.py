from Models.Personagem import Personagem

class Professores(Personagem):
    def __init__(self, x, y, nome, seta, sprite):
        super().__init__(x, y, nome, seta)

        self.vida = 50
        self.sprite = sprite
        
    def desenhar(self, tela):
        if self.seta == 'cima':
            tela.blit(self.sprite, (self.x, self.y))

        elif self.seta == 'baixo':
            tela.blit(self.sprite, (self.x, self.y))

        elif self.seta == 'esquerda':
            tela.blit(self.sprite, (self.x, self.y))

        elif self.seta == 'direita':
            tela.blit(self.sprite, (self.x, self.y))

        # IDLE
        else:
            tela.blit(self.sprite, (self.x, self.y))