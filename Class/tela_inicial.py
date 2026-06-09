import pygame

class TelaInicial:
    def __init__(self, largura, altura):

        self.largura = largura
        self.altura = altura

        self.botoes = ['comecar', 'score', 'creditos', 'sair']

        # Fundo
        self.img_f = pygame.image.load('Assets/Telas/tela_inicial.png').convert_alpha()

        # Logo
        self.img_l = pygame.image.load('Assets/Telas/logo.png').convert_alpha()

        self.img_b = {}

        for b in self.botoes:
            self.img_b[b] = pygame.image.load(f'Assets/Telas/b_{b}.png').convert_alpha()

        self.rects = {
            'comecar': pygame.Rect(820, 200, 200, 110),
            'score': pygame.Rect(820, 270, 200, 110),
            'creditos': pygame.Rect(820, 340, 200, 110),
            'sair': pygame.Rect(820, 410, 200, 110)
        }

    def desenhar(self, tela):
        tela.fill((20, 20, 20))

        fundo = pygame.transform.scale(self.img_f,(self.largura, self.altura))

        tela.blit(fundo, (0, 0))

        for b in self.botoes:
            botao = pygame.transform.scale(self.img_b[b],(200, 140))
            tela.blit(botao,(self.rects[b].x,self.rects[b].y))

        logo = pygame.transform.scale(self.img_l,(420, 270))
        tela.blit(logo, (20, 10))

    def verificar_clique(self, pos):
        for nome, rect in self.rects.items():
            if rect.collidepoint(pos):
                return nome
        return None