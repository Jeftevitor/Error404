import pygame

class Intro:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura

        self.img_f = pygame.image.load('Assets/Telas/tela_inicial.png').convert_alpha()

        self.img_l = pygame.image.load('Assets/Telas/logo.png').convert_alpha()

        self.fonte = pygame.font.Font(None, 60)

    def desenhar(self, tela):
        tela.fill((20, 20, 20))

        fundo = pygame.transform.scale(self.img_f,(self.largura, self.altura))
        tela.blit(fundo, (0, 0))

        logo = pygame.transform.scale(self.img_l,(self.largura // 2, self.altura // 2))

        x = self.largura // 2 - logo.get_width() // 2
        y = self.altura // 2 - logo.get_height() // 2

        tela.blit(logo, (x, y))

        tempo = pygame.time.get_ticks()

        if (tempo // 500) % 2 == 0:
            texto = self.fonte.render("APERTE ENTER",True,(255, 255, 255))
            texto_rect = texto.get_rect(center=(self.largura // 2, self.altura - 80))

            tela.blit(texto, texto_rect)