import pygame
from Class.seta import Seta
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
        pygame.mixer.music.load('Assets/Music/Menu.ogg')
        pygame.mixer.music.play(-1)

        self.largura = 1200
        self.altura = 720

        self.estado = "intro"

        self.fase_selecionada = 0

        self.fases = [
            {
                "nome": "Joaildo",
                "arquivo": "Assets/Arquivos_txt/fase1.txt",
                "musica": "Assets/Music/JOJO(freak-ariana grande).ogg",
                "desbloqueada": True
            },
            {
                "nome": "Max e Hugo",
                "arquivo": "Assets/Arquivos_txt/fase2.txt",
                "musica": "Assets/Music/Max_e_Hugo.ogg",
                "desbloqueada": False
            },
            {
                "nome": "Romerito",
                "arquivo": "Assets/Arquivos_txt/fase3.txt",
                "musica": "Assets/Music/Romerito.ogg",
                "desbloqueada": False
            }
        ]

        self.tela = pygame.display.set_mode(
            (self.largura, self.altura)
        )

        pygame.display.set_caption("Error404")

        self.tela_inicial = TelaInicial(self.largura,self.altura)

        self.intro = Intro(self.largura,self.altura)

        self.clock = pygame.time.Clock()
        self.rodando = True

        self.seta_esquerda = Seta(310,300,"esquerda")
        self.seta_baixo = Seta(410,300,"baixo")
        self.seta_cima = Seta(510,300,"cima")
        self.seta_direita = Seta(610,300,"direita")

        self.receptores = {
            "esquerda": self.seta_esquerda,
            "baixo": self.seta_baixo,
            "cima": self.seta_cima,
            "direita": self.seta_direita
        }

        self.setas = []

        self.notas = []

        self.indice_nota = 0
        self.tempo_inicio = 0

        self.pontuacao = Pontuacao()

        self.ultimo_julgamento = ""
        self.tempo_julgamento = 0
        self.duracao_exibicao = 500

        self.vida_jogador = 100
        self.vida_professor = 100

        self.barra_vida100 = pygame.image.load("Assets/Barras_de_vida/Joaildo(barra de vida - boy)100.png").convert_alpha()
        self.barra_vida60 = pygame.image.load("Assets/Barras_de_vida/Joaildo(barra de vida - boy)60.png").convert_alpha()
        self.barra_vida0 = pygame.image.load("Assets/Barras_de_vida/Joaildo(barra de vida - boy)0.png").convert_alpha()
        self.barra_vidaj60 = pygame.image.load("Assets/Barras_de_vida/Joaildo(barra de vida - boy)j60.png").convert_alpha()
        self.barra_vidaj0 = pygame.image.load("Assets/Barras_de_vida/Joaildo(barra de vida - boy)j0.png").convert_alpha()

        self.barra_vida_atual = self.barra_vida100

#=======================VERIFICAR TOQUE=====================

    def verificar_toque(self):
        teclas = pygame.key.get_pressed()
        for tecla, direcao in teclas_setas.items():
            if teclas[tecla]:
                receptor = self.receptores[direcao]
                for seta in self.setas:
                    if (seta.direcao == direcao and not seta.hit and seta.quem == "jogador"):
                        diferenca = abs(seta.y - receptor.y)

                        if (diferenca<= self.pontuacao.janela_ruim):
                            seta.hit = True

                            self.vida_professor -= 5
                            if self.vida_professor < 0:
                                self.vida_professor = 0
                            self.atualizar_barra_vida()

                            self.ultimo_julgamento = (self.pontuacao.calcular_pontos(diferenca))
                            self.tempo_julgamento =(pygame.time.get_ticks())

                            return
                        
#=======================PROCESSA EVENTOS=====================

    def processa_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False

            if self.estado == "intro":
                if (evento.type== pygame.KEYDOWN):
                    if evento.key == pygame.K_RETURN:
                        self.estado = "menu"

            elif self.estado == "menu":
                if (evento.type== pygame.MOUSEBUTTONDOWN):
                    botao = (self.tela_inicial.verificar_clique(evento.pos))

                    if botao == "comecar":
                        self.estado = "selecao"

                    elif botao == "score":
                        pass

                    elif botao == "creditos":
                        self.estado = "creditos"

                    elif botao == "sair":
                        self.rodando = False

            elif self.estado == "selecao":

                if evento.type == pygame.KEYDOWN:

                    if evento.key == pygame.K_UP:
                        if self.fase_selecionada > 0:
                            self.fase_selecionada -= 1

                    elif evento.key == pygame.K_DOWN:
                        if self.fase_selecionada < 2:
                            self.fase_selecionada += 1

                    elif evento.key == pygame.K_RETURN:

                        fase = self.fases[self.fase_selecionada]

                        if fase["desbloqueada"]:

                            self.vida_jogador = 100
                            self.vida_professor = 100
                            self.atualizar_barra_vida()

                            self.carregar_fase(fase["arquivo"])

                            pygame.mixer.music.stop()
                            pygame.mixer.music.load(fase["musica"])
                            pygame.mixer.music.play()

                            self.tempo_inicio = pygame.time.get_ticks()

                            self.estado = "jogo"

                    elif evento.key == pygame.K_ESCAPE:
                        self.estado = "menu"
        
            elif self.estado == "creditos":
                if (evento.type== pygame.KEYDOWN):
                    if evento.key == pygame.K_RETURN:
                        self.estado = "menu"

##=======================CARREGAR FASE=====================

    def carregar_fase(self, arquivo_txt):
        self.notas = []

        with open(arquivo_txt, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                partes = linha.strip().split()

                if len(partes) == 3:
                    tempo, direcao, quem = partes
                else:
                    tempo, direcao = partes
                    quem = "jogador"

                self.notas.append((int(tempo), direcao, quem))

        self.indice_nota = 0
        self.setas = []

#=======================ATUALIZAR=====================

    def atualizar(self):
        if self.estado != "jogo":
            return

        tempo = (pygame.time.get_ticks()- self.tempo_inicio)

        while (
            self.indice_nota < len(self.notas)
            and tempo >= self.notas[self.indice_nota][0]):
            _, direcao, quem= self.notas[self.indice_nota]

            receptor = self.receptores[direcao]

            self.setas.append(
                Seta(receptor.x,-100,direcao))

            self.indice_nota += 1

        for seta in self.setas:
            seta.mover()

            receptor = self.receptores[seta.direcao]

            if seta.quem == "professor":
                if not seta.hit and seta.y >= receptor.y:
                    seta.hit = True

                    self.vida_jogador -= 5
                    if self.vida_jogador < 0:
                        self.vida_jogador = 0
                    self.atualizar_barra_vida()
            else:

                if not seta.hit:
                    if seta.y > receptor.y + self.pontuacao.janela_ruim:
                        seta.hit = True

                        self.vida_jogador -= 10
                        if self.vida_jogador < 0:
                            self.vida_jogador = 0
                        self.atualizar_barra_vida()

                        self.ultimo_julgamento = "errou"
                        self.tempo_julgamento = pygame.time.get_ticks()

            seta.acertou()

        self.verificar_toque()
    

        if self.indice_nota >= len(self.notas):

            if self.fase_selecionada < len(self.fases)-1:
                self.fases[self.fase_selecionada+1]["desbloqueada"] = True

        if len(self.notas) > 0:

            if self.indice_nota >= len(self.notas):

                todas = True

                for seta in self.setas:
                    if not seta.hit:
                        todas = False

                if self.vida_jogador <= 0 or self.vida_professor <= 0:

                    self.estado = "selecao"

                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("Assets/Music/Menu.ogg")
                    pygame.mixer.music.play(-1)

#=======================DESENHAR=====================

    def desenhar(self):
        if self.estado == "intro":
            self.intro.desenhar(self.tela)
            pygame.display.update()

            return

        if self.estado == "menu":
            self.tela_inicial.desenhar(    self.tela)
            pygame.display.update()

            return
        
        if self.estado == "selecao":

            self.tela.fill((25,25,25))

            fonte = pygame.font.SysFont(None,60)

            titulo = fonte.render("ESCOLHA A FASE",True,(255,255,255))
            self.tela.blit(titulo,(350,70))

            y = 220

            for i,fase in enumerate(self.fases):

                texto = fase["nome"]

                if not fase["desbloqueada"]:
                    texto += " (Bloqueada)"

                if i == self.fase_selecionada:
                    texto = "> " + texto
                    cor = (0,255,0)
                else:
                    cor = (255,255,255)

                render = fonte.render(texto,True,cor)
                self.tela.blit(render, (350, y))
                y += 70

            pygame.display.update()
            return

        if self.estado == "creditos":
            self.tela_inicial.desenhar_creditos(self.tela)
            pygame.display.update()

            return

        self.tela.fill((0,0,0))

        x = (self.largura - self.barra_vida_atual.get_width()) // 2 - 40
        y = self.altura - self.barra_vida_atual.get_height() - 35

        self.tela.blit(self.barra_vida_atual, (x, y))

        self.seta_esquerda.desenhar(self.tela)
        self.seta_baixo.desenhar(self.tela)
        self.seta_cima.desenhar(self.tela)
        self.seta_direita.desenhar(self.tela)

        for seta in self.setas:
            seta.desenhar(self.tela)

        if (pygame.time.get_ticks()- self.tempo_julgamento< self.duracao_exibicao):
            self.pontuacao.desenhar(self.tela,self.ultimo_julgamento)

        pygame.display.update()

#=======================INICIAR=====================

    def iniciar(self):
        while self.rodando:
            self.processa_eventos()
            self.atualizar()
            self.desenhar()

            self.clock.tick(60)

#=======================ATUALIZAR BARRA VIDA=====================

    def atualizar_barra_vida(self):
        #Professor ganhando do jogador
        if self.vida_jogador < self.vida_professor:
            if self.vida_jogador <= 0:
                self.barra_vida_atual = self.barra_vidaj0
            elif self.vida_jogador <= 60:
                self.barra_vida_atual = self.barra_vida60
            else:
                self.barra_vida_atual = self.barra_vida100
        #Professor perdendo do jogador
        if self.vida_professor < self.vida_jogador:
                    if self.vida_professor <= 0:
                        self.barra_vida_atual = self.barra_vida0
                    elif self.vida_professor <= 60:
                        self.barra_vida_atual = self.barra_vidaj60
                    else:
                        self.barra_vida_atual = self.barra_vida100
                        
    #pygame.quit()