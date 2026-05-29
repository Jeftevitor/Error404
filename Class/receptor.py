import pygame

class Receptor:

    def __init__(self, x, y, direcao):
        self.x = x
        self.y = y
        self.direcao = direcao

        if self.direcao == 'cima':
            self.tecla = pygame.K_UP
        elif self.direcao == 'baixo':
            self.tecla = pygame.K_DOWN
        elif self.direcao == 'esquerda':
            self.tecla = pygame.K_LEFT
        elif self.direcao == 'direita':
            self.tecla = pygame.K_RIGHT

    def verificar_input(self):
        teclas = pygame.key.get_pressed()
        return teclas[self.tecla]

    def verificar_colisao(self, seta):
        if seta.direcao != self.direcao:
            return False
        
        distancia = abs(seta.y - self.y)
        if distancia < 20:
            return True
        else:
            return False
