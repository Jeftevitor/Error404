import pygame

class Fase:
    def __init__(self):
        self.fases = [
            {
                "nome": "Joaildo",
                "arquivo": "Assets/Arquivos_txt/fase1.txt",
                "musica": "Assets/Music/JOJO(Freak-Ariana grande).ogg",
                "professores": ["joaildo"],
                "pausa_final_ms": 850,
                "desbloqueada": True
            },
            {
                "nome": "Max e Hugo",
                "arquivo": "Assets/Arquivos_txt/fase2.txt",
                "musica": "Assets/Music/MAX_HUGO(Passeios noturnos- Jão).ogg",
                "professores": ["hugo", "max"],
                "pausa_final_ms": 800,
                "desbloqueada": False
            },
            {
                "nome": "Romerito",
                "arquivo": "Assets/Arquivos_txt/fase3.txt",
                "musica": "Assets/Music/ROMERITO(Nuevayol- Bad bunny).ogg",
                "professores": ["romerito"],
                "pausa_final_ms": 950,
                "desbloqueada": False
            }
        ]

        self.notas = []
        self.indice_nota = 0

        # Momento em que as setas terminaram e a música foi encerrada
        self.musica_terminou_em = None

    def fase_atual(self, indice):
        return self.fases[indice]

    def total_fases(self):
        return len(self.fases)

    def desbloquear_proxima(self, indice_atual):
        if indice_atual < len(self.fases) - 1:
            self.fases[indice_atual + 1]["desbloqueada"] = True

    def carregar_fase(self, arquivo_txt):
        self.notas = []

        with open(arquivo_txt, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                partes = linha.strip().split()

                if not partes:
                    continue

                if len(partes) == 2:
                    tempo, direcao = partes

                    self.notas.append(
                        (int(tempo), direcao)
                    )
        self.notas = sorted(set(self.notas))

        self.indice_nota = 0

        return self.notas

#Carrega e toca a música da fase e reinicia o controle de fim.
    def iniciar_musica(self, indice):
        pygame.mixer.music.load(self.fases[indice]["musica"])
        pygame.mixer.music.play()
        self.musica_terminou_em = None

    def fase_terminou(self, indice, notas_concluidas):
        if not notas_concluidas:
            return False

        if self.musica_terminou_em is None:
            pygame.mixer.music.stop()
            self.musica_terminou_em = pygame.time.get_ticks()
            return False

        return (
            pygame.time.get_ticks() - self.musica_terminou_em
            >= self.fases[indice]["pausa_final_ms"]
        )