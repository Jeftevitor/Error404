import pygame
from Class.seta import Seta

class Jogo:
    def __init__(self):
        pygame.init()
        self.largura = 1200
        self.altura = 720
        self.tela = pygame.display.set_mode((self.largura,self.altura))
        pygame.display.set_caption("Error404")
        self.seta_esquerda = Seta(310,300,direcao= "esquerda")
        self.seta_baixo = Seta(410,300,direcao= "baixo")
        self.seta_cima = Seta(510,300,direcao= "cima")
        self.seta_direita = Seta(610,300,direcao= "direita")
        self.rodando = True
        self.clock = pygame.time.Clock()
        
    def processa_evento(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False     

    def desenhar(self):
        self.tela.fill((0,0,0))
        self.seta_esquerda.desenhar(self.tela)
        self.seta_baixo.desenhar(self.tela)
        self.seta_cima.desenhar(self.tela)
        self.seta_direita.desenhar(self.tela)
        pygame.display.update()
    
    def iniciar(self):
        while self.rodando:
            self.desenhar()
            self.clock.tick(60)
        pygame.quit()