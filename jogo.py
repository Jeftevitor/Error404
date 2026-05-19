import pygame
from Models.Personagem import Personagem

class Jogo:

    def __init__(self):
        pygame.init()
        self.largura = 1000
        self.altura = 720
        self.tela = pygame.display.set_mode((self.largura,self.altura))
        pygame.display.set_caption("Principal")
        self.personagem = Personagem(100,650)
        self.rodando = True
        self.clock = pygame.time.Clock()
    
    def processa_evento(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False

    def setas(self, setas):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP]:
            self.setas.mover("cima")
        if teclas[pygame.K_DOWN]:
            self.setas.mover("baixo")
        if teclas[pygame.K_LEFT]:
            self.setas.mover("esquerda")
        if teclas[pygame.K_RIGHT]:
            self.setas.mover("direita")
        

    def desenhar(self):
        self.tela.fill((0,0,0))
        self.personagem.desenhar(self.tela)
        pygame.display.update()
    
    def iniciar(self):
        while self.rodando:
            self.processa_evento()
            self.desenhar()
            self.clock.tick(60)
        pygame.quit()