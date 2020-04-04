################# PRIMERA PARTE: LO BÁSICO #################
# Importar el módulo para juegos "pygame"
import pygame
# Importar el módilo para números aleatorios "random"
import random
# Importar el módilo para esperar un poco de tiempo "time"
import time
# from pygame.locals import *
from pygame.locals import (
  K_UP, # Flecha arriba
  K_DOWN, # Flecha abajo
  K_LEFT, #  Flecha izquierda
  K_RIGHT, #  Flecha derecha
  K_ESCAPE, # Flecha de escapar
  KEYDOWN, # Detectar tecla presionada
  QUIT, # Cerrar pantalla
  RLEACCEL, # Aceleración de diseños
)


################# SEGUNDA PARTE: LO BÁSICO #################
# Aquí vamos a definir las imágenes, sonidos, super poderes y la pantalla

# Definir las imágenes que vamos a usar
# Todos los sonidos por Alba González, ¡Síguelo en Instagram! @albaglezart
# https://opengameart.org/
DISEÑO_JUGADOR = 'chavito.png'
DISEÑO_VIRUS = 'covid.png'

# Definir los sonidos que vamos a usar
# Ve a mi página de GitHub y baja los sonidos
# Todos los sonidos por Rod D. Neyra, ¡Síguelo en Instagram! @rodd.neyra
SONIDO_ARRIBA = 'arriba.ogg'
SONIDO_ABAJO = 'abajo.ogg'
SONIDO_FINAL = 'tos.ogg'
SONIDO_MUSICA = 'rola.mp3'

# Definir las dimenciones de la pantalla
ANCHO_PANTALLA = 1000
ALTO_PANTALLA = 600

# Super poderes
VELOCIDAD = 10 # Cambia a 11, 12, etc para tener más velocidad
INMUNE = False # Cambia a "True" para que no te mate nada
CURA = False # Cambia a "True" para que no haya enemigos

# Dificultad
FASE1 = 1000
FASE2 = 500
FASE3 = 250
DIFICULTAD = FASE1

################# TERCERA PARTE: LAS CLASES #################
# Crearemos a un jugador usando "pygame.sprite.Sprite"
class Jugador(pygame.sprite.Sprite):
  def __init__(self):
    super(Jugador, self).__init__()
    self.surf = pygame.image.load(DISEÑO_JUGADOR).convert()
    self.surf.set_colorkey((0, 0, 0), RLEACCEL)
    self.rect = self.surf.get_rect()

  # Mover al jugador dependiendo de las teclas presionadas
  def update(self, teclas_presionadas):
    if teclas_presionadas[K_UP]:
      self.rect.move_ip(0, -VELOCIDAD)
      sonido_tecla_arriba.play()
    if teclas_presionadas[K_DOWN]:
      self.rect.move_ip(0, VELOCIDAD)
      sonido_tecla_abajo.play()
    if teclas_presionadas[K_LEFT]:
      self.rect.move_ip(-VELOCIDAD, 0)
    if teclas_presionadas[K_RIGHT]:
      self.rect.move_ip(VELOCIDAD, 0)

    # Mantener al jugador dentro de la pantala
    if self.rect.left < 0:
      self.rect.left = 0
    elif self.rect.right > ANCHO_PANTALLA:
      self.rect.right = ANCHO_PANTALLA
    if self.rect.top <= 0:
      self.rect.top = 0
    elif self.rect.bottom >= ALTO_PANTALLA:
      self.rect.bottom = ALTO_PANTALLA

# Crearemos un virus (enemigo) usando "pygame.sprite.Sprite"
class Virus(pygame.sprite.Sprite):
  def __init__(self):
    super(Virus, self).__init__()
    self.surf = pygame.image.load(DISEÑO_VIRUS).convert()
    self.surf.set_colorkey((0, 0, 0), RLEACCEL)
    # Definimos la posición usando el paquete random (random.randint)
    self.rect = self.surf.get_rect(center=(
      random.randint(ANCHO_PANTALLA + 20, ANCHO_PANTALLA + 100),
      random.randint(0, ALTO_PANTALLA),
      )
    )
    # Definimos la velocidad usando el paquete random (random.randint)
    self.speed = random.randint(5, 20)

  # Creamos una clase para el movimiento del virus
  def update(self):
    self.rect.move_ip(-self.speed, 0)
    # Si el virus sale de la pantalla, el enemigo se destruye
    if self.rect.right < 0:
      self.kill()


################# CUARTA PARTE: INICIAR LOS RECURSOS DEL JUEGO ##############
# Iniciar pantalla
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
# Iniciar los sonidos
pygame.mixer.init()
# Iniciar pygame
pygame.init()
# Iniciar el reloj interno del juego
clock = pygame.time.Clock()
# Crear un 'jugador'
jugador = Jugador()
# Crear nuevo enemigo usando "pygame.USEREVENT"
NUEVO_ENEMIGO = pygame.USEREVENT + 1
pygame.time.set_timer(NUEVO_ENEMIGO, DIFICULTAD)
# Creamos grupos de objetos en el juego: El jugador y los enemigos
virus = pygame.sprite.Group()
grupo_diseños = pygame.sprite.Group()
grupo_diseños.add(jugador) # El primer objeto añadido es el jugador
# Iniciar la música (puedes cambiar los sonidos en la PRIMERA PARTE)
pygame.mixer.music.load(SONIDO_MUSICA)
pygame.mixer.music.play(loops=-1)
# Cargar todos los archivos de sonido
sonido_tecla_arriba = pygame.mixer.Sound(SONIDO_ARRIBA)
sonido_tecla_abajo = pygame.mixer.Sound(SONIDO_ABAJO)
sonido_final = pygame.mixer.Sound(SONIDO_FINAL)
# Configurar el volúmen de los sonidos
sonido_tecla_arriba.set_volume(0.5)
sonido_tecla_abajo.set_volume(0.5)
sonido_final.set_volume(0.5)

################# QUINTA PARTE: INICIAR EL JUEGO ##############
# Variable para que el juego siga corriendo (mientras el valor sea "True")
correr_juego = True

# Iniciar el juego
while correr_juego:
  for event in pygame.event.get():  # Mirar cada evento

    if event.type == KEYDOWN: # Detectar teclas presionadas
      if event.key == K_ESCAPE: # Terminar si el jugador presiona "escape"
        correr_juego = False

    elif event.type == QUIT: # Terminar si el jugador cierra la ventana
      correr_juego = False

    # Agregar un nuevo virus cada X tiempo dependiendo de la dificultad
    elif event.type == NUEVO_ENEMIGO:
      if CURA:
        continue
      else:
        nuevo_virus = Virus()
        virus.add(nuevo_virus)
        grupo_diseños.add(nuevo_virus)


  ################# SEXTA PARTE: ACTUALIZAR EL JUEGO #################
  teclas_presionadas = pygame.key.get_pressed() # Detectar teclas presionadas
  jugador.update(teclas_presionadas) # Actualizar la posición del jugador
  virus.update() # Actualizar la posición de los virus (enemigos)

  # Elegir el color de la pantalla, puedes visitar: https://htmlcolorcodes.com/
  pantalla.fill((0, 0, 0))

  # Pasar los diseños a la pantalla
  for diseño in grupo_diseños:
    pantalla.blit(diseño.surf, diseño.rect)

  # Detectar si algún virus chocó contra el jugador
  if pygame.sprite.spritecollideany(jugador, virus):
    if INMUNE:
      continue
    else:
      jugador.kill() # Desaparecer al jugador
      sonido_tecla_arriba.stop() # Terminar el sonido de movimiento
      sonido_tecla_abajo.stop() # Terminar el sonido de movimiento
      sonido_final.play() # Hacer sonar la tos
      time.sleep(.7)
      correr_juego = False # Terminar el juego

  # Pasar todo a la pantalla (display)
  pygame.display.flip()

  # Mantener el juego a 30 cuadros por segundo
  clock.tick(30)

# Terminar la música y el sonido
pygame.mixer.music.stop()
pygame.mixer.quit()
