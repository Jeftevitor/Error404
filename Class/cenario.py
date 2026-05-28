class Cenario:

    def __init__(self, nome, descricao, largura=1280, altura=720):

        self.nome = nome
        self.descricao = descricao
        self.largura = largura
        self.altura = altura
        self.elementos = []  
        self.musica = None  
        self.dificuldade = 1
        self.background = None 
        self.professor = None  
