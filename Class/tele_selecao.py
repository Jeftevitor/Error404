
import os
import pygame


class Telaselecao:

    def __init__(self, largura, altura, fases):

        self.largura = largura
        self.altura = altura
        self.fases = fases

        self.fonte_titulo = pygame.font.Font(None, 65)
        self.fonte_nome = pygame.font.Font(None, 43)
        self.fonte_info = pygame.font.Font(None, 34)
        self.fonte_seta = pygame.font.Font(None, 100)

        self.amarelo = (255, 180, 40)
        self.branco = (255, 255, 255)
        self.cinza = (110, 110, 110)
        self.preto = (0, 0, 0)
        self.cartao = (0, 170, 135)

        self.imagens = {}
        self.imagens_cinza = {}

        self.carregar_imagens()

    # =========================================
    # CARREGAR IMAGENS
    # =========================================

    def carregar_imagens(self):

        nomes = set()

        for fase in self.fases:
            nomes.update(fase.get("professores", []))

        for nome in nomes:

            caminho = os.path.join(
                "Assets",
                "Sprites",
                f"{nome}_parado.png"
            )

            if not os.path.isfile(caminho):
                print(f"Sprite não encontrada: {caminho}")
                continue

            try:

                imagem = pygame.image.load(
                    caminho
                ).convert_alpha()

                self.imagens[nome] = imagem

                self.imagens_cinza[nome] = (
                    pygame.transform.grayscale(imagem)
                )

            except pygame.error as erro:

                print(f"Erro ao carregar {caminho}: {erro}")

    # =========================================
    # DESENHAR PROFESSORES
    # =========================================

    def desenhar_professores(
        self,
        tela,
        fase,
        area,
        desbloqueada
    ):

        professores = fase.get("professores", [])

        if not professores:
            return

        topo = area.top + 90
        base = area.bottom - 15

        altura_disponivel = base - topo
        quantidade = len(professores)

        largura_individual = (
            area.width - 30
        ) / quantidade

        for i, professor in enumerate(professores):

            imagens = (
                self.imagens
                if desbloqueada
                else self.imagens_cinza
            )

            imagem = imagens.get(professor)

            if imagem is None:
                continue

            largura_maxima = largura_individual - 10

            proporcao = min(
                largura_maxima / imagem.get_width(),
                altura_disponivel / imagem.get_height()
            )

            nova_largura = max(
                1,
                int(imagem.get_width() * proporcao)
            )

            nova_altura = max(
                1,
                int(imagem.get_height() * proporcao)
            )

            imagem = pygame.transform.smoothscale(
                imagem,
                (nova_largura, nova_altura)
            )

            centro_x = (
                area.left
                + 15
                + largura_individual * i
                + largura_individual / 2
            )

            centro_y = (
                topo + altura_disponivel / 2
            )

            tela.blit(
                imagem,
                imagem.get_rect(
                    center=(
                        int(centro_x),
                        int(centro_y)
                    )
                )
            )

    # =========================================
    # DESENHAR CARTÃO
    # =========================================

    def desenhar_cartao(
        self,
        tela,
        fase,
        centro_x,
        centro_y,
        largura,
        altura,
        selecionado=False
    ):

        desbloqueada = fase.get("desbloqueada", False)

        area = pygame.Rect(
            0,
            0,
            largura,
            altura
        )

        area.center = (centro_x, centro_y)

        pygame.draw.rect(
            tela,
            self.cartao,
            area,
            border_radius=18
        )

        cor_borda = (
            self.amarelo
            if selecionado
            else self.cinza
        )

        pygame.draw.rect(
            tela,
            cor_borda,
            area,
            width=6 if selecionado else 3,
            border_radius=18
        )

        cor_nome = (
            self.branco
            if desbloqueada
            else self.cinza
        )

        nome = self.fonte_nome.render(
            fase.get("nome", "Fase"),
            True,
            cor_nome
        )

        tela.blit(
            nome,
            nome.get_rect(
                center=(centro_x, area.top + 55)
            )
        )

        self.desenhar_professores(
            tela,
            fase,
            area,
            desbloqueada
        )

    # =========================================
    # DESENHAR TELA DE SELEÇÃO
    # =========================================

    def desenhar(self, tela, indice_selecionado):

        tela.fill(self.preto)

        total = len(self.fases)

        if total == 0:
            return

        indice = indice_selecionado % total

        centro_x = self.largura // 2
        centro_y = 425

        titulo = self.fonte_titulo.render(
            "SELECAO DE FASE",
            True,
            self.amarelo
        )

        tela.blit(
            titulo,
            titulo.get_rect(
                center=(centro_x, 90)
            )
        )

        # CARTÃO ESQUERDO

        if total > 1:

            indice_esquerda = (indice - 1) % total

            self.desenhar_cartao(
                tela,
                self.fases[indice_esquerda],
                centro_x - 440,
                centro_y,
                230,
                280
            )

        # CARTÃO DIREITO

        if total > 1:

            indice_direita = (indice + 1) % total

            self.desenhar_cartao(
                tela,
                self.fases[indice_direita],
                centro_x + 440,
                centro_y,
                230,
                280
            )

        # CARTÃO CENTRAL

        fase_atual = self.fases[indice]

        self.desenhar_cartao(
            tela,
            fase_atual,
            centro_x,
            centro_y,
            390,
            420,
            selecionado=True
        )

        # SETAS

        esquerda = self.fonte_seta.render(
            "<",
            True,
            self.amarelo
        )

        direita = self.fonte_seta.render(
            ">",
            True,
            self.amarelo
        )

        tela.blit(
            esquerda,
            esquerda.get_rect(
                center=(centro_x - 340, centro_y)
            )
        )

        tela.blit(
            direita,
            direita.get_rect(
                center=(centro_x + 340, centro_y)
            )
        )

        # TEXTO ENTER

        if fase_atual.get("desbloqueada", False):

            texto = "ENTER - JOGAR"
            cor = self.amarelo

        else:

            texto = "FASE BLOQUEADA"
            cor = self.cinza

        info = self.fonte_info.render(
            texto,
            True,
            cor
        )

        tela.blit(
            info,
            info.get_rect(
                center=(centro_x, 680)
            )
        )
