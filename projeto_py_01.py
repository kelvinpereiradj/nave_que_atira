import sys
from time import sleep

import pygame
from pygame.sprite import Sprite, Group



class Configurações():

	def __init__(self):
		self.tela_largura			= 600
		self.tela_altura			= 400
		self.tela_cor				= (221,225,70)		
		self.nave_velocidade 		= 1.5
		self.nave_limite 			= 3		
		self.bala_velocidade 		= 0.1
		self.bala_largura 			= 10
		self.bala_altura 			= 10
		self.bala_cor 				= 10, 100, 230
		self.balas_permitidas 		= 3		
		self.alieni_velocidade 		= 1
		self.frota_velocidade_queda = 3
		self.frota_direção 			= 1
		
		
		
class Nave():

	def __init__( self, configurações, tela):
		self.tela = tela
		self.configurações = configurações		
		self.nave_imagem = pygame.image.load('ima_pro_01/imagem_aa_01.jpg')
		self.rect = self.nave_imagem.get_rect()
		self.tela_rect = tela.get_rect()
		self.rect.centerx = self.tela_rect.centerx
		self.rect.bottom = self.tela_rect.bottom		
		self.center = float(self.rect.centerx) 
		self.nave_movimento_direita = False
		self.nave_movimento_esquerda = False
			
	def update(self):
		if self.nave_movimento_direita and self.rect.right < self.tela_rect.right:
			self.center += self.configurações.nave_velocidade
		if self.nave_movimento_esquerda and self.rect.left > 0:
			self.center -= self.configurações.nave_velocidade		
		self.rect.centerx = self.center
		
	def nave_desenhar(self):
		self.tela.blit( self.nave_imagem, self.rect)
	
	def nave_centro(self):
		self.center = self.tela_rect.centerx



class Bala(Sprite):

	def __init__( self, configurações, tela, nave):
		super().__init__() 
		self.tela = tela
		self.rect = pygame.Rect(
			0, 0, 
			configurações.bala_largura,
			configurações.bala_altura
		)
		self.rect.centerx = nave.rect.centerx
		self.rect.top = nave.rect.top
		self.y = float(self.rect.y)
		self.bala_cor = configurações.bala_cor
		self.bala_velocidade = configurações.bala_velocidade
		
	def update(self):
		self.y -= self.bala_velocidade
		self.rect.y = self.y
	
	def bala_desenhar(self):
		pygame.draw.rect( self.tela, self.bala_cor, self.rect)
	


def bala_atirar( configurações, tela, nave, balas):

	if len(balas) < configurações.balas_permitidas:
		bala_nova = Bala( configurações, tela, nave)
		balas.add(bala_nova)



def balas_atualizar( configurações, tela, nave, alienis, balas):

	balas.update()
	colisões = pygame.sprite.groupcollide( balas, alienis, True, True)
	for bala in balas.copy():
		if bala.rect.bottom <= 0:
			balas.remove(bala)
			


def alieni_bala_colisão_checar( configurações, tela, nave, alienis, balas):

	colisões = pygame.sprite.groupcollide( balas, alienis, True, True)
	if len(alienis) == 0:
		balas.empty()
		alieni_frota_criar( alienis, configurações, nave, tela)



class Alieni(Sprite):

	def __init__( self, configurações, tela):
		super().__init__()
		self.telaa = tela
		self.configurações = configurações		
		self.image = pygame.image.load('ima_pro_01/imagem_aa_02.png')
		self.rect = self.image.get_rect()	
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height		
		self.x = float(self.rect.x)
		
	def alieni_desenhar(self):
		self.telaa.blit( self.image, self.rect)
	
	def bordas_checagem(self):
		tela = self.telaa.get_rect()
		if self.rect.right >= tela.right:
			return True
		elif self.rect.left <= 0:
			return True
		
	def update(self):
		self.x += (
			self.configurações.alieni_velocidade * self.configurações.frota_direção
		)
		self.rect.x = self.x
		
	

def eventos_checagem(
	alienis, balas, 
	botão_iniciar, configurações,
	estatus, nave, tela
):

	for evento in pygame.event.get():

		if evento.type == pygame.QUIT:
			sys.exit()
		elif evento.type == pygame.KEYDOWN:
			evento_tecla_pressionar(
				configurações, tela, 
				nave, balas, evento
			)
		elif evento.type == pygame.KEYUP:
			evento_tecla_soltar( evento, nave)
		elif evento.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			botão_iniciar_checagem(
				alienis, balas, 
				botão_iniciar, configurações,
				estatus,mouse_x, mouse_y,nave,tela
			)



def botão_iniciar_checagem(
	alienis, balas, botão_iniciar, 
	configurações,estatus,mouse_x, mouse_y,nave,tela
):
	
	botão_clicado = botão_iniciar.quadrado.collidepoint( mouse_x, mouse_y)
	
	if botão_clicado and not estatus.jogo_ativar:

		pygame.mouse.set_visible(False)
		estatus.jogo_estatus_reiniciar()
		estatus.jogo_ativar = True		
		alienis.empty()
		balas.empty()		
		alieni_frota_criar( alienis, configurações, nave, tela)
		nave.nave_centro()
	
		

def evento_tecla_pressionar( configurações, tela, nave, balas, evento):

	if evento.key == pygame.K_RIGHT:
		nave.nave_movimento_direita = True
	elif evento.key == pygame.K_LEFT:
		nave.nave_movimento_esquerda = True
	elif evento.key == pygame.K_SPACE:
		bala_atirar( configurações, tela, nave, balas)



def evento_tecla_soltar( evento, nave):

	if evento.key == pygame.K_RIGHT:
		nave.nave_movimento_direita = False
	elif evento.key == pygame.K_LEFT:
		nave.nave_movimento_esquerda = False



def alieni_quantidade_obiter_rs(
	configurações, nave_altura, alieni_altura
):

	alieni_espaço_disponível_vertical = (
		configurações.tela_altura - (3*alieni_altura) - nave_altura
	)
	alieni_quantidade_vertical = int(
		alieni_espaço_disponível_vertical / (2*alieni_altura)
	)
	return alieni_quantidade_vertical



def alieni_quantidade_obiter_horizontal( configurações, alieni_largura):

	alieni_espaço_disponível_horizontal = (
		configurações.tela_largura - 2*alieni_largura
	)
	alieni_quantidade_horizontal = int( 
		alieni_espaço_disponível_horizontal / (2*alieni_largura)
	)
	return alieni_quantidade_horizontal



def alieni_criar(
	configurações, tela, alienis, 
	alieni_contagem_horizontal, alieni_contagem_vertical
):

	alieni = Alieni( configurações, tela)
	alieni_largura = alieni.rect.width
	alieni.x = alieni_largura + 2*alieni_largura*alieni_contagem_horizontal
	alieni.rect.x = alieni.x
	alieni.rect.y = (
		alieni.rect.height + 2*alieni.rect.height*alieni_contagem_vertical
	)
	alienis.add(alieni)



def alieni_frota_criar( alienis, configurações,nave, tela):

	alieni = Alieni( configurações, tela)
	alieni_quantidade_horizontal = alieni_quantidade_obiter_horizontal(
		configurações, alieni.rect.width
	)
	alieni_quantidade_vertical = alieni_quantidade_obiter_rs(
		configurações, nave.rect.height, alieni.rect.height
	)

	for alieni_contagem_vertical in range(alieni_quantidade_vertical):
		for alieni_contagem_horizontal in range( alieni_quantidade_horizontal):
			alieni_criar(
				configurações, tela, alienis, 
				alieni_contagem_horizontal, alieni_contagem_vertical
			)
	

	
def alienis_atualizar( nave, configurações, alienis, tela, estatus, balas):

	frota_bordas_checagem( configurações, alienis)
	alienis.update()

	if pygame.sprite.spritecollideany( nave, alienis):
		nave_atingir( nave, configurações, alienis, tela, estatus, balas)
	alieni_checagem_fundo( nave, configurações, alienis, tela, estatus, balas)



def frota_bordas_checagem( configurações, alienis):

	for alieni in alienis.sprites():
		if alieni.bordas_checagem():
			frota_direção_mudar( configurações, alienis)
			break



def frota_direção_mudar( configurações, alienis):

	for alieni in alienis.sprites():
		alieni.rect.y += configurações.frota_velocidade_queda
	configurações.frota_direção = configurações.frota_direção*(-1)
		


def tela_nova( 
	configurações, tela, 
	nave, alienis, balas, 
	estatus, botão_iniciar
):

	tela.fill(configurações.tela_cor)

	for bala in balas.sprites():
		bala.bala_desenhar()
	nave.nave_desenhar()
	alienis.draw(tela)

	if not estatus.jogo_ativar:
		botão_iniciar.desenhar_botão()
	pygame.display.flip()
	


class Jogo_Estatus():

	def __init__( self, configurações):
		self.configurações = configurações
		self.jogo_estatus_reiniciar()
		self.jogo_ativar = False
		
	def jogo_estatus_reiniciar(self):
		self.nave_esquerda = self.configurações.nave_limite



class Botão():

	def __init__( self, configurações, tela, msg):
		self.tela = tela
		self.tela_quadrado = tela.get_rect()	
		self.largura, self.altura = 50, 20
		self.botão_cor = 0, 255, 0
		self.texto_cor = 255, 255, 255
		self.fonte = pygame.font.SysFont( None, 48)		
		self.quadrado= pygame.Rect( 0, 0, self.largura, self.altura)
		self.quadrado.center = self.tela_quadrado.center	
		self.mensagem(msg)
		
	def mensagem( self, msg):
		self.mensagem_imagem = self.fonte.render(
			msg, True, self.texto_cor, self.botão_cor
		)
		self.mensagem_imagem_quadrado = self.mensagem_imagem.get_rect()
		self.mensagem_imagem_quadrado.center = self.quadrado.center
		
	def desenhar_botão(self):
		self.tela.fill( self.botão_cor, self.quadrado)
		self.tela.blit( self.mensagem_imagem, self.mensagem_imagem_quadrado)



def nave_atingir( nave, configurações, alienis, tela, estatus, balas):

	if estatus.nave_esquerda > 0:
		estatus.nave_esquerda -= 1
		alienis.empty()
		balas.empty()	
		alieni_frota_criar( alienis, configurações, nave, tela)
		nave.nave_centro()	
		sleep(0.5)
	else:
		estatus.jogo_ativar = False
		pygame.mouse.set_visible(True)
	


def alieni_checagem_fundo( 
	nave, configurações, 
	alienis, tela, 
	estatus, balas
):

	tela = tela.get_rect()

	for alieni in alienis.sprites():
		if alieni.rect.bottom >= tela.bottom:
			nave_atingir( 
				nave, configurações, 
				alienis, tela, 
				estatus, balas
			)
			break
		

	
def jogo_carregar():

	pygame.init()
	configurações = Configurações()
	tela = pygame.display.set_mode(
		( configurações.tela_largura, configurações.tela_altura)
	)
	pygame.display.set_caption("Invasão Alien")
	tela.fill(configurações.tela_cor)
	estatus = Jogo_Estatus(configurações)
	nave = Nave( configurações, tela)
	balas = Group()
	alienis = Group()
	alieni_frota_criar( alienis, configurações, nave, tela)
	botão_iniciar = Botão( configurações, tela, "Iniciar")

	while True:

		eventos_checagem(
			alienis, balas, botão_iniciar, 
			configurações, estatus, nave, tela
		)

		if estatus.jogo_ativar:
			nave.update()
			balas_atualizar( 
				configurações, tela, 
				nave, alienis, balas
			)
			alienis_atualizar(
				nave, configurações, 
				alienis, tela, estatus, balas
			)
		tela_nova( 
			configurações, tela, nave, 
			alienis, balas, 
			estatus, botão_iniciar
		)



jogo_carregar()

