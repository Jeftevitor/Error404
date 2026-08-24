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

        #Fundo de Creditos
        self.img_c = pygame.image.load('Assets/Telas/fundo_creditos.png').convert_alpha()

        #Bloco creditos

        self.img_p = pygame.image.load('Assets/Telas/bloco_creditos.png').convert_alpha()

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

        # fundo creditos
        fundo = pygame.transform.scale(
            self.img_c,
            (self.largura, self.altura)
        )
        tela.blit(fundo, (0, 0))

        # bloco de creditos
        bloco = pygame.transform.scale(
            self.img_p,
            (1000, 580)
        )

        bloco_rect = bloco.get_rect(
            center=(self.largura // 2, self.altura // 2)
        )

        tela.blit(bloco, bloco_rect)

        # fonte em pixel
        fonte = pygame.font.Font(
            'Assets/Fontes/PressStart2P-Regular.ttf',
            16
        )

        fonte_titulo = pygame.font.Font(
            'Assets/Fontes/PressStart2P-Regular.ttf',
            24
        )

        # titulo creditos
        titulo = fonte_titulo.render(
            "CRÉDITOS",
            True,
            (255, 255, 255)
        )

        titulo_rect = titulo.get_rect(
            center=(self.largura // 2, bloco_rect.top + 45)
        )

        tela.blit(titulo, titulo_rect)

        # Quem fez cada parte
        secoes = [
            ("DESENVOLVEDORES:", "Jefte Vitor e Isabela Nóbrega"),
            ("DESIGN:", "Jefte Vitor e Isabela Nóbrega"),
            ("MÚSICA:", "Jefte Vitor")
        ]

        y = bloco_rect.top + 135

        for titulo_secao, nomes in secoes:

            texto_titulo = fonte.render(
                titulo_secao,
                True,
                (0, 0, 0)
            )

            rect_titulo = texto_titulo.get_rect(
                center=(self.largura // 2, y)
            )

            tela.blit(texto_titulo, rect_titulo)

            y += 22

            texto_nomes = fonte.render(
                nomes,
                True,
                (0, 0, 0)
            )

            rect_nomes = texto_nomes.get_rect(
                center=(self.largura // 2, y)
            )

            tela.blit(texto_nomes, rect_nomes)

            y += 32

        # Descrição do jogo
        descricao = (
            "O Error404 é um jogo rítmico inspirado em Friday Night Funkin, "
            "ambientado no IFRN Campus Caicó, especialmente nos laboratórios "
            "de informática. A proposta é que o jogador enfrente professores "
            "em batalhas musicais para conseguir se formar no curso."
        )

        largura_maxima = 700

        sublinhas = self.quebrar_texto(
            descricao,
            fonte,
            largura_maxima
        )

        for sublinha in sublinhas:

            texto = fonte.render(
                sublinha,
                True,
                (0, 0, 0)
            )

            rect_texto = texto.get_rect(
                center=(self.largura // 2, y)
            )

            tela.blit(texto, rect_texto)

            y += 20

        # Sair
        enter = fonte.render(
            "Pressione ENTER para voltar ao Menu",
            True,
            (255, 255, 255)
        )

        enter_rect = enter.get_rect(
            center=(self.largura // 2, self.altura - 35)
        )

        tela.blit(enter, enter_rect)

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


