# H8Kombat
Jogo de luta com personagens da turma T25 do ITA, projeto da matéria CSI-22.

### Como executar o jogo:
```bash
py game.py setup

source .venv/bin/activate # Linux | MacOS
.venv\Scripts\activate # Windows

py game.py run
```

Executar como desenvolvedor (Direto para o cenário de luta)
```bash
py game.py run --dev
```

### Como jogar:
Controles:
|            |   Jogador 1   |   Jogador 2   |
-------------| ------------- | ------------- |
Movimentação | A (esquerda) D (direita)  | Seta esquerda (esquerda) Seta direita (direita)  |
Pulo         | W  | Seta cima |
Soco         | R  | Shift  |
Chute        | T  | ;  |
Defesa       | S  | Seta baixo  |


### Estrutura do projeto
```
.
├── assets      -> Sprites, Backgrounds, Fontes
├── constants   -> Constantes (Ex.: Cores, Configurações...)
├── include     -> Classes (Ex.: Jogador, Botão...)
├── scripts     -> Scripts de execução
├── main.py     -> Loop principal
├── game.py     -> CLI para scripts (setup, run)
├── paths.py
├── README.md
└── requirements.txt
```

### Desenvolvedores
https://github.com/andredifs

https://github.com/antgustavo

https://github.com/luccarhaddad
