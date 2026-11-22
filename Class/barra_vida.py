import math
import os
import unicodedata
import pygame


class BarraVida:
    # =====================================================
    # BALANCEAMENTO(%)
    # =====================================================
    VIDA_INICIAL = 50.0         # a barra começa na metade
    PERDA_SETA_PERDIDA = 7.0    # jogador deixou a seta passar
    CURA_ACERTO = 3.0           # jogador acertou uma seta
    PERDA_TOQUE_ERRADO = 4.0    # jogador apertou sem ter seta para acertar

    # =====================================================
    # ANIMAÇÃO
    # =====================================================
    SUAVIZACAO_DESCIDA = 15.0   
    SUAVIZACAO_SUBIDA = 9.0     
    DURACAO_FLASH = 0.25        

    # =====================================================
    # CABEÇAS NA PONTA DA BARRA VERDE
    # =====================================================
    PASTA_CABECAS = 'Assets/Barra'        # arquivos: cabeça_{personagem}_{estado}.png
    ALTURA_CABECA = 70                    # altura base do sprite (px)
    ESCALA_PROFESSOR = 1.10               # +10% nas cabeças dos professores
    ESCALA_MENINO = 1.20                  # +20% na cabeça do menino
    SOBREPOSICAO_CABECA = 10              # quanto a cabeça invade o outro lado (px)
    SOBREPOSICAO_PROFESSORES = 30         # quanto uma cabeça de professor cobre a outra (px)
    LIMITE_ESPANTADO = 30.0               # até 30%  -> e (espantado)
    LIMITE_SORRINDO = 70.0                # acima de 70% -> s (sorrindo)
                                          # no meio -> n (normal)
    PROFESSOR_ESPELHA = True              # professor sorri quando o jogador está mal (e vice-versa)

    def __init__(self, x, y, largura, altura):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.raio = altura // 2  # bordas totalmente arredondadas

        # Vida real (o jogo lê e altera esses valores)
        self.vida_maxima = 1000.0
        self.vida_jogador = self.vida_maxima * self.VIDA_INICIAL / 100.0

        # Valor só visual, em % (0 a 100)
        self.valor_exibido = self.VIDA_INICIAL

        self._alvo_anterior = self.VIDA_INICIAL
        self._flash = 0.0
        self._ultimo_tick = None

        self.cor_jogador = (90, 210, 130)
        self.cor_professor = (160, 32, 240)
        self.cor_borda = (0, 0, 0)

        # Personagens das cabeças: o protagonista fica sempre à esquerda
        # (lado verde); os professores mudam conforme a fase (lado roxo)
        self.protagonista = "menino"
        self.professores = []
        self._cache_cabecas = {}

        # Superfície reaproveitada e máscara com cantos arredondados
        self._superficie = pygame.Surface((largura, altura), pygame.SRCALPHA)
        self._mascara = pygame.Surface((largura, altura), pygame.SRCALPHA)
        pygame.draw.rect(
            self._mascara, (255, 255, 255, 255),
            (0, 0, largura, altura), border_radius=self.raio
        )

    # -----------------------------------------------------
    # Eventos do jogo
    # -----------------------------------------------------
    def _pct(self, porcentagem):
        return self.vida_maxima * porcentagem / 100.0

    def seta_perdida(self):
        self.dano_jogador(self._pct(self.PERDA_SETA_PERDIDA))

    def toque_errado(self):
        self.dano_jogador(self._pct(self.PERDA_TOQUE_ERRADO))

    def acerto(self, multiplicador=1.0):
        self.curar(self._pct(self.CURA_ACERTO) * multiplicador)

    def dano_jogador(self, dano):
        self.vida_jogador -= dano
        self.vida_jogador = max(0.0, min(self.vida_maxima, self.vida_jogador))

    def curar(self, valor):
        self.vida_jogador += valor
        self.vida_jogador = max(0.0, min(self.vida_maxima, self.vida_jogador))

    def dano_professor(self, dano):
        pass

    def reset(self):
        self.vida_jogador = self.vida_maxima * self.VIDA_INICIAL / 100.0
        self.valor_exibido = self.VIDA_INICIAL
        self._alvo_anterior = self.VIDA_INICIAL
        self._flash = 0.0
        self._ultimo_tick = None

    def definir_personagens(self, protagonista, professores):
        """Define quem aparece na ponta da barra (professores = lista de nomes)."""
        self.protagonista = protagonista
        self.professores = list(professores)

        # carrega tudo agora (na troca de fase) para não travar durante o jogo
        self._precarregar_cabecas()

    def _precarregar_cabecas(self):
        for estado in ("e", "n", "s"):
            self._cabeca(self.protagonista, estado, self.ESCALA_MENINO)

            for nome in self.professores:
                self._cabeca(nome, estado, self.ESCALA_PROFESSOR)

        # Carrega todas as cabeças agora (na troca de fase) para não ter
        # leitura de disco nem redimensionamento no meio da música
        for estado in ("e", "n", "s"):
            self._cabeca(self.protagonista, estado, self.ESCALA_MENINO)

            for nome in self.professores:
                self._cabeca(nome, estado, self.ESCALA_PROFESSOR)

    def jogador_perdeu(self):
        return self.vida_jogador <= 0

    # -----------------------------------------------------
    # Animação
    # -----------------------------------------------------
    def atualizar(self):
        agora = pygame.time.get_ticks()
        if self._ultimo_tick is None:
            dt = 1.0 / 60.0
        else:
            dt = (agora - self._ultimo_tick) / 1000.0
        self._ultimo_tick = agora
        dt = max(0.0, min(dt, 0.05))  # evita saltos após pausas/contagem

        alvo = (self.vida_jogador / self.vida_maxima) * 100.0

        if alvo < self._alvo_anterior - 1e-6:
            self._flash = 1.0
        self._alvo_anterior = alvo

        taxa = (
            self.SUAVIZACAO_DESCIDA
            if alvo < self.valor_exibido
            else self.SUAVIZACAO_SUBIDA
        )
        self.valor_exibido += (alvo - self.valor_exibido) * (1.0 - math.exp(-taxa * dt))
        if abs(alvo - self.valor_exibido) < 0.02:
            self.valor_exibido = alvo

        self._flash = max(0.0, self._flash - dt / self.DURACAO_FLASH)

    # -----------------------------------------------------
    # Cabeças
    # -----------------------------------------------------
    def _estado_protagonista(self):
        v = self.valor_exibido

        if v <= self.LIMITE_ESPANTADO:
            return "e"
        if v > self.LIMITE_SORRINDO:
            return "s"
        return "n"

    def _estado_professor(self):
        if not self.PROFESSOR_ESPELHA:
            return "n"

        return {"e": "s", "n": "n", "s": "e"}[self._estado_protagonista()]

    @staticmethod
    def _normalizar(texto):
        """Minúsculo e sem acento/forma Unicode, para comparar nomes de arquivo."""
        texto = unicodedata.normalize("NFKD", texto)
        texto = "".join(c for c in texto if not unicodedata.combining(c))
        return texto.lower()

    def _achar_arquivo_cabeca(self, nome, estado):
        """Procura cabeça_{nome}_{estado} ignorando maiúsculas, acentos e extensão."""
        # caminho direto (rápido); só procura na pasta se não existir
        direto = f"{self.PASTA_CABECAS}/cabeça_{nome}_{estado}.png"

        if os.path.isfile(direto):
            return direto

        alvo = self._normalizar(f"cabeça_{nome}_{estado}")

        try:
            arquivos = os.listdir(self.PASTA_CABECAS)
        except OSError:
            return None

        for arquivo in arquivos:
            sem_ext, ext = os.path.splitext(arquivo)

            if ext.lower() not in ("", ".png", ".jpg", ".jpeg", ".webp"):
                continue

            if self._normalizar(sem_ext) == alvo:
                return os.path.join(self.PASTA_CABECAS, arquivo)

        return None

    def _cabeca(self, nome, estado, escala=1.0):
        """Carrega (com cache) a cabeça; se faltar o estado, tenta o normal."""
        altura_final = int(round(self.ALTURA_CABECA * escala))
        chave = (nome, estado, altura_final)

        if chave in self._cache_cabecas:
            return self._cache_cabecas[chave]

        sprite = None

        for est in (estado, "n"):
            caminho = self._achar_arquivo_cabeca(nome, est)

            if caminho is None:
                if est == estado:
                    print(f"[barra] não achei a cabeça '{nome}' no estado "
                          f"'{est}' em {self.PASTA_CABECAS}/ "
                          f"(esperado: cabeça_{nome}_{est}[.png])")
                continue

            imagem = pygame.image.load(caminho).convert_alpha()
            largura = max(
                1,
                int(imagem.get_width() * altura_final
                    / imagem.get_height())
            )
            sprite = pygame.transform.smoothscale(
                imagem, (largura, altura_final)
            )
            break

        self._cache_cabecas[chave] = sprite
        return sprite

    def _desenhar_cabecas(self, tela, largura_jogador):
        ponta_x = self.x + largura_jogador
        centro_y = self.y + self.altura // 2

        # professores à direita da ponta. O último da lista é o da frente
        # (Max): fica primeiro, colado na ponta, e cobre o seguinte (Hugo)
        estado_prof = self._estado_professor()
        x = ponta_x - self.SOBREPOSICAO_CABECA
        desenhos = []

        for nome in reversed(self.professores):
            sprite = self._cabeca(
                nome, estado_prof, self.ESCALA_PROFESSOR
            )

            if sprite is None:
                continue

            desenhos.append((sprite, sprite.get_rect(midleft=(x, centro_y))))
            x += sprite.get_width() - self.SOBREPOSICAO_PROFESSORES

        # desenha de trás para frente: o primeiro (Max) fica por cima
        for sprite, rect in reversed(desenhos):
            tela.blit(sprite, rect)

        # protagonista à esquerda da ponta, sempre
        sprite = self._cabeca(
            self.protagonista, self._estado_protagonista(),
            self.ESCALA_MENINO
        )

        if sprite is not None:
            tela.blit(
                sprite,
                sprite.get_rect(
                    midright=(ponta_x + self.SOBREPOSICAO_CABECA, centro_y)
                )
            )

    # -----------------------------------------------------
    # Desenho
    # -----------------------------------------------------
    @staticmethod
    def _misturar(cor_a, cor_b, t):
        return tuple(int(a + (b - a) * t) for a, b in zip(cor_a, cor_b))

    def desenhar(self, tela):
        p = max(0.0, min(1.0, self.valor_exibido / 100.0))
        largura_jogador = int(round(self.largura * p))
        self._superficie.fill(self.cor_professor)

        if largura_jogador > 0:
            cor = self._misturar(self.cor_jogador, (255, 255, 255), 0.6 * self._flash)
            pygame.draw.rect(
                self._superficie, cor,
                (0, 0, largura_jogador, self.altura)
            )

        self._superficie.blit(
            self._mascara, (0, 0),
            special_flags=pygame.BLEND_RGBA_MULT
        )
        tela.blit(self._superficie, (self.x, self.y))

        pygame.draw.rect(
            tela, self.cor_borda,
            (self.x, self.y, self.largura, self.altura),
            2, border_radius=self.raio
        )

        self._desenhar_cabecas(tela, largura_jogador)