import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont
import funktsioonid as fn # funktsioonid

# Ained ja nende nimetus xlsx tabelis
AINED = {
    "Programmeerimine": "Programmeerimine 1",
    "Arvuti arhitektuur ja riistvara 1": "AAR 1",
    "Operatsioonisüsteemid": "Opsys",
    "Kõrgem matemaatika 1": "KÕM 1",
    "Sissejuhatus erialasse": "Sissejuhatus erialasse"
}

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hinde arvutaja - GUI")
        self.geometry("900x600")

        # jagatud font teksti ja sisendväljade jaoks
        self.teksti_font = tkfont.Font(family="TkFixedFont", size=12)

        self.salvestatud_andmed = fn.loe_kohalikud_andmed()
        if self.salvestatud_andmed is None:
            self.salvestatud_andmed = {}

        # UI elements
        top = tk.Frame(self)
        top.pack(fill=tk.X, padx=10, pady=8)

        tk.Label(top, text="Vali aine:").pack(side=tk.LEFT)
        self.aine_muutuja = tk.StringVar()
        ainete_nimistik = list(AINED.keys())
        self.aine_menu = ttk.Combobox(top, values=ainete_nimistik, state='readonly', width=30)
        self.aine_menu.current(0)
        self.aine_menu.pack(side=tk.LEFT, padx=6)

        btn_frame = tk.Frame(top)
        btn_frame.pack(side=tk.RIGHT)

        tk.Button(btn_frame, text="Sisesta punktid", command=self.ava_punktide_sisestus).pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text="Arvuta hinne", command=self.arvuta_hinne_kuva).pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text="Loe salvestatud andmed", command=self.kuva_salvestatud).pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text="Salvesta andmed", command=self.salvesta_kõik).pack(side=tk.LEFT, padx=4)

        # Põhisisu ala
        self.sisu = tk.Frame(self)
        self.sisu.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

        # Kategooriad kuvatakse siin
        self.kategooria_raam = tk.Frame(self.sisu)
        self.kategooria_raam.pack(fill=tk.BOTH, expand=True)

        # Väljundteksti ala
        self.väljund = tk.Text(self.sisu, height=15, font=self.teksti_font)
        self.väljund.pack(fill=tk.X, pady=8)

        # sisendite muutujad salvestatakse siia
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
                # ühenusta loendi väärtused komadega
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
        # ehita aine punktide struktuur
        aine_punktid = {}
        for k, (muutuja, maks) in self.sisend_muutujad.items():
            tekst = muutuja.get().strip()
            if tekst == "":
                aine_punktid[k] = None
                continue
            # analüüsi komadega eraldatud numbrid
            osad = [i.strip() for i in tekst.split(',') if i.strip() != ""]
            väärtused = []
            summa = 0
            kehtiv = True
            for i in osad:
                try:
                    v = float(i)
                    if v < 0:
                        kehtiv = False
                        break
                    summa += v
                    väärtused.append(v)
                except ValueError:
                    kehtiv = False
                    break
            if not kehtiv or summa > maks:
                messagebox.showerror("Viga", f"Kehtetud väärtused kategoorias {k} või summa ületab maksi ({maks}).")
                return
            aine_punktid[k] = väärtused

        # salvesta salvestatud_andmete sisse ja säilita
        self.salvestatud_andmed.setdefault(aine, {})
        self.salvestatud_andmed[aine].update(aine_punktid)
        fn.salvesta_kohalikult(self.salvestatud_andmed)

        messagebox.showinfo("Salvestatud", f"Punktid salvestatud ainele {aine}.")
        
        # puhasta kategooria raam (menüü kaob ära)
        for laps in self.kategooria_raam.winfo_children():
            laps.destroy()
        self.sisend_muutujad = {}

    def kuva_salvestatud(self):
        self.väljund.delete('1.0', tk.END)
        if not self.salvestatud_andmed:
            self.väljund.insert(tk.END, "Salvestatud andmed puuduvad.\n")
            return
        for aine, kateg in self.salvestatud_andmed.items():
            self.väljund.insert(tk.END, f"Aine: {aine}\n")
            for k, v in kateg.items():
                self.väljund.insert(tk.END, f"  {k}: {v}\n")
            self.väljund.insert(tk.END, "\n")

    def salvesta_kõik(self):
        fn.salvesta_kohalikult(self.salvestatud_andmed)
        messagebox.showinfo("Salvestatud", "Andmed salvestatud kettale.")

    def arvuta_hinne_kuva(self):
        aine = self.leia_aine_võti()
        if not aine:
            messagebox.showerror("Viga", "Palun vali aine.")
            return
        alampiirid, max_punktid, hinded, punktid_hindeks = fn.loe_aine_fail(aine)
        aine_punktid = self.salvestatud_andmed.get(aine)
        if not aine_punktid:
            messagebox.showerror("Viga", "Punktid selle aine jaoks puuduvad. Sisesta punktid enne arvutamist.")
            return
        try:
            # kutsu arvuta_hinne et kuvada tulemused
            fn.arvuta_hinne_gui(aine_punktid, alampiirid, punktid_hindeks, hinded, self, tk)
            # arvuta ka kokku punkte
            kokku_punkte = 0
            for k, väärtused in aine_punktid.items():
                if isinstance(väärtused, list):
                    for v in väärtused:
                        if v is not None:
                            kokku_punkte += v
            self.väljund.delete('1.0', tk.END)
            self.väljund.insert(tk.END, f"Kokku punkte: {round(kokku_punkte,2)}\n")
            self.väljund.insert(tk.END, "Vaata täpsemat tulemust konsoolist (arvutus logitakse sinna).\n")
        except Exception as e:
            messagebox.showerror("Viga arvutamisel", str(e))

    def muuda_fondi_suurust(self, delta):
        uus_suurus = max(8, self.teksti_font['size'] + delta)
        self.teksti_font.configure(size=uus_suurus)

if __name__ == "__main__":
    app = App()
    app.mainloop()
