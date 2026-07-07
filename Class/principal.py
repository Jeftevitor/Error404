import pygame
from Models.Personagem import Personagem

class Principal(Personagem):

    def __init__(self, x, y, nome, seta, sprite, setas, receptores):
        super().__init__(x, y, nome, seta)

        self.setas = setas
        self.receptores = receptores

        self.nota = 50
        self.estado = None
        self.sprite = sprite

    def perder_nota(self, seta_apertada):
        if seta_apertada != self.seta:
            self.nota -= 5
    
    def ganhar_nota(self, seta_apertada):
        if seta_apertada == self.seta:
            self.nota += 5

            if self.nota > 100:
                self.nota = 100
        
    def morrer(self):
        if self.nota <= 0:
            self.estado = 'morrer'
    
    def desenhar(self, tela):
        super().desenhar(tela)