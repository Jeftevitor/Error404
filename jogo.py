import pygame
from Class.seta import Seta
from Class.sinc import Sinc

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

        from Class.pontuacao import Pontuacao
        self.pontuacao = Pontuacao()

        self.duracao_exibicao = 500
        self.zona_hit = 300

        self.ultimo_julgamento = ""
        self.tempo_julgamento = 0

    def processa_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False

            elif evento.type == pygame.KEYDOWN:
                if evento.key in teclas_setas:
                    direcao = teclas_setas[evento.key]
                    self.verificar_toque(direcao)

    def verificar_toque(self, direcao):
        tempo_atual = pygame.time.get_ticks()

        nota_encontrada = None
        menor_distancia = float('inf')

        for seta in self.setas:
            if seta.direcao == direcao and not seta.hit:
                distancia = abs(seta.y - self.zona_hit)

                if distancia < self.pontuacao.janela_ruim:
                    menor_distancia = distancia
                    nota_encontrada = seta

        if nota_encontrada:
            nota_encontrada.hit = True
            julgamento = self.pontuacao.calcular_pontos(menor_distancia)
            self.ultimo_julgamento = julgamento
            self.tempo_julgamento = tempo_atual
        else:
            self.ultimo_julgamento = 'miss'
            self.tempo_julgamento = tempo_atual
            self.pontuacao.combo = 0
  


    def atualizar(self):
        for seta in self.setas:
            seta.mover()
            seta.acertou()

        for seta in self.setas:
            if seta.y > self.zona_hit + self.pontuacao.janela_ruim and not seta.hit:
                seta.hit = True # Marca como "passed"
                self.pontuacao.combo = 0
                self.ultimo_julgamento = "miss"
                self.tempo_julgamento = pygame.time.get_ticks()

        self.sinc.verificar_sinc(self.setas)

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

    def desenhar_pontuacao(self):
        fonte = pygame.font.SysFont(None, 36)
        texto_pontos = fonte.render(f'Pontos: {self.pontuacao.pontos}', True, (255, 255, 255))
        self.tela.blit(texto_pontos, (10, 10))
        
        if self.pontuacao.combo > 0:
            texto_combo = fonte.render(f'Combo: {self.pontuacao.combo}', True, (255, 255, 255))
            self.tela.blit(texto_combo, (10, 50))
        
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.tempo_julgamento < self.duracao_exibicao:
            if self.ultimo_julgamento == 'perfeito':
                cor = (0, 255, 0)
            elif self.ultimo_julgamento == 'bom':
                cor = (0, 100, 255)
            elif self.ultimo_julgamento == 'ruim':
                cor = (255, 255, 0)
            else:
                cor = (255, 0, 0)
            
            texto_julgamento = fonte.render(self.ultimo_julgamento.upper(), True, cor)
            x = (self.largura - texto_julgamento.get_width()) // 2
            y = self.altura // 2 - 100
            self.tela.blit(texto_julgamento, (x, y))

    def iniciar(self):
        while self.rodando:
            self.processa_eventos()
            self.atualizar()
            self.desenhar()
            self.clock.tick(60)
        pygame.quit()