from argparse import ArgumentParser, Namespace

# Aqui poderemos colocar o código que será executado quando o comando "run" for chamado
# Futuramente poderemos colocar mais flags para o comando "run", exemplos:
# py game.py run debug -> executa o jogo em modo debug com mais informações no console
# py game.py run unlock -> desbloqueia todos os poderes do personagem

def run(parser: ArgumentParser):
    def _run(_: Namespace):
        print('Running game...')

    parser.set_defaults(func=_run)

