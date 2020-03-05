#Martín España
#Carné: 19258
#Hoja de Trabajo 5
#Ultima decha de modificacion: 4/03/2020


import random
import simpy
import numpy

def simulate(env, join_time, identifier, ram, cpu, wait_status):
    #Variables que se utilizan de manera global
    global times_list
    global total_time
    
    yield env.timeout(join_time)
    
    #Se inicializan tiempos de entrada y de salida (Input/Output)
    starting_time = env.now
    exit_time = 0
    
    print("El proceso No. %d entra en tiempo = %s"%(identifier, starting_time))
    
    instructions = random.randint(1,10) #Se generan la cantidad de instrucciones
    space_required = random.randint(1,10) #Se crea el espacio requerido en la ram para ejecutar el proceso
    
    with ram.get(space_required) as row_one:
        #Muestra
        print("El proceso No. %d ingreso al espacio en la ram en tiempo = %s"%(identifier,env.now))
        print("El proceso No. %d requiere %s memoria en la ram"%(identifier,space_required))
        
        while instructions > 0:
            with cpu.request() as row_two:
                yield row_two
                print("El proceso No. %d ingreso al CPU en tiempo = %s"%(identifier, env.now))
                yield env.timeout(1)
                instructions -= 3 #Aqui se resta la cantidad de instrucciones realizadas (Cambiar para procesador mas rapido o lento)
                
                #Revisa si el CPU aun tiene instrucciones por ejecutar, de lo contrario se termina el proceso.
                if instructions <= 0:
                    instructions = 0 #Reinicia el contador de instrucciones para el siguiente proceso
                    exit_time = env.now
                    print("El proceso No. %d salió del CPU en tiempo = %s"%(identifier, exit_time))
                else:
                    decision = random.randint(1,2)
                    if decision == 1:
                        with wait_status.request() as row_three:
                            yield row_three
                            yield env.timeout(1)
    delta_time = exit_time - starting_time
    times_list.append(delta_time)
    total_time = exit_time
                    
                    
#Asignación de variables
random.seed(54321) #Se utiliza una seed para que los numeros generados en cada simulacion sean los mismos
env = simpy.Environment() #Se crea un nuevo ambiente
ram = simpy.Container(env, init = 100, capacity = 100) #Aqui se asigna el espacio de la ram en un container de simpy
cpu = simpy.Resource(env, capacity = 1) #Aquí se asigna la cantidad de procesadores
wait_status = simpy.Resource(env, capacity = 1)
process_interval = 10.0 #Aquí se cambia el intervalo de la creacion de procesos
total_time = 0
times_list = []
total_procedures = 25 #Aquí se cambia la cantidad de procesos que entraran a la simulación

for i in range(total_procedures):
    env.process(simulate(env, random.expovariate(1.0/process_interval), i, ram, cpu, wait_status))

env.run()
average_time = float(total_time)/float(total_procedures)
standard_dev = numpy.std(times_list, ddof = 1) #Se calcula la desviacion estandar utilizando el paquete NumPy


print("\no-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o \nResumen \no-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o")
print("Tiempo total: %d \nTiempo promedio por cada instruccion: %s \nDesviacion estandar: %.2f"%(total_time, average_time, standard_dev))