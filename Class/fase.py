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