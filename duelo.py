import pygame
import random

pygame.init()

largura_tela = 800
altura_tela = 600

tela = pygame.display.set_mode((largura_tela, altura_tela)) #Superficie principal onde tudo será desenhado
pygame.display.set_caption("Duelo no Velho-Oeste")

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
CINZA_FUNDO = (100, 100, 100)
VERDE = (0,255,0)

jogador1_rect = pygame.Rect(350, 250, 50, 100) 
jogador2_rect = pygame.Rect(400, 250, 50, 100)
velocidade = 1
estado_jogo = "ANDANDO"
vencedor = None 
tempo_sinal = random.uniform(3.0,5.0)
print(f"Tempo sorteado: {tempo_sinal} segundos")

tempo_inicio_espera = 0
sinal_ativo = False 

clock = pygame.time.Clock() #Devo controlar a velocidade dos frames

rodando = True
while rodando:
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            rodando = False
    
        if event.type == pygame.KEYDOWN:
            if estado_jogo == "SINAL" and vencedor is None:
                if event.key == pygame.K_a: # Tecla 'a'
                    print("JOGADOR 1 VENCEU!")
                    vencedor = "Jogador 1"
                    estado_jogo = "FIM"
                if event.key == pygame.K_l: # Tecla 'l'
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
    
    if estado_jogo == "ANDANDO":
        jogador1_rect.x = jogador1_rect.x - velocidade
        jogador2_rect.x = jogador2_rect.x + velocidade
        if jogador1_rect.left < 100 or jogador2_rect.right > 700:
            print("Parados! Esperando o sinal...")
            estado_jogo = "ESPERANDO"
            tempo_inicio_espera = pygame.time.get_ticks()
    elif estado_jogo == "ESPERANDO":
        tempo_agora = pygame.time.get_ticks()
        tempo_passados_ms = tempo_agora - tempo_inicio_espera
        tempo_sinal_ms = tempo_sinal * 1000
        if tempo_passados_ms > tempo_sinal_ms:
            print("SINAL VERDE!")
            estado_jogo = "SINAL"
            sinal_ativo = True
    
    if sinal_ativo == True:
        tela.fill(VERDE)
    else:
        tela.fill(CINZA_FUNDO)

    pygame.draw.rect(tela, BRANCO, jogador1_rect)
    pygame.draw.rect(tela, BRANCO, jogador2_rect)
    pygame.display.flip() #Atualiza a tela

    clock.tick(60)


pygame.quit()

