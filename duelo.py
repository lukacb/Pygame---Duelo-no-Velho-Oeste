# --- 1. Importação das Bibliotecas ---
import pygame
import random

# --- 2. Inicialização do Pygame ---
pygame.init()
pygame.font.init()

# --- 3. Configurações da Tela ---
largura_tela = 800
altura_tela = 600

tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Duelo no Velho-Oeste")

# --- 4. Constantes de Cor (R, G, B) ---
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)

# --- 5. Variáveis Principais do Jogo ---
jogador1_rect = pygame.Rect(350, 480, 50, 100)
jogador2_rect = pygame.Rect(400, 480, 50, 100)
velocidade = 1
estado_jogo = "INICIO"
vencedor = None

fonte_vencedor = pygame.font.Font(None, 45)
fonte_inicio = pygame.font.Font(None, 36)  # menor agora

sinal_ativo = False
tempo_inicio_espera = 0

# --- 6. Imagens ---
fundo_img_original = pygame.image.load("fundooestenovo.png").convert()
fundo_img = pygame.transform.scale(fundo_img_original, (largura_tela, altura_tela))

cowboybase = pygame.image.load("cowboy1.png").convert_alpha()
jogador1_img = cowboybase
jogador2_img = pygame.transform.flip(cowboybase, True, False)

# --- 7. Relógio ---
clock = pygame.time.Clock()

# --- 8. Loop Principal ---
rodando = True
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        # --- Tela inicial ---
        if estado_jogo == "INICIO":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                estado_jogo = "ANDANDO"
                print("Jogo iniciado! Os cowboys estão andando...")

        # --- Durante o jogo ---
        elif event.type == pygame.KEYDOWN:
            if estado_jogo == "SINAL" and vencedor is None:
                if event.key == pygame.K_a:
                    print("JOGADOR 1 VENCEU!")
                    vencedor = "Jogador 1"
                    estado_jogo = "FIM"
                if event.key == pygame.K_l:
                    print("JOGADOR 2 VENCEU!")
                    vencedor = "Jogador 2"
                    estado_jogo = "FIM"

            elif estado_jogo == "ESPERANDO":
                if event.key == pygame.K_a:
                    print("JOGADOR 1 SE ANTECIPOU! JOGADOR 2 VENCEU!")
                    vencedor = "Jogador 2 (J1 se antecipou)"
                    estado_jogo = "FIM"
                if event.key == pygame.K_l:
                    print("JOGADOR 2 SE ANTECIPOU! JOGADOR 1 VENCEU!")
                    vencedor = "Jogador 1 (J2 se antecipou)"
                    estado_jogo = "FIM"

    # --- Atualização da lógica ---
    if estado_jogo == "ANDANDO":
        jogador1_rect.x += velocidade
        jogador2_rect.x -= velocidade
        # Quando ambos chegam na posição correta, o sinal aparece imediatamente
        if jogador1_rect.left > 100 and jogador2_rect.right < 700:
            print("SINAL VERDE! Duelo começou!")
            estado_jogo = "SINAL"
            sinal_ativo = True

    # --- Desenho na tela ---
    if estado_jogo == "INICIO":
        tela.blit(fundo_img, (0, 0))
        texto_inicio = fonte_inicio.render("Pressione ESPAÇO para começar o duelo", True, BRANCO)
        texto_rect = texto_inicio.get_rect(center=(largura_tela / 2, altura_tela / 2 + 180))
        tela.blit(texto_inicio, texto_rect)

    else:
        if sinal_ativo:
            tela.fill(VERDE)
        else:
            tela.blit(fundo_img, (0, 0))

        tela.blit(jogador1_img, jogador1_rect)
        tela.blit(jogador2_img, jogador2_rect)

        if estado_jogo == "FIM":
            texto_surface = fonte_vencedor.render(f"VENCEDOR: {vencedor}", True, BRANCO)
            texto_rect = texto_surface.get_rect(center=(largura_tela / 2, altura_tela / 2))
            tela.blit(texto_surface, texto_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()


