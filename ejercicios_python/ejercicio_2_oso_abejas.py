"""
UNJu - Facultad de Ingeniería
Teoría de Sistemas Operativos (TSO) - Ciclo Lectivo 2026
Cátedra: Ing. María Fernanda Vázquez - JTP: Ing. Fabio D. Argañaraz

Ejercicio Práctico N° 2: El Problema del Oso y las Abejas
Bibliografía de Referencia:
- Silberschatz: Cap. 6.6 (Problemas clásicos de sincronización)
- Stallings: Cap. 5.4 (Sincronización con semáforos)
"""

import sys
import threading
import time
import random

# Configuración UTF-8 para consola Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

M = 10                  # Capacidad del tarro de miel
NUM_ABEJAS = 5          # Número de abejas obreras
tarro_miel = 0          # Variable compartida
simulacion_activa = True

# TODO PARA EL ESTUDIANTE:
# 1. Define los mecanismos de sincronización necesarios:
# - Un cerrojo (Lock) o semáforo binario para exclusión mutua en el tarro.
# - Un semáforo para despertar al oso cuando el tarro esté lleno.
# - Un semáforo para que las abejas esperen si el tarro está lleno o el oso está comiendo.
mutex = threading.Lock()
sem_oso = threading.Semaphore(0)
sem_tarro_disponible = threading.Semaphore(1)

def abeja(id_abeja):
    global tarro_miel, simulacion_activa
    while simulacion_activa:
        time.sleep(random.uniform(0.05, 0.2))
        
        # TODO: Sincronizar el acceso al tarro de miel:
        # 1. Esperar a que el tarro esté disponible.
        # 2. Entrar en exclusión mutua con el tarro.
        # 3. Depositar una porción de miel (tarro_miel += 1).
        # 4. Si tarro_miel == M, avisar/despertar al oso dormido.
        # 5. Si no está lleno, permitir que otras abejas sigan produciendo.
        sem_tarro_disponible.acquire()

        if not simulacion_activa:
            sem_tarro_disponible.release()
            break

        with mutex:
            tarro_miel += 1
            print(f"🐝 Abeja {id_abeja} depositó miel. Tarro: {tarro_miel}/{M}")
            if tarro_miel == M:
                print("🐻 El tarro está lleno! Despertando al oso...")
                sem_oso.release()
            else:
                sem_tarro_disponible.release()

        pass

def oso(max_tarros=2):
    global tarro_miel, simulacion_activa
    tarros_comidos = 0
    while tarros_comidos < max_tarros:
        # TODO: Esperar pasivamente (bloqueado) hasta que el tarro alcance M porciones
        # print("🐻 El oso se despierta y se come toda la miel!")
        # tarro_miel = 0
        # print("🐻 El oso vuelve a dormir.")
        # TODO: Avisar a las abejas que el tarro está vacío y disponible nuevamente.
        sem_oso.acquire()
        print("🐻 El oso se despierta y se come toda la miel!")
        tarro_miel = 0
        tarros_comidos += 1
        time.sleep(0.1)
        print("🐻 El oso vuelve a dormir.")

        sem_tarro_disponible.release()  # Permitir que las abejas llenen el tarro nuevamente
        
    simulacion_activa = False
    sem_tarro_disponible.release()  # Desbloquear a las abejas que puedan estar esperando

if __name__ == "__main__":
    print("=" * 60)
    print(" Iniciando Simulación: El Oso y las Abejas (UNJu FI)")
    print("=" * 60)
    # TODO: Crear e iniciar los hilos para el oso y las N abejas

    hilo_oso = threading.Thread(target=oso, args=(2,))
    hilo_oso.start()

    hilos_abejas = []
    for i in range(NUM_ABEJAS):
        hilo_abeja = threading.Thread(target=abeja, args=(i+1,))
        hilos_abejas.append(hilo_abeja)
        hilo_abeja.start()

    hilo_oso.join()

    for hilo in hilos_abejas:
        hilo.join()

    print(" Simulación finalizada.")
    pass

