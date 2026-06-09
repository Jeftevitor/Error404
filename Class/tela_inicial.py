import pygame

class TelaInicial:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura

        self.fonte_titulo = pygame.font.Font(None, 80)
        self.fonte_botao = pygame.font.Font(None, 50)

        self.botoes = {
            "comecar": pygame.Rect(largura // 2 - 100, 180, 200, 50),
            "score": pygame.Rect(largura // 2 - 100, 260, 200, 50),
            "creditos": pygame.Rect(largura // 2 - 100, 340, 200, 50),
            "sair": pygame.Rect(largura // 2 - 100, 420, 200, 50)
        }

    def desenhar(self, tela):
        tela.fill((20, 20, 20))

        titulo = self.fonte_titulo.render("ERROR404", True, (255, 255, 255))
        tela.blit(
            titulo,
            (self.largura // 2 - titulo.get_width() // 2, 50)
        )

        for nome, rect in self.botoes.items():
            pygame.draw.rect(tela, (80, 80, 80), rect)
            pygame.draw.rect(tela, (255, 255, 255), rect, 2)

            texto = self.fonte_botao.render(nome.upper(), True, (255, 255, 255))
            tela.blit(
                texto,
                (
                    rect.centerx - texto.get_width() // 2,
                    rect.centery - texto.get_height() // 2
                )
            )

    def verificar_clique(self, pos):
        for nome, rect in self.botoes.items():
            if rect.collidepoint(pos):
                return nome

        return None