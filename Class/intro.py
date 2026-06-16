import pygame

class Intro:
    def __init__(self, largura, altura):

        self.largura = largura
        self.altura = altura

        self.img_l = pygame.image.load('Assets/Telas/logo.png').convert_alpha()

    def desenhar(self, tela):
        tela.fill((0, 0, 0))
        logo = pygame.transform.scale(self.img_l,(self.largura // 2,self.altura // 2))
        x = self.largura * 0.5 - logo.get_width() * 0.5
        y = self.altura * 0.5 - logo.get_height() * 0.5

        tela.blit(logo, (x, y))