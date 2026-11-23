import os
import math
import pygame
from Class.seta import Seta
from Class.pontuacao import Pontuacao
from Class.tela_inicial import TelaInicial
from Class.intro import Intro
from Class.barra_vida import BarraVida
from Class.fase import Fase
from Class.sinc import Sinc
from Class.ranking import Ranking
from Class.tela_fim import TelaFim
from Class.tele_selecao import Telaselecao
from Class.final import Final


MUSICA_MENU = 'Assets/Music/MENU(Desmitificar- Marina sena).ogg'

# ======================= SPRITES DOS PERSONAGENS =======================

PASTA_SPRITES = 'Assets/Sprites'

PERSONAGEM_PROTAGONISTA = 'menino'

ESTADOS_PERSONAGEM = (
    'errando', 'cima', 'baixo',
    'direita', 'esquerda', 'parado'
)

TAM_FRENTE = (260, 360)
TAM_FUNDO = (240, 330)
MARGEM_LATERAL = 15
BASE_FRENTE = 635    # mantém os personagens acima da barra de vida
BASE_FUNDO = 620     # personagem de trás fica um pouco mais alto
RECUO_FUNDO = 45     # deslocamento lateral do personagem de trás
RECUO_FUNDO_FASE2 = 125

DURACAO_ESTADO_MS = 455
AVIAO_TAMANHO = (155, 140)
AVIAO_FRAME_MS = 200
AVIAO_Y_INICIO = 170
AVIAO_Y_FIM = -170
AVIAO_ARCO = 8
AVIAO_INCLINACAO_MAXIMA = 8
AVIAO_X_INICIO = -100
AVIAO_X_FIM = 420
# A ida chega à retomada rápida; a volta começa em seguida.
AVIAO_PASSAGENS_MS = (
    (70_230, 5_000, False),
    (75_230, 5_000, True),
)


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
        
        self.tela_selecao = Telaselecao(
        self.largura,
        self.altura,
        self.fases
    )

        self.tela = pygame.display.set_mode(
            (self.largura, self.altura)
        )

        pygame.display.set_caption("Error404")

        self.tela_inicial = TelaInicial(
            self.largura,
            self.altura
        )

        self.intro = Intro(
            self.largura,
            self.altura
        )

        self.clock = pygame.time.Clock()
        self.rodando = True

        # ======================= NOME / RANKING / TELAS FINAIS =======================

        self.nome_jogador = ""

        self.ranking = Ranking(
            self.largura,
            self.altura,
            [fase["nome"] for fase in self.fases]
        )

        self.tela_fim = TelaFim(
            self.largura,
            self.altura,
            PASTA_SPRITES,
            PERSONAGEM_PROTAGONISTA
        )

        self.final = Final(
            self.largura,
            self.altura
        )

        self.opcao_saida = 1
        self.tempo_pausa = 0
        self.admin_ativado = False

        self.carregar_fundo(0)
        self.carregar_sprites(0)

        # ======================= BARRA DE VIDA =======================

        largura_barra = 700
        altura_barra = 35

        x_barra = (
            self.largura - largura_barra
        ) // 2

        y_barra = (
            self.altura - altura_barra - 35
        )

        self.barra_vida = BarraVida(
            x_barra,
            y_barra,
            largura_barra,
            altura_barra
        )

        self.barra_vida.definir_personagens(
            PERSONAGEM_PROTAGONISTA,
            [professor["nome"] for professor in self.professores]
        )

        # ======================= SETAS =======================

        largura_seta = 150
        espaco_entre_setas = 125
        centro_x = self.largura // 2
        y_setas = y_barra - 160

        self.seta_esquerda = Seta(
            centro_x
            - int(espaco_entre_setas * 1.5)
            - largura_seta // 2,
            y_setas,
            "esquerda"
        )

        self.seta_baixo = Seta(
            centro_x
            - int(espaco_entre_setas * 0.5)
            - largura_seta // 2,
            y_setas,
            "baixo"
        )

        self.seta_cima = Seta(
            centro_x
            + int(espaco_entre_setas * 0.5)
            - largura_seta // 2,
            y_setas,
            "cima"
        )

        self.seta_direita = Seta(
            centro_x
            + int(espaco_entre_setas * 1.5)
            - largura_seta // 2,
            y_setas,
            "direita"
        )

        self.receptores = {
            "esquerda": self.seta_esquerda,
            "baixo": self.seta_baixo,
            "cima": self.seta_cima,
            "direita": self.seta_direita
        }

        self.setas = []

        # ======================= NOTAS =======================

        self.notas = []

        self.indice_nota = 0
        self.tempo_inicio = 0

        # ======================= PONTUAÇÃO =======================

        self.pontuacao = Pontuacao()

        self.sinc = Sinc(self)

        self.ultimo_julgamento = ""
        self.tempo_julgamento = 0
        self.duracao_exibicao = 500

        # ======================= CONTAGEM =======================

        self.contagem_textos = [
            "3",
            "2",
            "1",
            "VAI!"
        ]

        self.contagem_duracao_etapa = 700
        self.tempo_contagem_inicio = 0

        self.fase_pendente = None

        self.fonte_contagem = pygame.font.Font(
            'Assets/Fontes/PressStart2P-Regular.ttf',
            96
        )

        self.contagem_audio = pygame.mixer.Sound(
            'Assets/Music/321Go.ogg'
        )

    # =========================================================
    # PROCESSAR TOQUE
    # =========================================================

    def processar_toque(self, direcao):

        receptor = self.receptores[direcao]

        seta_alvo = None
        menor_diferenca = None

        for seta in self.setas:

            if (
                seta.direcao == direcao
                and not seta.hit
            ):

                diferenca = abs(
                    seta.y - receptor.y
                )

                if diferenca <= self.pontuacao.janela_ruim:

                    if (
                        menor_diferenca is None
                        or diferenca < menor_diferenca
                    ):
                        menor_diferenca = diferenca
                        seta_alvo = seta

        # ======================= ACERTO =======================

        if seta_alvo is not None:

            seta_alvo.hit = True

            self.definir_estado(self.protagonista, direcao)
            self.barra_vida.acerto()

            self.ultimo_julgamento = (
                self.pontuacao.calcular_pontos(
                    menor_diferenca
                )
            )

            self.tempo_julgamento = pygame.time.get_ticks()

        # ======================= ERRO =======================

        else:
            self.barra_vida.toque_errado()

            self.definir_estado(self.protagonista, "errando")

            self.ultimo_julgamento = "errou"

            self.tempo_julgamento = pygame.time.get_ticks()

    # =========================================================
    # PROCESSA EVENTOS
    # =========================================================

    def processa_eventos(self):

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                self.rodando = False

            # ======================= INTRO =======================
            if self.estado == "intro":

                nome = self.intro.processar_evento(evento)

                if nome is not None:

                    self.nome_jogador = nome
                    self.estado = "menu"

            # ======================= MENU =======================

            elif self.estado == "menu":

                if evento.type == pygame.KEYDOWN:

                    botao = self.tela_inicial.processar_evento(
                        evento
                    )

                    if botao == "comecar":
                        self.estado = "selecao"

                    elif botao == "score":
                        self.ranking.abrir()
                        self.estado = "score"

                    elif botao == "sair":
                        self.rodando = False

            # ======================= SCORE =======================

            elif self.estado == "score":

                if self.ranking.processar_evento(evento) == "voltar":
                    self.estado = "menu"

            # ======================= SELEÇÃO =======================

            elif self.estado == "selecao":

                if evento.type == pygame.KEYDOWN:

                    if evento.key == pygame.K_LEFT:

                        self.fase_selecionada = (
                            self.fase_selecionada - 1
                        ) % len(self.fases)

                    elif evento.key == pygame.K_RIGHT:

                        self.fase_selecionada = (
                            self.fase_selecionada + 1
                        ) % len(self.fases)

                    elif evento.key == pygame.K_RETURN:

                        fase = self.fases[self.fase_selecionada]

                        if fase["desbloqueada"]:

                            self.barra_vida.reset()
                            self.pontuacao.resetar()
                            self.ultimo_julgamento = ""

                            self.carregar_fase(fase["arquivo"])
                            self.carregar_fundo(self.fase_selecionada)
                            self.carregar_sprites(self.fase_selecionada)

                            pygame.mixer.music.stop()
                            self.contagem_audio.play()

                            self.fase_pendente = fase
                            self.tempo_contagem_inicio = pygame.time.get_ticks()

                            self.estado = "contagem"

                    elif evento.key == pygame.K_ESCAPE:

                        self.estado = "menu"
            # ======================= CONTAGEM =======================

            elif self.estado == "contagem":

                if evento.type == pygame.KEYDOWN:

                    if evento.key == pygame.K_ESCAPE:

                        self.contagem_audio.stop()

                        self.fase_pendente = None
                        self.estado = "selecao"

            # ======================= JOGO =======================

            elif self.estado == "jogo":

                if evento.type == pygame.KEYDOWN:

                    if evento.key == pygame.K_ESCAPE:

                        self._pedir_confirmacao_saida()

                    elif evento.key in teclas_setas:

                        self.processar_toque(
                            teclas_setas[evento.key]
                        )

            # ======================= CONFIRMAR SAÍDA =======================

            elif self.estado == "confirmar_saida":

                if evento.type == pygame.KEYDOWN:

                    if evento.key in (
                        pygame.K_LEFT,
                        pygame.K_RIGHT
                    ):

                        self.opcao_saida = 1 - self.opcao_saida

                    elif evento.key == pygame.K_RETURN:

                        if self.opcao_saida == 0:
                            self._voltar_para_selecao()
                        else:
                            self._retomar_fase()

                    elif evento.key == pygame.K_ESCAPE:

                        self._retomar_fase()

            # ======================= DERROTA / VITÓRIA =======================

            elif self.estado in ("derrota", "vitoria"):

                if evento.type == pygame.KEYDOWN:

                    if evento.key == pygame.K_RETURN:

                        # Venceu a última fase: diploma + créditos
                        if (
                            self.estado == "vitoria"
                            and self.fase_selecionada
                            == len(self.fases) - 1
                        ):
                            self.final.iniciar()
                            self.estado = "final"
                        else:
                            self._voltar_para_selecao()

            # ======================= FINAL (DIPLOMA / CRÉDITOS) =======================

            elif self.estado == "final":

                if self.final.processar_evento(evento) == "sair":
                    self._voltar_para_menu()

    # =========================================================
    # CARREGAR FASE
    # =========================================================

    def carregar_fase(self, arquivo_txt):

        self.notas = self.fase.carregar_fase(
            arquivo_txt
        )

        self.indice_nota = 0
        self.setas = []

    # =========================================================
    # CARREGAR FUNDO DA FASE
    # =========================================================

    def carregar_fundo(self, indice):

        nome = self.fase.fase_atual(indice)["nome"]
        nome = nome.lower().replace(" ", "_")

        caminho = f"Assets/Telas/fundo_{nome}.png"

        fundo = pygame.image.load(caminho).convert()

        self.fundo_jogo = pygame.transform.scale(
            fundo,
            (self.largura, self.altura)
        )

        self.python_monitor = None

        if indice == 1:
            imagem_python = pygame.image.load(
                "Assets/Telas/python.png"
            ).convert_alpha()
            self.python_monitor = pygame.transform.smoothscale(
                imagem_python,
                (22, 20)
            )
            self.python_monitor.set_alpha(140)

        self.aviao_frames = None
        self.aviao_frames_volta = None

        if indice == 2:
            frames = [
                pygame.transform.smoothscale(
                    pygame.image.load(
                        f"Assets/Telas/aviao_{numero}.png"
                    ).convert_alpha(),
                    AVIAO_TAMANHO
                )
                for numero in (1, 2, 3)
            ]
            self.aviao_frames = [
                frames[frame_indice]
                for frame_indice in (0, 1, 2, 1, 0)
            ]
            self.aviao_frames_volta = [
                pygame.transform.flip(frame, True, False)
                for frame in self.aviao_frames
            ]

    def _desenhar_python_monitor(self):
        if (
            self.python_monitor is not None
            and (pygame.time.get_ticks() // 600) % 2 == 0
        ):
            self.tela.blit(self.python_monitor, (784, 331))

    def _desenhar_aviao(self):
        if self.aviao_frames is None:
            return

        tempo = (
            self.tempo_pausa - self.tempo_inicio
            if self.estado == "confirmar_saida"
            else pygame.time.get_ticks() - self.tempo_inicio
        )

        for inicio, duracao, voltando in AVIAO_PASSAGENS_MS:
            tempo_passagem = tempo - inicio

            if 0 <= tempo_passagem < duracao:
                indice_frame = (
                    tempo_passagem // AVIAO_FRAME_MS
                ) % len(self.aviao_frames)
                progresso = tempo_passagem / duracao

                # Trilha suave: o avião sobe da esquerda para a direita,
                # acompanhando a direção inclinada mostrada no fundo.
                progresso_suave = (
                    progresso * progresso
                    * (3 - 2 * progresso)
                )
                if voltando:
                    x = int(
                        AVIAO_X_FIM
                        - (
                            AVIAO_X_FIM
                            - AVIAO_X_INICIO
                        ) * progresso_suave
                    )
                    y = int(
                        AVIAO_Y_FIM
                        + (
                            AVIAO_Y_INICIO
                            - AVIAO_Y_FIM
                        ) * progresso_suave
                        - math.sin(progresso * math.pi)
                        * AVIAO_ARCO
                    )
                    frames = self.aviao_frames_volta
                    inclinacao = -(
                        AVIAO_INCLINACAO_MAXIMA
                        + math.sin(progresso * math.pi)
                        * 2
                    )
                else:
                    x = int(
                        AVIAO_X_INICIO
                        + (
                            AVIAO_X_FIM
                            - AVIAO_X_INICIO
                        ) * progresso_suave
                    )
                    y = int(
                        AVIAO_Y_INICIO
                        + (
                            AVIAO_Y_FIM
                            - AVIAO_Y_INICIO
                        ) * progresso_suave
                        - math.sin(progresso * math.pi)
                        * AVIAO_ARCO
                    )
                    frames = self.aviao_frames
                    inclinacao = (
                        AVIAO_INCLINACAO_MAXIMA
                        + math.sin(progresso * math.pi)
                        * 2
                    )

                frame = pygame.transform.rotate(
                    frames[indice_frame],
                    inclinacao
                )
                self.tela.blit(
                    frame,
                    (
                        x - (frame.get_width() - AVIAO_TAMANHO[0]) // 2,
                        y - (frame.get_height() - AVIAO_TAMANHO[1]) // 2
                    )
                )
                return

    # =========================================================
    # CARREGAR SPRITES DOS PERSONAGENS
    # =========================================================

    def _carregar_sprite(self, personagem, estado, tamanho):
        caminho = f"{PASTA_SPRITES}/{personagem}_{estado}.png"

        # Se faltar o estado, usa o "parado"
        if not os.path.exists(caminho):
            print(f"[sprites] arquivo não encontrado: {caminho}")
            caminho = f"{PASTA_SPRITES}/{personagem}_parado.png"
        imagem = pygame.image.load(caminho).convert_alpha()

        return pygame.transform.smoothscale(imagem, tamanho)

    def _criar_personagem(self, nome, tamanho, x, base):

        return {
            "nome": nome,
            "estado": "parado",
            "estado_ate": 0,
            "pos": (x, base - tamanho[1]),
            "sprites": {
                estado: self._carregar_sprite(nome, estado, tamanho)
                for estado in ESTADOS_PERSONAGEM
            }
        }

    def carregar_sprites(self, indice):

        professores = self.fase.fase_atual(indice)["professores"]
        self.personagens = []

        # Protagonista (esquerda)
        self.protagonista = self._criar_personagem(
            PERSONAGEM_PROTAGONISTA,
            TAM_FRENTE,
            MARGEM_LATERAL,
            BASE_FRENTE
        )

        self.personagens.append(self.protagonista)

        # Professores (direita): o último da lista fica na frente
        x_frente = self.largura - MARGEM_LATERAL - TAM_FRENTE[0]
        recuo_fundo = RECUO_FUNDO_FASE2 if indice == 1 else RECUO_FUNDO

        self.professores = []

        for i, nome in enumerate(professores):

            recuo = len(professores) - 1 - i

            if recuo == 0:
                x_personagem = (
                    x_frente - recuo_fundo
                    if indice == 1
                    else x_frente
                )

                professor = self._criar_personagem(
                    nome,
                    TAM_FRENTE,
                    x_personagem,
                    BASE_FRENTE
                )

            else:
                x_personagem = (
                    x_frente
                    if indice == 1
                    else x_frente - RECUO_FUNDO * recuo
                )

                professor = self._criar_personagem(
                    nome,
                    TAM_FUNDO,
                    x_personagem,
                    BASE_FUNDO
                )

            self.professores.append(professor)
            self.personagens.append(professor)

        # atualiza as cabeças da barra de vida (ela só existe após o __init__)
        barra = getattr(self, "barra_vida", None)

        if barra is not None:
            barra.definir_personagens(
                PERSONAGEM_PROTAGONISTA,
                [professor["nome"] for professor in self.professores]
            )

    def definir_estado(self, personagem, estado, duracao=DURACAO_ESTADO_MS):
        personagem["estado"] = estado

        personagem["estado_ate"] = (
            pygame.time.get_ticks() + duracao
        )

    def atualizar_personagens(self):

        agora = pygame.time.get_ticks()

        for personagem in self.personagens:

            if (
                personagem["estado"] != "parado"
                and agora >= personagem["estado_ate"]
            ):
                personagem["estado"] = "parado"

    def desenhar_personagens(self):

        for personagem in self.personagens:

            sprite = personagem["sprites"][personagem["estado"]]

            self.tela.blit(
                sprite,
                personagem["pos"]
            )

    # =========================================================
    # ATUALIZAR
    # =========================================================

    def atualizar(self):
        self.atualizar_personagens()

        # ======================= PASSE DE ADMIN =======================

        teclas = pygame.key.get_pressed()

        if (
            self.estado == "selecao"
            and teclas[pygame.K_a]
            and teclas[pygame.K_b]
        ):
            if not self.admin_ativado:
                for fase in self.fases:
                    fase["desbloqueada"] = True

                self.admin_ativado = True

        else:
            self.admin_ativado = False

        if self.estado == "final":

            self.final.atualizar()
            return

        if self.estado == "contagem":

            self._atualizar_contagem()
            return

        if self.estado != "jogo":
            return

        # ======================= PASSE DE ADMIN (VITÓRIA) =======================

        if teclas[pygame.K_a] and teclas[pygame.K_b]:

            self._finalizar_fase(
                venceu=True,
                salvar_ranking=False
            )

            return

        tempo = (
            pygame.time.get_ticks()
            - self.tempo_inicio
        )

        # ======================= CRIAR SETAS =======================

        while (
            self.indice_nota < len(self.notas)
            and tempo >= self.notas[self.indice_nota][0]
        ):

            _, direcao = self.notas[
                self.indice_nota
            ]

            receptor = self.receptores[direcao]

            self.setas.append(
                Seta(
                    receptor.x,
                    -100,
                    direcao
                )
            )

            self.indice_nota += 1

        # ======================= ATUALIZAR SETAS =======================

        for seta in self.setas:

            seta.mover()

            receptor = self.receptores[
                seta.direcao
            ]

            # ================= PROFESSORES =================

            if (
                not getattr(seta, "professor_reagiu", False)
                and seta.y >= receptor.y
            ):

                seta.professor_reagiu = True

                for professor in self.professores:

                    self.definir_estado(
                        professor,
                        seta.direcao
                    )

            # ================= SETA PERDIDA =================

            if not seta.hit:

                if (
                    seta.y
                    > receptor.y
                    + self.pontuacao.janela_ruim
                ):

                    seta.hit = True
                    self.barra_vida.seta_perdida()

                    self.definir_estado(self.protagonista, "errando")

                    self.ultimo_julgamento = "errou"

                    self.tempo_julgamento = (
                        pygame.time.get_ticks()
                    )

            seta.acertou()

        # ======================= SINCRONIZAÇÃO =======================

        self.sinc.verificar_sinc(
            self.setas
        )
        self.barra_vida.atualizar()

        # ======================= DERROTA =======================

        if self.barra_vida.vida_jogador <= 0:

            self._finalizar_fase(
                venceu=False
            )

        # ======================= VITÓRIA =======================
        elif self.fase.fase_terminou(
            self.fase_selecionada,
            self.indice_nota >= len(self.notas) and not self.setas
        ):

            self._finalizar_fase(
                venceu=True
            )

    # =========================================================
    # ATUALIZAR CONTAGEM
    # =========================================================

    def _atualizar_contagem(self):

        tempo_decorrido = (
            pygame.time.get_ticks()
            - self.tempo_contagem_inicio
        )

        duracao_total = (
            len(self.contagem_textos)
            * self.contagem_duracao_etapa
        )

        if tempo_decorrido >= duracao_total:

            self.contagem_audio.stop()

            self.fase.iniciar_musica(
                self.fase_selecionada
            )

            self.tempo_inicio = (
                pygame.time.get_ticks()
            )

            self.fase_pendente = None

            self.estado = "jogo"

    # =========================================================
    # CONFIRMAÇÃO DE SAÍDA (PAUSA)
    # =========================================================

    def _pedir_confirmacao_saida(self):

        self.tempo_pausa = pygame.time.get_ticks()

        pygame.mixer.music.pause()

        # Começa em "Não" para ninguém sair sem querer
        self.opcao_saida = 1

        self.estado = "confirmar_saida"

    def _retomar_fase(self):

        pausado = (
            pygame.time.get_ticks()
            - self.tempo_pausa
        )

        self.tempo_inicio += pausado
        self.tempo_julgamento += pausado

        for personagem in self.personagens:
            personagem["estado_ate"] += pausado

        pygame.mixer.music.unpause()

        self.estado = "jogo"

    # =========================================================
    # FINALIZAR FASE (DERROTA / VITÓRIA)
    # =========================================================

    def _finalizar_fase(self, venceu, salvar_ranking=True):

        pygame.mixer.music.stop()

        nome_fase = self.fases[
            self.fase_selecionada
        ]["nome"]

        if venceu:

            self.fase.desbloquear_proxima(
                self.fase_selecionada
            )

            pontos = self.pontuacao.pontos

            classificacao = TelaFim.calcular_classificacao(
                pontos,
                len(self.notas),
                self.pontuacao.pontos_perfeitos
            )

            if salvar_ranking:
                self.ranking.salvar(
                    self.nome_jogador,
                    nome_fase,
                    pontos,
                    classificacao
                )

            self.tela_fim.mostrar_vitoria(
                nome_fase,
                pontos,
                classificacao
            )

            self.estado = "vitoria"

        else:

            self.tela_fim.mostrar_derrota(
                nome_fase
            )

            self.estado = "derrota"

    # =========================================================
    # VOLTAR PARA A SELEÇÃO DE FASE
    # =========================================================

    def _voltar_para_selecao(self):

        self.estado = "selecao"

        pygame.mixer.music.stop()

        pygame.mixer.music.load(
            MUSICA_MENU
        )

        pygame.mixer.music.play(-1)

    # =========================================================
    # VOLTAR PARA O MENU (DEPOIS DOS CRÉDITOS)
    # =========================================================

    def _voltar_para_menu(self):

        self.estado = "menu"

        pygame.mixer.music.stop()

        pygame.mixer.music.load(
            MUSICA_MENU
        )

        pygame.mixer.music.play(-1)

    # =========================================================
    # DESENHAR
    # =========================================================

    def _desenhar_cena_jogo(self):

        self.tela.blit(
            self.fundo_jogo,
            (0, 0)
        )

        self._desenhar_python_monitor()
        self._desenhar_aviao()
        self.desenhar_personagens()

        self.barra_vida.desenhar(
            self.tela
        )

        self.seta_esquerda.desenhar(
            self.tela
        )

        self.seta_baixo.desenhar(
            self.tela
        )

        self.seta_cima.desenhar(
            self.tela
        )

        self.seta_direita.desenhar(
            self.tela
        )

        for seta in self.setas:

            seta.desenhar(
                self.tela
            )

        if (
            pygame.time.get_ticks()
            - self.tempo_julgamento
            < self.duracao_exibicao
        ):

            self.pontuacao.desenhar(
                self.tela,
                self.ultimo_julgamento
            )

    def desenhar(self):

        # ======================= INTRO =======================

        if self.estado == "intro":

            self.intro.desenhar(
                self.tela
            )

            pygame.display.update()

            return

        # ======================= MENU =======================

        if self.estado == "menu":

            self.tela_inicial.desenhar(
                self.tela
            )

            pygame.display.update()

            return

        # ======================= SCORE =======================

        if self.estado == "score":

            self.ranking.desenhar(
                self.tela,
                self.nome_jogador
            )

            pygame.display.update()

            return

        # ======================= SELEÇÃO =======================

        if self.estado == "selecao":

            self.tela_selecao.desenhar(
                self.tela,
                self.fase_selecionada
            )

            pygame.display.update()

            return

        # ======================= FINAL =======================

        if self.estado == "final":

            self.final.desenhar(
                self.tela
            )

            pygame.display.update()

            return

        # ======================= CONTAGEM =======================

        if self.estado == "contagem":

            self.tela.blit(
                self.fundo_jogo,
                (0, 0)
            )

            self._desenhar_python_monitor()
            self.desenhar_personagens()

            tempo_decorrido = (
                pygame.time.get_ticks()
                - self.tempo_contagem_inicio
            )

            indice = min(
                tempo_decorrido
                // self.contagem_duracao_etapa,
                len(self.contagem_textos) - 1
            )

            texto_contagem = (
                self.contagem_textos[indice]
            )

            render = self.fonte_contagem.render(
                texto_contagem,
                True,
                (255, 255, 255)
            )

            rect = render.get_rect(
                center=(
                    self.largura // 2,
                    self.altura // 2
                )
            )

            self.tela.blit(
                render,
                rect
            )

            pygame.display.update()

            return

        # ======================= DERROTA / VITÓRIA =======================

        if self.estado in ("derrota", "vitoria"):

            self.tela_fim.desenhar(
                self.tela,
                self.fundo_jogo
            )

            pygame.display.update()

            return

        # ======================= CONFIRMAR SAÍDA =======================

        if self.estado == "confirmar_saida":

            self._desenhar_cena_jogo()

            self.tela_fim.desenhar_confirmacao(
                self.tela,
                self.opcao_saida
            )

            pygame.display.update()

            return

        # ======================= JOGO =======================

        self._desenhar_cena_jogo()

        pygame.display.update()

    # =========================================================
    # INICIAR
    # =========================================================

    def iniciar(self):

        while self.rodando:

            self.processa_eventos()
            self.atualizar()
            self.desenhar()

            self.clock.tick(60)

        pygame.quit()