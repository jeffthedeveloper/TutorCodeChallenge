
```markdown
# Dungeon Explorer - Python Tutor Assessment

Este jogo foi criado como uma ferramenta de avaliação para tutores de Python. Ele demonstra o uso dos módulos PgZero, math e random para criar um jogo Rogue-like totalmente funcional.

## Objetivo do Jogo
Controle seu herói por uma masmorra, coletando tesouros enquanto evita inimigos. Avance pelos níveis coletando todos os tesouros em cada um deles.

## Controles
- Teclas de Seta: Movem o personagem do jogador
- Mouse: Navega no menu
- Enter: Inicia o jogo ou reinicia após o Game Over

## Funcionalidades
- Menu principal com botões "Start Game", "Sound On/Off" e "Exit"
- Música de fundo e efeitos sonoros com opção de ligar/desligar
- Múltiplos inimigos perigosos que se movem dentro de suas áreas definidas
- Classes para movimento do personagem e animação de sprites
- Animação de sprites para os estados de movimento e inativo do herói e dos inimigos
- Rastreamento de pontuação e salvamento de recorde
- Múltiplos níveis com dificuldade crescente

## Critérios de Avaliação
Este código demonstra:
1. Fundamentos de Python (variáveis, funções, loops, condicionais)
2. Conceitos de programação orientada a objetos (classes, herança)
3. Princípios de desenvolvimento de jogos (detecção de colisão, gerenciamento de sprites, animação)
4. Organização e comentários de código limpos
5. Implementação usando módulos restritos (PgZero, math, random, Rect do Pygame)

## Requisitos
- Python 3.6 ou superior (recomendado Python 3.9 para evitar potenciais conflitos com versões mais recentes)
- PgZero (Pygame Zero)

## Instalando as Dependências e Executando o Jogo

Para garantir que o jogo funcione corretamente, siga estas instruções para instalar as dependências e executar o jogo usando `pgzrun`.

**1. Verificando sua versão do Python:**

Abra o terminal (ou Prompt de Comando no Windows) e digite:
```bash
python --version
```
ou
```bash
py --version
```
Isso mostrará a versão padrão do Python que está sendo usada.

**2. Instalando o PgZero:**

O PgZero geralmente inclui o Pygame como dependência. Use o `pip`, o gerenciador de pacotes do Python, para instalar o PgZero.

```bash
pip install pgzero --user
```

Se você estiver usando uma versão específica do Python (como o Python 3.9 instalado alternativamente), pode direcionar a instalação para essa versão usando o `py`:

```bash
py -3.9 -m pip install pgzero --user
```

O `--user` instala o pacote no seu diretório de usuário, evitando problemas de permissão.

**3. Executando o Jogo com `pgzrun`:**

Para executar o jogo, navegue até o diretório onde o arquivo `dungeon_explorer.py` está salvo no seu terminal. Em vez de usar `python`, utilize o comando `pgzrun` seguido do nome do arquivo:

```bash
pgzrun dungeon_explorer.py
```

O `pgzrun` é um utilitário fornecido com o PgZero que simplifica a execução de jogos feitos com essa biblioteca.

**4. Resolvendo Conflitos com Versões Modernas do Python (Exemplo: Python 3.12 e 3.13):**

Versões mais recentes do Python podem, ocasionalmente, apresentar incompatibilidades com bibliotecas mais antigas ou com as dependências delas. Se você encontrar problemas ao tentar executar o jogo com sua versão padrão do Python (por exemplo, 3.12 ou 3.13), uma solução é usar uma versão mais antiga e estável do Python, como o Python 3.9, conforme mencionado que você fez.

**Se você instalou o Python 3.9 como uma versão alternativa:**

- **Certifique-se de que o Python 3.9 esteja no seu PATH (opcional, mas útil).**
- **Use o `py` para direcionar a instalação do PgZero para o Python 3.9:**
  ```bash
  py -3.9 -m pip install pgzero --user
  ```
- **Execute o jogo usando o `pgzrun` associado ao Python 3.9 (se necessário, pode ser preciso especificar a versão ao chamar o `pgzrun`, embora geralmente ele use a versão padrão associada ao PgZero instalado):**
  ```bash
  py -3.9 -m pgzrun dungeon_explorer.py
  ```
  Em muitos sistemas, após instalar o PgZero para uma versão específica do Python, o comando `pgzrun` já estará configurado para usar essa versão.

**Observações:**

- Certifique-se de ter o `pip` instalado para a versão do Python que você está usando. Geralmente, ele vem instalado por padrão com o Python.
- Se você ainda tiver problemas, pode ser útil verificar se o diretório de instalação dos pacotes do Python (para a versão que você está usando) está no seu PATH do sistema operacional.

Seguindo estas instruções, você deverá conseguir instalar as dependências necessárias e executar o jogo "Dungeon Explorer" utilizando o PgZero corretamente, mesmo lidando com diferentes versões do Python no seu sistema.
