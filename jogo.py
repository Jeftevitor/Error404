import pygame
from Class.seta import Seta
from Class.pontuacao import Pontuacao
from Class.tela_inicial import TelaInicial
from Class.intro import Intro
from Class.barra_vida import BarraVida
from Class.fase import Fase
from Class.sinc import Sinc

MUSICA_MENU = 'Assets/Music/MENU(Desmitificar- Marina sena).ogg'

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
        pygame.mixer.music.load(MUSICA_MENU)
        pygame.mixer.music.play(-1)

        self.largura = 1200
        self.altura = 720

        self.estado = "intro"

        self.fase_selecionada = 0

        self.fase = Fase()
        self.fases = self.fase.fases

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

        self.sinc = Sinc(self)

        self.ultimo_julgamento = ""
        self.tempo_julgamento = 0
        self.duracao_exibicao = 500

#=======================CONTAGEM=====================
        self.contagem_textos = ["3", "2", "1", "VAI!"]
        self.contagem_duracao_etapa = 700
        self.tempo_contagem_inicio = 0
        self.fase_pendente = None
        self.fonte_contagem = pygame.font.Font(None, 150)
        self.contagem_audio = pygame.mixer.Sound('Assets/Music/321Go.ogg')

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
                        if self.fase_selecionada < len(self.fases) - 1:
                            self.fase_selecionada += 1

                    elif evento.key == pygame.K_RETURN:

                        fase = self.fases[self.fase_selecionada]

                        if fase["desbloqueada"]:

                            self.barra_vida.reset()

                            self.carregar_fase(fase["arquivo"])

                            pygame.mixer.music.stop()
                            self.contagem_audio.play()

                            self.fase_pendente = fase
                            self.tempo_contagem_inicio = pygame.time.get_ticks()

                            self.estado = "contagem"

                    elif evento.key == pygame.K_ESCAPE:
                        self.estado = "menu"
        
            elif self.estado == "creditos":
                if (evento.type== pygame.KEYDOWN):
                    if evento.key == pygame.K_RETURN:
                        self.estado = "menu"

            elif self.estado == "contagem":
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        self.fase_pendente = None
                        self.estado = "selecao"

            elif self.estado == "jogo":
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        self._encerrar_fase(venceu=False)

##=======================CARREGAR FASE=====================

    def carregar_fase(self, arquivo_txt):
        self.notas = self.fase.carregar_fase(arquivo_txt)
        self.indice_nota = 0
        self.setas = []

#=======================ATUALIZAR=====================

    def atualizar(self):
        if self.estado == "contagem":
            self._atualizar_contagem()
            return

        if self.estado != "jogo":
            return

        tempo = pygame.time.get_ticks() - self.tempo_inicio

        while self.indice_nota < len(self.notas) and tempo >= self.notas[self.indice_nota][0]:
            _, direcao = self.notas[self.indice_nota]
            receptor = self.receptores[direcao]

            self.setas.append(
                Seta(receptor.x, -100, direcao)
            )

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

        self.sinc.verificar_sinc(self.setas)

        self.barra_vida.atualizar()

        self.verificar_toque()

        acabou_a_musica = self.indice_nota >= len(self.notas)
        todas_setas_resolvidas = all(seta.hit for seta in self.setas)

        if self.barra_vida.jogador_perdeu() or self.barra_vida.professor_perdeu():
            self._encerrar_fase(venceu=False)

        elif acabou_a_musica and todas_setas_resolvidas:
            self._encerrar_fase(venceu=True)

    #=======================ATUALIZAR CONTAGEM=====================
    def _atualizar_contagem(self):
        tempo_decorrido = pygame.time.get_ticks() - self.tempo_contagem_inicio
        duracao_total = len(self.contagem_textos) * self.contagem_duracao_etapa

        if tempo_decorrido >= duracao_total:
            self.contagem_audio.stop()
            pygame.mixer.music.load(self.fase_pendente["musica"])
            pygame.mixer.music.play()

            self.tempo_inicio = pygame.time.get_ticks()
            self.fase_pendente = None

            self.estado = "jogo"

    #=======================ENCERRAR FASE=====================
    def _encerrar_fase(self, venceu):
        if venceu:
            self.fase.desbloquear_proxima(self.fase_selecionada)

        self.estado = "selecao"

        pygame.mixer.music.stop()
        pygame.mixer.music.load(MUSICA_MENU)
        pygame.mixer.music.play(-1)

#=======================DESENHAR=====================

    def desenhar(self):
        if self.estado == "intro":
            self.intro.desenhar(self.tela)
            pygame.display.update()

            return

        if self.estado == "menu":
            self.tela_inicial.desenhar(self.tela)
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

        if self.estado == "contagem":
            self.tela.blit(self.fundo_jogo, (0, 0))

            tempo_decorrido = pygame.time.get_ticks() - self.tempo_contagem_inicio
            indice = min(
                tempo_decorrido // self.contagem_duracao_etapa,
                len(self.contagem_textos) - 1
            )

            texto_contagem = self.contagem_textos[indice]

            render = self.fonte_contagem.render(texto_contagem, True, (255, 255, 255))
            rect = render.get_rect(center=(self.largura // 2, self.altura // 2))

            self.tela.blit(render, rect)

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

        pygame.display.update()

#=======================INICIAR=====================

    def iniciar(self):
        while self.rodando:
            self.processa_eventos()
            self.atualizar()
            self.desenhar()

            self.clock.tick(60)

    #pygame.quit()