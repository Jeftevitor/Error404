import os
import random
import pygame
from Class.seta import Seta


CAMINHO_FONTE = 'Assets/Fontes/PressStart2P-Regular.ttf'
IMAGEM_DIPLOMA = 'Assets/Telas/diploma.png'
MUSICA_DIPLOMA = 'Assets/Music/diploma.ogg'      # toca uma vez só
MUSICA_CREDITOS = 'Assets/Music/creditos.ogg'    # toca em loop

TEXTO_DIPLOMA = "Parabéns! Você conquistou o seu diploma!"
TEXTO_OBRIGADO = "Obrigado por jogar<3"

# (texto, tipo)  tipo: "titulo" | "rotulo" | "texto" | "espaco"
CREDITOS = [
    ("CRÉDITOS", "titulo"),
    ("", "espaco"),
    ("Música", "rotulo"),
    ("Jefte", "texto"),
    ("", "espaco"),
    ("Programadores", "rotulo"),
    ("Jefte e Isabela", "texto"),
    ("", "espaco"),
    ("Artes", "rotulo"),
    ("ChatGPT", "texto"),
    ("", "espaco"),
    ("Professor", "rotulo"),
    ("Max", "texto"),
    ("", "espaco"),
    ("Matéria", "rotulo"),
    ("Programação Orientada a Objetos", "texto"),
    ("", "espaco"),
    ("Ferramentas", "rotulo"),
    ("Feito com Python e Pygame", "texto"),
    ("", "espaco"),
    ("Músicas Utilizadas", "rotulo"),
    ("", "espaco"),
    ("Joaildo", "rotulo"),
    ("Freak (Ariana Grande)", "texto"),
    ("", "espaco"),
    ("Max e Hugo", "rotulo"),
    ("Passeios Noturnos (Jão)", "texto"),
    ("", "espaco"),
    ("Romerito", "rotulo"),
    ("Nuevayol (Bad Bunny)", "texto"),
    ("", "espaco"),
    ("Menu", "rotulo"),
    ("Desmitificar (Marina Sena)", "texto"),
    ("", "espaco"),
    ("Tela de Créditos", "rotulo"),
    ("Tema de Abertura (Zelda Ocarina of Time)", "texto"),
    ("", "espaco"),
    ("", "espaco"),
    ("", "espaco"),
    ("Nenhum professor foi machucado na criação deste jogo!", "rotulo"),
]

COR_FUNDO = (15, 12, 30)
COR_TITULO = (255, 220, 80)
COR_ROTULO = (255, 170, 60)
COR_TEXTO = (255, 255, 255)

DURACAO_DIPLOMA_MS = 8000     # tempo até os créditos começarem sozinhos
VELOCIDADE_CREDITOS = 70      # pixels por segundo
FADE_MS = 800

SPRITE_BOBINHA = 'Assets/Barra/cabeça_joaildo_s.png'   # tenta também com .png
TEXTO_BOBINHA = '"Bobinha!"'
ATRASO_BOBINHA_MS = 15000      # tempo parado na tela até começar a aparecer
FADE_BOBINHA_MS = 3000         # tempo que leva para aparecer por completo
ALTURA_BOBINHA = 90            # altura do sprite (px)
AUDIO_BOBINHA = 'Assets/Music/joaildo.ogg'   # toca uma vez quando a bobinha aparece

ESCALA_DIPLOMA = 0.95         # % da janela ocupado pelo diploma (largura e altura)

QTD_SETAS_FUNDO = 14
FAIXA_LATERAL = 0.17                   # fração da largura de cada lado onde as setas caem (o meio fica livre)
ALPHA_SETAS_FUNDO = 70                 # 0-255: quanto menor, mais discretas
VEL_SETAS_FUNDO = (60, 140)            # pixels por segundo (min, max)
TAM_SETAS_FUNDO = (22, 44)             # tamanho (min, max)

COR_SETAS = {
    "esquerda": (190, 80, 255),
    "baixo": (60, 210, 255),
    "cima": (80, 255, 120),
    "direita": (255, 80, 80),
}

FORMA_SETA = [
    (0, -1), (0.9, 0), (0.4, 0), (0.4, 1),
    (-0.4, 1), (-0.4, 0), (-0.9, 0)
]

ROTACAO_SETA = {
    "cima": lambda x, y: (x, y),
    "baixo": lambda x, y: (-x, -y),
    "direita": lambda x, y: (-y, x),
    "esquerda": lambda x, y: (y, -x),
}


class Final:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura

        self._fontes = {}

        self.etapa = "diploma"
        self.tempo_etapa = 0
        self.pos_y = 0.0
        self.ultimo_tick = 0

        self.imagem_diploma = self._carregar_imagem_diploma()
        self.surfaces_creditos = []
        self.altura_creditos = 0

        self.tem_musica = os.path.exists(MUSICA_DIPLOMA)

        self.setas_fundo = []
        self.tick_fundo = 0
        self.camada_setas = pygame.Surface(
            (self.largura, self.altura), pygame.SRCALPHA
        )

        # sprites reais das setas (pegos da classe Seta) e cache de tamanhos
        self.sprites_base = None
        self.sprite_bobinha = None
        self._bobinha_carregado = False
        self._audio_bobinha_tocado = False
        self.cache_sprites = {}

    def _fonte(self, tamanho):
        if tamanho not in self._fontes:
            self._fontes[tamanho] = pygame.font.Font(
                CAMINHO_FONTE, tamanho
            )
        return self._fontes[tamanho]

    def _render_ajustado(self, texto, tamanho, cor, largura_max):
        while tamanho > 8:
            render = self._fonte(tamanho).render(texto, True, cor)

            if render.get_width() <= largura_max:
                return render

            tamanho -= 2

        return self._fonte(8).render(texto, True, cor)

    def _carregar_imagem_diploma(self):
        largura_max = int(self.largura * ESCALA_DIPLOMA)
        altura_max = int(self.altura * ESCALA_DIPLOMA)

        if os.path.exists(IMAGEM_DIPLOMA):
            imagem = pygame.image.load(IMAGEM_DIPLOMA).convert()

            return pygame.transform.smoothscale(
                imagem,
                (largura_max, altura_max)
            )

        print(f"[final] imagem não encontrada: {IMAGEM_DIPLOMA} ""(usando diploma desenhado)")
        return self._desenhar_diploma_padrao(largura_max, altura_max)

    def _desenhar_diploma_padrao(self, largura, altura):
        surf = pygame.Surface((largura, altura), pygame.SRCALPHA)

        surf.fill((245, 230, 190))
        pygame.draw.rect(surf, (140, 90, 30), surf.get_rect(), 10)
        pygame.draw.rect(
            surf, (200, 150, 60),
            surf.get_rect().inflate(-40, -40), 4
        )

        titulo = self._render_ajustado(
            "DIPLOMA", 56, (90, 50, 20), largura - 120
        )
        surf.blit(titulo, titulo.get_rect(center=(largura // 2, altura // 3)))

        sub = self._render_ajustado(
            "Error404", 28, (140, 90, 30), largura - 120
        )
        surf.blit(sub, sub.get_rect(center=(largura // 2, altura // 2 + 10)))

        # selo
        centro = (largura // 2, int(altura * 0.75))
        pygame.draw.circle(surf, (190, 30, 40), centro, 40)
        pygame.draw.circle(surf, (120, 15, 25), centro, 40, 5)

        return surf

    def _montar_creditos(self):
        self.surfaces_creditos = []
        largura_max = self.largura - 80

        for texto, tipo in CREDITOS:
            if tipo == "espaco":
                self.surfaces_creditos.append(
                    pygame.Surface((1, 30), pygame.SRCALPHA)
                )
                continue

            if tipo == "titulo":
                render = self._render_ajustado(
                    texto, 44, COR_TITULO, largura_max
                )
            elif tipo == "rotulo":
                render = self._render_ajustado(
                    texto, 22, COR_ROTULO, largura_max
                )
            else:
                render = self._render_ajustado(
                    texto, 20, COR_TEXTO, largura_max
                )

            self.surfaces_creditos.append(render)

        self.altura_creditos = sum(
            s.get_height() + 14 for s in self.surfaces_creditos
        )


    def _carregar_sprites_setas(self):
        self.sprites_base = {}
        self.cache_sprites = {}

        for direcao in COR_SETAS:
            try:
                temp = pygame.Surface((600, 600), pygame.SRCALPHA)

                Seta(0, 0, direcao).desenhar(temp)

                recorte = temp.get_bounding_rect()

                if recorte.width == 0 or recorte.height == 0:
                    raise ValueError("seta desenhou vazio")

                self.sprites_base[direcao] = temp.subsurface(
                    recorte
                ).copy()

            except Exception as erro:
                print(f"[final] sprite da seta '{direcao}' " 
                    f"indisponível ({erro}); usando desenho simples")
                self.sprites_base[direcao] = None

    def _sprite_seta(self, direcao, tam):
        chave = (direcao, tam)

        if chave not in self.cache_sprites:
            base = self.sprites_base.get(direcao)

            if base is None:
                self.cache_sprites[chave] = None
            else:
                altura = tam * 2
                largura = max(
                    1, int(base.get_width() * altura / base.get_height())
                )

                sprite = pygame.transform.smoothscale(
                    base, (largura, altura)
                )
                sprite.set_alpha(ALPHA_SETAS_FUNDO)

                self.cache_sprites[chave] = sprite

        return self.cache_sprites[chave]

    def _nova_seta_fundo(self, y):
        borda = int(self.largura * FAIXA_LATERAL)

        if random.random() < 0.5:
            x = random.randint(30, borda)
        else:
            x = random.randint(self.largura - borda, self.largura - 30)

        return {
            "x": x,
            "y": y,
            "dir": random.choice(list(COR_SETAS)),
            "vel": random.uniform(*VEL_SETAS_FUNDO),
            "tam": random.randint(*TAM_SETAS_FUNDO),
        }

    def _criar_fundo_setas(self):
        if self.sprites_base is None:
            self._carregar_sprites_setas()

        self.setas_fundo = [
            self._nova_seta_fundo(random.uniform(0, self.altura))
            for _ in range(QTD_SETAS_FUNDO)
        ]
        self.tick_fundo = pygame.time.get_ticks()

    def _atualizar_fundo_setas(self):
        agora = pygame.time.get_ticks()
        dt = (agora - self.tick_fundo) / 1000
        self.tick_fundo = agora

        for i, seta in enumerate(self.setas_fundo):
            seta["y"] += seta["vel"] * dt

            if seta["y"] - seta["tam"] > self.altura:
                self.setas_fundo[i] = self._nova_seta_fundo(
                    -seta["tam"]
                )

    def _desenhar_fundo_setas(self, tela):
        self.camada_setas.fill((0, 0, 0, 0))

        for seta in self.setas_fundo:
            sprite = self._sprite_seta(seta["dir"], seta["tam"])

            if sprite is not None:
                tela.blit(
                    sprite,
                    sprite.get_rect(center=(seta["x"], int(seta["y"])))
                )
                continue

            girar = ROTACAO_SETA[seta["dir"]]
            r, g, b = COR_SETAS[seta["dir"]]
            t = seta["tam"]

            pontos = []
            for px, py in FORMA_SETA:
                gx, gy = girar(px, py)
                pontos.append((seta["x"] + gx * t, seta["y"] + gy * t))

            pygame.draw.polygon(
                self.camada_setas,
                (r, g, b, ALPHA_SETAS_FUNDO),
                pontos
            )

        tela.blit(self.camada_setas, (0, 0))

    def iniciar(self):
        self.etapa = "diploma"
        self.tempo_etapa = pygame.time.get_ticks()
        self.ultimo_tick = self.tempo_etapa

        pygame.mixer.music.stop()

        if self.tem_musica:
            pygame.mixer.music.load(MUSICA_DIPLOMA)
            pygame.mixer.music.play(0)   # sem loop
        else:
            print(f"[final] música não encontrada: {MUSICA_DIPLOMA}")

    def _iniciar_creditos(self):
        self._montar_creditos()
        if os.path.exists(MUSICA_CREDITOS):
            pygame.mixer.music.stop()
            pygame.mixer.music.load(MUSICA_CREDITOS)
            pygame.mixer.music.play(-1)
        else:
            print(f"[final] música não encontrada: {MUSICA_CREDITOS}")

        self._criar_fundo_setas()

        self.etapa = "creditos"
        self.tempo_etapa = pygame.time.get_ticks()
        self.ultimo_tick = self.tempo_etapa
        self.pos_y = float(self.altura)

    def _iniciar_obrigado(self):
        self._audio_bobinha_tocado = False
        self.etapa = "obrigado"
        self.tempo_etapa = pygame.time.get_ticks()

    def processar_evento(self, evento):
        if evento.type != pygame.KEYDOWN:
            return None

        if evento.key == pygame.K_ESCAPE:
            return "sair"

        if evento.key == pygame.K_RETURN:

            if self.etapa == "diploma":
                self._iniciar_creditos()

            elif self.etapa == "obrigado":
                return "sair"

        return None

    def atualizar(self):
        agora = pygame.time.get_ticks()

        if self.etapa == "diploma":

            if agora - self.tempo_etapa >= DURACAO_DIPLOMA_MS:
                self._iniciar_creditos()

        if self.etapa in ("creditos", "obrigado"):
            self._atualizar_fundo_setas()

        if self.etapa == "creditos":

            dt = (agora - self.ultimo_tick) / 1000
            self.ultimo_tick = agora

            self.pos_y -= VELOCIDADE_CREDITOS * dt

            if self.pos_y + self.altura_creditos < 0:
                self._iniciar_obrigado()

    def _alpha(self):
        decorrido = pygame.time.get_ticks() - self.tempo_etapa
        return max(0, min(255, int(255 * decorrido / FADE_MS)))

    def _desenhar_diploma(self, tela):
        rect_img = self.imagem_diploma.get_rect(
            center=(self.largura // 2, self.altura // 2)
        )

        tela.blit(self.imagem_diploma, rect_img)

        altura_faixa = 130
        faixa = pygame.Surface(
            (rect_img.width, altura_faixa), pygame.SRCALPHA
        )
        faixa.fill((0, 0, 0, 170))
        tela.blit(faixa, (rect_img.left, rect_img.bottom - altura_faixa))

        texto = self._render_ajustado(
            TEXTO_DIPLOMA, 24, COR_TEXTO, rect_img.width - 60
        )
        tela.blit(
            texto,
            texto.get_rect(
                center=(self.largura // 2, rect_img.bottom - 80)
            )
        )

        if (pygame.time.get_ticks() // 500) % 2 == 0:
            dica = self._fonte(14).render(
                "ENTER para continuar", True, (160, 160, 180)
            )
            tela.blit(
                dica,
                dica.get_rect(
                    center=(self.largura // 2, rect_img.bottom - 35)
                )
            )

    def _desenhar_creditos(self, tela):
        y = self.pos_y

        for surf in self.surfaces_creditos:
            if y + surf.get_height() > 0 and y < self.altura:
                tela.blit(
                    surf,
                    surf.get_rect(midtop=(self.largura // 2, int(y)))
                )

            y += surf.get_height() + 14

    def _carregar_sprite_bobinha(self):
        self._bobinha_carregado = True

        for caminho in (SPRITE_BOBINHA, SPRITE_BOBINHA + ".png"):
            if os.path.isfile(caminho):
                imagem = pygame.image.load(caminho).convert_alpha()

                largura = max(
                    1,
                    int(imagem.get_width() * ALTURA_BOBINHA
                        / imagem.get_height())
                )

                self.sprite_bobinha = pygame.transform.smoothscale(
                    imagem, (largura, ALTURA_BOBINHA)
                )
                return

        print(f"[final] sprite não encontrado: {SPRITE_BOBINHA}")

    def _desenhar_bobinha(self, tela):
        espera = (
            pygame.time.get_ticks() - self.tempo_etapa - ATRASO_BOBINHA_MS
        )

        if espera < 0:
            return

        # aparece devagar (fade-in)
        alpha = min(255, int(255 * espera / FADE_BOBINHA_MS))

        if not self._bobinha_carregado:
            self._carregar_sprite_bobinha()

        if not self._audio_bobinha_tocado:
            self._audio_bobinha_tocado = True

            if os.path.isfile(AUDIO_BOBINHA):
                pygame.mixer.Sound(AUDIO_BOBINHA).play()

        texto = self._fonte(24).render(TEXTO_BOBINHA, True, COR_TEXTO)
        texto.set_alpha(alpha)

        if self.sprite_bobinha:
            self.sprite_bobinha.set_alpha(alpha)

        largura_sprite = (
            self.sprite_bobinha.get_width() + 20
            if self.sprite_bobinha else 0
        )

        x = (self.largura - (largura_sprite + texto.get_width())) // 2
        centro_y = int(self.altura * 0.74)

        if self.sprite_bobinha:
            tela.blit(
                self.sprite_bobinha,
                self.sprite_bobinha.get_rect(
                    midleft=(x, centro_y)
                )
            )

        tela.blit(
            texto,
            texto.get_rect(midleft=(x + largura_sprite, centro_y))
        )

    def _desenhar_obrigado(self, tela):
        texto = self._render_ajustado(
            TEXTO_OBRIGADO, 56, COR_TITULO, self.largura - 60
        )

        sombra = self._render_ajustado(
            TEXTO_OBRIGADO, 56, (120, 60, 20), self.largura - 60
        )
        centro = (self.largura // 2, self.altura // 2)

        tela.blit(sombra, sombra.get_rect(center=(centro[0] + 4, centro[1] + 4)))
        tela.blit(texto, texto.get_rect(center=centro))

        self._desenhar_bobinha(tela)

        if (pygame.time.get_ticks() // 500) % 2 == 0:
            dica = self._fonte(14).render(
                "ENTER para voltar ao menu", True, (160, 160, 180)
            )
            tela.blit(
                dica,
                dica.get_rect(center=(self.largura // 2, self.altura - 45))
            )

    def desenhar(self, tela):
        tela.fill(COR_FUNDO)

        if self.etapa == "diploma":
            self._desenhar_diploma(tela)

        elif self.etapa == "creditos":
            self._desenhar_fundo_setas(tela)
            self._desenhar_creditos(tela)

        else:
            self._desenhar_fundo_setas(tela)
            self._desenhar_obrigado(tela)

        alpha = self._alpha()

        if alpha < 255:
            veu = pygame.Surface((self.largura, self.altura))
            veu.fill((0, 0, 0))
            veu.set_alpha(255 - alpha)
            tela.blit(veu, (0, 0))