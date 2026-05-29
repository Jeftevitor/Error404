import pygame
from Class.seta import Seta
from Class.sinc import Sinc

class Jogo:
    def __init__(self):
        pygame.init()

        self.largura = 1200
        self.altura = 720
        
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Error404")
        self.clock = pygame.time.Clock()
        self.rodando = True
        
        self.seta_esquerda = Seta(310,300,direcao= "esquerda")
        self.seta_baixo = Seta(410,300,direcao= "baixo")
        self.seta_cima = Seta(510,300,direcao= "cima")
        self.seta_direita = Seta(610,300,direcao= "direita")

        self.setas = []

        self.setas.append(Seta(self.seta_esquerda.x, -100, 'esquerda'))
        self.setas.append(Seta(self.seta_baixo.x, -300, 'baixo'))
        self.setas.append(Seta(self.seta_cima.x, -500, 'cima'))
        self.setas.append(Seta(self.seta_cima.x, -500, 'cima'))
        self.setas.append(Seta(self.seta_direita.x, -700, 'direita'))
        self.setas.append(Seta(self.seta_direita.x, -800, 'direita'))
        self.setas.append(Seta(self.seta_cima.x, -900, 'cima'))

        self.sinc = Sinc(self)

    def processa_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
                
    def atualizar(self):
        for seta in self.setas:
            seta.mover()
            seta.acertou()
        self.sinc.verificar_sinc(self.setas)

    def desenhar(self):
        self.tela.fill((0, 0, 0))
        self.seta_esquerda.desenhar(self.tela)
        self.seta_baixo.desenhar(self.tela)
        self.seta_cima.desenhar(self.tela)
        self.seta_direita.desenhar(self.tela)
        for seta in self.setas:
            seta.desenhar(self.tela)
        pygame.display.update()

    def iniciar(self):
        while self.rodando:
            self.processa_eventos()
            self.atualizar()
            self.desenhar()
            self.clock.tick(60)
        pygame.quit()