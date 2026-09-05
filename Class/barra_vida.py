import pygame


class BarraVida:

    def __init__(self, x, y, largura, altura, vida_maxima=100):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.vida_maxima = vida_maxima

        self.vida_jogador = vida_maxima
        self.vida_professor = vida_maxima

        self.valor_exibido = 50.0

        self.velocidade = 0.08

        self.cor_fundo = (35, 35, 40)
        self.cor_jogador = (90, 210, 130)      # verde (lado direito)
        self.cor_professor = (160, 32, 240)     # vermelho (lado esquerdo)
        self.cor_borda = (0, 0, 0)
        self.espessura_borda = 3


    def reset(self):
        self.vida_jogador = self.vida_maxima
        self.vida_professor = self.vida_maxima
        self.valor_exibido = 50.0

    def dano_jogador(self, quantidade):
        self.vida_jogador -= quantidade
        if self.vida_jogador < 0:
            self.vida_jogador = 0

    def dano_professor(self, quantidade):
        self.vida_professor -= quantidade
        if self.vida_professor < 0:
            self.vida_professor = 0

    def jogador_perdeu(self):
        return self.vida_jogador <= 0

    def professor_perdeu(self):
        return self.vida_professor <= 0


    def atualizar(self):
        total = self.vida_jogador + self.vida_professor

        if total <= 0:
            valor_alvo = 50.0
        else:
            valor_alvo = (self.vida_jogador / total) * 100.0


        self.valor_exibido += (valor_alvo - self.valor_exibido) * self.velocidade

    def desenhar(self, tela):

        pygame.draw.rect(
            tela, self.cor_fundo,
            (self.x, self.y, self.largura, self.altura),
            border_radius=self.altura // 2
        )

        corte = int(self.largura * (self.valor_exibido / 100))
        corte = max(0, min(self.largura, corte))  

        superficie = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)

        pygame.draw.rect(superficie, self.cor_professor, (0, 0, corte, self.altura))

        pygame.draw.rect(superficie, self.cor_jogador, (corte, 0, self.largura - corte, self.altura))

        mascara = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        pygame.draw.rect(mascara, (255, 255, 255, 255), (0, 0, self.largura, self.altura),
                          border_radius=self.altura // 2)
        superficie.blit(mascara, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

        tela.blit(superficie, (self.x, self.y))

        pygame.draw.rect(
            tela, self.cor_borda,
            (self.x, self.y, self.largura, self.altura),
            width=self.espessura_borda, border_radius=self.altura // 2
        )