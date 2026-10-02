import os
import pygame
from Class.ranking import formatar_pontos

LIMITES_CLASSIFICACAO = (
    (0.90, "Perfeito"),
    (0.75, "Ótimo"),
    (0.55, "Bom"),
    (0.35, "Regular"),
    (0.00, "Ruim"),
)

CORES_CLASSIFICACAO = {
    "Perfeito": (255, 215, 0),
    "Ótimo": (120, 255, 120),
    "Bom": (120, 200, 255),
    "Regular": (255, 180, 80),
    "Ruim": (255, 100, 100),
}

TAM_DERROTA = (450, 600)
TAM_VITORIA = (270, 360)

ALPHA_DERROTA = 190
FADE_DERROTA_MS = 800
PISCA_MS = 500

MUSICAS_FIM = {
    "derrota": "Assets/Music/DERROTA(Asset- Clement panchout).ogg",
    "vitoria": "Assets/Music/VITORIA(Asset- Clement panchout).ogg",
}


class TelaFim:

    def __init__(self, largura, altura, pasta_sprites, personagem):
        self.largura = largura
        self.altura = altura

        self.sprite_derrota = self._carregar_sprite(
            pasta_sprites, personagem,
            ("derrota", "errando", "parado"), TAM_DERROTA
        )

        self.sprite_vitoria = self._carregar_sprite(
            pasta_sprites, personagem,
            ("vitoria", "parado"), TAM_VITORIA
        )

        self.fonte_derrota = pygame.font.Font(None, 170)
        self.fonte_titulo = pygame.font.Font(None, 80)
        self.fonte_fase = pygame.font.Font(None, 48)
        self.fonte_rotulo = pygame.font.Font(None, 38)
        self.fonte_pontos = pygame.font.Font(None, 130)
        self.fonte_classificacao = pygame.font.Font(None, 100)
        self.fonte_dica = pygame.font.Font(None, 32)
        self.fonte_confirmacao = pygame.font.Font(None, 54)
        self.fonte_opcao = pygame.font.Font(None, 60)

        self.tipo = None
        self.inicio = 0
        self.nome_fase = ""
        self.pontos = 0
        self.classificacao = ""

    # =========================================================
    # CLASSIFICAÇÃO
    # =========================================================

    @staticmethod
    def calcular_classificacao(pontos, total_notas, pontos_perfeitos):

        maximo = total_notas * pontos_perfeitos

        proporcao = pontos / maximo if maximo > 0 else 0

        for limite, nome in LIMITES_CLASSIFICACAO:
            if proporcao >= limite:
                return nome

        return "Ruim"

    # =========================================================
    # SPRITES
    # =========================================================

    def _carregar_sprite(self, pasta, personagem, estados, tamanho):
        for i, estado in enumerate(estados):

            caminho = f"{pasta}/{personagem}_{estado}.png"

            if os.path.exists(caminho):

                imagem = pygame.image.load(caminho).convert_alpha()

                return pygame.transform.smoothscale(imagem, tamanho)

            if i == 0:
                print(f"[tela_fim] arquivo não encontrado: {caminho}")

        return pygame.Surface(tamanho, pygame.SRCALPHA)

    # =========================================================
    # MÚSICA
    # =========================================================

    def _tocar_musica(self):

        caminho = MUSICAS_FIM.get(self.tipo)

        if caminho is None or not os.path.exists(caminho):
            print(f"[tela_fim] música não encontrada: {caminho}")
            return

        pygame.mixer.music.stop()
        pygame.mixer.music.load(caminho)
        pygame.mixer.music.play()

    # =========================================================
    # INICIAR TELAS
    # =========================================================

    def mostrar_derrota(self, nome_fase):

        self.tipo = "derrota"
        self.nome_fase = nome_fase
        self.inicio = pygame.time.get_ticks()
        self._tocar_musica()

    def mostrar_vitoria(self, nome_fase, pontos, classificacao):

        self.tipo = "vitoria"
        self.nome_fase = nome_fase
        self.pontos = pontos
        self.classificacao = classificacao
        self.inicio = pygame.time.get_ticks()
        self._tocar_musica()

    # =========================================================
    # DESENHAR
    # =========================================================

    def desenhar(self, tela, fundo):

        if self.tipo == "derrota":
            self._desenhar_derrota(tela, fundo)

        elif self.tipo == "vitoria":
            self._desenhar_vitoria(tela, fundo)

    def _desenhar_derrota(self, tela, fundo):

        tela.blit(fundo, (0, 0))

        decorrido = pygame.time.get_ticks() - self.inicio

        alpha = min(
            ALPHA_DERROTA,
            int(ALPHA_DERROTA * decorrido / FADE_DERROTA_MS)
        )

        escurecer = pygame.Surface(
            (self.largura, self.altura), pygame.SRCALPHA
        )

        escurecer.fill((110, 20, 70, alpha))

        tela.blit(escurecer, (0, 0))

        rect = self.sprite_derrota.get_rect(
            midbottom=(self.largura // 2, self.altura)
        )

        tela.blit(self.sprite_derrota, rect)

        if (decorrido // PISCA_MS) % 2 == 0:

            sombra = self.fonte_derrota.render(
                "DERROTA", True, (40, 0, 20)
            )

            texto = self.fonte_derrota.render(
                "DERROTA", True, (255, 235, 240)
            )

            centro = (self.largura // 2, 75)

            tela.blit(
                sombra,
                sombra.get_rect(center=(centro[0] + 5, centro[1] + 5))
            )

            tela.blit(texto, texto.get_rect(center=centro))

        dica = self.fonte_dica.render(
            "ENTER para continuar", True, (255, 220, 230)
        )

        tela.blit(
            dica,
            dica.get_rect(
                bottomright=(self.largura - 30, self.altura - 25)
            )
        )

    def _desenhar_vitoria(self, tela, fundo):

        tela.blit(fundo, (0, 0))

        escurecer = pygame.Surface(
            (self.largura, self.altura), pygame.SRCALPHA
        )

        escurecer.fill((0, 0, 0, 160))

        tela.blit(escurecer, (0, 0))

        margem = 50

        # ======================= CANTO SUPERIOR ESQUERDO =======================

        titulo = self.fonte_titulo.render(
            "FASE CONCLUÍDA!", True, (255, 255, 255)
        )

        tela.blit(titulo, (margem, 40))

        nome_fase = self.fonte_fase.render(
            self.nome_fase, True, (200, 200, 200)
        )

        tela.blit(nome_fase, (margem, 105))

        # ======================= CANTO SUPERIOR DIREITO =======================

        rotulo = self.fonte_rotulo.render(
            "TOTAL DE PONTOS", True, (200, 200, 200)
        )

        tela.blit(
            rotulo,
            rotulo.get_rect(topright=(self.largura - margem, 35))
        )

        pontos = self.fonte_pontos.render(
            formatar_pontos(self.pontos), True, (255, 255, 255)
        )

        pontos_rect = pontos.get_rect(
            topright=(self.largura - margem, 65)
        )

        tela.blit(pontos, pontos_rect)

        cor = CORES_CLASSIFICACAO.get(
            self.classificacao, (255, 255, 255)
        )

        classificacao = self.fonte_classificacao.render(
            self.classificacao.upper() + "!", True, cor
        )

        tela.blit(
            classificacao,
            classificacao.get_rect(
                topright=(self.largura - margem, pontos_rect.bottom + 10)
            )
        )

        # ======================= PERSONAGEM (CANTO INFERIOR DIREITO) =======================

        rect = self.sprite_vitoria.get_rect(
            bottomright=(self.largura - 20, self.altura)
        )

        tela.blit(self.sprite_vitoria, rect)

        dica = self.fonte_dica.render(
            "ENTER para continuar", True, (200, 200, 200)
        )

        tela.blit(
            dica,
            dica.get_rect(bottomleft=(margem, self.altura - 25))
        )

    # =========================================================
    # CONFIRMAÇÃO DE SAÍDA
    # =========================================================

    def desenhar_confirmacao(self, tela, opcao):

        escurecer = pygame.Surface(
            (self.largura, self.altura), pygame.SRCALPHA
        )

        escurecer.fill((0, 0, 0, 170))

        tela.blit(escurecer, (0, 0))

        caixa = pygame.Rect(0, 0, 760, 280)
        caixa.center = (self.largura // 2, self.altura // 2)

        pygame.draw.rect(
            tela, (35, 35, 35), caixa, border_radius=18
        )

        pygame.draw.rect(
            tela, (255, 255, 255), caixa, width=3, border_radius=18
        )

        pergunta = self.fonte_confirmacao.render(
            "Deseja mesmo sair desta fase?", True, (255, 255, 255)
        )

        tela.blit(
            pergunta,
            pergunta.get_rect(
                center=(caixa.centerx, caixa.top + 80)
            )
        )

        for i, texto in enumerate(("Sim", "Não")):

            selecionada = (i == opcao)

            cor = (0, 255, 0) if selecionada else (255, 255, 255)

            if selecionada:
                texto = "> " + texto

            render = self.fonte_opcao.render(texto, True, cor)

            x = caixa.centerx + (-130 if i == 0 else 130)

            tela.blit(
                render,
                render.get_rect(center=(x, caixa.top + 165))
            )

        dica = self.fonte_dica.render(
            "< >  escolher     ENTER  confirmar     ESC  voltar",
            True,
            (140, 140, 140)
        )

        tela.blit(
            dica,
            dica.get_rect(
                center=(caixa.centerx, caixa.bottom - 35)
            )
        )