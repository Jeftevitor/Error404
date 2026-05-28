from Models.personagem import Personagem

class Principal(Personagem):

    def __init__(self, x, y, nome, seta, sprite):
        super().__init__(x, y, nome, seta)

        self.nota = 50
        self.estado = None
        self.sprite = sprite

    def perder_nota(self, seta_apertada):
        if seta_apertada != self.seta:
            self.nota -= 5
    
    def ganhar_nota(self, seta_apertada):
        if seta_apertada == self.seta:
            self.nota += 5

            if self.nota > 100:
                self.nota = 100
        
    def morrer(self):
        if self.nota <= 0:
            self.estado = 'morrer'
            
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