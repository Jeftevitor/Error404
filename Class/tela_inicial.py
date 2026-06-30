import pygame

class TelaInicial:
    def __init__(self, largura, altura):

        self.largura = largura
        self.altura = altura

        self.botoes = ['comecar', 'score', 'creditos', 'sair']

        # Fundo
        self.img_f = pygame.image.load('Assets/Telas/fundo.jpg').convert_alpha()

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
    
    def desenhar_creditos(self, tela):
        tela.fill((20, 20, 20))
        fonte = pygame.font.SysFont(None, 36)
        linhas = [
            "Créditos",
            "Desenvolvedores: Jefte Vitor e Isabela Nóbrega",
            "Design: Jefte Vitor e Isabela Nóbrega",
            "Música: Jefte Vitor",
            "O Error404 é um jogo rítmico inspirado em Friday Night Funkin, ambientado no IFRN Campus Caicó, especialmente nos laboratórios de informática. A proposta é que o jogador enfrente professores em batalhas musicais para conseguir se formar no curso."
            "",
            "Pressione qualquer tecla ou clique para voltar"
        ]
        y = 60
        for linha in linhas:
            texto = fonte.render(linha, True, (255, 255, 255))
            tela.blit(texto, (60, y))
            y += 42