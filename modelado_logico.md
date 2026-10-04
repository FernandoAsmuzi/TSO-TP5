# 🧩 Problemas de Modelado Lógico: Sincronización y Concurrencia
## Cátedra de Teoría de Sistemas Operativos — UNJu FI 2026

Resuelve los siguientes problemas utilizando pseudocódigo con **Semáforos** (`wait()` y `signal()`) o **Monitores** (variables de condición). Para cada problema:
- Identifica claramente las variables compartidas.
- Especifica el tipo de cada semáforo (binario o contador) y su **valor de inicialización**.
- Escribe el pseudocódigo estructurado de cada hebra o proceso concurrente.

---

## 📌 Mapeo Teórico-Práctico: Del Pseudocódigo a Python (`threading`)

Antes de comenzar a programar en `ejercicios_python/`, utiliza esta guía rápida de equivalencias:

| Concepto Teórico | Notación Lógica / Pseudocódigo | Implementación en Python (`import threading`) |
| :--- | :--- | :--- |
| **Semáforo Binario (Mutex)** | `S = Semáforo(1)` | `S = threading.Semaphore(1)` o `lock = threading.Lock()` |
| **Semáforo de Evento (Señal)** | `S = Semáforo(0)` | `S = threading.Semaphore(0)` |
| **Semáforo Contador (Recursos)** | `S = Semáforo(N)` | `S = threading.Semaphore(N)` |
| **Operación $P$ / Esperar** | `wait(S)` | `S.acquire()` |
| **Operación $V$ / Señalizar** | `signal(S)` | `S.release()` |
| **Crear Monitor / Lock de Estado** | `Monitor M { ... }` | `class MiMonitor: def __init__(self): self.lock = threading.Lock()` |
| **Variable de Condición** | `cond = Condicion()` | `cond = threading.Condition(self.lock)` |
| **Esperar en Condición** | `cond.wait()` | `with self.lock: while not condicion: cond.wait()` |
| **Despertar a un proceso** | `cond.signal()` | `with self.lock: cond.notify()` |
| **Despertar a todos (Broadcast)** | `cond.broadcast()` | `with self.lock: cond.notify_all()` |
| **Crear y lanzar hilo** | `iniciar_hebra(f, args)` | `t = threading.Thread(target=f, args=(...)); t.start()` |
| **Esperar finalización de hilo** | `esperar_hebra(t)` | `t.join()` |

---

## Problema 1: Sincronización de Secuencias Estrictas y Alternadas

Encontrar la secuencia lógica y los valores iniciales de los semáforos que permitan forzar de manera determinista las siguientes trazas de ejecución en un sistema multiproceso:

1. **Secuencia con Prioridad Fija (`ABCABC`):**
   - Un emisor ($A$) y dos receptores ($B$ y $C$) que retiran la misma información en momentos distintos ($B$ tiene prioridad sobre $C$). Secuencia esperada: $A \rightarrow B \rightarrow C \rightarrow A \rightarrow B \rightarrow C...$
2. **Secuencia Alternada (`ABACABAC`):**
   - Un emisor ($A$) y dos receptores ($B$ y $C$) que retiran información en forma alternada (comienza $B$). Secuencia esperada: $A \rightarrow B \rightarrow A \rightarrow C \rightarrow A \rightarrow B \rightarrow A \rightarrow C...$
3. **Secuencia con No-Determinismo Regulado (`(A o B) C (A o B) C`):**
   - Dos emisores ($A$ y $B$) y un receptor ($C$). Los emisores compiten al azar, pero el receptor siempre debe intercalarse entre cada emisión: $(A \lor B) \rightarrow C \rightarrow (A \lor B) \rightarrow C...$

**Tu tarea:**
1. En cada caso, define la cantidad de semáforos necesarios y su inicialización.
2. Escribe el pseudocódigo de cada proceso involucrado con sus llamadas a `wait()` y `signal()`.

1. Secuencia con Prioridad Fija

      sem_A = Semaforo(1): Semaforo binario para iniciar.
      sem_B = Semaforo(0): Semaforo binario. Bloquea a B hasta que A termine.
      sem_C = Semaforo(0): Semaforo binario. Bloquea a C hasta que B termine.

   Proceso A():
      repetir:
         wait(sem_A)
         // Codigo A
         emitir_A()
         signal(sem_B)

   Proceso B():
      repetir:
         wait(sem_B)
         // Codigo B
         emitir_B()
         signal(sem_C)

   Proceso C():
      repetir:
         wait(sem_C)
         // Codigo C
         emitir_C()
         signal(sem_A)

2. Secuencia Alternada

      sem_A = Semáforo(1): Semáforo binario. Permite la ejecución de A.
      sem_B = Semáforo(0): Semáforo binario. Habilita el turno de B.
      sem_C = Semáforo(0): Semáforo binario. Habilita el turno de C.
      turno_B = true: Variable booleana.

   Proceso A():
      repetir:
         wait(sem_A)
         // SC A
         emitir_A()
         si turno_B == true entonces:
               signal(sem_B)
               turno_B = false
         sino:
               signal(sem_C)
               turno_B = true

   Proceso B():
      repetir:
         wait(sem_B)
         // SC B
         emitir_B()
         signal(sem_A)

   Proceso C():
      repetir:
         wait(sem_C)
         // SC C
         emitir_C()
         signal(sem_A)

3. Secuencia con No-Determinismo Regulado

      sem_emisor = Semáforo(1): Semáforo binario. Emisores que permiten la ejecucion.
      sem_receptor = Semáforo(0): Semáforo binario. Espera al emisor.
   
   Proceso A():
      repetir:
         wait(sem_emisor)
         // SC A
         emitir_A()
         signal(sem_receptor)

   Proceso B():
      repetir:
         wait(sem_emisor)
         // SC B
         emitir_B()
         signal(sem_receptor)

   Proceso C():
      repetir:
         wait(sem_receptor)
         // SC C
         emitir_C()
         signal(sem_emisor)

---

## Problema 2: El Comedor Escolar (Recursos Heterogéneos)

En un colegio hay un comedor con capacidad para 18 personas. El estudiante, cuando desea comer, entra en el comedor y coge una bandeja con comida de cualquiera de los dos mostradores disponibles; a continuación, selecciona agua o coca cola. Si escoge coca cola, dispone de 3 abridores para abrir la botella; si escoge agua no necesita abridor. Después de la comida puede seleccionar un postre de 2 mostradores disponibles para ello, siempre y cuando desee postre. Cuando termina el postre, o si ha optado por no tomarlo, sale del comedor.

**Tu tarea:**
1. Identifica los semáforos necesarios y su valor de inicialización.
2. Escribe el pseudocódigo del proceso `Estudiante()`.

   capacidad_comedor = Semáforo(18): Semáforo contador. Controla el límite de ocupación total del salón.

   mostradores_comida = Semáforo(2): Semáforo contador. Controla el acceso a los 2 puestos de entrega de bandejas de comida.

   abridores = Semáforo(3): Semáforo contador. Controla el uso de los 3 abridores disponibles.

   mostradores_postre = Semáforo(2): Semáforo contador. Controla el acceso a los 2 puestos de distribución de postre.

   Proceso Estudiante():
      // Ingreso al comedor
      wait(capacidad_comedor)

      // Elegir comida
      wait(mostradores_comida)
      // Elegir mostrador
      signal(mostradores_comida)

      // Selección de bebida
      bebida = elegir_bebida() // 'coca_cola' o 'agua'
      si bebida == 'coca_cola' entonces:
         wait(abridores)
         // Abrir botella de gaseosa
         signal(abridores)
      
      // Ingerir la comida

      // Postre opcional
      quiere_postre = decidir_postre() // bool
      si quiere_postre == true entonces:
         wait(mostradores_postre)
         // Elegir plato de postre
         signal(mostradores_postre)
         // Comer postre...

      // Salida del comedor
      signal(capacidad_comedor)
---

## Problema 3: El Puente Levadizo (Monitores y Prioridad)

Tenemos un puente levadizo sobre un río con las siguientes condiciones de utilización:
- Los barcos tienen siempre prioridad de paso, pero para levantar el puente han de esperar a que no haya ningún coche sobre él.
- Los coches pueden utilizar el puente si no hay ningún barco pasando (en cuyo caso el puente estará levantado) o esperando.

**Tu tarea:**
1. Diseña la solución utilizando **Monitores** (variables de condición).
2. Escribe el pseudocódigo para los métodos `entrar_coche()`, `salir_coche()`, `entrar_barco()`, `salir_barco()`.

      coches_puente = 0: Número de coches circulando sobre el puente.

      barcos_puente = 0: Vale 1 si hay un barco cruzando (puente levantado), 0 si no.

      barcos_esperando = 0: Barcos en cola que requieren pasar, prioridad sobre los coches.

      cola_coches: Donde se suspenden los coches cuando hay barcos pasando o esperando cruzar.

      cola_barcos: Donde se suspenden los barcos mientras haya coches sobre el puente o un barco previo esté pasando.

   Monitor PuenteLevadizo:
      variables:
         coches_puente: entero = 0
         barcos_puente: entero = 0
         barcos_esperando: entero = 0
         cola_coches: Condicion
         cola_barcos: Condicion

      // --- MÉTODOS PARA COCHES ---

      entrar_coche():
         // Un coche solo entra si no hay barcos pasando NI esperando cruzar
         mientras barcos_puente > 0 o barcos_esperando > 0 hacer:
               cola_coches.wait()
         coches_puente = coches_puente + 1

      salir_coche():
         coches_puente = coches_puente - 1
         // Si no quedan coches y hay barcos esperando, se despierta a un barco
         si coches_puente == 0 y barcos_esperando > 0 entonces:
               cola_barcos.signal()
         // Si no hay barcos esperando, pueden avanzar coches rezagados
         sino si barcos_esperando == 0 entonces:
               cola_coches.signal()

      // --- MÉTODOS PARA BARCOS ---

      entrar_barco():
         barcos_esperando = barcos_esperando + 1
         // Un barco debe esperar a que el puente quede completamente vacío de coches
         // y a que ningún otro barco esté cruzando actualmente
         mientras coches_puente > 0 o barcos_puente > 0 hacer:
               cola_barcos.wait()
         barcos_esperando = barcos_esperando - 1
         barcos_puente = 1

      salir_barco():
         barcos_puente = 0
         // Como los barcos tienen prioridad absoluta:
         si barcos_esperando > 0 entonces:
               cola_barcos.signal()
         sino:
               // Si no hay más barcos, se habilita el paso a todos los coches en espera
               cola_coches.signal()
