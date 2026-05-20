#Dependencias
import pygame
import random
import asyncio
from platform import window


pygame.init()#Inicio de la pestaña


ANCHO = 1020
ALTO = 720
TAM = 20
MID = ANCHO // 2
puntuacion = 0

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("SERPIENTE")#Título de pestaña
reloj = pygame.time.Clock()
fuente = pygame.font.Font(None, 60)
modo = 1 #Individual(1) o multijugador(2)


async def main(modo):

    #OBTENER MODO DESDE URL (PYGBAG)
    url = window.location.search

    if "modo=2" in url:
        modo = 2
    else:
        modo = 1


    #Partida
    async def partida(modo):
        #Preparación de partida
        global puntuacion  
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
            serpientes.append([(x1, y1), (x1 +20, y1)])
            direcciones.append((20, 0))

            #Posición inicial de la manzana para el jugador1
            x1m = (ANCHO // 4) // TAM * TAM
            y1m = (ALTO // 3) // TAM * TAM
            manzanas.append((x1m, y1m))

        elif modo == 2:
            #Posición inicial de la serpiente1 y 2
            x1 = (ANCHO // 4) // TAM * TAM
            y1 = (ALTO // 2) // TAM * TAM
            serpientes.append([(x1, y1), (x1 +20, y1)])

            x2 = (3 * ANCHO // 4) // TAM * TAM
            y2 = (ALTO // 2) // TAM * TAM
            serpientes.append([(x2, y2), (x2 +20, y2)])

            direcciones.append((20, 0))
            direcciones.append((-20, 0))

            dx2, dy2 = direcciones[1]

            #Posición inicial de la manzana para el jugador 1 y 2
            x1m = (ANCHO // 4) // TAM * TAM
            y1m = (ALTO // 3) // TAM * TAM
            manzanas.append((x1m, y1m))

            x2m = (3 * ANCHO // 4) // TAM * TAM
            y2m = (ALTO // 3) // TAM * TAM
            manzanas.append((x2m, y2m))
   
        dx1, dy1 = direcciones[0]


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
            reloj.tick(12)

            pantalla.fill((40, 40, 50))

            if modo == 1:
                pantalla.fill((180, 200, 220))


            elif modo == 2: 
                pygame.draw.rect(pantalla, (180, 200, 220), (0, 0, ANCHO // 2, ALTO))
                pygame.draw.rect(pantalla, (120, 120, 130), ((ANCHO //2)-10, 0, 20,ALTO))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    marcha = False

                if event.type == pygame.KEYDOWN:
                    if modo == 1:
                        if event.key == pygame.K_w and dy1 == 0:
                            direcciones[0] = (0, -20)
                        if event.key == pygame.K_s and dy1 == 0:
                            direcciones[0] = (0, 20)
                        if event.key == pygame.K_d and dx1 == 0:
                            direcciones[0] = (20, 0)
                        if event.key == pygame.K_a and dx1 == 0:
                            direcciones[0] = (-20, 0)

                    if modo == 2:
                        if event.key == pygame.K_w and dy1 == 0:
                            direcciones[0] = (0, -20)
                        if event.key == pygame.K_s and dy1 == 0:
                            direcciones[0] = (0, 20)
                        if event.key == pygame.K_d and dx1 == 0:
                            direcciones[0] = (20, 0)
                        if event.key == pygame.K_a and dx1 == 0:
                            direcciones[0] = (-20, 0)

                        if event.key == pygame.K_UP and dy2 == 0:
                            direcciones[1] = (0, -20)
                        if event.key == pygame.K_DOWN and dy2 == 0:
                            direcciones[1] = (0, 20)
                        if event.key == pygame.K_RIGHT and dx2 == 0:
                            direcciones[1] = (TAM, 0)
                        if event.key == pygame.K_LEFT and dx2 == 0:
                            direcciones[1] = (-TAM, 0)

                        dx2, dy2 = direcciones[1]

                    dx1, dy1 = direcciones[0]


            for i, serpiente in enumerate(serpientes):
                if i == 0:
                    color = COLOR1
                    cax1, cay1 = serpiente[0]
                    paso_cabeza1 = (cax1 + dx1, cay1 + dy1)
                    for trozo in serpiente:
                        if trozo == serpiente[0]:
                            cabeza_siguiente = pygame.Rect(paso_cabeza1[0], paso_cabeza1[1], 20, 20)
                    if modo == 1:
                        if cabeza_siguiente.left < 0 or cabeza_siguiente.right > ANCHO  or cabeza_siguiente.top < 0 or cabeza_siguiente.bottom > ALTO:
                            marcha = False
                        else:
                            serpiente.insert(0, paso_cabeza1)
                
                            if paso_cabeza1 == manzanas[0]:
                                manzanas[0] = gen_manz(TAM, 40, ANCHO-32, 40, ALTO-40, serpientes, manzanas)
                                puntuacion += 1
                            else:
                                serpiente.pop()
                    elif cabeza_siguiente.left < 0 or cabeza_siguiente.right > MID  or cabeza_siguiente.top < 0 or cabeza_siguiente.bottom > ALTO:
                        marcha = False
                    else:
                        serpiente.insert(0, paso_cabeza1)
                        if paso_cabeza1 == manzanas[0] and modo == 2:
                            manzanas[0] = gen_manz(TAM, 40, (ANCHO // 2) // TAM * TAM, 40, ALTO - 40, serpientes, manzanas)
                            puntuacion += 1
                        else:
                            serpiente.pop()

                else:
                    color = COLOR2
                    cax2, cay2 = serpiente[0]
                    paso_cabeza2 = (cax2 + dx2, cay2 + dy2)
                    for trozo in serpiente:
                        if trozo == serpiente[0]:
                            cabeza_siguiente = pygame.Rect(paso_cabeza2[0], paso_cabeza2[1], 20, 20)
                    if cabeza_siguiente.left < MID or cabeza_siguiente.right > ANCHO  or cabeza_siguiente.top < 0 or cabeza_siguiente.bottom > ALTO:
                            marcha = False
                    else:
                        serpiente.insert(0, paso_cabeza2)

                        if paso_cabeza2 == manzanas[1]:
                            manzanas[1] = gen_manz(TAM, ((ANCHO // 2) // TAM * TAM) + 40, ANCHO - 40, 40, ALTO - 40, serpientes, manzanas)
                            puntuacion += 1
                        else:
                            serpiente.pop()
                    
                
                
                if serpiente[0] in serpiente[1:]:
                    marcha= False
                for trozo in serpiente:
                    pygame.draw.rect(pantalla, color, (trozo[0], trozo[1], 20, 20))
            for manzana in manzanas:
                pygame.draw.rect(pantalla, (255, 0, 0), (manzana[0], manzana[1], 20, 20))
            
            text_puntuacion = fuente.render(f"Puntuación: {puntuacion}", True, (150, 150, 150))
            pantalla.blit(text_puntuacion, (7, 7))

            pygame.display.flip()
            await asyncio.sleep(0)
     
        paus = pygame.Surface((ANCHO, ALTO))
        paus.set_alpha(150)
        paus.fill((0, 0, 0))
        pantalla.blit(paus, (0, 0))
       

        perdido = True
        while perdido:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    return False
               
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if bt_reintentar.collidepoint(mouse_pos):
                        puntuacion = 0
                        return True
                    if bt_salir.collidepoint(mouse_pos):
                        window.location.href = "../../../../web/frontend/menu.html"
                        return False
            
            bt_reintentar = pygame.draw.rect(pantalla, COLOR2, ((ANCHO // 2) - 300, (ALTO // 2) - 40, 600, 100))
            bt_salir = pygame.draw.rect(pantalla, COLOR1, ((ANCHO // 2) - 300, (ALTO // 2) + 120, 600, 100))

            text_rein = fuente.render("Reintentar", True, COLOR1)
            text_salir = fuente.render("Guardar y salir", True, COLOR2)
            text_fin = fuente.render(f"FIN DE PARTIDA", True, (255, 255, 255))
            text_finpuntos = fuente.render(f"Puntuación final: {puntuacion}", True, (255, 255, 255))

            rect_rein = text_rein.get_rect(center=bt_reintentar.center)
            rect_salir = text_salir.get_rect(center=bt_salir.center)

            pantalla.blit(text_rein, rect_rein)
            pantalla.blit(text_salir, rect_salir)
            pantalla.blit(text_fin, ((ANCHO//2)-180, (ALTO//2)-220))
            pantalla.blit(text_finpuntos, ((ANCHO//2)-200, (ALTO//2)-160))
            pygame.display.flip()
            await asyncio.sleep(0)


    while True:
        repetir = await partida(modo)
        if not repetir:
            break

    pygame.quit()


asyncio.run(main(1))