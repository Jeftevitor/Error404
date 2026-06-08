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
    
    def desenhar(self, tela):
        if self.seta == 'cima':
            tela.blit(self.sprite, (self.x, self.y))

        elif self.seta == 'baixo':
            tela.blit(self.sprite, (self.x, self.y))

        elif self.seta == 'esquerda':
            tela.blit(self.sprite, (self.x, self.y))

        elif self.seta == 'direita':
            tela.blit(self.sprite, (self.x, self.y))
            
        elif self.estado == 'morrer':
            tela.blit(self.sprite, (self.x, self.y))
        
        # IDLE 
        else:
            tela.blit(self.sprite, (self.x, self.y))