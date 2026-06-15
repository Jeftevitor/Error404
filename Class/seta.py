import pygame

class Seta:
    def __init__(self, x, y, direcao):
        self.x = x
        self.y = y
        self.direcao = direcao
        self.velocidade = 5
        self.hit = False
        
        if self.direcao == 'esquerda':
            self.imagem = pygame.image.load('Assets/Sprites/esquerda.png').convert_alpha()

        elif self.direcao == 'direita':
            self.imagem = pygame.image.load('Assets/Sprites/direita.png').convert_alpha()

        elif self.direcao == 'cima':
            self.imagem = pygame.image.load('Assets/Sprites/cima.png').convert_alpha()

        elif self.direcao == 'baixo':
            self.imagem = pygame.image.load('Assets/Sprites/baixo.png').convert_alpha()
            
        self.imagem = pygame.transform.scale(self.imagem,(210, 200))
        
    def acertou(self):
        if self.hit:
            self.x = 1500
            self.y = 1500
        
    def mover(self):
        self.y += self.velocidade

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x, self.y))

    

