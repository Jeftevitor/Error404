import pygame
from Class.seta import Seta
from Class.sinc import Sinc
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
        self.sinc = Sinc(self)

        from Class.pontuacao import Pontuacao
        self.pontuacao = Pontuacao()

      
        self.nota_player = 50
        self.nota_enemy = 50

      
        self.player_name = 'DUDU'
        self.player_gender = 'M'
        self.enemy_name = 'VILÃO'

        
        self.fase_atual = 1
        self.fases_desbloqueadas = [True, False, False]
        self.fase_vencida = False
        self.rodando_fase = False

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

            self.atualizar_vida(julgamento)
        else:
            self.ultimo_julgamento = 'miss'
            self.tempo_julgamento = tempo_atual
            self.pontuacao.combo = 0
            self.atualizar_vida('miss')
  


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
        self.verificar_fim_de_fase()

    def desenhar(self):
        self.tela.fill((0, 0, 0))
        self.seta_esquerda.desenhar(self.tela)
        self.seta_baixo.desenhar(self.tela)
        self.seta_cima.desenhar(self.tela)
        self.seta_direita.desenhar(self.tela)
        for seta in self.setas:
            seta.desenhar(self.tela)
        self.desenhar_barra_vida()
        self.desenhar_pontuacao()
        pygame.display.update()

    def iniciar_fase(self, fase):
        self.fase_atual = fase
        self.fase_vencida = False
        self.rodando_fase = True

        self.pontuacao.pontos = 0
        self.pontuacao.combo = 0
        self.pontuacao.max_combo = 0

        self.nota_player = 50
        self.nota_enemy = 50
        self.setas = []
        self.carregar_setas_fase(fase)

        while self.rodando and self.rodando_fase:
            self.processa_eventos()
            self.atualizar()
            self.desenhar()
            self.clock.tick(60)

        return self.fase_vencida

    def carregar_setas_fase(self, fase):
        if fase == 1:
            self.setas.append(Seta(self.seta_esquerda.x, -100, 'esquerda'))
            self.setas.append(Seta(self.seta_baixo.x, -300, 'baixo'))
            self.setas.append(Seta(self.seta_cima.x, -500, 'cima'))
            self.setas.append(Seta(self.seta_cima.x, -700, 'cima'))
            self.setas.append(Seta(self.seta_direita.x, -900, 'direita'))
            self.setas.append(Seta(self.seta_direita.x, -1100, 'direita'))
            self.setas.append(Seta(self.seta_cima.x, -1300, 'cima'))

            #Apenas teste para futuramente colocar os arquivos txt em cada fase.

        elif fase == 2:
            self.setas.append(Seta(self.seta_cima.x, -80, 'cima'))
            self.setas.append(Seta(self.seta_direita.x, -180, 'direita'))
            self.setas.append(Seta(self.seta_esquerda.x, -280, 'esquerda'))
            self.setas.append(Seta(self.seta_baixo.x, -380, 'baixo'))
            self.setas.append(Seta(self.seta_cima.x, -480, 'cima'))
            self.setas.append(Seta(self.seta_direita.x, -580, 'direita'))
            self.setas.append(Seta(self.seta_esquerda.x, -680, 'esquerda'))
            self.setas.append(Seta(self.seta_baixo.x, -780, 'baixo'))
        elif fase == 3:
            self.setas.append(Seta(self.seta_cima.x, -40, 'cima'))
            self.setas.append(Seta(self.seta_direita.x, -120, 'direita'))
            self.setas.append(Seta(self.seta_esquerda.x, -200, 'esquerda'))
            self.setas.append(Seta(self.seta_baixo.x, -280, 'baixo'))
            self.setas.append(Seta(self.seta_cima.x, -360, 'cima'))
            self.setas.append(Seta(self.seta_direita.x, -440, 'direita'))
            self.setas.append(Seta(self.seta_esquerda.x, -520, 'esquerda'))
            self.setas.append(Seta(self.seta_baixo.x, -600, 'baixo'))
            self.setas.append(Seta(self.seta_cima.x, -680, 'cima'))
            self.setas.append(Seta(self.seta_direita.x, -760, 'direita'))

    def verificar_fim_de_fase(self):
        if self.nota_enemy <= 0:
            self.fase_vencida = True
            self.rodando_fase = False
            return

        if self.nota_player <= 0:
            self.fase_vencida = False
            self.rodando_fase = False
            return

        if len(self.setas) > 0 and all(seta.hit for seta in self.setas):
            self.fase_vencida = self.nota_player >= self.nota_enemy
            self.rodando_fase = False

    def atualizar_vida(self, julgamento):

        if julgamento == 'perfeito':
            delta_player = 6
            delta_enemy = -6
        elif julgamento == 'bom':
            delta_player = 3
            delta_enemy = -3
        elif julgamento == 'ruim':
            delta_player = -2
            delta_enemy = 2
        else:  
            delta_player = -5
            delta_enemy = 5

        self.nota_player = max(0, min(100, self.nota_player + delta_player))
        self.nota_enemy = max(0, min(100, self.nota_enemy + delta_enemy))

    def desenhar_barra_vida(self):
        largura_total = 600
        altura = 24
        x = (self.largura - largura_total) // 2
        y = 10

        pygame.draw.rect(self.tela, (40, 40, 40), (x, y, largura_total, altura), border_radius=6)

        largura_inimigo = int((self.nota_enemy / 100) * largura_total)
        largura_player = int((self.nota_player / 100) * largura_total)

        if largura_inimigo > 0:
            pygame.draw.rect(self.tela, (200, 50, 50), (x, y, largura_inimigo, altura), border_radius=6)

        if largura_player > 0:
            px = x + largura_total - largura_player
            pygame.draw.rect(self.tela, (80, 170, 255), (px, y, largura_player, altura), border_radius=6)

            pygame.draw.rect(self.tela, (255, 255, 255), (x, y, largura_total, altura), 2, border_radius=6)

       
        fonte = pygame.font.SysFont(None, 24)
        texto_enemy = fonte.render(self.enemy_name, True, (255, 255, 255))
        texto_player = fonte.render(self.player_name, True, (255, 255, 255))
        self.tela.blit(texto_enemy, (x - texto_enemy.get_width() - 8, y))
        self.tela.blit(texto_player, (x + largura_total + 8, y))

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
        tela_ini = TelaInicial(self.tela, self.largura, self.altura)
        player_info = tela_ini.run()
        if not player_info:
            pygame.quit()
            return

        self.player_name = player_info.get('name', self.player_name)
        self.player_gender = player_info.get('gender', self.player_gender)

        while self.rodando:
            fase = tela_ini.escolher_fase(self.fases_desbloqueadas)
            if fase is None:
                break

            fase_vencida = self.iniciar_fase(fase)
            if fase_vencida:
                if fase < len(self.fases_desbloqueadas):
                    self.fases_desbloqueadas[fase] = True
            else:
                break

        pygame.quit()