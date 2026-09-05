import pygame
from Class.seta import Seta
from Class.pontuacao import Pontuacao
from Class.tela_inicial import TelaInicial
from Class.intro import Intro
from Class.barra_vida import BarraVida

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

        self.turno_atual = None
        self.tempo_aviso = 0
        self.duracao_aviso = 1200
        self.fonte_aviso = pygame.font.SysFont(None, 80)

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
                "musica": "Assets/Music/ROMERITO(Nuevayol- bad bunny).ogg",
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

        self.fundo_jogo = pygame.image.load("Assets/Telas/fundo_joaildo.png").convert()
        self.fundo_jogo = pygame.transform.scale(self.fundo_jogo, (self.largura, self.altura))

        largura_barra = 750
        altura_barra = 45
        x_barra = (self.largura - largura_barra) // 2
        y_barra = self.altura - altura_barra - 35

        self.barra_vida = BarraVida(x_barra, y_barra, largura_barra, altura_barra)


        largura_seta = 150  
        espaco_entre_setas = 160
        centro_x = self.largura // 2
        y_setas = y_barra - 160

        self.seta_esquerda = Seta(centro_x - int(espaco_entre_setas * 1.5) - largura_seta // 2, y_setas, "esquerda")
        self.seta_baixo = Seta(centro_x - int(espaco_entre_setas * 0.5) - largura_seta // 2, y_setas, "baixo")
        self.seta_cima = Seta(centro_x + int(espaco_entre_setas * 0.5) - largura_seta // 2, y_setas, "cima")
        self.seta_direita = Seta(centro_x + int(espaco_entre_setas * 1.5) - largura_seta // 2, y_setas, "direita")

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

                            self.barra_vida.dano_professor(5)

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

                            self.barra_vida.reset()

                            self.carregar_fase(fase["arquivo"])

                            pygame.mixer.music.stop()
                            pygame.mixer.music.load(fase["musica"])
                            pygame.mixer.music.play()

                            self.tempo_inicio = pygame.time.get_ticks()

                            self.turno_atual = None
                            self.tempo_aviso = 0

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

            if quem != self.turno_atual:
                self.turno_atual = quem
                self.tempo_aviso = pygame.time.get_ticks()

            receptor = self.receptores[direcao]

            self.setas.append(
                Seta(receptor.x,-100,direcao, quem))

            self.indice_nota += 1

        for seta in self.setas:
            seta.mover()

            receptor = self.receptores[seta.direcao]

            if seta.quem == "professor":
                if not seta.hit and seta.y >= receptor.y:
                    seta.hit = True

                    self.barra_vida.dano_jogador(5)
            else:

                if not seta.hit:
                    if seta.y > receptor.y + self.pontuacao.janela_ruim:
                        seta.hit = True

                        self.barra_vida.dano_jogador(10)

                        self.ultimo_julgamento = "errou"
                        self.tempo_julgamento = pygame.time.get_ticks()

            seta.acertou()

        self.barra_vida.atualizar()

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

                if self.barra_vida.jogador_perdeu() or self.barra_vida.professor_perdeu():

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

        self.tela.blit(self.fundo_jogo, (0, 0))

        self.barra_vida.desenhar(self.tela)

        self.seta_esquerda.desenhar(self.tela)
        self.seta_baixo.desenhar(self.tela)
        self.seta_cima.desenhar(self.tela)
        self.seta_direita.desenhar(self.tela)

        for seta in self.setas:
            seta.desenhar(self.tela)

        if (pygame.time.get_ticks()- self.tempo_julgamento< self.duracao_exibicao):
            self.pontuacao.desenhar(self.tela,self.ultimo_julgamento)

        if (pygame.time.get_ticks() - self.tempo_aviso) < self.duracao_aviso:
            if self.turno_atual == "professor":
                texto_aviso = "VEZ DO PROFESSOR"
                cor_aviso = (255, 100, 100)
            else:
                texto_aviso = "SUA VEZ!"
                cor_aviso = (100, 255, 100)

            render_aviso = self.fonte_aviso.render(texto_aviso, True, cor_aviso)
            rect_aviso = render_aviso.get_rect(center=(self.largura // 2, 150))
            self.tela.blit(render_aviso, rect_aviso)

        pygame.display.update()

#=======================INICIAR=====================

    def iniciar(self):
        while self.rodando:
            self.processa_eventos()
            self.atualizar()
            self.desenhar()

            self.clock.tick(60)

    #pygame.quit()