import pygame
import random

pygame.init()
pygame.font.init()

# --- Configurações da Tela ---
largura_tela = 800
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Duelo no Velho-Oeste")

# --- Cores ---
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
CINZA_FUNDO = (100, 100, 100)
VERDE = (0, 255, 0)

# --- Fontes ---
fonte_titulo = pygame.font.Font(None, 48)
fonte_texto = pygame.font.Font(None, 28)
fonte_vencedor = pygame.font.Font(None, 45)

# --- Imagens ---
fundo_inicio = pygame.image.load("fundooestenovo.png").convert()
fundo_inicio = pygame.transform.scale(fundo_inicio, (largura_tela, altura_tela))

cowboy_img = pygame.image.load("cowboysorrindo.png").convert_alpha()
cowboy_img = pygame.transform.scale(cowboy_img, (largura_tela, altura_tela))  # Cowboy ocupa a tela inteira

cowboybase = pygame.image.load("cowboy1.png").convert_alpha()
jogador1_img = cowboybase
jogador2_img = pygame.transform.flip(cowboybase, True, False)

# --- Retângulos dos jogadores ---
jogador1_rect = pygame.Rect(350, 480, 50, 100)
jogador2_rect = pygame.Rect(400, 480, 50, 100)
velocidade = 1

# --- Estados do jogo ---
estado_jogo = "INICIO"  # INICIO -> EXPLICACAO -> ANDANDO -> SINAL -> FIM
fala_index = 0
vencedor = None
sinal_ativo = False

clock = pygame.time.Clock()
rodando = True

# --- Falas do Cowboy ---
falas = [
    "Olá, forasteiro!",
    "Bem-vindo ao Velho Oeste, terra dos duelos!",
    "Atirador 1: aperte a tecla A para atirar.",
    "Atirador 2: aperte a tecla L para atirar.",
    "Mas cuidado para não se antecipar!",
    "Espere o sinal verde para vencer o duelo!"
]

# --- Função para desenhar botão ---
def desenhar_botao(texto, pos_y):
    botao_rect = pygame.Rect(largura_tela/2 - 100, pos_y, 200, 50)
    pygame.draw.rect(tela, PRETO, botao_rect)
    pygame.draw.rect(tela, BRANCO, botao_rect, 2)
    txt = fonte_texto.render(texto, True, BRANCO)
    tela.blit(txt, txt.get_rect(center=botao_rect.center))
    return botao_rect

# --- Função para desenhar balão retangular ---
def desenhar_balao(fala):
    # Retângulo fixo no canto superior direito
    balao_rect = pygame.Rect(largura_tela - 350, 40, 320, 160)
    pygame.draw.rect(tela, BRANCO, balao_rect, border_radius=15)
    pygame.draw.rect(tela, PRETO, balao_rect, 3, border_radius=15)

    # Quebra automática de linha para o texto
    palavras = fala.split(" ")
    linhas = []
    linha_atual = ""
    for palavra in palavras:
        teste = linha_atual + palavra + " "
        if fonte_texto.size(teste)[0] < balao_rect.width - 30:
            linha_atual = teste
        else:
            linhas.append(linha_atual)
            linha_atual = palavra + " "
    linhas.append(linha_atual)

    # Desenha o texto dentro do retângulo
    y = balao_rect.y + 20
    for linha in linhas:
        texto = fonte_texto.render(linha.strip(), True, PRETO)
        tela.blit(texto, (balao_rect.x + 15, y))
        y += 35

# --- Loop Principal ---
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        # --- Controles de fluxo ---
        if estado_jogo == "INICIO":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                estado_jogo = "EXPLICACAO"

        elif estado_jogo == "EXPLICACAO":
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or event.type == pygame.MOUSEBUTTONDOWN:
                if fala_index < len(falas) - 1:
                    fala_index += 1
                else:
                    estado_jogo = "ANDANDO"

        elif estado_jogo == "SINAL" and vencedor is None:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    vencedor = "Atirador 1"
                    estado_jogo = "FIM"
                elif event.key == pygame.K_l:
                    vencedor = "Atirador 2"
                    estado_jogo = "FIM"

        elif estado_jogo in ("ANDANDO", "ESPERANDO") and vencedor is None:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    vencedor = "Atirador 2 (Atirador 1 se antecipou)"
                    estado_jogo = "FIM"
                elif event.key == pygame.K_l:
                    vencedor = "Atirador 1 (Atirador 2 se antecipou)"
                    estado_jogo = "FIM"

    # --- Lógica ---
    if estado_jogo == "ANDANDO":
        jogador1_rect.x += velocidade
        jogador2_rect.x -= velocidade
        if jogador1_rect.left > 100 and jogador2_rect.right < 700:
            estado_jogo = "SINAL"
            sinal_ativo = True

    # --- Desenho ---
    if estado_jogo == "INICIO":
        tela.blit(fundo_inicio, (0, 0))
        instrucao = fonte_texto.render("Pressione ESPAÇO para começar o duelo!", True, BRANCO)
        tela.blit(instrucao, instrucao.get_rect(center=(largura_tela/2, altura_tela/2 + 50)))

    elif estado_jogo == "EXPLICACAO":
        tela.blit(cowboy_img, (0, 0))
        desenhar_balao(falas[fala_index])

        # Botão aparece só na última fala
        if fala_index == len(falas) - 1:
            desenhar_botao("Começar Duelo", altura_tela - 80)

    else:
        if sinal_ativo:
            tela.fill(VERDE)
        else:
            tela.fill(CINZA_FUNDO)

        tela.blit(jogador1_img, jogador1_rect)
        tela.blit(jogador2_img, jogador2_rect)

        if estado_jogo == "FIM":
            texto = fonte_vencedor.render(f"VENCEDOR: {vencedor}", True, BRANCO)
            tela.blit(texto, texto.get_rect(center=(largura_tela/2, altura_tela/2)))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
