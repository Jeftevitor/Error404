import pygame

class Pontuacao:
    def __init__(self):
        self.pontos = 0
        self.combo = 0
        self.max_combo = 0

        self.pontos_perfeitos = 350
        self.pontos_bons = 200
        self.pontos_ruins = 50
        self.pontos_perdidos = 0

        self.janela_perfeita = 50
        self.janela_boa = 100
        self.janela_ruim = 150

        self.fonte = pygame.font.Font(None, 60)

    def calcular_pontos(self, tempo_reacao):
        tempo_reacao = abs(tempo_reacao)

        if tempo_reacao <= self.janela_perfeita:
            self.pontos += self.pontos_perfeitos
            self.combo += 1

            if self.combo > self.max_combo:
                self.max_combo = self.combo

            return "perfeito"

        elif tempo_reacao <= self.janela_boa:
            self.pontos += self.pontos_bons
            self.combo += 1

            if self.combo > self.max_combo:
                self.max_combo = self.combo

            return "bom"

        elif tempo_reacao <= self.janela_ruim:
            self.pontos += self.pontos_ruins
            self.combo = 0

            return "ruim"

        else:
            self.pontos += self.pontos_perdidos
            self.combo = 0

            return "errou"

    def resetar(self):
        self.pontos = 0
        self.combo = 0
        self.max_combo = 0
    
    def desenhar(self, tela, estado):
        if estado == "perfeito":
            texto = self.fonte.render("Perfeito!", True, (255, 255, 255))
        elif estado == "bom":
            texto = self.fonte.render("Bom!", True, (255, 255, 255))
        elif estado == "ruim":
            texto = self.fonte.render("É...", True, (255, 255, 255))
        elif estado == "errou":
            texto = self.fonte.render("Errou!", True, (255, 255, 255))
        else:
            return

        texto_rect = texto.get_rect(center=(600, 100))
        tela.blit(texto, texto_rect)