import pygame


class Seta:
    imagens_cache = {}

    def __init__(self, x, y, direcao, quem="jogador"):
        self.x = x
        self.y = y
        self.direcao = direcao
        self.quem = quem
        self.velocidade = 5
        self.hit = False

        self.imagem = Seta.carregar_imagem(direcao)

    @classmethod
    def carregar_imagem(cls, direcao):
        if direcao not in cls.imagens_cache:
            caminho = f'Assets/Sprites/{direcao}.png'
            imagem = pygame.image.load(caminho).convert_alpha()
            imagem = pygame.transform.scale(imagem, (180, 160))
            cls.imagens_cache[direcao] = imagem

        return cls.imagens_cache[direcao]

    def acertou(self):
        if self.hit:
            self.x = 1500
            self.y = 1500

    def mover(self):
        self.y += self.velocidade

    def perdeu(self, receptor_y):
        return self.y > receptor_y + 150

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x, self.y))