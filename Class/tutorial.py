import os
import pygame

from Class.seta import Seta

FONTE = 'Assets/Fontes/PressStart2P-Regular.ttf'

BRANCO = (255, 255, 255)
COR_TECLA = (51, 51, 51)
COR_TECLA_PRESSIONADA = (105, 105, 105)
COR_BORDA = (130, 130, 130)
COR_TEXTO_PAPEL = (45, 30, 20)   # texto escuro sobre o papel

# Medidas-base (para um painel de 640x440); tudo é escalado com o painel
LARGURA_BASE = 640
ALTURA_BASE = 440
TECLA_BASE = 84          # lado das teclas das setas
ESPACO_BASE = 10         # espaço entre as teclas
ESC_LARGURA_BASE = 130   # a tecla ESC é mais larga

ATRASO_MS = 1500         # tempo mínimo na tela antes de poder continuar


class TutorialControles:
    """Painel de controles mostrado antes do 3-2-1-VAI! da primeira fase."""

    def __init__(self, largura, altura, caminho_painel=None,
                 tamanho_painel=(640, 440)):

        self.largura = largura
        self.altura = altura
        self.tamanho_painel = tamanho_painel

        self.painel = None
        self.cor_texto = BRANCO

        # Use a MESMA imagem e o MESMO tamanho da confirmação de sair da fase
        if caminho_painel and os.path.exists(caminho_painel):
            imagem = pygame.image.load(caminho_painel).convert_alpha()
            self.painel = pygame.transform.smoothscale(
                imagem, tamanho_painel
            )
            self.cor_texto = COR_TEXTO_PAPEL

        self.rect_painel = pygame.Rect(0, 0, *tamanho_painel)
        self.rect_painel.center = (largura // 2, altura // 2)

        self.escurecer = pygame.Surface((largura, altura), pygame.SRCALPHA)
        self.escurecer.fill((0, 0, 0, 150))

        # fator de escala do conteúdo em relação ao painel-base
        self.escala = min(
            tamanho_painel[0] / LARGURA_BASE,
            tamanho_painel[1] / ALTURA_BASE
        )

        e = self.escala
        self.tecla = int(TECLA_BASE * e)
        self.espaco = int(ESPACO_BASE * e)
        self.esc_largura = int(ESC_LARGURA_BASE * e)

        self.fonte_titulo = pygame.font.Font(FONTE, int(22 * e))
        self.fonte_rotulo = pygame.font.Font(FONTE, int(12 * e))
        self.fonte_esc = pygame.font.Font(FONTE, int(24 * e))
        self.fonte_rodape = pygame.font.Font(FONTE, int(14 * e))

        self.inicio = 0

        self.icones = {
            direcao: self._carregar_icone_seta(direcao, int(self.tecla * 0.62))
            for direcao in ("esquerda", "baixo", "cima", "direita")
        }

    # ---------------------------------------------------------
    # Atraso para garantir que o jogador viu o tutorial
    # ---------------------------------------------------------

    def iniciar(self):
        self.inicio = pygame.time.get_ticks()

    def pronto(self):
        return pygame.time.get_ticks() - self.inicio >= ATRASO_MS

    # ---------------------------------------------------------
    # Pega a imagem da seta do próprio jogo (classe Seta)
    # ---------------------------------------------------------

    def _carregar_icone_seta(self, direcao, lado):

        try:
            folha = pygame.Surface((600, 600), pygame.SRCALPHA)
            Seta(150, 150, direcao).desenhar(folha)

            area = folha.get_bounding_rect()

            if area.width == 0 or area.height == 0:
                return None

            recorte = folha.subsurface(area).copy()

            escala = lado / max(area.width, area.height)
            novo = (
                max(1, int(area.width * escala)),
                max(1, int(area.height * escala))
            )

            return pygame.transform.smoothscale(recorte, novo)

        except Exception as erro:
            print(f"[tutorial] não foi possível carregar a seta: {erro}")
            return None

    # ---------------------------------------------------------
    # Desenho das teclas
    # ---------------------------------------------------------

    def _desenhar_tecla(self, tela, rect, pressionada):

        cor = COR_TECLA_PRESSIONADA if pressionada else COR_TECLA

        pygame.draw.rect(tela, cor, rect, border_radius=int(16 * self.escala))
        pygame.draw.rect(
            tela, COR_BORDA, rect,
            width=max(2, int(3 * self.escala)),
            border_radius=int(16 * self.escala)
        )

    def _desenhar_tecla_seta(self, tela, centro, direcao, pressionada):

        rect = pygame.Rect(0, 0, self.tecla, self.tecla)
        rect.center = centro

        self._desenhar_tecla(tela, rect, pressionada)

        icone = self.icones[direcao]

        if icone is not None:
            tela.blit(icone, icone.get_rect(center=rect.center))
        else:
            self._desenhar_seta_reserva(tela, rect.center, direcao)

    def _desenhar_seta_reserva(self, tela, centro, direcao):
        # só aparece se a imagem da Seta não puder ser carregada
        cx, cy = centro
        t = int(18 * self.escala)

        pontos = {
            "cima": [(cx, cy - t), (cx - t, cy + t), (cx + t, cy + t)],
            "baixo": [(cx, cy + t), (cx - t, cy - t), (cx + t, cy - t)],
            "esquerda": [(cx - t, cy), (cx + t, cy - t), (cx + t, cy + t)],
            "direita": [(cx + t, cy), (cx - t, cy - t), (cx - t, cy + t)],
        }[direcao]

        pygame.draw.polygon(tela, BRANCO, pontos)

    def _texto_centralizado(self, tela, fonte, texto, centro):

        render = fonte.render(texto, True, self.cor_texto)
        tela.blit(render, render.get_rect(center=centro))

    # ---------------------------------------------------------
    # Painel completo
    # ---------------------------------------------------------

    def desenhar(self, tela):

        teclas = pygame.key.get_pressed()
        pr = self.rect_painel
        e = self.escala
        tecla = self.tecla

        tela.blit(self.escurecer, (0, 0))

        if self.painel is not None:
            tela.blit(self.painel, pr)
        else:
            pygame.draw.rect(tela, (0, 0, 0), pr, border_radius=int(24 * self.escala))
            pygame.draw.rect(
                tela, BRANCO, pr,
                width=max(3, int(4 * self.escala)),
                border_radius=int(24 * self.escala)
            )

        # Título
        self._texto_centralizado(
            tela, self.fonte_titulo, "CONTROLES",
            (pr.centerx, pr.top + int(45 * e))
        )

        # ---------- Setas do teclado (esquerda / baixo+cima / direita) ----------

        cx = pr.left + int(pr.width * 0.30)
        y_baixo = pr.top + int(175 * e) + tecla // 2
        y_cima = y_baixo - tecla - self.espaco
        passo = tecla + self.espaco

        self._desenhar_tecla_seta(
            tela, (cx - passo, y_baixo), "esquerda", teclas[pygame.K_LEFT]
        )
        self._desenhar_tecla_seta(
            tela, (cx, y_baixo), "baixo", teclas[pygame.K_DOWN]
        )
        self._desenhar_tecla_seta(
            tela, (cx + passo, y_baixo), "direita", teclas[pygame.K_RIGHT]
        )
        self._desenhar_tecla_seta(
            tela, (cx, y_cima), "cima", teclas[pygame.K_UP]
        )

        self._texto_centralizado(
            tela, self.fonte_rotulo, "ACERTAR AS SETAS",
            (cx, y_baixo + tecla // 2 + int(32 * e))
        )

        # ---------- Tecla ESC ----------

        cx_esc = pr.left + int(pr.width * 0.76)
        cy_esc = (y_cima - tecla // 2 + y_baixo + tecla // 2) // 2

        rect_esc = pygame.Rect(0, 0, self.esc_largura, tecla)
        rect_esc.center = (cx_esc, cy_esc)

        self._desenhar_tecla(tela, rect_esc, teclas[pygame.K_ESCAPE])

        self._texto_centralizado(
            tela, self.fonte_esc, "ESC", rect_esc.center
        )

        self._texto_centralizado(
            tela, self.fonte_rotulo, "SAIR DA FASE",
            (cx_esc, y_baixo + tecla // 2 + int(32 * e))
        )

        # ---------- Rodapé (pisca) ----------

        # só aparece depois do atraso, quando já dá para continuar
        if self.pronto() and (pygame.time.get_ticks() // 500) % 2 == 0:
            self._texto_centralizado(
                tela, self.fonte_rodape, "ENTER PARA COMEÇAR",
                (pr.centerx, pr.bottom - int(45 * e))
            )