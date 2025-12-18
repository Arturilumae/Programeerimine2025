"""
Programm: Hinnete analüüsimise programm
Autorid: Artur Ilumäe ja Hannela Haavel

Kasutatavad allikad:
- Real Python Tkinter tutoriaals: https://realpython.com/python-gui-tkinter/
- Pandas Excel töötlemine: https://pandas.pydata.org/docs/
- Python JSON moodul: https://docs.python.org/3/library/json.html

Programm töötamiseks peab pyhon olema installitud koos pandas ja openpyxl teekidega.

programm käivitamiseks:
python main.py

"""

import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont
import funktsioonid as fn # abifunktsioonid

# Ained ja nende nimetus xlsx tabelis
AINED = {
    "Programmeerimine": "Programmeerimine 1",
    "Arvuti arhitektuur ja riistvara 1": "AAR 1",
    "Operatsioonisüsteemid": "Opsys",
    "Kõrgem matemaatika 1": "KÕM 1",
    "Sissejuhatus erialasse": "Sissejuhatus erialasse"
}

class App(tk.Tk): # Põhirakenduse klass lihtsamaks haldamiseks
    def __init__(self):
        super().__init__()
        self.title("Hinde arvutaja - GUI")
        self.geometry("900x600")

        # jagatud font teksti ja sisendväljade jaoks
        self.teksti_font = tkfont.Font(family="TkFixedFont", size=12)

        self.salvestatud_andmed = fn.loe_kohalikud_andmed()
        if self.salvestatud_andmed is None:
            self.salvestatud_andmed = {}

        # UI elemendid
        üla_raam = tk.Frame(self)
        üla_raam.pack(fill=tk.X, padx=10, pady=8)

        tk.Label(üla_raam, text="Vali aine:").pack(side=tk.LEFT)
        self.aine_muutuja = tk.StringVar()
        ainete_nimistik = list(AINED.keys())
        self.aine_menu = ttk.Combobox(üla_raam, values=ainete_nimistik, state='readonly', width=30)
        self.aine_menu.current(0)
        self.aine_menu.pack(side=tk.LEFT, padx=6)

        nuppude_raam = tk.Frame(üla_raam)
        nuppude_raam.pack(side=tk.RIGHT)

        tk.Button(nuppude_raam, text="Sisesta punktid", command=self.ava_punktide_sisestus).pack(side=tk.LEFT, padx=4)
        tk.Button(nuppude_raam, text="Arvuta hinne", command=self.arvuta_hinne_kuva).pack(side=tk.LEFT, padx=4)
        tk.Button(nuppude_raam, text="Loe salvestatud andmed", command=self.kuva_salvestatud).pack(side=tk.LEFT, padx=4)
        tk.Button(nuppude_raam, text="Salvesta andmed", command=self.salvesta_kõik).pack(side=tk.LEFT, padx=4)

        self.sisu = tk.Frame(self)
        self.sisu.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

        self.kategooria_raam = tk.Frame(self.sisu)
        self.kategooria_raam.pack(fill=tk.BOTH, expand=True)

        self.väljund = tk.Text(self.sisu, height=15, font=self.teksti_font)
        self.väljund.pack(fill=tk.X, pady=8)

        self.sisend_muutujad = {}

    def leia_aine_võti(self):
        valik = self.aine_menu.get()
        return AINED.get(valik)

    def ava_punktide_sisestus(self):
        aine = self.leia_aine_võti()
        if not aine:
            messagebox.showerror("Viga", "Palun vali aine.")
            return
        alampiirid, max_punktid, hinded, punktid_hindeks = fn.loe_aine_fail(aine)
        if not max_punktid:
            messagebox.showerror("Viga", "Seda aineandmeid ei leitud.")
            return
        # kasuta esimest plokki enne 'UUS'
        kategooriad = max_punktid[0]

        # puhasta varasemad
        for laps in self.kategooria_raam.winfo_children():
            laps.destroy()
        self.sisend_muutujad = {}

        tk.Label(self.kategooria_raam, text=f"Sisesta punktid ainele: {aine}", font=(None, 12, 'bold')).pack(anchor='w')
        rida = tk.Frame(self.kategooria_raam)
        rida.pack(fill=tk.X, pady=4)

        for k, maks in kategooriad.items():
            alamraam = tk.Frame(self.kategooria_raam)
            alamraam.pack(fill=tk.X, pady=2)
            tk.Label(alamraam, text=f"{k} (max {maks}):", width=30, anchor='w').pack(side=tk.LEFT)
            muutuja = tk.StringVar()
            # eelkomplekteeri salvestatud andmetest kui olemas
            aine_salvestatud = self.salvestatud_andmed.get(aine, {})
            if aine_salvestatud and k in aine_salvestatud and aine_salvestatud[k] is not None:
                olemasolevad = aine_salvestatud[k]
                if isinstance(olemasolevad, list):
                    muutuja.set(",".join(str(x) for x in olemasolevad if x is not None))
            sisend = tk.Entry(alamraam, textvariable=muutuja, width=60, font=self.teksti_font)
            sisend.pack(side=tk.LEFT, padx=4)
            self.sisend_muutujad[k] = (muutuja, maks)

        tk.Button(self.kategooria_raam, text="Salvesta kategooria punktid", command=lambda a=aine: self.salvesta_punktid(a)).pack(pady=8)

        # Menüü fondi suuruse muutmiseks
        menüüriba = tk.Menu(self)
        vaata_menüü = tk.Menu(menüüriba, tearoff=0)
        vaata_menüü.add_command(label="Suurenda teksti", command=lambda: self.muuda_fondi_suurust(2))
        vaata_menüü.add_command(label="Vähenda teksti", command=lambda: self.muuda_fondi_suurust(-2))
        menüüriba.add_cascade(label="Vaata", menu=vaata_menüü)
        self.config(menu=menüüriba)

    def salvesta_punktid(self, aine):
        edukus, sõnum, uuendatud_andmed = fn.valideeri_ja_salvesta(aine, self.sisend_muutujad, self.salvestatud_andmed)
        if not edukus:
            messagebox.showerror("Viga", sõnum)
            return
        # värskenda salvestatud andmed
        self.salvestatud_andmed = uuendatud_andmed
        messagebox.showinfo("Salvestatud", f"Punktid salvestatud ainele {aine}.")
        

    def kuva_salvestatud(self):
        self.väljund.delete('1.0', tk.END)
        aine = self.leia_aine_võti()
    
        tekst = fn.kuvamiseks_andmed(aine, self.salvestatud_andmed)
        self.väljund.insert(tk.END, tekst)

    def salvesta_kõik(self):
        fn.salvesta_kohalikult(self.salvestatud_andmed)
        messagebox.showinfo("Salvestatud", "Andmed salvestatud kettale.")

    def arvuta_hinne_kuva(self):
        self.väljund.delete('1.0', tk.END)
        aine = self.leia_aine_võti()
        if not aine:
            messagebox.showerror("Viga", "Palun vali aine.")
            return
        alampiirid, max_punktid, hinded, punktid_hindeks = fn.loe_aine_fail(aine)
        aine_punktid = self.salvestatud_andmed.get(aine)
        if not aine_punktid:
            messagebox.showerror("Viga", "Punktid selle aine jaoks puuduvad. Sisesta punktid enne arvutamist.")
            return
        # kutsub arvuta_hinne et kuvada tulemused
        fn.arvuta_hinne(aine_punktid, alampiirid, punktid_hindeks, hinded, väljund=self.väljund)

    def muuda_fondi_suurust(self, delta): 
        uus_suurus = max(8, self.teksti_font['size'] + delta)
        self.teksti_font.configure(size=uus_suurus)

if __name__ == "__main__":
    app = App()
    app.mainloop()
