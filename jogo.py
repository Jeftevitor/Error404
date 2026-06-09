import pygame
from Class.seta import Seta
from Class.sinc import Sinc
from Class.pontuacao import Pontuacao
from Class.tela_inicial import TelaInicial

teclas_setas = {
    pygame.K_LEFT: 'esquerda',
    pygame.K_DOWN: 'baixo', 
    pygame.K_UP: 'cima',
    pygame.K_RIGHT: 'direita'
}

class Jogo:
    def __init__(self):
        pygame.init()

        self.largura = 1200
        self.altura = 720

        self.tela_inicial = TelaInicial(1200, 720)
        self.estado = "menu"

        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Error404")
        self.clock = pygame.time.Clock()
        self.rodando = True
        
        self.seta_esquerda = Seta(310,300,direcao= "esquerda")
        self.seta_baixo = Seta(410,300,direcao= "baixo")
        self.seta_cima = Seta(510,300,direcao= "cima")
        self.seta_direita = Seta(610,300,direcao= "direita")

        self.receptores = {
            'esquerda': self.seta_esquerda,
            'baixo': self.seta_baixo,
            'cima': self.seta_cima,
            'direita': self.seta_direita
        }

        self.setas = []

        self.setas.append(Seta(self.seta_esquerda.x, -100, 'esquerda'))
        self.setas.append(Seta(self.seta_baixo.x, -300, 'baixo'))
        self.setas.append(Seta(self.seta_cima.x, -500, 'cima'))
        self.setas.append(Seta(self.seta_cima.x, -500, 'cima'))
        self.setas.append(Seta(self.seta_direita.x, -700, 'direita'))
        self.setas.append(Seta(self.seta_direita.x, -800, 'direita'))
        self.setas.append(Seta(self.seta_cima.x, -900, 'cima'))

        self.sinc = Sinc(self)

        self.pontuacao = Pontuacao()

        self.duracao_exibicao = 500
        self.zona_hit = 300

        self.ultimo_julgamento = ""
        self.tempo_julgamento = 0

    def verificar_toque(self, direcao):
        receptor = self.receptores[direcao]

        for seta in self.setas:
            if seta.direcao == direcao and not seta.hit:

                diferenca = abs(seta.y - receptor.y)

                if diferenca <= self.pontuacao.janela_ruim:
                    seta.hit = True

                    julgamento = self.pontuacao.calcular_pontos(diferenca)

                    self.julgamento = julgamento
                    self.tempo_reacao = pygame.time.get_ticks()

                    return
                
    def processa_eventos(self):
        if self.estado == "menu":
            if evento.type == pygame.MOUSEBUTTONDOWN:

                botao = self.tela_inicial.verificar_clique(evento.pos)

                if botao == "comecar":
                    self.estado = "jogo"

                elif botao == "score":
                    print("Tela de score")

                elif botao == "creditos":
                    print("Tela de créditos")

                elif botao == "sair":
                    self.rodando = False
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
                
    def atualizar(self):
        for seta in self.setas:
            seta.mover()
            seta.acertou()
        self.verificar_toque()

    def desenhar(self):
        self.tela.fill((0, 0, 0))
        self.seta_esquerda.desenhar(self.tela)
        self.seta_baixo.desenhar(self.tela)
        self.seta_cima.desenhar(self.tela)
        self.seta_direita.desenhar(self.tela)
        for seta in self.setas:
            seta.desenhar(self.tela)
            self.desenhar_pontuacao()
        pygame.display.update()

    def iniciar(self):
        while self.rodando:
            if self.estado == "menu":
                self.tela_inicial.desenhar(self.tela)
            self.processa_eventos()
            self.atualizar()
            self.desenhar()
            self.clock.tick(60)
        pygame.quit()