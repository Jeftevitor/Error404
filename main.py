from jogo import Jogo

try:
    jogo = Jogo()
    jogo.iniciar()

except Exception as erro:
    print(erro)