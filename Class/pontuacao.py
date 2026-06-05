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

    def calcular_pontos(self, tempo_reacao):
        tempo_reacao = abs(tempo_reacao)

        if tempo_reacao <= self.janela_perfeita:
            self.pontos += self.pontos_perfeitos
            self.combo += 1
            return 'perfeito'

        elif tempo_reacao <= self.janela_boa:
            self.pontos += self.pontos_bons
            self.combo += 1
            return 'bom'

        elif tempo_reacao <= self.janela_ruim:
            self.pontos += self.pontos_ruins
            self.combo = 0 
            return 'ruim'

        else:
            self.pontos += self.pontos_perdidos
            self.combo = 0 
            return 'miss'

        if self.combo > self.max_combo:
            self.max_combo = self.combo

    def resetar_combo(self):
        self.ponto = 0  
        self.combo = 0
        self.max_combo = 0