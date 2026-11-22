import os
import pygame


class Telaselecao:

    def __init__(self, largura, altura, fases):

        self.largura = largura
        self.altura = altura
        self.fases = fases

        caminho_fonte = 'Assets/Fontes/PressStart2P-Regular.ttf'
        if not os.path.exists(caminho_fonte):
            caminho_fonte = None

        self.fonte_titulo = pygame.font.Font(caminho_fonte, 40)
        self.fonte_nome = pygame.font.Font(caminho_fonte, 24)
        self.fonte_nome_reduzida = pygame.font.Font(caminho_fonte, 18)
        self.fonte_info = pygame.font.Font(caminho_fonte, 20)
        self.fonte_seta = pygame.font.Font(caminho_fonte, 72)
        self.fonte_voltar = pygame.font.Font(caminho_fonte, 18)

        self.amarelo = (255, 180, 40)
        self.branco = (255, 255, 255)
        self.cinza = (110, 110, 110)
        self.preto = (0, 0, 0)
        self.cartao = (0, 170, 135)

        self.imagens = {}
        self.imagens_cinza = {}
        self.fundos = {}
        self.fundos_cinza = {}
        self.fundos_cache = {}
        self.fundo_selecao = None

        # As imagens só são carregadas na primeira vez que a tela é
        # desenhada, porque convert_alpha() precisa que o pygame.display
        # já tenha sido criado (set_mode).
        self.imagens_carregadas = False

    # =========================================
    # CARREGAR IMAGENS
    # =========================================

    def _criar_versao_cinza(self, imagem):

        if hasattr(pygame.transform, "grayscale"):
            return pygame.transform.grayscale(imagem)

        # Fallback para versões antigas do pygame: escurece a imagem
        cinza = imagem.copy()
        cinza.fill((110, 110, 110), special_flags=pygame.BLEND_RGB_MULT)

        return cinza

    def _criar_fundo_cartao(self, imagem, tamanho):
        largura, altura = tamanho
        escala = max(
            largura / imagem.get_width(),
            altura / imagem.get_height()
        )
        tamanho_ampliado = (
            max(largura, int(imagem.get_width() * escala)),
            max(altura, int(imagem.get_height() * escala))
        )
        imagem = pygame.transform.smoothscale(
            imagem,
            tamanho_ampliado
        )

        recorte = imagem.subsurface(
            (
                (tamanho_ampliado[0] - largura) // 2,
                (tamanho_ampliado[1] - altura) // 2,
                largura,
                altura
            )
        ).copy()

        sombra = pygame.Surface(tamanho, pygame.SRCALPHA)
        sombra.fill((0, 0, 0, 85))
        recorte.blit(sombra, (0, 0))

        return recorte

    def _obter_fundo_cartao(self, fase, tamanho, desbloqueada):
        nome = fase.get("nome", "").lower().replace(" ", "_")
        imagens = (
            self.fundos
            if desbloqueada
            else self.fundos_cinza
        )
        imagem = imagens.get(nome)

        if imagem is None:
            return None

        chave = (nome, tamanho, desbloqueada)

        if chave not in self.fundos_cache:
            self.fundos_cache[chave] = self._criar_fundo_cartao(
                imagem,
                tamanho
            )

        return self.fundos_cache[chave]

    def carregar_imagens(self):

        caminho_fundo = os.path.join(
            "Assets",
            "Telas",
            "fundo_selecao.png"
        )

        if os.path.isfile(caminho_fundo):
            try:
                self.fundo_selecao = pygame.transform.smoothscale(
                    pygame.image.load(caminho_fundo).convert(),
                    (self.largura, self.altura)
                )
            except pygame.error as erro:
                print(f"Erro ao carregar {caminho_fundo}: {erro}")
        else:
            print(f"Fundo da seleção não encontrado: {caminho_fundo}")

        for fase in self.fases:
            nome = fase.get("nome", "").lower().replace(" ", "_")
            caminho = os.path.join(
                "Assets",
                "Telas",
                f"fundo_{nome}.png"
            )

            if not os.path.isfile(caminho):
                print(f"Fundo da fase não encontrado: {caminho}")
                continue

            try:
                imagem = pygame.image.load(caminho).convert()
                self.fundos[nome] = imagem
                self.fundos_cinza[nome] = self._criar_versao_cinza(
                    imagem
                )
            except pygame.error as erro:
                print(f"Erro ao carregar {caminho}: {erro}")

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
                self.imagens_cinza[nome] = self._criar_versao_cinza(imagem)

            except pygame.error as erro:
                print(f"Erro ao carregar {caminho}: {erro}")

        self.imagens_carregadas = True

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

        topo = area.top + 75
        base = area.bottom - 30

        altura_disponivel = base - topo
        quantidade = len(professores)

        largura_individual = (area.width - 30) / quantidade

        imagens = (
            self.imagens
            if desbloqueada
            else self.imagens_cinza
        )
        imagens_redimensionadas = []

        for professor in professores:

            imagem = imagens.get(professor)

            if imagem is None:
                continue

            largura_maxima = largura_individual - 10

            proporcao = min(
                largura_maxima / imagem.get_width(),
                altura_disponivel / imagem.get_height()
            )

            nova_largura = max(1, int(imagem.get_width() * proporcao))
            nova_altura = max(1, int(imagem.get_height() * proporcao))

            imagem = pygame.transform.smoothscale(
                imagem,
                (nova_largura, nova_altura)
            )
            imagens_redimensionadas.append(imagem)

        if not imagens_redimensionadas:
            return

        posicoes_x = []
        limites = [
            imagem.get_bounding_rect()
            for imagem in imagens_redimensionadas
        ]

        for i, limite in enumerate(limites):
            if i == 0:
                posicoes_x.append(0)
                continue

            limite_anterior = limites[i - 1]
            sobreposicao = int(
                min(
                    limite_anterior.width,
                    limite.width
                ) * 0.2
            )
            posicoes_x.append(
                posicoes_x[i - 1]
                + limite_anterior.right
                - limite.left
                - sobreposicao
            )

        esquerda = min(
            posicao + limite.left
            for posicao, limite in zip(posicoes_x, limites)
        )
        direita = max(
            posicao + limite.right
            for posicao, limite in zip(posicoes_x, limites)
        )
        deslocamento_x = area.centerx - (esquerda + direita) / 2
        centro_y = topo + altura_disponivel / 2

        for imagem, posicao_x, limite in zip(
            imagens_redimensionadas,
            posicoes_x,
            limites
        ):
            tela.blit(
                imagem,
                (
                    int(deslocamento_x + posicao_x),
                    int(centro_y - limite.centery)
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

        area = pygame.Rect(0, 0, largura, altura)
        area.center = (centro_x, centro_y)

        pygame.draw.rect(
            tela,
            self.cartao,
            area,
            border_radius=18
        )

        area_fundo = area.inflate(-16, -16)
        fundo = self._obter_fundo_cartao(
            fase,
            area_fundo.size,
            desbloqueada
        )

        if fundo is not None:
            tela.blit(fundo, area_fundo)

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

        fonte_nome = self.fonte_nome
        nome_texto = fase.get("nome", "Fase")
        nome = fonte_nome.render(
            nome_texto,
            True,
            cor_nome
        )

        if nome.get_width() > area.width - 24:
            fonte_nome = self.fonte_nome_reduzida
            nome = fonte_nome.render(
                nome_texto,
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

        if not self.imagens_carregadas:
            self.carregar_imagens()

        if self.fundo_selecao is not None:
            tela.blit(self.fundo_selecao, (0, 0))
        else:
            tela.fill(self.preto)

        total = len(self.fases)

        if total == 0:
            return

        indice = indice_selecionado % total

        centro_x = self.largura // 2
        centro_y = 380

        # TÍTULO

        titulo = self.fonte_titulo.render(
            "SELECAO DE FASE",
            True,
            self.amarelo
        )

        tela.blit(
            titulo,
            titulo.get_rect(center=(centro_x, 90))
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

        esquerda = self.fonte_seta.render("<", True, self.amarelo)
        direita = self.fonte_seta.render(">", True, self.amarelo)

        tela.blit(
            esquerda,
            esquerda.get_rect(center=(centro_x - 340, centro_y))
        )

        tela.blit(
            direita,
            direita.get_rect(center=(centro_x + 340, centro_y))
        )

        # TEXTO ENTER

        if fase_atual.get("desbloqueada", False):
            texto = "ENTER - JOGAR"
            cor = self.amarelo
        else:
            texto = "FASE BLOQUEADA"
            cor = self.cinza

        info = self.fonte_info.render(texto, True, cor)

        tela.blit(
            info,
            info.get_rect(center=(centro_x, 668))
        )

        # TEXTO VOLTAR

        texto_voltar = self.fonte_voltar.render(
            "APERTE ESC PARA VOLTAR",
            True,
            self.branco
        )

        tela.blit(
            texto_voltar,
            texto_voltar.get_rect(center=(centro_x, 703))
        )