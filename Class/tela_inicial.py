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
            " ",
            "Desenvolvedores: Jefte Vitor e Isabela Nóbrega",
            " ",
            "Design: Jefte Vitor e Isabela Nóbrega",
            " ",
            "Música: Jefte Vitor",
            " ",
            "O Error404 é um jogo rítmico inspirado em Friday Night Funkin, ambientado no IFRN Campus Caicó, especialmente nos laboratórios de informática. A proposta é que o jogador enfrente professores em batalhas musicais para conseguir se formar no curso.",
            "",
            "Pressione a tecla Enter para voltar para tela de Menu"
        ]

        largura_maxima = 1080
        y = 60

        for linha in linhas:
            if fonte.size(linha)[0] <= largura_maxima:
                texto = fonte.render(linha, True, (255, 255, 255))
                tela.blit(texto, (60, y))
                y += 42
            else:
                sublinhas = self.quebrar_texto(linha, fonte, largura_maxima)
                for sublinha in sublinhas:
                    texto = fonte.render(sublinha, True, (255, 255, 255))
                    tela.blit(texto, (60, y))
                    y += 42

    def quebrar_texto(self, texto, fonte, largura_maxima):
        palavras  = texto.split(" ")
        linhas = []
        linha_atual = ""

        for palavra in palavras:
            teste = (linha_atual + " " + palavra).strip()

            if fonte.size(teste)[0] <= largura_maxima:
                linha_atual = teste
            else:
                linhas.append(linha_atual)
                linha_atual = palavra

        linhas.append(linha_atual)

        return linhas


