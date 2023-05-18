import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

# Funzione per aggiungere un nuovo appuntamento

def aggiungi_appuntamento():
    data = f"{anno_corrente}-{mese_corrente}-{giorno_selezionato.get():02d}"
    titolo = entry_titolo.get()
    descrizione = entry_descrizione.get()
    
    conn = sqlite3.connect('agenda.db')
    c = conn.cursor()
    c.execute("INSERT INTO appuntamenti (data, titolo, descrizione) VALUES (?, ?, ?)", (data, titolo, descrizione))
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Agenda", "Appuntamento aggiunto con successo!")
    visualizza_appuntamenti()

# Funzione per visualizzare gli appuntamenti per una data specifica
def visualizza_appuntamenti():
    data = f"{anno_corrente}-{mese_corrente}-{giorno_selezionato.get():02d}"
    
    conn = sqlite3.connect('agenda.db')
    c = conn.cursor()
    c.execute("SELECT titolo, descrizione FROM appuntamenti WHERE data=?", (data,))
    appuntamenti = c.fetchall()
    conn.close()
    
    # Pulisci la visualizzazione degli appuntamenti precedenti
    text_appuntamenti.delete("1.0", tk.END)
    
    # Aggiungi gli appuntamenti alla visualizzazione
    if len(appuntamenti) > 0:
        for appuntamento in appuntamenti:
            text_appuntamenti.insert(tk.END, f"Titolo: {appuntamento[0]}\nDescrizione: {appuntamento[1]}\n\n")
    else:
        text_appuntamenti.insert(tk.END, "Nessun appuntamento per questa data.")

# Funzione per eliminare un appuntamento
def elimina_appuntamento():
    data = f"{anno_corrente}-{mese_corrente}-{giorno_selezionato.get():02d}"
    titolo = entry_titolo.get()
    
    conn = sqlite3.connect('agenda.db')
    c = conn.cursor()
    c.execute("DELETE FROM appuntamenti WHERE data=? AND titolo=?", (data, titolo))
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Agenda", "Appuntamento eliminato con successo!")
    visualizza_appuntamenti()

# Funzione per aggiornare il calendario
def aggiorna_calendario():
    global mese_corrente, anno_corrente
    
    mese_corrente = combo_mesi.current() + 1
    anno_corrente = combo_anni.get()
    
    # Pulisci il calendario precedente
    for giorno in giorni_calendario:
        giorno.destroy()
    
    # Aggiorna il calendario per il mese corrente
    giorni_del_mese = calcola_giorni_mese(mese_corrente, anno_corrente)
    giorno_inizio_settimana, giorni_mese_prec, giorni_mese_succ = calcola_giorni_settimana(mese_corrente, anno_corrente)
    
    for i in range(giorno_inizio_settimana):
        giorno = tk.Label(frame_calendario, text=giorni_mese_prec - giorno_inizio_settimana + i + 1, bg="lightgray")
        giorno.grid(row=1, column=i, padx=5, pady=5)
        giorni_calendario.append(giorno)
    
    for i in range(1, giorni_del_mese + 1):
        if (giorno_inizio_settimana + i - 1) % 7 == 0:
            riga = len(giorni_calendario) + 1
            colonna = 0
        else:
            riga = len(giorni_calendario)
            colonna = (giorno_inizio_settimana + i - 1) % 7
        
        giorno = tk.Button(frame_calendario, text=i, bg="white", command=lambda x=i: seleziona_giorno(x))
        giorno.grid(row=riga, column=colonna, padx=5, pady=5)
        giorni_calendario.append(giorno)
    
    for i in range(giorno_inizio_settimana + giorni_del_mese, 7):
        giorno = tk.Label(frame_calendario, text=i - (giorno_inizio_settimana + giorni_del_mese - 1), bg="lightgray")
        giorno.grid(row=len(giorni_calendario), column=i % 7, padx=5, pady=5)
        giorni_calendario.append(giorno)
    
    visualizza_appuntamenti()

# Funzione per calcolare il numero di giorni in un determinato mese
def calcola_giorni_mese(mese, anno):
    if mese in [4, 6, 9, 11]:
        return 30
    elif mese == 2:
        if (anno % 4 == 0 and anno % 100 != 0) or (anno % 400 == 0):
            return 29
        else:
            return 28
    else:
        return 31

# Funzione per calcolare il giorno della settimana in cui inizia il mese
def calcola_giorni_settimana(mese, anno):
    giorno_inizio = tk.StringVar(window)
    giorno_inizio.set("Lunedi")
    giorni_settimana = ["Lunedi", "Martedi", "Mercoledi", "Giovedi", "Venerdi", "Sabato", "Domenica"]
    giorno_mese_prec = calcola_giorni_mese(mese - 1, anno)
    giorno_inizio_settimana = (giorno_mese_prec + 1) % 7
    giorni_mese_prec = giorno_mese_prec - giorno_inizio_settimana + 1
    giorni_mese_succ = 7 - ((giorno_inizio_settimana + calcola_giorni_mese(mese, anno)) % 7)
    
    return giorno_inizio_settimana, giorni_mese_prec, giorni_mese_succ

# Funzione per selezionare un giorno nel calendario
def seleziona_giorno(giorno):
    giorno_selezionato.set(giorno)
    visualizza_appuntamenti()

# Creazione della finestra principale
window = tk.Tk()
window.title("Agenda")
window.geometry("800x500")

# Creazione del frame per il calendario
frame_calendario = tk.Frame(window)
frame_calendario.pack(pady=20)

# Creazione del menu per selezionare il mese e l'anno
frame_menu = tk.Frame(window)
frame_menu.pack(pady=10)

mesi = [
    "Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
    "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"
]
combo_mesi = ttk.Combobox(frame_menu, values=mesi)
combo_mesi.current(0)
combo_mesi.grid(row=0, column=0, padx=5, pady=5)

anni = [str(i) for i in range(2022, 2030)]
combo_anni = ttk.Combobox(frame_menu, values=anni)
combo_anni.current(0)
combo_anni.grid(row=0, column=1, padx=5, pady=5)

button_aggiorna = tk.Button(frame_menu, text="Aggiorna", command=aggiorna_calendario)
button_aggiorna.grid(row=0, column=2, padx=5, pady=5)

# Creazione del frame per gli appuntamenti
frame_appuntamenti = tk.Frame(window)
frame_appuntamenti.pack(pady=20)

label_titolo = tk.Label(frame_appuntamenti, text="Titolo:")
label_titolo.grid(row=0, column=0, padx=5, pady=5)
entry_titolo = tk.Entry(frame_appuntamenti)
entry_titolo.grid(row=0, column=1, padx=5, pady=5)

label_descrizione = tk.Label(frame_appuntamenti, text="Descrizione:")
label_descrizione.grid(row=1, column=0, padx=5, pady=5)
entry_descrizione = tk.Entry(frame_appuntamenti)
entry_descrizione.grid(row=1, column=1, padx=5, pady=5)

button_aggiungi = tk.Button(frame_appuntamenti, text="Aggiungi", command=aggiungi_appuntamento)
button_aggiungi.grid(row=2, column=0, padx=5, pady=5)

button_elimina = tk.Button(frame_appuntamenti, text="Elimina", command=elimina_appuntamento)
button_elimina.grid(row=2, column=1, padx=5, pady=5)

# Creazione del frame per la visualizzazione degli appuntamenti
frame_visualizzazione = tk.Frame(window)
frame_visualizzazione.pack(pady=20)

text_appuntamenti = tk.Text(frame_visualizzazione, height=10, width=50)
text_appuntamenti.pack()

# Variabili globali per il giorno selezionato
giorno_selezionato = tk.IntVar()
giorno_selezionato.set(1)
mese_corrente = combo_mesi.current() + 1
anno_corrente = int(combo_anni.get())

# Creazione del database
conn = sqlite3.connect('agenda.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS appuntamenti
             (data TEXT, titolo TEXT, descrizione TEXT)''')
conn.commit()
conn.close()

# Creazione dei widget iniziali


# Avvio dell'interfaccia grafica
window.mainloop()

