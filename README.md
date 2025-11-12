# Duelo no Velho-Oeste

Um jogo rápido de reflexos e duelo no estilo Velho-Oeste, construído em Python com a biblioteca Pygame. Dois jogadores se enfrentam para ver quem saca a arma mais rápido!

---

## Vídeo de Apresentação

**[>> Clique aqui para ver o vídeo <<](https://www.youtube.com/watch?v=COLOQUE-O-RESTO-DO-SEU-LINK-AQUI)**

---

## Membros do Grupo

* [Luka Cione Buchviser]
* [Frederico da Costa Marques]
* [Tadeu Henrique Brostowicz Martins]

---

## Uso de Inteligência Artificial

Para o desenvolvimento deste projeto, utilizamos a ferramenta institucional de IA generativa como assistente de programação (em formato *pair programming*).

A estrutura principal do jogo, a lógica de estados e a implementação inicial das animações foram desenvolvidas pelo grupo.

A IA foi consultada para as seguintes tarefas de refatoração e adição:

1.  **Tela Final:** Ajudou a refatorar a lógica de desenho para criar uma tela de "campeão" (com o fundo preto e o cowboy sorrindo) que fosse diferente da tela de "fim de rodada".
2.  **Implementação de Sons:** Sugeriu os comandos do `pygame.mixer` para carregar (`.Sound()`) e tocar (`.play()`) os arquivos de áudio nos momentos corretos (tiro e vitória).
3.  **Revisão de Código:** Atuou na "limpeza" do código, removendo comentários desnecessários para a entrega final.
4.  **Análise da Rubrica:** Ajudou a comparar o código final com os requisitos da rubrica de avaliação.

**Declaração:** Nenhuma função principal foi "100% gerada". Todas as sugestões da IA foram revisadas, compreendidas e integradas manualmente pelo grupo. Estimamos que a contribuição da IA se concentrou na **refatoração da função de desenho final (cerca de 30%)** e na **implementação dos sons (cerca de 50%)**. O restante do código (lógica de estados, animação, movimento) é 100% autoral do grupo.

---

## Como Rodar o Jogo

Para jogar, você precisará ter o **Python 3** e a biblioteca **Pygame** instalados em seu computador.

### 1. Instalação de Dependências

Se você ainda não tem o Pygame, pode instalá-lo facilmente usando `pip`. Abra seu terminal ou prompt de comando e digite:

pip install pygame