import pygame

class Seta:
    def __init__(self, x, y, direcao):
        self.x = x
        self.y = y
        self.direcao = direcao
        self.velocidade = 5
        self.acertada = False
        
        if self.direcao == 'esquerda':
            self.imagem = pygame.image.load(
                'Assets/Sprites/esquerda.png'
            ).convert_alpha()

        elif self.direcao == 'direita':
            self.imagem = pygame.image.load(
                'Assets/Sprites/direita.png'
            ).convert_alpha()

        elif self.direcao == 'cima':
            self.imagem = pygame.image.load(
                'Assets/Sprites/cima.png'
            ).convert_alpha()

        elif self.direcao == 'baixo':
            self.imagem = pygame.image.load(
                'Assets/Sprites/baixo.png'
            ).convert_alpha()
        self.imagem = pygame.transform.scale(
            self.imagem,
            (420, 400)
        )

    def mover(self):
        self.y += self.velocidade

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x, self.y))

    def verificar_colisao(self, receptor_y):

        if abs(self.y - receptor_y) < 20:
            return True

        return False

