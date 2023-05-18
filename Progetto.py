import tkinter as tk
from tkinter import messagebox

class Agenda:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Agenda")
        
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)
        
        self.label = tk.Label(self.frame, text="Seleziona un giorno:")
        self.label.pack()
        
        self.calendario = tk.Calendar(self.frame, selectmode="day", date_pattern="dd/MM/yyyy")
        self.calendario.pack()
        
        self.evento_label = tk.Label(self.frame, text="Inserisci un evento:")
        self.evento_label.pack()
        
        self.evento_entry = tk.Entry(self.frame)
        self.evento_entry.pack()
        
        self.aggiungi_button = tk.Button(self.frame, text="Aggiungi", command=self.aggiungi_evento)
        self.aggiungi_button.pack()
        
        self.modifica_button = tk.Button(self.frame, text="Modifica", command=self.modifica_evento)
        self.modifica_button.pack()
        
        self.elimina_button = tk.Button(self.frame, text="Elimina", command=self.elimina_evento)
        self.elimina_button.pack()
        
        self.eventi_listbox = tk.Listbox(self.root, width=50)
        self.eventi_listbox.pack(pady=20)
        
    def aggiungi_evento(self):
        data_selezionata = self.calendario.get_date()
        evento = self.evento_entry.get()
        if data_selezionata and evento:
            evento_completo = f"{data_selezionata}: {evento}"
            self.eventi_listbox.insert(tk.END, evento_completo)
            self.evento_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Attenzione", "Seleziona una data e inserisci un evento!")
        
    def modifica_evento(self):
        selezionato = self.eventi_listbox.curselection()
        if selezionato:
            evento_selezionato = self.eventi_listbox.get(selezionato)
            data, evento = evento_selezionato.split(": ")
            self.calendario.set_date(data)
            self.evento_entry.delete(0, tk.END)
            self.evento_entry.insert(0, evento)
            self.eventi_listbox.delete(selezionato)
        else:
            messagebox.showwarning("Attenzione", "Seleziona un evento da modificare!")
        
    def elimina_evento(self):
        selezionato = self.eventi_listbox.curselection()
        if selezionato:
            self.eventi_listbox.delete(selezionato)
        else:
            messagebox.showwarning("Attenzione", "Seleziona un evento da eliminare!")

if __name__ == '__main__':
    agenda = Agenda()
    agenda.root.mainloop()
