agenda = {}

def aggiungi_evento():
    data = input("Inserisci la data dell'evento (formato: gg/mm/aaaa): ")
    evento = input("Inserisci il nome dell'evento: ")
    agenda[data] = evento
    print("Evento aggiunto con successo!")

def visualizza_eventi():
    if not agenda:
        print("L'agenda è vuota.")
    else:
        print("Eventi nella tua agenda:")
        for data, evento in agenda.items():
            print(f"{data}: {evento}")

def elimina_evento():
    data = input("Inserisci la data dell'evento da eliminare (formato: gg/mm/aaaa): ")
    if data in agenda:
        del agenda[data]
        print("Evento eliminato con successo!")
    else:
        print("Nessun evento trovato per la data specificata.")

def menu():
    print("Benvenuto nell'agenda! Cosa desideri fare?")
    print("1. Aggiungi un evento")
    print("2. Visualizza gli eventi")
    print("3. Elimina un evento")
    print("4. Esci")

    scelta = input("Inserisci il numero corrispondente all'azione da eseguire: ")

    if scelta == "1":
        aggiungi_evento()
    elif scelta == "2":
        visualizza_eventi()
    elif scelta == "3":
        elimina_evento()
    elif scelta == "4":
        print("Grazie per aver usato l'agenda. Arrivederci!")
        return
    else:
        print("Scelta non valida. Riprova.")

    menu()

menu()
