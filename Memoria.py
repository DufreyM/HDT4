import random 
import simpy 

PROCESOS_INTERVALO = 10
NEW_PROCESOS = 18
RANDOM_SEED = 20
INSTRUCTIONS_CPU = 1

def proceso(env, name, COUNTER_CPU, instrucciones):
    global RAM
    starts = env.now

    MEMORY = random.uniform(0,10)
    while MEMORY > RAM.level: 
        print("%7.4f %s: Memoria insuficiente" % (starts, name))
        yield env.event()
        yield env.timeout(1)
    
    RAM.get(MEMORY)
    print("%7.4f Starting process %s, Memory available: %d" % (starts, name, RAM.level))

    while instrucciones > 0: 
        with COUNTER_CPU.request() as req:
            yield req 
            Execute = min(instrucciones, INSTRUCTIONS_CPU)
            yield env.timeout(1)
            instrucciones -= Execute

            if instrucciones > 0:
                WAITING = random.randint(1,2)
                if WAITING == 1: 
                    print ("%7.4f Proceso %s se va a poner en Waiting" % (starts, name))
                    yield env.timeout(1)
                    print ("%7.4f Proceso %s se va a ready" % (starts, name))
                
                elif WAITING == 2:  
                    print ("%7.4f Proceso %s se va a ready" % (starts, name))
                
                    
            else: 
                print ("%7.4f Proceso %s terminado" % (env.now, name))
                RAM.put(MEMORY)
    

def procces(env, procesos, interval, counter): 
    for x in range(procesos): 
        instrucciones = random.expovariate(1.0/ interval) 
        p = proceso(env, "Process%02d" % x, counter, instrucciones)
        env.process(p)
        t = random.expovariate(1.0/interval)
        yield env.timeout(t)

# Simulation
random.seed(RANDOM_SEED)
env = simpy.Environment()
RAM = simpy.Container(env, init=100, capacity=100)
COUNTER_CPU = simpy.Resource(env, capacity=1)
env.process(procces(env, NEW_PROCESOS, PROCESOS_INTERVALO, COUNTER_CPU))
env.run()
