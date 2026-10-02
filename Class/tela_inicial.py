import os
import pygame


class TelaInicial:
    def __init__(self, largura, altura):

        self.largura = largura
        self.altura = altura

        # Seções do menu (de cima para baixo)
        self.botoes = ['comecar', 'score', 'creditos', 'sair']

        self.textos = {
            'comecar': 'COMEÇAR',
            'score': 'SCORE',
            'creditos': 'CRÉDITOS',
            'sair': 'SAIR'
        }

        # Setas que cada seção mostra: (tem seta em cima, tem seta embaixo)
        self.setas = {
            'comecar': (False, True),
            'score': (True, True),
            'creditos': (True, True),
            'sair': (True, False)
        }

        self.selecionado = 0

        # ---------------- CORES ----------------
        self.cor_amarelo = (255, 243, 150)   # amarelo claro
        self.cor_verde = (165, 232, 178)     # verde claro

        self.cor_texto = (196, 164, 132)           # marrom claro (não selecionado)
        self.cor_texto_sel = (139, 94, 60)         # marrom claro mais forte (selecionado)

        self.mistura = 0.0

        # ---------------- IMAGENS ----------------
        self.img_d = self.carregar_imagem('Assets/Telas/fundo_telainicial.png')

        # Fundo de créditos
        self.img_c = pygame.image.load('Assets/Telas/fundo_creditos.png').convert_alpha()

        # Bloco créditos
        self.img_p = pygame.image.load('Assets/Telas/bloco_creditos.png').convert_alpha()

        # ---------------- FONTES ----------------
        caminho_fonte = 'Assets/Fontes/PressStart2P-Regular.ttf'
        if not os.path.exists(caminho_fonte):
            caminho_fonte = None

        self.fonte_menu = pygame.font.Font(caminho_fonte, 44)
        self.fonte = pygame.font.Font(caminho_fonte, 16)
        self.fonte_titulo = pygame.font.Font(caminho_fonte, 24)

        # Posição do menu (coluna da direita)
        self.menu_x = 920
        self.menu_y_inicial = 190
        self.menu_espaco = 130

    # =========================================================
    # UTILIDADES
    # =========================================================

    def carregar_imagem(self, caminho):
        if os.path.exists(caminho):
            return pygame.image.load(caminho).convert_alpha()
        return None

    def misturar(self, cor_a, cor_b, t):
        return tuple(int(a + (b - a) * t) for a, b in zip(cor_a, cor_b))

    def desenhar_seta(self, tela, cx, cy, direcao, cor):
        larg = 34
        alt = 18
        haste_larg = 12
        haste_alt = 10

        if direcao == 'cima':
            ponta = [(cx, cy - alt), (cx - larg // 2, cy), (cx + larg // 2, cy)]
            haste = pygame.Rect(cx - haste_larg // 2, cy, haste_larg, haste_alt)
        else:
            ponta = [(cx, cy + alt), (cx - larg // 2, cy), (cx + larg // 2, cy)]
            haste = pygame.Rect(cx - haste_larg // 2, cy - haste_alt, haste_larg, haste_alt)

        pygame.draw.polygon(tela, cor, ponta)
        pygame.draw.rect(tela, cor, haste)

    # =========================================================
    # NAVEGAÇÃO (teclado)
    # =========================================================

    def processar_evento(self, evento):
        if evento.type != pygame.KEYDOWN:
            return None

        if evento.key == pygame.K_UP:
            self.selecionado = max(0, self.selecionado - 1)

        elif evento.key == pygame.K_DOWN:
            self.selecionado = min(len(self.botoes) - 1, self.selecionado + 1)

        elif evento.key == pygame.K_RETURN:
            return self.botoes[self.selecionado]

        return None

    # =========================================================
    # MENU
    # =========================================================

    def desenhar(self, tela):
        alvo = self.selecionado / (len(self.botoes) - 1)
        self.mistura += (alvo - self.mistura) * 0.18

        cor_fundo = self.misturar(self.cor_amarelo, self.cor_verde, self.mistura)
        tela.fill(cor_fundo)

        if self.img_d is not None:
            desenho = pygame.transform.scale(self.img_d, (self.largura, self.altura))
            tela.blit(desenho, (0, 0))

        for i, nome in enumerate(self.botoes):
            ativo = (i == self.selecionado)
            cor = self.cor_texto_sel if ativo else self.cor_texto

            cy = self.menu_y_inicial + i * self.menu_espaco

            texto = self.fonte_menu.render(self.textos[nome], True, cor)
            rect = texto.get_rect(center=(self.menu_x, cy))
            tela.blit(texto, rect)

            if ativo:
                tem_cima, tem_baixo = self.setas[nome]

                if tem_cima:
                    self.desenhar_seta(tela, self.menu_x, cy - 62, 'cima', cor)
                if tem_baixo:
                    self.desenhar_seta(tela, self.menu_x, cy + 62, 'baixo', cor)

    # =========================================================
    # CRÉDITOS
    # =========================================================

    def desenhar_creditos(self, tela):

        fundo = pygame.transform.scale(self.img_c, (self.largura, self.altura))
        tela.blit(fundo, (0, 0))

        bloco = pygame.transform.scale(self.img_p, (1000, 580))
        bloco_rect = bloco.get_rect(center=(self.largura // 2, self.altura // 2))
        tela.blit(bloco, bloco_rect)

        fonte = self.fonte
        fonte_titulo = self.fonte_titulo

        titulo = fonte_titulo.render("CRÉDITOS", True, (255, 255, 255))
        titulo_rect = titulo.get_rect(center=(self.largura // 2, bloco_rect.top + 45))
        tela.blit(titulo, titulo_rect)

        secoes = [
            ("DESENVOLVEDORES:", "Jefte Vitor e Isabela Nóbrega"),
            ("DESIGN:", "Jefte Vitor e Isabela Nóbrega"),
            ("MÚSICA:", "Jefte Vitor")
        ]

        y = bloco_rect.top + 135

        for titulo_secao, nomes in secoes:

            texto_titulo = fonte.render(titulo_secao, True, (0, 0, 0))
            tela.blit(texto_titulo, texto_titulo.get_rect(center=(self.largura // 2, y)))
            y += 22

            texto_nomes = fonte.render(nomes, True, (0, 0, 0))
            tela.blit(texto_nomes, texto_nomes.get_rect(center=(self.largura // 2, y)))
            y += 32

        descricao = (
            "O Error404 é um jogo rítmico inspirado em Friday Night Funkin, "
            "ambientado no IFRN Campus Caicó, especialmente nos laboratórios "
            "de informática. A proposta é que o jogador enfrente professores "
            "em batalhas musicais para conseguir se formar no curso."
        )

        for sublinha in self.quebrar_texto(descricao, fonte, 700):
            texto = fonte.render(sublinha, True, (0, 0, 0))
            tela.blit(texto, texto.get_rect(center=(self.largura // 2, y)))
            y += 20

        enter = fonte.render("Pressione ENTER para voltar ao Menu", True, (255, 255, 255))
        tela.blit(enter, enter.get_rect(center=(self.largura // 2, self.altura - 35)))

    def quebrar_texto(self, texto, fonte, largura_maxima):
        palavras = texto.split(" ")
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