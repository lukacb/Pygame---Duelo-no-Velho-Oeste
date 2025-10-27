import pygame
import random

pygame.init()

largura_tela = 800
altura_tela = 600

tela = pygame.display.set_mode((largura_tela, altura_tela)) #superficie principal onde tudo será desenhado
pygame.display.set_caption("Duelo no Velho-Oeste")

rodando = True
while rodando:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    cor_fundo = (0, 0, 0)
    tela.fill(cor_fundo)
    pygame.display.flip()

pygame.quit()

