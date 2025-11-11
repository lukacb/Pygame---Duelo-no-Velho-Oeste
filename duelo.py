import pygame
import random

pygame.init()
pygame.font.init()

pygame.mixer.init()  # inicializa o mixer de áudio

pygame.mixer.music.load("faroeste.mp3")  # nome do teu arquivo de música
pygame.mixer.music.play(-1)  # -1 faz a música tocar em loop
pygame.mixer.music.set_volume(0.5)  # volume de 0.0 a 1.0


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
fonte_titulo = pygame.font.Font("PressStart2P-Regular.ttf", 20)
fonte_texto = pygame.font.Font("PressStart2P-Regular.ttf", 14)
fonte_vencedor = pygame.font.Font("PressStart2P-Regular.ttf", 15)

# --- Imagens ---
fundo_inicio = pygame.image.load("fundooestenovo.png").convert()
fundo_inicio = pygame.transform.scale(fundo_inicio, (largura_tela, altura_tela))

cowboy_img = pygame.image.load("cowboysorrindo.png").convert_alpha()
cowboy_img = pygame.transform.scale(cowboy_img, (largura_tela, altura_tela))

# --- IMAGENS DOS PERSONAGENS ---
LARGURA_COWBOY = 80
ALTURA_COWBOY = 150

cowboybase_original = pygame.image.load("Cowboydelado.png").convert_alpha()
cowboybase = pygame.transform.scale(cowboybase_original, (LARGURA_COWBOY, ALTURA_COWBOY))

walk_right_frames = [pygame.transform.scale(pygame.image.load("Cowboydelado.png").convert_alpha(), (LARGURA_COWBOY, ALTURA_COWBOY))]
walk_left_frames = [pygame.transform.flip(walk_right_frames[0], True, False)]

back_frames = [pygame.transform.scale(pygame.image.load("cowboydecostas.png").convert_alpha(), (LARGURA_COWBOY, ALTURA_COWBOY))]

aim_right_frames = [pygame.transform.scale(pygame.image.load("Cowboydefrente.png").convert_alpha(), (LARGURA_COWBOY, ALTURA_COWBOY))]
aim_left_frames = [pygame.transform.flip(aim_right_frames[0], True, False)]

# --- Função de carregamento ---
def carrega_frames(padrao, qtd):
    frames = []
    for i in range(qtd):
        img = pygame.image.load(padrao.format(i)).convert_alpha()
        frames.append(pygame.transform.scale(img, (LARGURA_COWBOY, ALTURA_COWBOY)))
    return frames

try:
    walk_right_frames = carrega_frames("Cowboydelado{:02d}.png", 6)
except:
    walk_right_frames = [cowboybase]
walk_left_frames = [pygame.transform.flip(f, True, False) for f in walk_right_frames]

try:
    back_frames = carrega_frames("cowboydecostas{:02d}.png", 4)
except:
    back_frames = [cowboybase]

try:
    aim_right_frames = carrega_frames("Cowboydelado{:02d}.png", 3)
except:
    aim_right_frames = [cowboybase]
aim_left_frames = [pygame.transform.flip(f, True, False) for f in aim_right_frames]

# --- Controle de animação ---
p1_action = "back_left"
p2_action = "back_right"
p1_frame = 0
p2_frame = 0
anim_fps = 10
anim_timer_ms = 0

def frame_seq(acao):
    if acao == "walk_left":
        return walk_left_frames
    if acao == "walk_right":
        return walk_right_frames
    if acao == "aim_left":
        return aim_left_frames
    if acao == "aim_right":
        return aim_right_frames
    return back_frames

# --- Retângulos dos jogadores ---
jogador1_img = back_frames[0]
jogador2_img = back_frames[0]
jogador1_rect = jogador1_img.get_rect()
jogador2_rect = jogador2_img.get_rect()

pos_y_chao = 450
pos_x_jogador1 = 350
pos_x_jogador2 = 400
jogador1_rect.topleft = (pos_x_jogador1, pos_y_chao)
jogador2_rect.topleft = (pos_x_jogador2, pos_y_chao)

velocidade = 1
direcao_jogador1 = -1
direcao_jogador2 = 1

limite_esquerda = 10
limite_direita = largura_tela - LARGURA_COWBOY - 10

mirando_duracao_ms = 1200
mirando_inicio_ms = 0

# --- Estados do jogo ---
estado_jogo = "INICIO"
fala_index = 0
vencedor = None
sinal_ativo = False
tempo_sinal = random.uniform(2.0, 5.0)
tempo_inicio_espera = 0

clock = pygame.time.Clock()
rodando = True

# --- Falas do Cowboy ---
falas = [
    "Olá, forasteiro!",
    "Bem-vindo ao Velho Oeste, terra dos duelos!",
    "Aqui vão as instruções para jogar",
    "Atirador 1: aperte a tecla A para atirar.",
    "Atirador 2: aperte a tecla L para atirar.",
    "Mas cuidado para não se antecipar!",
    "Espere o sinal verde para vencer o duelo!"
]

# --- Controle de morte ---
jogador1_vivo = True
jogador2_vivo = True
velocidade_queda = 6

# --- Balas ---
balas = []
velocidade_bala = 300

def disparar(origem_rect, direcao):
    """Cria uma bala a partir do jogador."""
    x = origem_rect.centerx + (40 * direcao)
    y = origem_rect.centery - 40
    balas.append([x, y, direcao])

# --- Funções auxiliares ---
def desenhar_botao(texto, pos_y):
    botao_rect = pygame.Rect(largura_tela/2 - 100, pos_y, 200, 50)
    pygame.draw.rect(tela, PRETO, botao_rect)
    pygame.draw.rect(tela, BRANCO, botao_rect, 2)
    txt = fonte_texto.render(texto, True, BRANCO)
    tela.blit(txt, txt.get_rect(center=botao_rect.center))
    return botao_rect

def desenhar_balao(fala):
    balao_rect = pygame.Rect(largura_tela - 350, 40, 320, 160)
    pygame.draw.rect(tela, BRANCO, balao_rect, border_radius=15)
    pygame.draw.rect(tela, PRETO, balao_rect, 3, border_radius=15)
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
    y = balao_rect.y + 20
    for linha in linhas:
        texto = fonte_texto.render(linha.strip(), True, PRETO)
        tela.blit(texto, (balao_rect.x + 15, y))
        y += 35

def desenhar_barra_reacao(ativo):
    barra = pygame.Rect(largura_tela//2 - 150, 20, 300, 20)
    pygame.draw.rect(tela, CINZA_FUNDO, barra, border_radius=10)
    if ativo:
        pygame.draw.rect(tela, VERDE, barra, border_radius=10)
    pygame.draw.rect(tela, BRANCO, barra, 2, border_radius=10)
    rotulo = "ATIRE!" if ativo else "Espere..."
    txt = fonte_texto.render(rotulo, True, BRANCO)
    tela.blit(txt, (barra.centerx - txt.get_width()//2, barra.y - 28))

def desenhar_placar():
    txt = fonte_texto.render(f"Rodada {rodada}/3 P1 {pontos_p1} - {pontos_p2} P2", True, BRANCO)
    tela.blit(txt, (20, 20))

# --- Loop Principal ---
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        if estado_jogo == "INICIO":
            pontos_p1 = 0
            pontos_p2 = 0
            rodada = 1
            MAX_PONTOS = 2
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
                    disparar(jogador1_rect, 1)
                    vencedor = "Atirador 1"
                    jogador2_vivo = False
                    pontos_p1 += 1
                    estado_jogo = "FIM"
                elif event.key == pygame.K_l:
                    disparar(jogador2_rect, -1)
                    vencedor = "Atirador 2"
                    jogador1_vivo = False
                    pontos_p2 += 1
                    estado_jogo = "FIM"

        elif estado_jogo in ("ANDANDO", "ESPERANDO", "MIRANDO") and vencedor is None:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    vencedor = "Atirador 2 (Atirador 1 se antecipou)"
                    jogador1_vivo = False
                    pontos_p2 += 1
                    estado_jogo = "FIM"
                elif event.key == pygame.K_l:
                    vencedor = "Atirador 1 (Atirador 2 se antecipou)"
                    jogador2_vivo = False
                    pontos_p1 += 1
                    estado_jogo = "FIM"

        elif estado_jogo == "FIM":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                jogador1_vivo = True
                jogador2_vivo = True
                if pontos_p1 >= MAX_PONTOS or pontos_p2 >= MAX_PONTOS:
                    pontos_p1 = pontos_p2 = 0
                    rodada = 1
                    vencedor = None
                    sinal_ativo = False
                    jogador1_rect.topleft = (pos_x_jogador1, pos_y_chao)
                    jogador2_rect.topleft = (pos_x_jogador2, pos_y_chao)
                    tempo_sinal = random.uniform(2.0, 5.0)
                    estado_jogo = "INICIO"
                else:
                    rodada += 1
                    vencedor = None
                    sinal_ativo = False
                    jogador1_rect.topleft = (pos_x_jogador1, pos_y_chao)
                    jogador2_rect.topleft = (pos_x_jogador2, pos_y_chao)
                    tempo_sinal = random.uniform(2.0, 5.0)
                    estado_jogo = "ANDANDO"

    # --- Lógica do jogo ---
    if estado_jogo == "ANDANDO":
        if jogador1_rect.x > limite_esquerda:
            jogador1_rect.x += direcao_jogador1 * velocidade
        else:
            jogador1_rect.x = limite_esquerda
        if jogador2_rect.x < limite_direita:
            jogador2_rect.x += direcao_jogador2 * velocidade
        else:
            jogador2_rect.x = limite_direita
        if jogador1_rect.x <= limite_esquerda and jogador2_rect.x >= limite_direita:
            jogador1_rect.x = limite_esquerda
            jogador2_rect.x = limite_direita
            p1_action, p2_action = "aim_right", "aim_left"
            estado_jogo = "MIRANDO"
            mirando_inicio_ms = pygame.time.get_ticks()

    elif estado_jogo == "MIRANDO":
        if pygame.time.get_ticks() - mirando_inicio_ms >= mirando_duracao_ms:
            estado_jogo = "ESPERANDO"
            tempo_inicio_espera = pygame.time.get_ticks()

    elif estado_jogo == "ESPERANDO":
        tempo_agora = pygame.time.get_ticks()
        tempo_passados_ms = tempo_agora - tempo_inicio_espera
        tempo_sinal_ms = tempo_sinal * 1000
        if tempo_passados_ms > tempo_sinal_ms:
            estado_jogo = "SINAL"
            sinal_ativo = True

    # --- Atualização das balas ---
    for bala in balas:
        bala[0] += bala[2] * velocidade_bala
    balas = [b for b in balas if 0 < b[0] < largura_tela]

    # --- Seleção das ações ---
    if estado_jogo in ("INICIO", "EXPLICACAO"):
        p1_action, p2_action = "back_left", "back_right"
    elif estado_jogo == "ANDANDO":
        p1_action, p2_action = "walk_left", "walk_right"
    elif estado_jogo in ("MIRANDO", "ESPERANDO", "SINAL"):
        p1_action, p2_action = "aim_right", "aim_left"

    # --- Animação ---
    anim_timer_ms += clock.get_time()
    if anim_timer_ms >= int(1000 / anim_fps):
        anim_timer_ms = 0
        p1_frame = (p1_frame + 1) % len(frame_seq(p1_action))
        p2_frame = (p2_frame + 1) % len(frame_seq(p2_action))

    jogador1_img = frame_seq(p1_action)[p1_frame]
    jogador2_img = frame_seq(p2_action)[p2_frame]

    # --- Desenho ---
    if estado_jogo == "INICIO":
        tela.blit(fundo_inicio, (0, 0))
        instrucao = fonte_texto.render("Pressione ESPAÇO para começar o duelo!", True, BRANCO)
        tela.blit(instrucao, instrucao.get_rect(center=(largura_tela/2, altura_tela/2 + 50)))

    elif estado_jogo == "EXPLICACAO":
        tela.blit(cowboy_img, (0, 0))
        desenhar_balao(falas[fala_index])
        if fala_index == len(falas) - 1:
            desenhar_botao("Começar Duelo", altura_tela - 80)

    else:
        tela.blit(fundo_inicio, (0, 0))
        desenhar_barra_reacao(sinal_ativo)
        desenhar_placar()

        # Morte animada
        if not jogador1_vivo:
            jogador1_rect.y += velocidade_queda
            jogador1_img = pygame.transform.rotate(jogador1_img, 90)
        if not jogador2_vivo:
            jogador2_rect.y += velocidade_queda
            jogador2_img = pygame.transform.rotate(jogador2_img, -90)

        if jogador1_vivo:
            tela.blit(jogador1_img, jogador1_rect)
        if jogador2_vivo:
            tela.blit(jogador2_img, jogador2_rect)

        # Desenhar balas
        for bala in balas:
            AMARELO = (255, 255, 0)

            pygame.draw.circle(tela, AMARELO, (int(bala[0]), int(bala[1])), 5)

    if estado_jogo == "FIM":
        if pontos_p1 >= MAX_PONTOS or pontos_p2 >= MAX_PONTOS:
            campeao = "Atirador 1" if pontos_p1 > pontos_p2 else "Atirador 2"
            texto = fonte_vencedor.render(f"CAMPEÃO: {campeao} (melhor de 3)", True, BRANCO)
            sub = fonte_texto.render("Pressione ESPAÇO para reiniciar", True, BRANCO)
        else:
            texto = fonte_vencedor.render(f"Vencedor da rodada: {vencedor}", True, BRANCO)
            sub = fonte_texto.render("Pressione ESPAÇO para a próxima rodada", True, BRANCO)
        tela.blit(texto, texto.get_rect(center=(largura_tela/2, altura_tela/2 - 20)))
        tela.blit(sub, sub.get_rect(center=(largura_tela/2, altura_tela/2 + 25)))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
