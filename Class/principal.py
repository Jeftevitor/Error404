import pygame
from Models.personagem import Personagem
from Models.pontuacao import Pontuacao  

class Principal(Personagem):

    def __init__(self, x, y, nome, seta, sprite):
        super().__init__(x, y, nome, seta)

        self.nota = 50
        self.estado = None
        self.sprite = sprite
        self.pontuacao = Pontuacao()
        self.julgamento = ""
        self.tempo_reacao = 0
        self.duracao_exibicao = 0

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
        if self.seta == 'cima':
            tela.blit(self.sprite, (self.x, self.y))

        elif self.seta == 'baixo':
            tela.blit(self.sprite, (self.x, self.y))

        elif self.seta == 'esquerda':
            tela.blit(self.sprite, (self.x, self.y))

        elif self.seta == 'direita':
            tela.blit(self.sprite, (self.x, self.y))
            
        elif self.estado == 'morrer':
            tela.blit(self.sprite, (self.x, self.y))
        
        # IDLE 
        else:
            tela.blit(self.sprite, (self.x, self.y))

        self.desenhar_julgamento(tela)
        self.desenhar_pontos(tela)
    
    def verificar_toque(self, tempo_reacao):
        tempo_atual = pygame.time.get_ticks()
        diferenca = tempo_atual - tempo_reacao

        if abs(diferenca) <= self.pontuacao.janela_ruim:
            julgamento = self.pontuacao.calcular_pontos(diferenca)
            self.julgamento = julgamento
            self.tempo_reacao = pygame.time.get_ticks()
        else:
            self.julgamento = 'miss'
            self.tempo_reacao = pygame.time.get_ticks()

    def desenhar_julgamento(self, tela):
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.tempo_reacao < self.duracao_exibicao:
            if self.julgamento == 'perfeito':
                cor = (0, 255, 0)
            elif self.julgamento == 'bom':
                cor = (0, 100, 255)
            elif self.julgamento == 'ruim':
                cor = (255, 255, 0)
            else:
                cor = (255, 0, 0)

            fonte = pygame.font.Font(None, 36)
            texto = fonte.render(self.julgamento.upper(), True, cor)
            tela.blit(texto, (self.x, self.y - 50))

    def desenhar_pontos(self, tela):
        fonte = pygame.font.Font(None, 36)
        texto_pontos = fonte.render(f'Pontos: {self.pontuacao.pontos}', True, (255, 255, 255))
        tela.blit(texto_pontos, (10, 10))

        if self.pontuacao.combo > 0:
            texto_combo = fonte.render(f'Combo: {self.pontuacao.combo}', True, (255, 255, 255))
            tela.blit(texto_combo, (10, 50))