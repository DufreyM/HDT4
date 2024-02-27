import random 
import simpy 
import numpy 

PROCESOS_INTERVALO = 1
NEW_PROCESOS = 200
RANDOM_SEED = 20
INSTRUCTIONS_CPU = 3
inicio = {}
fin = {}


def proceso(env, name, COUNTER_CPU, instrucciones):
    global RAM
    starts = env.now
    inicio[name] =  starts
    MEMORY = random.uniform(0,10)
    
    while MEMORY > RAM.level: 
        print("%7.4f %s: Memoria insuficiente" % (starts, name))
        yield env.timeout(1)
    
    RAM.get(MEMORY)
    print("%7.4f Starting %s, Memory available: %d" % (starts, name, RAM.level))

    while instrucciones > 0: 
        with COUNTER_CPU.request() as req:
            yield req 
            Execute = min(instrucciones, INSTRUCTIONS_CPU)
            yield env.timeout(1)
            instrucciones -= Execute

            if instrucciones > 0:
                WAITING = random.randint(1,2)
                if WAITING == 1: 
                    #print ("%7.4f Proceso %s se va a poner en Waiting" % (starts, name))
                    yield env.timeout(1)
                
                elif WAITING == 2:  
                    #print ("%7.4f Proceso %s se va a ready" % (starts, name))
                    a=1
                
                    
            else: 
                print ("%7.4f Proceso %s terminado" % (env.now, name))
                fin[name] = env.now
                RAM.put(MEMORY)
    

def procces(env, procesos, interval, counter): 
    for x in range(procesos): 
        instrucciones = random.uniform(1,10) 
        p = proceso(env, "Process%02d" % x, counter, instrucciones)
        env.process(p)
        t = random.expovariate(1.0/interval)
        yield env.timeout(t)

# Simulation
random.seed(RANDOM_SEED)
env = simpy.Environment()
RAM = simpy.Container(env, init=100, capacity=100)
COUNTER_CPU = simpy.Resource(env, capacity=2)
env.process(procces(env, NEW_PROCESOS, PROCESOS_INTERVALO, COUNTER_CPU))
env.run()

tiempos_procesamiento = [fin[name] - inicio[name] for name in inicio]
tiempo_promedio = numpy.mean(tiempos_procesamiento)
desviacion_estandar = numpy.std(tiempos_procesamiento)

print("Tiempo promedio de procesamiento:", tiempo_promedio)
print("Desviación estándar del tiempo de procesamiento:", desviacion_estandar)