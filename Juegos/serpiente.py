#Dependencias
import pygame
import random

pygame.init()#Inicio de la pestaña

ANCHO = 1024
ALTO = 724
TAM = 20

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("SERPIENTE")#Título de pestaña
reloj = pygame.time.Clock()
modo = 1 #Individual(1) o multijugador(2)

#Selección de modo(para comprobar)
sel = True
while sel:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                sel = False
            elif event.key == pygame.K_2:
                modo = 2
                sel = False
        
#Partida
def partida(modo):
    #Preparación de partida  
    marcha = True
    serpientes = []
    direcciones = []
    manzanas = []
    COLOR1 = (40, 40, 50)#Color azul oscuro de la serpiente1
    COLOR2 = (180, 200, 220)#Color celeste de la serpiente2
    if modo == 1:
        #Posición y dirección inicial de la serpiente del jugador1
        x1 = (ANCHO // 4) // TAM * TAM
        y1 = (ALTO // 2) // TAM * TAM
        serpientes.append([(x1, y1), (x1 +20, y1)])#Añadimos a serpientes la lista de tuplas que simulará la posición inicial de los trozos de la serpiente1
        direcciones.append((20, 0))

        #Posición inicial de la manzana para el jugador1
        x1m = (ANCHO // 4) // TAM * TAM
        y1m = (ALTO // 3) // TAM * TAM
        manzanas.append((x1m, y1m))
    elif modo == 2:
        #Posición inicial de la serpiente1 y 2
        x1 = (ANCHO // 4) // TAM * TAM
        y1 = (ALTO // 2) // TAM * TAM
        serpientes.append([(x1, y1), (x1 +20, y1)])#Añadimos a serpientes la lista de tuplas que simulará la posición inicial de los trozos de la serpiente1
        x2 = (3 * ANCHO // 4) // TAM * TAM
        y2 = (ALTO // 2) // TAM * TAM
        serpientes.append([(x2, y2), (x2 +20, y2)])#Añadimos a serpientes la lista de tuplas que simulará la posición inicial de los trozos de la serpiente2
        direcciones.append((20, 0))#Dirección de serpiente1 añadiendose a las direcciones
        direcciones.append((-20, 0))#Dirección de la serpiente2 añadiendose a las direcciones
        dx2, dy2 = direcciones[1]#Direcciones eje "x" e "y"de la serpiente2

        #Posición inicial de la manzana para el jugador 1 y 2
        x1m = (ANCHO // 4) // TAM * TAM
        y1m = (ALTO // 3) // TAM * TAM 
        manzanas.append((x1m, y1m))
        x2m = (3 * ANCHO // 4) // TAM * TAM
        y2m = (ALTO // 3) // TAM * TAM 
        manzanas.append((x2m, y2m))
    
    dx1, dy1 = direcciones[0]#Direcciones eje "x" e "y" de la serpiente1

    #Bucle para sacar una posición desocupada a la manzana
    def gen_manz(salto, x_min, x_max, y_min, y_max, serpientes, manzanas):
        while True:
            xm = random.randrange(x_min, x_max, salto)
            ym = random.randrange(y_min, y_max, salto)
            nueva_manz = (xm, ym)
            ocupado = False
            for serpiente in serpientes:
                if nueva_manz in serpiente:
                    ocupado = True
                    break
            if nueva_manz not in manzanas and not ocupado:
                return nueva_manz
                
    #Acciones de la partida
    while marcha:
        reloj.tick(12)#FPS
        
        pantalla.fill((40, 40, 50))#Color de pantalla

        #Si el modo és individual se pintará el fondo de otro color y se comprobará tanto en el eje "x" e "y" de la cabeza de la serpiente si ha llegado a algún borde de la pantalla, de ser así se terminará la marcha de la partida.
        if modo == 1:
            pantalla.fill((180, 200, 220))
            for i, serpiente in enumerate(serpientes):
               for ind, eje in enumerate(serpiente[0]):
                    if ind == 0:
                        if eje <= 24 or eje >= ANCHO - 32:
                            marcha = False
                    elif ind == 1:
                        if eje <=24 or eje >= ALTO - 52:
                            marcha = False
        
        #Si el modo és multijugador se dibujará una línea en medio de la pantalla (la cual se tratará como una pared que dividirá las serpientes) y se comprobará la detección de bordes de cada serpiente de la misma manera que se explicó para el modo individual
        elif modo == 2:
            pygame.draw.rect(pantalla, (180, 200, 220), (0, 0, ANCHO // 2, ALTO))
            pygame.draw.rect(pantalla, (120, 120, 130), ((ANCHO //2)-10, 0, 20,ALTO))
            for i, serpiente in enumerate(serpientes):
                if i == 0:
                    for ind, eje in enumerate(serpiente[0]):
                        if ind == 0:
                            if eje <= 24 or eje >= (ANCHO//2) - 60:
                                marcha = False
                        elif ind == 1:
                            if eje <=24 or eje >= ALTO - 52:
                                marcha = False
                if i == 1:
                    for ind, eje in enumerate(serpiente[0]):
                        if ind == 0:
                            if eje <= ANCHO//2 + 40 or eje >=  ANCHO - 32:
                                marcha = False
                        elif ind == 1:
                            if eje <=24 or eje >= ALTO - 52:
                                marcha = False
            

        for event in pygame.event.get():
            if event.type == pygame.QUIT:#Si se clica cerrar la pestaña
                marcha = False
            if event.type == pygame.KEYDOWN:
                if modo == 1:
                    #MOVIMIENTOS DE LA SERPIENTE1 (AWSD)
                    if event.key == pygame.K_w and dy1 == 0:
                        direcciones[0] = (0, -20)
                    if event.key == pygame.K_s and dy1 == 0:
                        direcciones[0] = (0, 20) 
                    if event.key == pygame.K_d and dx1 == 0:
                        direcciones[0] = (20, 0)
                    if event.key == pygame.K_a and dx1 == 0:
                        direcciones[0] = (-20, 0)
                if modo == 2:
                    #MOVIMIENTOS DE LA SERPIENTE1 (AWSD)
                    if event.key == pygame.K_w and dy1 == 0:
                        direcciones[0] = (0, -20)
                    if event.key == pygame.K_s and dy1 == 0:
                        direcciones[0] = (0, 20) 
                    if event.key == pygame.K_d and dx1 == 0:
                        direcciones[0] = (20, 0)
                    if event.key == pygame.K_a and dx1 == 0:
                        direcciones[0] = (-20, 0)
                    #MOVIMIENTOS DE LA SERPIENTE2 (Flechas)
                    if event.key == pygame.K_UP and dy2 == 0:
                        direcciones[1] = (0, -20)
                    if event.key == pygame.K_DOWN and dy2 == 0:
                        direcciones[1] = (0, 20) 
                    if event.key == pygame.K_RIGHT and dx2 == 0:
                        direcciones[1] = (TAM, 0)
                    if event.key == pygame.K_LEFT and dx2 == 0:
                        direcciones[1] = (-TAM, 0)
                    dx2, dy2 = direcciones[1]#Direcciones eje "x" e "y"de la serpiente2
                dx1, dy1 = direcciones[0] #Dirección de la serpiente1

    
        for i, serpiente in enumerate(serpientes):#Bucle para separar las serpientes
            if i == 0:#Condicional para que si és la primera serpiente se dibujen los trozos con un color o si és otra pues con el otro.
                color = COLOR1

                #Creamos la nueva cabeza de la serpiente y la añadimos a la lista de trozos de serpiente como nuevo trozo (tupla)
                cax1, cay1 = serpiente[0]
                paso_cabeza1 = (cax1 + dx1, cay1 + dy1)
                serpiente.insert(0, paso_cabeza1)

                #Spawn aleatorio de la manzana1 dependiendo del modo
                if paso_cabeza1 == manzanas[0] and modo == 1:
                    manzanas[0] = gen_manz(TAM, 40, ANCHO-32, 40, ALTO-40, serpientes, manzanas)                   
                elif paso_cabeza1 == manzanas[0] and modo == 2:
                    manzanas[0] = gen_manz(TAM, 40, (ANCHO // 2) // TAM * TAM, 40, ALTO - 40, serpientes, manzanas)
                else:
                    serpiente.pop()
            else:
                color = COLOR2

                #Creamos la nueva cabeza de la serpiente y la añadimos a la lista de trozos de serpiente como nuevo trozo (tupla)
                cax2, cay2 = serpiente[0]
                paso_cabeza2 = (cax2 + dx2, cay2 + dy2)
                serpiente.insert(0, paso_cabeza2)

                #Spawn aleatorio de la manzana2
                if paso_cabeza2 == manzanas[1]:
                    manzanas[1] = gen_manz(TAM, ((ANCHO // 2) // TAM * TAM) + 40, ANCHO - 40, 40, ALTO - 40, serpientes, manzanas)
                else:
                    serpiente.pop()#Eliminamos el último trozo de la serpiente
            for trozo in serpiente:#Bucle para que cada trozo(tupla) dentro de la serpiente dibuje un cuadrado de 20x20 pixeles en las coordenadas, color y pantalla específicadas
                pygame.draw.rect(pantalla, color, (trozo[0], trozo[1], 20, 20))
        #Dibujar manzanas
        for manzana in manzanas:
                pygame.draw.rect(pantalla, (255, 0, 0), (manzana[0], manzana[1], 20, 20))
        pygame.display.flip()#Actualizar
    
    paus = pygame.Surface((ANCHO, ALTO))#Crear lienzo del tamaño de la pantalla
    paus.set_alpha(150)#Volver el lienzo semitransparente
    paus.fill((0, 0, 0))#Hacer que el lienzo semitransparente sea negro
    pantalla.blit(paus, (0, 0))#colocar el lienzo sobre la pantalla
    
    #Creación del estilo de letra y tamaño que tendrán los botones de Game Over (Reintentar, Salir)
    fuente = pygame.font.Font(None, 60)

    #Pantalla de Game Over
    perdido = True
    while perdido:
        for event in pygame.event.get():

            #Si se pulsa la "x" de la pestaña se cierra el bucle
            if event.type == pygame.QUIT:
                perdido = False
            
            #Cuando se presione el mouse si está encima de reintentar se reinicia la partida y se cierra este bucle pero si está en salir se sale de la partida
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if bt_reintentar.collidepoint(mouse_pos):
                    partida(modo)
                    return
                if bt_salir.collidepoint(mouse_pos):
                    return
        
        #Creación de los rectangulos que simularán los botones
        bt_reintentar = pygame.draw.rect(pantalla, COLOR2, ((ANCHO // 2) - 300, (ALTO // 2) - 40, 600, 100))
        bt_salir = pygame.draw.rect(pantalla, COLOR1, ((ANCHO // 2) - 300, (ALTO // 2) + 120, 600, 100))
        
        #Creamos lógicamente el texto, haciendo que tenga bordes suaves y un color
        text_rein = fuente.render("Reintentar", True, COLOR1)
        text_salir = fuente.render("Salir", True, COLOR2)
        
        #Hacemos un rectangulo invisible con las medidas del texto para que se centre en su botón indicado
        rect_rein = text_rein.get_rect(center=bt_reintentar.center)
        rect_salir = text_salir.get_rect(center=bt_salir.center)

        #Enganchamos el texto en la posición de su rectangulo invisible
        pantalla.blit(text_rein, rect_rein)
        pantalla.blit(text_salir, rect_salir)

        pygame.display.flip()#Actualizar
                

    


partida(modo)#Llamar la partida

pygame.quit()#Fin de la pestaña
