import os
import pygame

ARQUIVO_RANKING = "Assets/Arquivos_txt/ranking.txt"
LINHAS_POR_FASE = 10

OURO = (255, 215, 0)
PRATA = (205, 205, 215)
BRONZE = (205, 127, 50)
BRANCO = (255, 255, 255)
CINZA = (140, 140, 140)
VERDE = (0, 255, 0)


def formatar_pontos(pontos):
    return f"{pontos:,}".replace(",", ".")


class Ranking:
    def __init__(self, largura, altura, nomes_fases, arquivo=ARQUIVO_RANKING):
        self.largura = largura
        self.altura = altura
        self.nomes_fases = nomes_fases
        self.arquivo = arquivo

        self.registros = []
        self.aba = 0

        self.fonte_titulo = pygame.font.Font(None, 90)
        self.fonte_aba = pygame.font.Font(None, 44)
        self.fonte_cabecalho = pygame.font.Font(None, 32)
        self.fonte_linha = pygame.font.Font(None, 40)
        self.fonte_rodape = pygame.font.Font(None, 30)

    # =========================================================
    # ARQUIVO
    # =========================================================

    def salvar(self, nome, fase, pontos, classificacao):

        # ";" é o separador do arquivo, então não pode aparecer no nome
        nome = nome.replace(";", "").strip() or "Jogador"

        pasta = os.path.dirname(self.arquivo)

        if pasta:
            os.makedirs(pasta, exist_ok=True)

        with open(self.arquivo, "a", encoding="utf-8") as arquivo:
            arquivo.write(
                f"{nome};{fase};{pontos};{classificacao}\n"
            )

    def carregar(self):

        self.registros = []

        if not os.path.exists(self.arquivo):
            return

        with open(self.arquivo, "r", encoding="utf-8") as arquivo:

            for linha in arquivo:

                partes = linha.strip().split(";")

                # Ignora linhas quebradas em vez de travar o jogo
                if len(partes) != 4:
                    continue

                nome, fase, pontos, classificacao = partes

                try:
                    pontos = int(pontos)
                except ValueError:
                    continue

                self.registros.append({
                    "nome": nome,
                    "fase": fase,
                    "pontos": pontos,
                    "classificacao": classificacao
                })

    def melhores(self, fase):

        # Só a melhor pontuação de cada jogador em cada fase
        melhores = {}

        for registro in self.registros:

            if registro["fase"] != fase:
                continue

            chave = registro["nome"].lower()

            if (
                chave not in melhores
                or registro["pontos"] > melhores[chave]["pontos"]
            ):
                melhores[chave] = registro

        ordenados = sorted(
            melhores.values(),
            key=lambda r: r["pontos"],
            reverse=True
        )

        return ordenados[:LINHAS_POR_FASE]

    # =========================================================
    # TELA
    # =========================================================

    def abrir(self):

        # Chamar ao entrar na tela de score: relê o txt
        self.carregar()
        self.aba = 0

    def processar_evento(self, evento):

        if evento.type != pygame.KEYDOWN:
            return None

        if evento.key == pygame.K_LEFT:
            self.aba = (self.aba - 1) % len(self.nomes_fases)

        elif evento.key == pygame.K_RIGHT:
            self.aba = (self.aba + 1) % len(self.nomes_fases)

        elif evento.key in (pygame.K_RETURN, pygame.K_ESCAPE):
            return "voltar"

        return None

    def desenhar(self, tela, nome_jogador=""):

        tela.fill((25, 25, 25))

        # ======================= TÍTULO =======================

        titulo = self.fonte_titulo.render("RANKING", True, BRANCO)

        tela.blit(
            titulo,
            titulo.get_rect(center=(self.largura // 2, 55))
        )

        # ======================= ABAS (FASES) =======================

        total = len(self.nomes_fases)
        espaco = 320

        for i, nome in enumerate(self.nomes_fases):

            cor = VERDE if i == self.aba else CINZA

            render = self.fonte_aba.render(nome, True, cor)

            x = (
                self.largura // 2
                + int((i - (total - 1) / 2) * espaco)
            )

            rect = render.get_rect(center=(x, 125))

            tela.blit(render, rect)

            if i == self.aba:
                pygame.draw.line(
                    tela,
                    VERDE,
                    (rect.left, rect.bottom + 4),
                    (rect.right, rect.bottom + 4),
                    3
                )

        # ======================= PAINEL =======================

        largura_painel = 900
        x0 = (self.largura - largura_painel) // 2

        painel = pygame.Rect(x0, 160, largura_painel, 490)

        pygame.draw.rect(
            tela, (40, 40, 40), painel, border_radius=14
        )

        col_pos = x0 + 40
        col_nome = x0 + 120
        col_pontos_direita = x0 + 600
        col_nota = x0 + 650

        # Cabeçalho
        for texto, x, alinhamento in (
            ("#", col_pos, "left"),
            ("NOME", col_nome, "left"),
            ("PONTOS", col_pontos_direita, "right"),
            ("NOTA", col_nota, "left"),
        ):
            render = self.fonte_cabecalho.render(texto, True, CINZA)

            rect = render.get_rect()

            if alinhamento == "left":
                rect.topleft = (x, 180)
            else:
                rect.topright = (x, 180)

            tela.blit(render, rect)

        pygame.draw.line(
            tela,
            (90, 90, 90),
            (x0 + 25, 212),
            (x0 + largura_painel - 25, 212),
            2
        )

        # ======================= LINHAS =======================

        fase = self.nomes_fases[self.aba]
        linhas = self.melhores(fase)

        if not linhas:

            vazio = self.fonte_linha.render(
                "Ninguém jogou esta fase ainda.", True, CINZA
            )

            tela.blit(
                vazio,
                vazio.get_rect(
                    center=(self.largura // 2, 400)
                )
            )

        cores_posicao = (OURO, PRATA, BRONZE)

        y = 228

        for i, registro in enumerate(linhas):

            cor = cores_posicao[i] if i < 3 else BRANCO

            # Destaca a linha do jogador atual
            if (
                nome_jogador
                and registro["nome"].lower() == nome_jogador.lower()
            ):
                pygame.draw.rect(
                    tela,
                    (45, 85, 45),
                    (x0 + 15, y - 4, largura_painel - 30, 38),
                    border_radius=8
                )

            pos = self.fonte_linha.render(f"{i + 1}", True, cor)
            nome = self.fonte_linha.render(registro["nome"], True, cor)
            pontos = self.fonte_linha.render(
                formatar_pontos(registro["pontos"]), True, cor
            )
            nota = self.fonte_linha.render(
                registro["classificacao"], True, cor
            )

            tela.blit(pos, (col_pos, y))
            tela.blit(nome, (col_nome, y))
            tela.blit(
                pontos,
                pontos.get_rect(topright=(col_pontos_direita, y))
            )
            tela.blit(nota, (col_nota, y))

            y += 42

        # ======================= RODAPÉ =======================

        rodape = self.fonte_rodape.render(
            "<  >  trocar fase        ENTER  voltar",
            True,
            CINZA
        )

        tela.blit(
            rodape,
            rodape.get_rect(
                center=(self.largura // 2, self.altura - 35)
            )
        )