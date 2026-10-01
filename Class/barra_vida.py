import math
import pygame


class BarraVida:
    # =====================================================
    # BALANCEAMENTO(%)
    # =====================================================
    VIDA_INICIAL = 50.0         # a barra começa na metade
    PERDA_SETA_PERDIDA = 7.0    # jogador deixou a seta passar
    CURA_ACERTO = 3.0           # jogador acertou uma seta
    PERDA_TOQUE_ERRADO = 4.0    # jogador apertou sem ter seta para acertar

    # =====================================================
    # ANIMAÇÃO
    # =====================================================
    SUAVIZACAO_DESCIDA = 15.0   
    SUAVIZACAO_SUBIDA = 9.0     
    DURACAO_FLASH = 0.25        

    def __init__(self, x, y, largura, altura):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.raio = altura // 2  # bordas totalmente arredondadas

        # Vida real (o jogo lê e altera esses valores)
        self.vida_maxima = 1000.0
        self.vida_jogador = self.vida_maxima * self.VIDA_INICIAL / 100.0

        # Valor só visual, em % (0 a 100)
        self.valor_exibido = self.VIDA_INICIAL

        self._alvo_anterior = self.VIDA_INICIAL
        self._flash = 0.0
        self._ultimo_tick = None

        self.cor_jogador = (90, 210, 130)
        self.cor_professor = (160, 32, 240)
        self.cor_borda = (255, 255, 255)

        # Superfície reaproveitada e máscara com cantos arredondados
        self._superficie = pygame.Surface((largura, altura), pygame.SRCALPHA)
        self._mascara = pygame.Surface((largura, altura), pygame.SRCALPHA)
        pygame.draw.rect(
            self._mascara, (255, 255, 255, 255),
            (0, 0, largura, altura), border_radius=self.raio
        )

    # -----------------------------------------------------
    # Eventos do jogo
    # -----------------------------------------------------
    def _pct(self, porcentagem):
        return self.vida_maxima * porcentagem / 100.0

    def seta_perdida(self):
        self.dano_jogador(self._pct(self.PERDA_SETA_PERDIDA))

    def toque_errado(self):
        self.dano_jogador(self._pct(self.PERDA_TOQUE_ERRADO))

    def acerto(self, multiplicador=1.0):
        self.curar(self._pct(self.CURA_ACERTO) * multiplicador)

    def dano_jogador(self, dano):
        self.vida_jogador -= dano
        self.vida_jogador = max(0.0, min(self.vida_maxima, self.vida_jogador))

    def curar(self, valor):
        self.vida_jogador += valor
        self.vida_jogador = max(0.0, min(self.vida_maxima, self.vida_jogador))

    def dano_professor(self, dano):
        pass

    def reset(self):
        self.vida_jogador = self.vida_maxima * self.VIDA_INICIAL / 100.0
        self.valor_exibido = self.VIDA_INICIAL
        self._alvo_anterior = self.VIDA_INICIAL
        self._flash = 0.0
        self._ultimo_tick = None

    def jogador_perdeu(self):
        return self.vida_jogador <= 0

    # -----------------------------------------------------
    # Animação
    # -----------------------------------------------------
    def atualizar(self):
        agora = pygame.time.get_ticks()
        if self._ultimo_tick is None:
            dt = 1.0 / 60.0
        else:
            dt = (agora - self._ultimo_tick) / 1000.0
        self._ultimo_tick = agora
        dt = max(0.0, min(dt, 0.05))  # evita saltos após pausas/contagem

        alvo = (self.vida_jogador / self.vida_maxima) * 100.0

        if alvo < self._alvo_anterior - 1e-6:
            self._flash = 1.0
        self._alvo_anterior = alvo

        taxa = (
            self.SUAVIZACAO_DESCIDA
            if alvo < self.valor_exibido
            else self.SUAVIZACAO_SUBIDA
        )
        self.valor_exibido += (alvo - self.valor_exibido) * (1.0 - math.exp(-taxa * dt))
        if abs(alvo - self.valor_exibido) < 0.02:
            self.valor_exibido = alvo

        self._flash = max(0.0, self._flash - dt / self.DURACAO_FLASH)

    # -----------------------------------------------------
    # Desenho
    # -----------------------------------------------------
    @staticmethod
    def _misturar(cor_a, cor_b, t):
        return tuple(int(a + (b - a) * t) for a, b in zip(cor_a, cor_b))

    def desenhar(self, tela):
        p = max(0.0, min(1.0, self.valor_exibido / 100.0))
        largura_jogador = int(round(self.largura * p))
        self._superficie.fill(self.cor_professor)

        if largura_jogador > 0:
            cor = self._misturar(self.cor_jogador, (255, 255, 255), 0.6 * self._flash)
            pygame.draw.rect(
                self._superficie, cor,
                (0, 0, largura_jogador, self.altura)
            )

        self._superficie.blit(
            self._mascara, (0, 0),
            special_flags=pygame.BLEND_RGBA_MULT
        )
        tela.blit(self._superficie, (self.x, self.y))

        pygame.draw.rect(
            tela, self.cor_borda,
            (self.x, self.y, self.largura, self.altura),
            2, border_radius=self.raio
        )