from prettytable import PrettyTable # Importation de la bibliothèque PrettyTable qui permet de créer des tableaux formatés.

abc = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "h,", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
       "u",
       "v", "w"]  # Alphabet
det_etats_nouvaux = [] # Liste contenant les nouveaux etats pour la determinisation
nom_fichier = "Automates/E2_"
saisi = input("Entrez le numero de l'automate: ")
nom_fichier = nom_fichier + saisi + ".txt" # Traitement du nom de fichier

def process_input_string(input_string): # Convertir les lignes du fichier en chaine de caractère
    input_string = input_string.rstrip("\n")
    input_list = input_string.split(",")
    return input_list

with open(nom_fichier, "r") as f:
    # extraction des informations du fichier
    liste = f.readlines()
    alphabet = liste[0]
    nbr_etats = liste[1]
    etats_init = liste[2]
    etats_term = liste[3]
    nbr_transi = liste[4]
    transi = liste[6:-1]

    # gestion des informations en données utilisables (reformatages des données)

    alphabet = process_input_string(alphabet)
    nbr_etats = process_input_string(nbr_etats)
    etats_init = process_input_string(etats_init)
    etats_term = process_input_string(etats_term)
    nbr_transi = nbr_transi.split(",")

    trans = [] # Transitions

    for i in transi:
        i = i.rstrip("\n")
        trans.append(i.split(","))
    f.close()

liste_etats = []
for i in range(int(nbr_etats[0])):
    liste_etats.append(i)

def tr_interpretor(a):
    # TRADUCTION D'UNE TRANSITION SOUS LA FORME '2a3' A LA FORME [2,0,3]
    l = [int(a[0])]
    b = a[1]
    l.append(abc.index(b))
    l.append(a[2])
    return l

# intialisation de la matrice automate sous la forme de matrice carrée remplie de '-'
Automate = []
nbr_transi = len(alphabet)
nbr_etats = int(nbr_etats[0])
for i in range(nbr_etats):
    temp = []
    for j in range(nbr_transi):
        temp.append('-')
    Automate.append(temp)

# remplissage d'Automate avec les transitions
for i in trans:
    for j in i:
        l = tr_interpretor(j)
        if Automate[l[0]][l[1]] == '-':
            Automate[l[0]][l[1]] = l[2]
        else:
            Automate[l[0]][l[1]] += ',' + l[2]


def affichage_B(alphabet, Automate):
    # AFFICHAGE D'UN AUTOMATE COMPLET SOUS LA FORME DE TABLEAU
    print(" ", alphabet)
    n = 0
    for i in Automate[0:-1]:
        print(n, i)
        n += 1
    print('P', Automate[-1])

# remarque l'algo ne marche que pour des transition litterales de (a à v) et des etats allant de 0 a 9

def est_deter(Automate):
    # VERIFIE SI L'AUTOMATE EST DETERMINISTE OU NON, RENVOIE True/False
    for i in Automate:
        for j in i:
            if len(j) >= 3:
                return False
    if len(etats_init) != 1:
        return False

    return True

def est_complet(Automate):
    # VERIFIE SI L'AUTOMATE EST DETERMINISTE OU NON, RENVOIE True/False
    for i in Automate:
        for j in i:
            if j == '-':
                return False
    return True

def rendrecomplet(Automate):
    # COMPLETE UN AUTOMATE AVEC UN POUBELLE
    c1 = 0
    c2 = 0
    for i in Automate:
        c2 = 0
        for j in i:
            if '-' == j:
                Automate[c1][c2] = 'P'

            c2 += 1
        c1 += 1
    ltemp = []
    for i in range(len(Automate[0])):
        ltemp.append('P')
    Automate.append(ltemp)
    return Automate

def donne_type(etat, etat_term, etat_init):
    # DONNE LE TYPE DE L'ETAT, 0 SI QUELQUONQUE ,1 SI INTIAL, 2 SI FINAL
    for i in etat_term:
        if int(i) == etat:
            return 2
    for i in etat_init:
        if int(i) == etat:
            return 1
    return 0

def determinisation(Automate):
    det_etats_nouvaux = [] # Initialise une liste pour stocker les nouveaux états
    non_parcouru_etats = [] # Initialise une liste pour stocker les états non encore parcourus
    temp = ""
    for i in etats_init:
        temp = temp + i
    det_init = temp # Concatène les états initiaux
    non_parcouru_etats.append(det_init) # Ajoute les états initiaux à la liste des états non parcourus
    stockage = ""
    supprimer_doublon = ""
    det_transition = [] # Initialise une liste pour stocker les transitions déterminisées
    while len(non_parcouru_etats) != 0: # Boucle jusqu'à ce que tous les états soient parcourus
        for j in range(len(alphabet)):
            for i in range(len(non_parcouru_etats[0])):
                if not Automate[int(non_parcouru_etats[0][i])][j].replace(",", "") == "-":
                    stockage = stockage + Automate[int(non_parcouru_etats[0][i])][j].replace(",", "")

            for caractere in stockage:
                if caractere not in supprimer_doublon:
                    supprimer_doublon += caractere # Supprime les doublons dans les transitions
            if not supprimer_doublon == "":
                det_transition.append(supprimer_doublon) # Ajoute les transitions déterminisées à la liste
            else:
                det_transition.append("-")
            if not supprimer_doublon in det_etats_nouvaux:
                if supprimer_doublon != det_init:
                    if supprimer_doublon != "":
                        det_etats_nouvaux.append(supprimer_doublon) # Ajoute les nouveaux états à la liste s'ils n'ont pas été déjà explorés
                        non_parcouru_etats.append(supprimer_doublon) # Supprime l'état exploré de la liste des états non parcourus

            stockage = ""
            supprimer_doublon = ""

        non_parcouru_etats.remove(non_parcouru_etats[0])

    det_etats_nouvaux.insert(0, det_init) # Insère l'état initial dans la liste des nouveaux états
    seen = set()
    result = []
    for s in det_etats_nouvaux:
        sorted_s = ''.join(sorted(s))
        if sorted_s not in seen:
            seen.add(sorted_s)
            result.append(s) # Trie les nouveaux états et élimine les doublons

    print("Nouveux états apres determinisation: ", result, "\n")
    det_Automate = [] # Initialise une liste pour stocker les transitions déterminisées
    liste_temp = []
    n = 0
    for i in range(len(result)):
        for j in range(len(alphabet)):
            liste_temp.append(det_transition[n])
            n = n + 1
        det_Automate.append(liste_temp)
        liste_temp = []
    return det_Automate, result # Ajoute les transitions déterminisées

def affichage_automate_quelconque(Automate):
    tableau = PrettyTable() # Initialisation d'une variable "tableau" pour stocker les données du tableau de transition.

    # Définition des en-têtes de colonnes en fonction de la taille de l'alphabet.

    if len(alphabet) == 2:
        colonne = ["--", "Etat", "a", "b"]
    elif len(alphabet) == 4:
        colonne = ["--", "Etat", "a", "b", "c", "d"]
    elif len(alphabet) == 1:
        colonne = ["--", "Etat", "a"]
    else:
        colonne = ["--", "Etat", "a", "b", "c"]
    # Attribution des en-têtes de colonnes à la variable "tableau".
    tableau.field_names = colonne
    # Initialisation d'une liste vide "combolist" pour stocker les données de chaque ligne du tableau.
    combolist = []

    # Boucle sur chaque état de l'automate pour remplir les données de chaque ligne du tableau.
    for i in range(nbr_etats):
        # Vérification de si l'état est un état initial ou un état final, ou les deux.
        if str(i) in etats_init:
            if str(i) in etats_term:
                combolist.append("ES") # État initial et final
            else:
                combolist.append("E") # État initial seulement

        elif str(i) in etats_term:
            combolist.append("S") # État final seulement
        else:
            combolist.append("-") # Ni état initial ni état final

        # Ajout de l'indice de l'état courant dans la liste "combolist".
        combolist.append(i)

        # Boucle sur chaque symbole de l'alphabet pour remplir les données de chaque colonne.
        for j in range(len(alphabet)):
            combolist.append(Automate[i][j])

        # Ajout de la liste "combolist" comme une nouvelle ligne dans la variable "tableau".
        tableau.add_row(combolist)

        # Réinitialisation de la liste "combolist" pour remplir la prochaine ligne.
        combolist = []
    # Affichage du tableau de transition.
    print(tableau)

def est_standard(etats_init):
    if len(etats_init) == 1:
        for i in trans:
            for j in i:
                if j[2] != etats_init[0]:
                    return False
        return True
    return False


# Définition de la fonction standardiser qui prend en entrée un automate et l'état initial.
def standardiser(Automate,etat_init):
    stand_transition = [] # Initialisation d'une liste "stand_transition" qui va stocker les transitions de l'état initial.
    # Initialisation d'une liste "etats" avec l'état initial "i".
    etats = ["i"]
    tempo = ""
    for i in range(nbr_etats):
        etats.append(i)
    # Boucle sur chaque état de l'automate.
    for i in range(len(alphabet)):
        for j in range(nbr_etats):
            if not Automate[j][i] == "-":
                if str(j) in etat_init:
                    for z in Automate[j][i]:
                        if z not in tempo:
                            tempo = tempo + Automate[j][i]


        stand_transition.append(tempo)
        tempo = ""
    # Initialisation d'une liste "temp" pour stocker les transitions standardisées.
    temp = []
    for i in range(len(stand_transition)):
        temp.append(stand_transition[i].replace(",",""))
    etat_init.clear()
    etat_init.append("i")
    Automate.insert(0,temp)
    # Retourne les listes "etats" et "temp".
    return etats,temp

Automate_std = []
def affichage_automate_std(etats,auto):
    tableau = PrettyTable()
    sortie = 0
    if len(alphabet) == 2:
        colonne = ["--", "Etat", "a", "b"]
    elif len(alphabet) == 4:
        colonne = ["--", "Etat", "a", "b", "c", "d"]
    elif len(alphabet) == 1:
        colonne = ["--", "Etat", "a"]
    else:
        colonne = ["--", "Etat", "a", "b", "c"]
    tableau.field_names = colonne
    combolist = []
    for i in range(len(etats)):
        if i == 0:
            type = "E"
        else:
            type = "-"
        if str(etats[i]) in etats_term:
            sortie = sortie + 1

        if sortie > 0:
            type = "S"
        sortie = 0
        combolist.append(type)
        type = ""
        combolist.append(etats[i])
        for j in range(len(alphabet)):
            combolist.append(auto[i][j])
        tableau.add_row(combolist)
        combolist.pop(0)
        combolist.pop(0)
        Automate_std.append(combolist)
        combolist = []
    print(tableau)
def affichage_automate_deter(etats, auto, etats_init, etats_term):
    tableau = PrettyTable()
    type = ""
    sortie = 0
    if len(alphabet) == 2:
        colonne = ["--", "Etat", "a", "b"]
    elif len(alphabet) == 4:
        colonne = ["--", "Etat", "a", "b", "c", "d"]
    elif len(alphabet) == 1:
        colonne = ["--", "Etat", "a"]
    else:
        colonne = ["--", "Etat", "a", "b", "c"]
    tableau.field_names = colonne
    combolist = []
    for i in range(len(etats)):
        for j in range(len(etats[i])):
            if i != 0:
                if etats[i][j] in etats_term:
                    sortie = sortie + 1
            else:
                type = "E"
        if sortie > 0:
            type = type + "S"
        if type == "" and i != 0:
            type = "-"
        sortie = 0

        combolist.append(type)
        type = ""
        combolist.append(etats[i])
        for j in range(len(alphabet)):
            combolist.append(auto[i][j])
        tableau.add_row(combolist)
        combolist = []
    print(tableau)
Automate2 = []


for i in Automate:
    Automate2.append(i)
verif = 0


def affichage_complet():
    print("\033[34m----------------------------------------------------------------------------------------\033[34m")
    print("                     \033[34mPROJET AUTOMATE S4 : TRAITEMENT D'AUTOMATE FINI\033[0m")
    print("\033[34m----------------------------------------------------------------------------------------\033[0m")
    print("AFFICHAGE DES INFORMATIONS DE NOTRE FICHIER :")
    print("Alphabet: ", alphabet)
    print("Etats initiaux: ", etats_init)
    print("Etats terminaux: ", etats_term)
    print("Nombre d'états: ", nbr_etats)
    print("Les differentes transitions: ", trans, "\n")

    print("Apres la creation d'une table de transition et le remplissage de celle-ci, voici l'automate sous la forme matricielle :")
    print(Automate)

    print("\nMenu : plusieurs choix s'offrent à vous :")
    print("1. Option 1 : Affichage d'un automate quelconque sous la forme de tableau")
    print("2. Option 2 : Affichage d'un automate complet sous la forme de tableau")
    print("3. Option 3 : Passez ces étapes")
    print("4. Option 4 (dédié pour les traces d'executions): Tout afficher (quelconque, standard, deterministe et complet) ")

    # Boucle principale
    while True:
        # Demande à l'utilisateur de choisir une option
        choix = input("Entrez le numéro de l'option que vous voulez choisir : ")
        # Vérification de l'option choisie
        if choix == '1':
            print("\n============================== TABLE DE TRANSITION DE BASE DE L'AUTOMATE ==============================\n")
            affichage_automate_quelconque(Automate)
        elif choix == '2':
            rendrecomplet(Automate)
            affichage_automate_quelconque(Automate)
        elif choix == '3':
            break
        elif choix == '4':

            print(
                "\n\n \033[34m============================== TABLE DE TRANSITION DE BASE DE L'AUTOMATE ==============================\n\n \033[0m")
            affichage_automate_quelconque(Automate)

            if not est_deter(Automate):

                var = est_deter(Automate)
                if var == False:
                    determini = determinisation(Automate)
                    print("\n \n \033[34m============================== DETERMINISATION ET COMPLET: ==============================\n\n \033[0m")
                    print("\nTable de transition après determinisation\n")
                    if est_complet(determini[0]):
                        print("L'automate est déjà complet donc pas de completion a faire")
                        for i in range(len(Automate)):
                            for j in range(len(alphabet)):
                                if Automate[i][j] == "P":
                                    Automate[i][j] = "-"

                        rendrecomplet(determini[0])
                        affichage_automate_deter(determini[1], determini[0], etats_init, etats_term)
                    else:
                        print("\033[34mAVANT COMPLETION: \033[0m")
                        determini = determinisation(Automate)
                        affichage_automate_deter(determini[1], determini[0], etats_init, etats_term)

                        rendrecomplet(determini[0])

                        print("\n\033[34mAPRES COMPLETION: \n\033[0m")
                        affichage_automate_deter(determini[1], determini[0], etats_init, etats_term)

                else:
                    determini2 = rendrecomplet(Automate)
                    affichage_automate_deter(determini2[1], determini2[0], etats_init, etats_term)
            else:
                print("\n \n \033[34m============================== DETERMINISATION ET COMPLET: ==============================\n\n \033[0m")
                print("L'automate est déjà deterministe !")


            print("\n \033[34m ============================== STANDARDISATION: ==============================\n\033[0m")
            if not est_standard(etats_init):
                print("L'automate n'est pas standard a la base, voici la version standardisé: \n\n")
                std = standardiser(Automate, etats_init)
                affichage_automate_std(std[0], Automate)
            else:
                print("L'automate est déjà standard \n\n")

        else:
            break


    print("\nMenu : plusieurs choix s'offrent à vous :")
    print("1. Option 1 : L'automate est standard ?")
    print("2. Option 2 : L'automate est deterministe ?")
    print("3. Option 3 : L'automate est complet ?")
    print("5. Option 5 : Passez ces étapes")

    while True:
        # Demande à l'utilisateur de choisir une option
        choix = input("Entrez le numéro de l'option que vous voulez choisir : ")
        # Vérification de l'option choisie
        if choix == '1':

            if est_standard(Automate) == False:
                print("L'automate n'est pas standard, voulez vous le rendre standard ? : tappez y pour oui et n pour non")
                choix = input("")
                if choix == 'y':
                    print("\n \033[34m ============================== STANDARDISATION: ==============================\n\033[0m")
                    std = standardiser(Automate,etats_init)
                    affichage_automate_std(std[0],Automate)
                    if not est_complet(Automate):
                        choix = input("Il n'est pas complet voulez vous le completer ? (y ou n): ")

                        if choix == "y":
                            rendrecomplet(Automate_std)
                            affichage_automate_std(std[0],Automate_std)
                            continue
                        elif choix == "n":
                            break
                        else:
                            print("Choix incorrect")
                if choix == 'n':
                    break
            else:
                print("L'automate est déjà standard !")

        if choix == '2':
            var = est_deter(Automate)
            if var == False:
                print("Non, voulez vous le rendre déterministe ? : tappez y pour oui et n pour non")
                choix = input("")
                if choix == 'y':
                    print("\n ============================== DETERMINISATION: ==============================\n")
                    print("\nTable de transition après determinisation\n")
                    if est_complet(Automate):
                        for i in range(len(Automate)):
                            for j in range(len(alphabet)):
                                if Automate[i][j] == "P":
                                    Automate[i][j] = "-"

                        determini = determinisation(Automate)
                        rendrecomplet(determini[0])
                        affichage_automate_deter(determini[1], determini[0], etats_init, etats_term)
                    else:
                        determini = determinisation(Automate)
                        affichage_automate_deter(determini[1], determini[0], etats_init, etats_term)
                        print("Oui, mais voulez vous le rendre complet ? : tappez y pour oui et n pour non")
                        choix = input("")
                        if choix == 'y':
                            rendrecomplet(determini[0])
                            affichage_automate_deter(determini[1], determini[0], etats_init, etats_term)
                            if choix == 'n':
                                break
                        if choix == 'n':
                            break
            if est_deter(Automate) == True:
                print("Oui, mais voulez vous le rendre complet ? : tappez y pour oui et n pour non")
                choix = input("")
                if choix == 'y':
                    determini2 = rendrecomplet(Automate)
                    affichage_automate_deter(determini2[1], determini2[0], etats_init, etats_term)
                if choix == 'n':
                    break
        elif choix == '3':
            var = est_complet(Automate)
            if var == False:
                print("Non, voulez vous le rendre complet ? : tappez y pour oui et n pour non")
                choix = input("")
                if choix == 'y':
                    rendrecomplet(Automate)
                    affichage_automate_quelconque(Automate)
                if choix == 'n':
                    break
            else:
                print("L'automate est déjà complet !")
        else:
            break

affichage_complet()
