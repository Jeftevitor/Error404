import os
import pygame


class TelaInicial:
    def __init__(self, tela, largura, altura):
        self.tela = tela
        self.largura = largura
        self.altura = altura
        self.clock = pygame.time.Clock()

        self.fonte_titulo = pygame.font.SysFont(None, 72)
        self.fonte_botao = pygame.font.SysFont(None, 36)

        self.bg_image = None
        bg_path = os.path.join('Assets', 'Sprites', 'fundo.png')
        if os.path.exists(bg_path):
            try:
                imagem = pygame.image.load(bg_path)
                self.bg_image = pygame.transform.scale(imagem, (largura, altura)).convert()
            except pygame.error:
                self.bg_image = None

        largura_botao = 240
        altura_botao = 64
        x = (self.largura - largura_botao) // 2
        self.botao_comecar = pygame.Rect(x, self.altura // 2 - 40, largura_botao, altura_botao)
        self.botao_creditos = pygame.Rect(x, self.altura // 2 + 40, largura_botao, altura_botao)

        self.rodando = True

    def run(self):
        while self.rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.rodando = False
                    return None
                elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if self.botao_comecar.collidepoint(evento.pos):
                        info = self.coletar_informacoes()
                        return info
                    elif self.botao_creditos.collidepoint(evento.pos):
                        self.mostrar_creditos()

            self.desenhar()
            pygame.display.update()
            self.clock.tick(60)

        return None

    def desenhar(self):
        if self.bg_image:
            self.tela.blit(self.bg_image, (0, 0))
        else:
            self.tela.fill((20, 20, 30))

        titulo = self.fonte_titulo.render('ERROR404', True, (255, 255, 255))
        x_t = (self.largura - titulo.get_width()) // 2
        self.tela.blit(titulo, (x_t, 100))

        mouse_pos = pygame.mouse.get_pos()
        for botao, texto in [(self.botao_comecar, 'COMEÇAR'), (self.botao_creditos, 'CRÉDITOS')]:
            cor = (100, 180, 255) if botao.collidepoint(mouse_pos) else (60, 140, 220)
            pygame.draw.rect(self.tela, cor, botao, border_radius=8)
            pygame.draw.rect(self.tela, (255, 255, 255), botao, 2, border_radius=8)
            txt = self.fonte_botao.render(texto, True, (255, 255, 255))
            tx = botao.x + (botao.width - txt.get_width()) // 2
            ty = botao.y + (botao.height - txt.get_height()) // 2
            self.tela.blit(txt, (tx, ty))

    def mostrar_creditos(self):
        rodando_creditos = True
        fonte = pygame.font.SysFont(None, 30)
        linhas = [
            'Desenvolvedores: Jefte Vitor, Isabela Nóbrega',
            'Disciplina: Programação Orientada a Objetos',
            'Professor responsavel pelo desenvolvimento: Max Miller',
            '',
            'Clique para voltar'
        ]

        while rodando_creditos:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando_creditos = False
                    self.rodando = False
                elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    rodando_creditos = False

            if self.bg_image:
                self.tela.blit(self.bg_image, (0, 0))
            else:
                self.tela.fill((10, 10, 20))

            y = 120
            for linha in linhas:
                txt = fonte.render(linha, True, (255, 255, 255))
                x = (self.largura - txt.get_width()) // 2
                self.tela.blit(txt, (x, y))
                y += 40

            pygame.display.update()
            self.clock.tick(60)

    def escolher_fase(self, desbloqueios):
        largura_botao = 180
        altura_botao = 60
        x_center = self.largura // 2

        botao_fase1 = pygame.Rect(x_center - 310, self.altura // 2 - 40, largura_botao, altura_botao)
        botao_fase2 = pygame.Rect(x_center - 90, self.altura // 2 - 40, largura_botao, altura_botao)
        botao_fase3 = pygame.Rect(x_center + 130, self.altura // 2 - 40, largura_botao, altura_botao)

        rodando_fase = True
        while rodando_fase:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return None
                elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if botao_fase1.collidepoint(evento.pos) and desbloqueios[0]:
                        return 1
                    elif botao_fase2.collidepoint(evento.pos) and desbloqueios[1]:
                        return 2
                    elif botao_fase3.collidepoint(evento.pos) and desbloqueios[2]:
                        return 3

            if self.bg_image:
                self.tela.blit(self.bg_image, (0, 0))
            else:
                self.tela.fill((15, 15, 30))
            titulo = self.fonte_titulo.render('Escolha a fase', True, (255, 255, 255))
            self.tela.blit(titulo, ((self.largura - titulo.get_width()) // 2, 100))

            mouse_pos = pygame.mouse.get_pos()
            for botao, texto, desbloqueado in [
                (botao_fase1, 'Fase 1', desbloqueios[0]),
                (botao_fase2, 'Fase 2', desbloqueios[1]),
                (botao_fase3, 'Fase 3', desbloqueios[2])
            ]:
                cor = (100, 180, 255) if botao.collidepoint(mouse_pos) and desbloqueado else (60, 140, 220)
                if not desbloqueado:
                    cor = (80, 80, 80)
                pygame.draw.rect(self.tela, cor, botao, border_radius=8)
                pygame.draw.rect(self.tela, (255, 255, 255), botao, 2, border_radius=8)
                txt = self.fonte_botao.render(texto, True, (255, 255, 255))
                tx = botao.x + (botao.width - txt.get_width()) // 2
                ty = botao.y + (botao.height - txt.get_height()) // 2
                self.tela.blit(txt, (tx, ty))

            pygame.display.update()
            self.clock.tick(60)

    def coletar_informacoes(self):
        nome = ""
        genero = None

        largura_botao = 160
        altura_botao = 56
        x_center = self.largura // 2

        input_rect = pygame.Rect(x_center - 200, self.altura // 2 - 40, 400, 52)
        botao_m = pygame.Rect(x_center - 190, self.altura // 2 + 30, 160, altura_botao)
        botao_f = pygame.Rect(x_center + 30, self.altura // 2 + 30, 160, altura_botao)
        botao_confirm = pygame.Rect(x_center - largura_botao // 2, self.altura // 2 + 110, largura_botao, altura_botao)

        ativo = True
        clock = pygame.time.Clock()

        while ativo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return None
                elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if botao_m.collidepoint(evento.pos):
                        genero = 'M'
                    elif botao_f.collidepoint(evento.pos):
                        genero = 'F'
                    elif botao_confirm.collidepoint(evento.pos) and nome.strip() != "" and genero is not None:
                        return {'name': nome.strip(), 'gender': genero}
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_BACKSPACE:
                        nome = nome[:-1]
                    elif evento.key == pygame.K_RETURN:
                        if nome.strip() != "" and genero is not None:
                            return {'name': nome.strip(), 'gender': genero}
                    else:
                        if len(nome) < 16 and evento.unicode.isprintable():
                            nome += evento.unicode

            if self.bg_image:
                self.tela.blit(self.bg_image, (0, 0))
            else:
                self.tela.fill((15, 15, 25))
            titulo = self.fonte_titulo.render('Insira seu nome:', True, (255, 255, 255))
            self.tela.blit(titulo, ((self.largura - titulo.get_width()) // 2, 80))

            label_nome = self.fonte_botao.render('Nome:', True, (200, 200, 200))
            self.tela.blit(label_nome, (input_rect.x, input_rect.y - 35))
            pygame.draw.rect(self.tela, (255, 255, 255), input_rect, 2, border_radius=6)
            fonte_input = self.fonte_botao
            txt_nome = fonte_input.render(nome or 'Digite seu nome...', True, (255, 255, 255))
            self.tela.blit(txt_nome, (input_rect.x + 8, input_rect.y + (input_rect.height - txt_nome.get_height()) // 2))

            cor_m = (100, 180, 255) if genero == 'M' else (60, 140, 220)
            cor_f = (100, 180, 255) if genero == 'F' else (60, 140, 220)
            pygame.draw.rect(self.tela, cor_m, botao_m, border_radius=8)
            pygame.draw.rect(self.tela, cor_f, botao_f, border_radius=8)
            pygame.draw.rect(self.tela, (255, 255, 255), botao_m, 2, border_radius=8)
            pygame.draw.rect(self.tela, (255, 255, 255), botao_f, 2, border_radius=8)
            txt_m = fonte_input.render('Menino', True, (255, 255, 255))
            txt_f = fonte_input.render('Menina', True, (255, 255, 255))
            self.tela.blit(txt_m, (botao_m.x + (botao_m.width - txt_m.get_width()) // 2, botao_m.y + 10))
            self.tela.blit(txt_f, (botao_f.x + (botao_f.width - txt_f.get_width()) // 2, botao_f.y + 10))

            cor_conf = (80, 200, 120) if nome.strip() != "" and genero is not None else (80, 80, 80)
            pygame.draw.rect(self.tela, cor_conf, botao_confirm, border_radius=8)
            pygame.draw.rect(self.tela, (255, 255, 255), botao_confirm, 2, border_radius=8)
            txt_conf = fonte_input.render('CONFIRMAR', True, (255, 255, 255))
            self.tela.blit(txt_conf, (botao_confirm.x + (botao_confirm.width - txt_conf.get_width()) // 2, botao_confirm.y + 8))

            pygame.display.update()
            clock.tick(60)