#! /usr/bin/env python3

from pandas import Series
from time import time

# TO-DO
# - Organizar por categorías
# - Guardar la hora

def main():
    """Project description"""
    global num_v, times_dict

    times_dict = {}

    print("ANTES DE COMENZAR LA CARRERA:")
    print("Ingrese el número de vueltas: ")

    num_v = input("$: ")
    while True:
        try: num_v = int(num_v);    break
        except: 
            print("Introduzca un valor válido.")
            num_v = input("$: ")

    print("* Para iniciar la carrera, escriba START y pulse enter.")

    inp = input("$: ")
    while inp!="START":
        print("\t Ingrese un valor válido. START, todo en mayúscula!")
        inp = input("$: ")

    t0 = time()  # Start counting time after user inputs START

    print("\nComienza la carrera!\n")
    print("* Para tomar el tiempo de un/a participante, introduzca el número de participante y pulse enter.")
    print("* Para terminar la carrera, escriba END y pulse enter.\n")

    while inp!="END":
        inp = input("$: ")
        if inp == "END":   
            exit_status = check_out()  # Make sure user wants to end race
            if exit_status: break
            print("OK. Puede seguir entrando valores.")
            inp = input("$: ")

        try: 
            inp = int(inp)
            valid = True
        except: 
            if inp!="END":
                print("Introduzca un valor válido.")
                valid = False
            else:
                break

        if valid:
            # Check if competitor is already on list
            # In case not, create record
            if inp not in times_dict.keys():        times_dict[inp] = []

            t = time() - t0
            if num_v - len(times_dict[inp]) > 0:
                times_dict[inp].append(t)

                print("\tTiempo para corredor/a {0}: {1:.0f}h {2:.0f}m {3:.2f}s.".format(inp, t//3600,(t%3600)//60,t%60,2 ))
                
                lefalta = num_v - len(times_dict[inp])
                if lefalta > 0:        print("\t\t* Le faltan {} vueltas.".format(num_v - len(times_dict[inp])))
                else:                  print("\t\t******** Terminó la carrera! ******** ")

            else: 
                print("\tOJO: Esta corredora ya terminó la carrera!")


    # Get sorted list of runners (ascending order) 
    # Count only runners that completed the race. (num_v = number of laps for each runner)
    final_res = Series({ID:times_dict[ID][-1] for ID in times_dict.keys() if len(times_dict[ID])==num_v}).sort_values()
    print("\n*******************")
    print("\n\nRESULTADOS:\n\n")
    print("*******************")

    print("\t\tPosición\t|\tID\t|\t Tiempo")
    print("\t\t________________________________________________\n")

    for i,ID in enumerate(final_res.index):
        t = final_res[ID]
        print("\t\t{0:>4}{1:>22}{2:>10}h {3:.0f}m {4:.2f}s".format(i+1,ID, int(t//3600),(t%3600)//60,t%60,2 ))
    
###########################

def check_out():
    print("\n\t ** Confirme que quiere terminar la carrera.")

    quien_falta = []
    for ID in times_dict.keys():
        lefalta = num_v - len(times_dict[ID]) 
        if lefalta > 0 :
            quien_falta.append("{} le faltan {} vueltas".format(ID,lefalta))

    if len(quien_falta) > 0:
        print("\t\tTodavía faltan por llegar:")
        for i in quien_falta:
            print(i)

    print("\t * Para confirmar la terminación de la carrera, escriba SISAS y pulse enter.")
    print("\t * De otra manera, escriba TIRAS y pulse enter")
    
    confirm = input("$: ")
    while confirm not in ["SISAS","TIRAS"]:
        print("Ingrese un valor válido")
        confirm = input("$: ")

    if confirm=="SISAS": return True
    else: return False


if __name__=="__main__":
    main()

