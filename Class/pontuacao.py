import pygame
import os

class Pontuacao:
    def __init__(self):
        self.pontos = 0
        self.combo = 0
        self.max_combo = 0

        self.pontos_perfeitos = 250
        self.pontos_bons = 150
        self.pontos_ruins = 50
        self.pontos_perdidos = 0

        self.janela_perfeita = 50
        self.janela_boa = 100
        self.janela_ruim = 150

        imagens = {
            "perfeito": "Assets/Telas/p_perfeito.png",
            "bom": "Assets/Telas/p_bom.png",
            "ruim": "Assets/Telas/p_é.png",
            "errou": "Assets/Telas/p_errou.png",
        }

        self.imagens = {}
        for julgamento, caminho in imagens.items():
            if os.path.exists(caminho):
                imagem = pygame.image.load(caminho).convert_alpha()
                tamanho = (220, 147) if julgamento == "bom" else (240, 160)
                self.imagens[julgamento] = pygame.transform.smoothscale(
                    imagem,
                    tamanho
                )
            else:
                self.imagens[julgamento] = None

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
        if estado not in self.imagens:
            return

        imagem = self.imagens[estado]
        if imagem is not None:
            tela.blit(imagem, imagem.get_rect(center=(600, 145)))