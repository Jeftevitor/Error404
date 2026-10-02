import pygame

LIMITE_NOME = 12

class Intro:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura

        self.img_f = pygame.image.load('Assets/Telas/fundo.jpg').convert_alpha()

        self.img_l = pygame.image.load('Assets/Telas/logo.png').convert_alpha()

        self.fonte = pygame.font.Font(None, 60)

        # ======================= NOME =======================

        self.etapa = "logo"
        self.nome = ""

        self.fonte_titulo = pygame.font.Font(None, 80)
        self.fonte_nome = pygame.font.Font(None, 70)
        self.fonte_dica = pygame.font.Font(None, 32)

    # =========================================================
    # EVENTOS
    # =========================================================

    def processar_evento(self, evento):

        if evento.type != pygame.KEYDOWN:
            return None

        # ======================= ETAPA LOGO =======================

        if self.etapa == "logo":

            if evento.key == pygame.K_RETURN:
                self.etapa = "nome"

            return None

        # ======================= ETAPA NOME =======================

        if evento.key == pygame.K_RETURN:

            if self.nome.strip():
                return self.nome.strip()

        elif evento.key == pygame.K_BACKSPACE:

            self.nome = self.nome[:-1]

        else:

            letra = evento.unicode
            if (
                letra
                and letra.isprintable()
                and letra != ";"
                and len(self.nome) < LIMITE_NOME
                and not (letra == " " and not self.nome)
            ):
                self.nome += letra

        return None

    # =========================================================
    # DESENHAR
    # =========================================================

    def _desenhar_fundo(self, tela):
        tela.fill((20, 20, 20))

        fundo = pygame.transform.scale(self.img_f,(self.largura, self.altura))
        tela.blit(fundo, (0, 0))

    def desenhar(self, tela):

        self._desenhar_fundo(tela)

        if self.etapa == "nome":
            self._desenhar_nome(tela)
            return

        logo = pygame.transform.scale(self.img_l,(self.largura // 2, self.altura // 2))

        x = self.largura // 2 - logo.get_width() // 2
        y = self.altura // 2 - logo.get_height() // 2

        tela.blit(logo, (x, y))

        tempo = pygame.time.get_ticks()

        if (tempo // 500) % 2 == 0:
            texto = self.fonte.render("APERTE ENTER",True,(255, 255, 255))
            texto_rect = texto.get_rect(center=(self.largura // 2, self.altura - 80))

            tela.blit(texto, texto_rect)

    def _desenhar_nome(self, tela):
        escurecer = pygame.Surface(
            (self.largura, self.altura), pygame.SRCALPHA
        )

        escurecer.fill((0, 0, 0, 160))

        tela.blit(escurecer, (0, 0))

        titulo = self.fonte_titulo.render(
            "DIGITE SEU NOME", True, (255, 255, 255)
        )

        tela.blit(
            titulo,
            titulo.get_rect(center=(self.largura // 2, 220))
        )

        caixa = pygame.Rect(0, 0, 560, 90)
        caixa.center = (self.largura // 2, 360)

        pygame.draw.rect(
            tela, (40, 40, 40), caixa, border_radius=14
        )

        pygame.draw.rect(
            tela, (0, 255, 0), caixa, width=3, border_radius=14
        )

        cursor = "|" if (pygame.time.get_ticks() // 500) % 2 == 0 else ""

        texto = self.fonte_nome.render(
            self.nome + cursor, True, (255, 255, 255)
        )

        tela.blit(
            texto,
            texto.get_rect(center=caixa.center)
        )

        dica = self.fonte_dica.render(
            f"ENTER para confirmar  ({len(self.nome)}/{LIMITE_NOME})",
            True,
            (180, 180, 180)
        )

        tela.blit(
            dica,
            dica.get_rect(center=(self.largura // 2, 450))
        )