import pygame
from Class.seta import Seta
from Class.sinc import Sinc
from Class.pontuacao import Pontuacao
from Class.tela_inicial import TelaInicial
from Class.intro import Intro

teclas_setas = {
    pygame.K_LEFT: 'esquerda',
    pygame.K_DOWN: 'baixo',
    pygame.K_UP: 'cima',
    pygame.K_RIGHT: 'direita'
}

class Jogo:
    def __init__(self):
        pygame.init()

        pygame.mixer.init()

        pygame.mixer.music.load(
            'Assets/Music/Menu.ogg'
            )

        pygame.mixer.music.play(-1)

        self.tempo_inicio = pygame.time.get_ticks()

        self.largura = 1200
        self.altura = 720
        
        self.estado = "intro"

        self.tela = pygame.display.set_mode((self.largura, self.altura))

        pygame.display.set_caption("Error404")

        self.tela_inicial = TelaInicial(self.largura,self.altura)
        self.intro = Intro(self.largura,self.altura)
        
        pygame.display.set_caption("Error404")
        self.clock = pygame.time.Clock()
        self.rodando = True

        self.seta_esquerda = Seta(310, 300, direcao="esquerda")
        self.seta_baixo = Seta(410, 300, direcao="baixo")
        self.seta_cima = Seta(510, 300, direcao="cima")
        self.seta_direita = Seta(610, 300, direcao="direita")

        self.receptores = {
            'esquerda': self.seta_esquerda,
            'baixo': self.seta_baixo,
            'cima': self.seta_cima,
            'direita': self.seta_direita
        }

        self.setas = []

        self.notas = []

        with open("Assets/Arquivos_txt/fase1.txt", "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                tempo, direcao = linha.strip().split()
                self.notas.append((int(tempo), direcao))
            
        self.indice_nota = 0
        self.tempo_inicio = 0



        self.pontuacao = Pontuacao()

        self.duracao_exibicao = 500
        self.zona_hit = 300

        self.ultimo_julgamento = ""
        self.tempo_julgamento = 0

    def verificar_toque(self):
        teclas = pygame.key.get_pressed()
        for tecla, direcao in teclas_setas.items():
            if teclas[tecla]:
                receptor = self.receptores[direcao]
                for seta in self.setas:
                    if seta.direcao == direcao:
                        diferenca = abs(seta.y - receptor.y)
                        if diferenca <= self.pontuacao.janela_ruim:
                            seta.hit = True
                            julgamento = (self.pontuacao.calcular_pontos(diferenca))
                            self.ultimo_julgamento = julgamento
                            self.tempo_julgamento = (
                                pygame.time.get_ticks()
                            )
                            return

    def processa_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
            if self.estado == "intro":
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        self.estado = "menu"
            elif self.estado == "menu":

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    botao = self.tela_inicial.verificar_clique(
                        evento.pos
                    )
                    if botao == "comecar":
                        self.estado = "jogo"
                        pygame.mixer.music.stop()

                        pygame.mixer.music.load(
                            'Assets/Music/Joaildo.ogg'
                        )
                        pygame.mixer.music.play()
                    elif botao == "score":
                        pass
                    elif botao == "creditos":
                        pass
                    elif botao == "sair":
                        self.rodando = False
    def atualizar(self):
        if self.estado != "jogo":
            return
        
        tempo = pygame.time.get_ticks() - self.tempo_inicio

        while (
        self.indice_nota < len(self.notas)
        and tempo >= self.notas[self.indice_nota][0]
    ):
            _, direcao = self.notas[self.indice_nota]

        receptor = self.receptores[direcao]

        self.setas.append(
            Seta(receptor.x, -100, direcao)
        )

        self.indice_nota += 1

        for seta in self.setas:
            seta.mover()
            seta.acertou()
        self.verificar_toque()
        
    def desenhar(self):
        if self.estado == "intro":
            self.intro.desenhar(self.tela)
            pygame.display.update()
            return
        if self.estado == "menu":
            self.tela_inicial.desenhar(self.tela)
            pygame.display.update()
            return
        
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