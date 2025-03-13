from tkinter import *
from tkinter import ttk, messagebox, filedialog
import json







class MediaPlayer():
    def __init__(self):
        self.root=Tk()
        self.root.title("Video Oynatıcı")
        self.root.geometry("300x720+320+150")
        #self.root.resizable(False, False)

        



        self.frameSol=Frame(self.root, width=300, height=720)


        self.frameSol.pack(side="left", fill="both", expand=True)

        




        self.aramaCubugu=Entry(self.frameSol, width=17, font=("Airal", 14))
        self.araButon=Button(self.frameSol, text="Ara", width=5, height=1, command=self.ara)
        self.filtreButon=Button(self.frameSol, width=5, height=1, text="Filtrele", command=self.filtrele)
        self.liste=Listbox(self.frameSol, width=26, height=20, font=("Airal", 14))
        self.liste.bind("<ButtonRelease-1>", self.bilgi_goster)
        self.bilgilerLabel=Label(self.frameSol, width=26, height=6, font=("Airal", 14), bg="white")


        self.ekleButon=Button(self.frameSol, text="Ekle", width=19, command=self.ekle)
        self.silButon=Button(self.frameSol, text="Sil", width=19, command=self.sil)
        self.duzenleButon=Button(self.frameSol, text="Düzenle", width=40, command=self.duzenle)


        self.araButon.place(x=200, y=5)
        self.aramaCubugu.place(x=5, y=5)
        self.filtreButon.place(x=250, y=5)
        self.bilgilerLabel.place(x=5, y=510)

        self.ekleButon.place(x=5, y=660)
        self.silButon.place(x=152, y=660)
        self.duzenleButon.place(x=5, y=690)

        self.liste.place(x=5, y=40)
        self.guncelle()
        self.root.mainloop()

 

    def bilgi_goster(self, event):
        veriler=self.loadfromJSON()
        secili_indeks=self.liste.curselection()[0]

        for index, i in enumerate(veriler):
            if i["ad"]==self.liste.get(secili_indeks):
                self.bilgilerLabel.config(text=f"Ad: {i["ad"]}\nTür: {i["tur"]}\nDurum: {i["durum"]}\nYıldız: {i["yildiz"]}\nNot: {i["not"]}")

    def filtrele(self):
        self.filtrele_root=Toplevel()
        self.filtrele_root.geometry("590x280+710+300")

        spinbox_var=StringVar()
        spinbox_var.set("")
        
        self.filtreleAdEntry=Entry(self.filtrele_root)
        self.filtreleTurCombobox=ttk.Combobox(self.filtrele_root, values=["Dizi", "Film"])
        self.filtreleDurumCombobox=ttk.Combobox(self.filtrele_root, values=["İzlendi", "İzleniyor", "İzlenecek"])
        self.filtreleYildizSpinbox=Spinbox(self.filtrele_root, from_=1, to=5, textvariable=spinbox_var)
        self.filtreleYildizSpinbox.delete(0, "end")
        self.filtreleNotEntry=Entry(self.filtrele_root)

        adLabel=Label(self.filtrele_root, text="Ad:", font=("Airal", 20), width=20)
        turLabel=Label(self.filtrele_root, text="Tür:", font=("Airal", 20), width=20)
        durumLabel=Label(self.filtrele_root, text="Durum:", font=("Airal", 20), width=20)
        yildizLabel=Label(self.filtrele_root, text="Yıldız:", font=("Airal", 20), width=20)
        notLabel=Label(self.filtrele_root, text="Not:", font=("Airal", 20), width=20)

        filtreleButon=Button(self.filtrele_root, text="Filtrele", command=self.filtrele_islemi)
        

        adLabel.grid(row=0, column=0)
        self.filtreleAdEntry.grid(row=0, column=1)
        
        turLabel.grid(row=1, column=0)
        self.filtreleTurCombobox.grid(row=1, column=1)

        durumLabel.grid(row=2, column=0)
        self.filtreleDurumCombobox.grid(row=2, column=1)

        yildizLabel.grid(row=3, column=0)
        self.filtreleYildizSpinbox.grid(row=3, column=1)

        notLabel.grid(row=4, column=0)
        self.filtreleNotEntry.grid(row=4, column=1)

        filtreleButon.grid(row=5, column=0, sticky="e")
        

    def filtrele_islemi(self):
        
        ad=self.filtreleAdEntry.get() if self.filtreleAdEntry.get()!="" else None
        tur=self.filtreleTurCombobox.get() if self.filtreleTurCombobox.get()!="" else None
        durum=self.filtreleDurumCombobox.get() if self.filtreleDurumCombobox.get()!="" else None
        yildiz=self.filtreleYildizSpinbox.get() if self.filtreleYildizSpinbox.get()!="" else None
        note=self.filtreleNotEntry.get() if self.filtreleNotEntry.get()!="" else None

        veriler=self.loadfromJSON()
        liste=list()
        
        

        for i in veriler:
            if ((ad==None or ad in i["ad"]) and 
                (tur==None or i["tur"]==tur) and 
                (durum==None or i["durum"]==durum) and 
                (yildiz==None or i["yildiz"]==yildiz) and 
                (note==None or i["not"]==note)):

                liste.append(i)

        self.liste.delete(0, END)

        if liste:
            for i in liste:
                self.liste.insert(END, i["ad"])
        
        self.filtrele_root.destroy()

    def ara(self):
        if self.aramaCubugu.get()!="":
            ad=self.aramaCubugu.get()
            veriler=self.loadfromJSON()
            videolar=list()
            for i in veriler:
                if ad in i["ad"]:
                    videolar.append(i)
                    
            self.liste.delete(0, END)
            for i in videolar:
                self.liste.insert(END, i["ad"])  
                      

        else:
            self.guncelle()

    def duzenle(self):
        secili_indeks=self.liste.curselection()
        if secili_indeks:
            self.duzenle_popup()

    def duzenle_popup(self):
        self.duzenlePopup_root=Toplevel()
        self.duzenlePopup_root.geometry("500x250+710+300")

        spinbox_var=StringVar()
        spinbox_var.set("")

        self.duzenleAdEntry=Entry(self.duzenlePopup_root)
        self.duzenleTurCombobox=ttk.Combobox(self.duzenlePopup_root, values=["Dizi", "Film"])
        self.duzenleDurumCombobox=ttk.Combobox(self.duzenlePopup_root, values=["İzlendi", "İzleniyor", "İzlenecek"])
        self.duzenleYildizSpinbox=Spinbox(self.duzenlePopup_root, from_=1, to=5)
        self.duzenleYildizSpinbox.delete(0, "end")
        self.duzenleNotEntry=Entry(self.duzenlePopup_root)

        adLabel=Label(self.duzenlePopup_root, text="Ad:", font=("Airal", 20), width=20)
        turLabel=Label(self.duzenlePopup_root, text="Tür:", font=("Airal", 20), width=20)
        durumLabel=Label(self.duzenlePopup_root, text="Durum:", font=("Airal", 20), width=20)
        yildizLabel=Label(self.duzenlePopup_root, text="Yıldız:", font=("Airal", 20), width=20)
        notLabel=Label(self.duzenlePopup_root, text="Not:", font=("Airal", 20), width=20)

        kaydetButon=Button(self.duzenlePopup_root, text="Kaydet", command=self.duzenle_islemi)

        adLabel.grid(row=0, column=0)
        self.duzenleAdEntry.grid(row=0, column=1)
        
        turLabel.grid(row=1, column=0)
        self.duzenleTurCombobox.grid(row=1, column=1)

        durumLabel.grid(row=2, column=0)
        self.duzenleDurumCombobox.grid(row=2, column=1)

        yildizLabel.grid(row=3, column=0)
        self.duzenleYildizSpinbox.grid(row=3, column=1)

        notLabel.grid(row=4, column=0)
        self.duzenleNotEntry.grid(row=4, column=1)

        kaydetButon.grid(row=5, column=0, columnspan=2)
        
    def duzenle_islemi(self):
    
        secili_indeks=self.liste.curselection()[0]
        veriler=self.loadfromJSON()
        
        

        for i in veriler:
            if i["ad"]==self.liste.get(secili_indeks):
                currentVideo=i
        
        currentVideo["ad"]=currentVideo["ad"] if self.duzenleAdEntry.get()=="" else self.duzenleAdEntry.get()
        currentVideo["tur"]=currentVideo["tur"] if self.duzenleTurCombobox.get()=="" else self.duzenleTurCombobox.get()
        currentVideo["durum"]=currentVideo["durum"] if self.duzenleDurumCombobox.get()=="" else self.duzenleDurumCombobox.get()
        currentVideo["yildiz"]=currentVideo["yildiz"] if self.duzenleYildizSpinbox.get()=="" else self.duzenleYildizSpinbox.get()
        currentVideo["not"]=currentVideo["not"] if self.duzenleNotEntry.get()=="" else self.duzenleNotEntry.get()

        self.savetoJSON(veriler)
        self.duzenlePopup_root.destroy()
        self.guncelle()


    def guncelle(self):
        self.liste.delete(0, END)


        with open("veriler.json", "r", encoding="utf-8") as file:
            veriler=json.load(file)

        for i in veriler:
            self.liste.insert(END, i["ad"])

    
    def ekle(self):
        self.ekle_root=Toplevel(self.root)
        self.ekle_root.geometry("500x280+710+300")

        self.adEntry=Entry(self.ekle_root)
        self.turCombobox=ttk.Combobox(self.ekle_root, values=["Dizi", "Film"])
        self.durumCombobox=ttk.Combobox(self.ekle_root, values=["İzlendi", "İzleniyor", "İzlenecek"])
        self.yildizSpinbox=Spinbox(self.ekle_root, from_=1, to=5)
        self.notEntry=Entry(self.ekle_root)

        adLabel=Label(self.ekle_root, text="Ad:", font=("Airal", 20), width=20)
        turLabel=Label(self.ekle_root, text="Tür:", font=("Airal", 20), width=20)
        durumLabel=Label(self.ekle_root, text="Durum:", font=("Airal", 20), width=20)
        yildizLabel=Label(self.ekle_root, text="Yıldız:", font=("Airal", 20), width=20)
        notLabel=Label(self.ekle_root, text="Not:", font=("Airal", 20), width=20)


        ekleButon=Button(self.ekle_root, text="Ekle", command=self.check, font=("Airal", 15))

        adLabel.grid(row=0, column=0)
        self.adEntry.grid(row=0, column=1)

        turLabel.grid(row=1, column=0)
        self.turCombobox.grid(row=1, column=1)

        durumLabel.grid(row=2, column=0)
        self.durumCombobox.grid(row=2, column=1)

        yildizLabel.grid(row=3, column=0)
        self.yildizSpinbox.grid(row=3, column=1)

        notLabel.grid(row=4, column=0)
        self.notEntry.grid(row=4, column=1)

        
        ekleButon.grid(row=6, column=0, columnspan=2)



    def sil(self):
        secili_indeks=self.liste.curselection()
        if secili_indeks:
            self.sil_pupop()
            


    def sil_pupop(self):
        self.silPupop_root=Toplevel()
        self.silPupop_root.geometry("300x100+830+350")
        bilgiLabel=Label(self.silPupop_root, text="Bu videoyu listeden silmek istediğinize emin misiniz?")
        yesButton=Button(self.silPupop_root, text="Evet", command=self.sil_islemi)
        noButton=Button(self.silPupop_root, text="Hayır", command=self.silPupop_root.destroy)

        bilgiLabel.grid(row=0, column=0, columnspan=2)
        yesButton.grid(row=1, column=0, pady=20)
        noButton.grid(row=1,column=1, pady=20)

    def sil_islemi(self):
            
            veriler=self.loadfromJSON()
            secili_indeks=self.liste.curselection()[0]
            
            for index, i in enumerate(veriler):
                if i["ad"]==self.liste.get(secili_indeks):
                    veriler.pop(index)
            
            


            
            self.savetoJSON(veriler)
            self.guncelle()
            self.silPupop_root.destroy()
            self.bilgilerLabel.config(text="")
            





    def ekle_2(self):
        ad=self.adEntry.get()
        tur=self.turCombobox.get()
        durum=self.durumCombobox.get()
        yildiz=self.yildizSpinbox.get()
        note=self.notEntry.get()
        
        

        data={
            "ad": ad,
            "tur": tur,
            "durum": durum,
            "yildiz": yildiz,
            "not": note
        }

        veriler=self.loadfromJSON()
        veriler.append(data)
        self.savetoJSON(veriler)

        self.popup_root.destroy()
        self.ekle_root.destroy()
        
        self.guncelle()






    def check(self):
        if self.adEntry.get()!="" and self.turCombobox.get()!="" and self.durumCombobox.get()!="":
            self.popup_eminMisin()
        else:
            self.ekle_root.destroy()
            messagebox.showerror("Hata", "Alanları Doldurunuz!")

    def popup_eminMisin(self):
        self.popup_root=Toplevel()
        self.popup_root.geometry("200x100+855+350")
        bilgiLabel=Label(self.popup_root, text="Kaydetmek istediğinize emin misiniz?")
        yesButton=Button(self.popup_root, text="Evet", command=self.ekle_2, width=5)
        noButton=Button(self.popup_root, text="Hayır", width=5)        

        bilgiLabel.grid(row=0, column=0, columnspan=2)
        yesButton.grid(row=1, column=0)
        noButton.grid(row=1, column=1)

    def savetoJSON(self, data, filename="veriler.json"):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def loadfromJSON(self, filename="veriler.json"):
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
        
    






app=MediaPlayer()