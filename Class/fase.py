import pygame


class Fase:
    def __init__(self):
        self.fases = [
            {
                "nome": "Joaildo",
                "arquivo": "Assets/Arquivos_txt/fase1.txt",
                "musica": "Assets/Music/JOJO(Freak-Ariana grande).ogg",
                "desbloqueada": True
            },
            {
                "nome": "Max e Hugo",
                "arquivo": "Assets/Arquivos_txt/fase2.txt",
                "musica": "Assets/Music/MAX_HUGO(Passeios noturnos- Jão).ogg",
                "desbloqueada": False
            },
            {
                "nome": "Romerito",
                "arquivo": "Assets/Arquivos_txt/fase3.txt",
                "musica": "Assets/Music/ROMERITO(Nuevayol- Bad bunny).ogg",
                "desbloqueada": False
            }
        ]

        self.notas = []
        self.indice_nota = 0

        # Controle de fim de fase pela música
        self.pausa_final_ms = 1500      # pausa depois que a música acaba
        self.musica_terminou_em = None  # momento (ms) em que a música acabou

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

        self.indice_nota = 0

        return self.notas

    def iniciar_musica(self, indice):
        """Carrega e toca a música da fase e reinicia o controle de fim."""
        pygame.mixer.music.load(self.fases[indice]["musica"])
        pygame.mixer.music.play()
        self.musica_terminou_em = None

    def fase_terminou(self):
        """True somente depois que a música acabou + a pausa final.

        Chame esta função a cada frame, mas só quando o jogo NÃO estiver
        pausado (com a música pausada, get_busy() pode retornar False).
        """
        if self.musica_terminou_em is None:
            if not pygame.mixer.music.get_busy():
                self.musica_terminou_em = pygame.time.get_ticks()
            return False

        return (
            pygame.time.get_ticks() - self.musica_terminou_em
            >= self.pausa_final_ms
        )