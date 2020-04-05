################# PRIMERA PARTE: LO BÁSICO #################
# Importar el módulo para juegos "pygame"
import pygame
# Importar el módulo para números aleatorios "random"
import random
# Importar el módulo para esperar un poco de tiempo "time"
import time
# Importar las teclas
from pygame.locals import (
  K_UP, # Flecha arriba
  K_DOWN, # Flecha abajo
  K_LEFT, #  Flecha izquierda
  K_RIGHT, #  Flecha derecha
  K_ESCAPE, # Tecla "escape"
  KEYDOWN, # Detectar tecla presionada
  QUIT, # Cerrar pantalla
  RLEACCEL, # Render de diseños
)


################# SEGUNDA PARTE: DEFINICIONES #################
# Aquí vamos a definir las imágenes, los sonidos y la pantalla.
# Recuerda que todos los sonidos, música y diseños deben de estar en la misma
# carpeta que este programa y asegúrate de que tengan los mismos nombres.
# Busca los materiales en https://github.com/damian-romero/cuarentena_2020

# Definir las imágenes que vamos a usar.
# Todos los diseños por Alba González, ¡Síguela en Instagram! @albaglezart
# Licencia: https://creativecommons.org/licenses/by-nc-nd/4.0/deed.es_ES
DISEÑO_JUGADOR = 'chavito.png'
DISEÑO_VIRUS = 'covid.png'

# Definir los sonidos que vamos a usar.
# Todos sonidos y música por Rod D. Neyra, ¡Síguelo en Instagram! @rodd.neyra
# Licencia: https://creativecommons.org/licenses/by-nc-nd/4.0/deed.es_ES
SONIDO_ARRIBA = 'arriba.ogg'
SONIDO_ABAJO = 'abajo.ogg'
SONIDO_FINAL = 'tos.ogg'
SONIDO_MÚSICA = 'rola.mp3'

# Definir las dimenciones de la pantalla.
ANCHO_PANTALLA = 1000
ALTO_PANTALLA = 600

# Super poderes (Mira mi tercer video para aprender a programar esta parte.)
# Usaremos una variable para cambiar rápidamente la velocidad del jugador.
# --> Ve a las líneas # 69, 72, 75 y 77 y cambia los números por la variable.

# Dificultad (Mira mi tercer video para aprender a programar esta parte).
# Con una variable cambiaremos la velocidad con la que aparecen los  virus.
# --> Ve a la línea # 123 y cambia el número 250 por la variable


################# TERCERA PARTE: LAS CLASES #################
# En esta parte crearemos "clases" Jugador y Virus que nos van a ayudar.
# a crear varios objetos para el juego.

# Creamos la clase "Jugador" usando "pygame.sprite.Sprite".
class Jugador(pygame.sprite.Sprite):
  def __init__(self):
    super(Jugador, self).__init__()
    self.surf = pygame.image.load(DISEÑO_JUGADOR).convert()
    self.surf.set_colorkey((0, 0, 0), RLEACCEL)
    self.rect = self.surf.get_rect()

  # Creamos una función para mover al jugador usando las teclas presionadas.
  def update(self, teclas_presionadas):
    if teclas_presionadas[K_UP]:
      self.rect.move_ip(0, -10)
      sonido_tecla_arriba.play()
    if teclas_presionadas[K_DOWN]:
      self.rect.move_ip(0, 10)
      sonido_tecla_abajo.play()
    if teclas_presionadas[K_LEFT]:
      self.rect.move_ip(-10, 0)
    if teclas_presionadas[K_RIGHT]:
      self.rect.move_ip(10, 0)

    # Mantener al jugador dentro de la pantalla.
    if self.rect.left < 0:
      self.rect.left = 0
    elif self.rect.right > ANCHO_PANTALLA:
      self.rect.right = ANCHO_PANTALLA
    if self.rect.top <= 0:
      self.rect.top = 0
    elif self.rect.bottom >= ALTO_PANTALLA:
      self.rect.bottom = ALTO_PANTALLA

# Creamos la clase "Virus" (para los enemigos) usando "pygame.sprite.Sprite".
class Virus(pygame.sprite.Sprite):
  def __init__(self):
    super(Virus, self).__init__()
    self.surf = pygame.image.load(DISEÑO_VIRUS).convert()
    self.surf.set_colorkey((0, 0, 0), RLEACCEL)
    # Definimos la posición usando el paquete random (random.randint).
    self.rect = self.surf.get_rect(center=(
      random.randint(ANCHO_PANTALLA + 20, ANCHO_PANTALLA + 100),
      random.randint(0, ALTO_PANTALLA),
      )
    )
    # Definimos la velocidad usando el paquete random (random.randint).
    self.speed = random.randint(5, 20)

  # Creamos una función para el movimiento del virus.
  def update(self):
    self.rect.move_ip(-self.speed, 0)
    # Si el virus sale de la pantalla, el enemigo se destruye.
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
reloj = pygame.time.Clock()
# Crear un 'jugador'
jugador = Jugador()
# Crear nuevo enemigo usando "pygame.USEREVENT"
NUEVO_ENEMIGO = pygame.USEREVENT + 1
pygame.time.set_timer(NUEVO_ENEMIGO, 250)
# Creamos grupos de objetos en el juego: El jugador y los enemigos
virus = pygame.sprite.Group()
grupo_diseños = pygame.sprite.Group()
grupo_diseños.add(jugador) # El primer objeto añadido es el jugador
# Iniciar la música (puedes cambiar los sonidos en la PRIMERA PARTE)
pygame.mixer.music.load(SONIDO_MÚSICA)
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
      nuevo_virus = Virus()
      virus.add(nuevo_virus)
      grupo_diseños.add(nuevo_virus)


  ################# SEXTA PARTE: ACTUALIZAR EL JUEGO #################
  teclas_presionadas = pygame.key.get_pressed() # Detectar teclas presionadas
  jugador.update(teclas_presionadas) # Actualizar la posición del jugador
  virus.update() # Actualizar la posición de los virus (enemigos)

  # Elegir el color de la pantalla (el esquema se llama RGB)
  # Si quieres elegir otros colores, visita: https://htmlcolorcodes.com/
  pantalla.fill((0, 0, 0)) # Cambia esta línea para elegir colores

  # Pasar los diseños a la pantalla
  for diseño in grupo_diseños:
    pantalla.blit(diseño.surf, diseño.rect)

  # Detectar si algún virus chocó contra el jugador
  if pygame.sprite.spritecollideany(jugador, virus):
    jugador.kill() # Desaparecer al jugador
    sonido_tecla_arriba.stop() # Terminar el sonido de movimiento
    sonido_tecla_abajo.stop() # Terminar el sonido de movimiento
    sonido_final.play() # Hacer sonar la tos
    time.sleep(.7) # Esperar .7 segundos para que termine la tos
    correr_juego = False # Terminar el juego

  # Pasar todo a la pantalla (display)
  pygame.display.flip()

  # Mantener el juego a 30 cuadros por segundo
  reloj.tick(60)

# Terminar la música y el sonido
pygame.mixer.music.stop()
pygame.mixer.quit()
