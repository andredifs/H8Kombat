from argparse import ArgumentParser, Namespace
from main import main
from art import tprint


# Aqui poderemos colocar o código que será executado quando o comando "run" for chamado
# Futuramente poderemos colocar mais flags para o comando "run", exemplos:
# py game.py run debug -> executa o jogo em modo debug com mais informações no console
# py game.py run unlock -> desbloqueia todos os poderes do personagem
def run(parser: ArgumentParser):
    def _run(arg: Namespace):
        tprint("H8 KOMBAT", font="small", chr_ignore=True)

        if arg.dev:
            print('[ Running as dev ]')
            main(True)

        else:
            print('Running game...')
            main()

    parser.set_defaults(func=_run)
