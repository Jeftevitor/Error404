import pygame
from Class.receptor import Receptor

class Sinc:
    def __init__(self,jogo):
        self.receptores = []

        self.receptores.append(Receptor (jogo.seta_esquerda.x, jogo.seta_esquerda.y, 'esquerda' )) 
        self.receptores.append(Receptor (jogo.seta_baixo.x, jogo.seta_baixo.y, 'baixo' )) 
        self.receptores.append(Receptor (jogo.seta_cima.x, jogo.seta_cima.y, 'cima' )) 
        self.receptores.append(Receptor (jogo.seta_direita.x, jogo.seta_direita.y, 'direita' ))

    def verificar_sinc(self, setas):
        for receptor in self.receptores:
            if receptor.verificar_input():
                for seta in setas:
                    if receptor.verificar_colisao(seta):
                        seta.acertada = True