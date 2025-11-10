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

# cowboy_img é a imagem grande do início (mantenha ela assim)
cowboy_img = pygame.image.load("cowboysorrindo.png").convert_alpha()
cowboy_img = pygame.transform.scale(cowboy_img, (largura_tela, altura_tela)) 

# --- AQUI VAI A MUDANÇA ---
# 1. Carrega a imagem base
cowboybase_original = pygame.image.load("cowboy1.png").convert_alpha()

# 2. REDIMENSIONA a imagem base para um tamanho menor e visível
LARGURA_COWBOY = 80  # Experimente este valor!
ALTURA_COWBOY = 150 # Experimente este valor!
cowboybase = pygame.transform.scale(cowboybase_original, (LARGURA_COWBOY, ALTURA_COWBOY))

# --- Animações (carregamento seguro, com fallback) ---
def carrega_frames(padrao, qtd):
    frames = []
    for i in range(qtd):
        img = pygame.image.load(padrao.format(i)).convert_alpha()
        frames.append(pygame.transform.scale(img, (LARGURA_COWBOY, ALTURA_COWBOY)))
    return frames

# Tente carregar sprites; se não existirem, usa a base como fallback (sem animação)
try:
    walk_right_frames = carrega_frames("sprites/cowboy_walk_right_{:02d}.png", 6)
except:
    walk_right_frames = [cowboybase]

walk_left_frames  = [pygame.transform.flip(f, True, False) for f in walk_right_frames]

try:
    back_frames = carrega_frames("sprites/cowboy_back_{:02d}.png", 4)
except:
    back_frames = [cowboybase]  # fallback simples

try:
    aim_right_frames = carrega_frames("sprites/cowboy_aim_right_{:02d}.png", 3)
except:
    aim_right_frames = [cowboybase]

aim_left_frames = [pygame.transform.flip(f, True, False) for f in aim_right_frames]

# Controle de animação
p1_action = "back_left"   # INÍCIO: de costas, cada um voltado para fora
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
    # "back_*"
    return back_frames


# Agora, define as imagens dos jogadores (elas já estão redimensionadas)
jogador1_img = cowboybase
jogador2_img = pygame.transform.flip(cowboybase, True, False)

# --- Retângulos dos jogadores ---
# 1. Pega o retângulo (com o tamanho certo) da imagem
jogador1_rect = jogador1_img.get_rect() 
jogador2_rect = jogador2_img.get_rect()

# 2. Define as posições X e Y iniciais
pos_y_chao = 450 
pos_x_jogador1 = 350
pos_x_jogador2 = 400

# 3. Posiciona os retângulos no lugar certo
jogador1_rect.topleft = (pos_x_jogador1, pos_y_chao)
jogador2_rect.topleft = (pos_x_jogador2, pos_y_chao)

# (O 'velocidade = 1' continua igual)
velocidade = 1

direcao_jogador1 = -1   # começa indo para a esquerda
direcao_jogador2 = 1    # começa indo para a direita

limite_esquerda = 10
limite_direita  = largura_tela - LARGURA_COWBOY - 10

mirando_duracao_ms = 1200
mirando_inicio_ms = 0


# --- Estados do jogo ---
estado_jogo = "INICIO"  # INICIO -> EXPLICACAO -> ANDANDO -> SINAL -> FIM
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
    
    # --- 1. PROCESSAMENTO DE EVENTOS ---
    # (Esta seção cuida de todos os inputs)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        # --- Controles de fluxo (baseado em estado) ---
        if estado_jogo == "INICIO":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                estado_jogo = "EXPLICACAO"

        elif estado_jogo == "EXPLICACAO":
            # Avança a fala com ESPAÇO ou clique
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or event.type == pygame.MOUSEBUTTONDOWN:
                if fala_index < len(falas) - 1:
                    fala_index += 1
                else:
                    estado_jogo = "ANDANDO" # Fim das falas, começa o jogo

        # Lógica de Tiro 1: Atirar na hora certa
        elif estado_jogo == "SINAL" and vencedor is None:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    vencedor = "Atirador 1"
                    estado_jogo = "FIM"
                elif event.key == pygame.K_l:
                    vencedor = "Atirador 2"
                    estado_jogo = "FIM"

        # Lógica de Tiro 2: Atirar antes da hora
        elif estado_jogo in ("ANDANDO", "ESPERANDO","MIRANDO") and vencedor is None:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    vencedor = "Atirador 2 (Atirador 1 se antecipou)"
                    estado_jogo = "FIM"
                elif event.key == pygame.K_l:
                    vencedor = "Atirador 1 (Atirador 2 se antecipou)"
                    estado_jogo = "FIM"

    # --- 2. LÓGICA DO JOGO ---
    # (Esta seção atualiza o estado do jogo automaticamente)
    # (Esta é a parte que foi corrigida)
    
    if estado_jogo == "ANDANDO":
        if jogador1_rect.x > limite_esquerda:
            jogador1_rect.x += direcao_jogador1 * velocidade
        else:
            jogador1_rect.x = limite_esquerda  # trava na borda

        if jogador2_rect.x < limite_direita:
            jogador2_rect.x += direcao_jogador2 * velocidade
        else:
            jogador2_rect.x = limite_direita   # trava na borda
        if jogador1_rect.x <= limite_esquerda and jogador2_rect.x >= limite_direita:
            jogador1_rect.x = limite_esquerda
            jogador2_rect.x = limite_direita
            p1_action, p2_action = "aim_right", "aim_left"
            estado_jogo = "MIRANDO"
            mirando_inicio_ms = pygame.time.get_ticks()
    # quando ambos estiverem nas bordas, viram e passam a mirar um ao outro
        if jogador1_rect.x == limite_esquerda and jogador2_rect.x == limite_direita:
        # esquerda olha para a direita; direita olha para a esquerda
            jogador1_img = cowboybase
            jogador2_img = pygame.transform.flip(cowboybase, True, False)
            estado_jogo = "MIRANDO"
            mirando_inicio_ms = pygame.time.get_ticks()
    
    elif estado_jogo == "MIRANDO":
        if pygame.time.get_ticks() - mirando_inicio_ms >= mirando_duracao_ms:
            estado_jogo = "ESPERANDO"
            tempo_inicio_espera = pygame.time.get_ticks()
    
    elif estado_jogo == "ESPERANDO":
        # 3. Se estiver esperando, checa o timer
        tempo_agora = pygame.time.get_ticks()
        tempo_passados_ms = tempo_agora - tempo_inicio_espera
        tempo_sinal_ms = tempo_sinal * 1000 
        
        # 4. CHECA SE O TEMPO ACABOU (DENTRO do "ESPERANDO")
        if tempo_passados_ms > tempo_sinal_ms:
            estado_jogo = "SINAL" 
            sinal_ativo = True
    
    if estado_jogo in ("INICIO", "EXPLICACAO"):
        p1_action, p2_action = "back_left", "back_right"
    elif estado_jogo == "ANDANDO":
        p1_action, p2_action = "walk_left", "walk_right"
    elif estado_jogo in ("MIRANDO", "ESPERANDO", "SINAL"):
        p1_action, p2_action = "aim_right", "aim_left"

    # --- Avança frames de animação com base no tempo ---
    anim_timer_ms += clock.get_time()
    if anim_timer_ms >= int(1000 / anim_fps):
        anim_timer_ms = 0
        p1_frame = (p1_frame + 1) % len(frame_seq(p1_action))
        p2_frame = (p2_frame + 1) % len(frame_seq(p2_action))

    # Atualiza as imagens atuais dos jogadores para o frame correspondente
    jogador1_img = frame_seq(p1_action)[p1_frame]
    jogador2_img = frame_seq(p2_action)[p2_frame]
    
    # --- 3. DESENHO ---
    # (Esta seção desenha tudo na tela, baseado no estado)
    
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

    else: # Cuida de ANDANDO, ESPERANDO, SINAL, FIM
        
        # 1. Desenha o fundo (Verde ou o normal)
        if sinal_ativo:
            tela.fill(VERDE)
        else:
            tela.blit(fundo_inicio, (0, 0)) # Fundo do jogo

        # 2. Desenha os jogadores (CÓDIGO CORRIGIDO)
        tela.blit(jogador1_img, jogador1_rect) # <-- DESCOMENTADO
        tela.blit(jogador2_img, jogador2_rect) # <-- DESCOMENTADO
        
        # E adicione estas linhas:
        COR_TESTE = (255, 0, 0) # Vermelho brilhante
        pygame.draw.rect(tela, COR_TESTE, jogador1_rect)
        pygame.draw.rect(tela, COR_TESTE, jogador2_rect)
        # --- FIM DO TESTE ---

        if estado_jogo == "FIM":
            texto = fonte_vencedor.render(f"VENCEDEDOR: {vencedor}", True, BRANCO)
            tela.blit(texto, texto.get_rect(center=(largura_tela/2, altura_tela/2)))

    # --- 4. ATUALIZAÇÃO FINAL ---
    pygame.display.flip()
    clock.tick(60)

# --- Fim do Jogo ---
pygame.quit()