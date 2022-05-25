import tkinter as tk
import sqlite3
from tkcalendar import DateEntry
from tkinter import ttk
from tkinter.messagebox import showinfo, showwarning, showerror

veritabanı = sqlite3.connect("HavalimanıYönetimSistemi.db")
işleç = veritabanı.cursor()




def menüGüncelle():
    liste = ["Uçuş Seçiniz"]
    uçuşKontrol = veritabanı.execute("SELECT UÇAK_KODU FROM UÇUŞ_TABLO").fetchall()
    for uçuş in uçuşKontrol:
        liste.append(uçuş[0])
    ttk.OptionMenu(solAltÇerçeve,uçuşKodu2,*liste).place(x=48,y=220,relwidth=0.5)

def uçuşKayıtGöster():
    ortaVeritabanı.delete(*ortaVeritabanı.get_children())
    veritabanıGetir = veritabanı.execute("SELECT * FROM UÇUŞ_TABLO")
    veriler = veritabanıGetir.fetchall()

    for veri in veriler:
        ortaVeritabanı.insert("",tk.END,values=veri)

def yolcuKayıtGöster():
    altVeritabanı.delete(*altVeritabanı.get_children())
    veritabanıGetir = veritabanı.execute("SELECT * FROM YOLCU_TABLO")
    veriler = veritabanıGetir.fetchall()

    for veri in veriler:
        altVeritabanı.insert("",tk.END,values=veri) 


def uçuşKayıtEkle():
    neredenDB = nereden.get()
    nereyeDB = nereye.get()
    uçuşKoduDB = uçuşKodu.get()
    tarihDB = tarihMenü.get_date()
    
    if neredenDB == "Şehir Seçiniz" or nereyeDB == "Şehir Seçiniz" or uçuşKoduDB == "Uçuş Seçiniz":
        showerror(title="Hata!",message="Lütfen Eksik Bilgileri Doldur!")
    else:
        try:
            veritabanı.execute("INSERT INTO UÇUŞ_TABLO (UÇAK_KODU,NEREDEN,NEREYE,TARİH) VALUES (?,?,?,?)",(uçuşKoduDB,neredenDB,nereyeDB,tarihDB))
            veritabanı.commit()
            showinfo(title="Başarılı",message="Uçuş Kayıt Ekleme İşlemi Başarılı!")
            uçuşKayıtGöster()
            menüGüncelle()
        except sqlite3.IntegrityError:
            showerror(title="Hata!",message="Aynı Koda Sahip Bir Uçak Bulunmakta!")


def uçuşKayıtKaldır():
    if not ortaVeritabanı.selection():
        showwarning(title="Hata!",message="Herhangi Bir Kayıt Seçmeden Silme İşlemi Yapamazsın!")
    else:
        mevcutVeri = ortaVeritabanı.focus()
        veriler = ortaVeritabanı.item(mevcutVeri)
        seçim = veriler['values']
        
        ortaVeritabanı.delete(mevcutVeri)
        veritabanı.execute(f"DELETE FROM UÇUŞ_TABLO WHERE UÇAK_KODU = {seçim[0]}")
        veritabanı.execute(f"DELETE FROM YOLCU_TABLO WHERE UÇUŞ_KODU = {seçim[0]}")
        veritabanı.commit()
        showinfo(title="Başarılı",message="Uçuş Kayıt Kaldırma İşlemi Başarılı!")
        uçuşKayıtGöster()
        yolcuKayıtGöster()
        menüGüncelle()


def yolcuKayıtEkle():
    isimDB = isim.get()
    soyİsimDB = soyİsim.get()
    uçuşKodu2DB = uçuşKodu2.get()
    uçuşKontrol = veritabanı.execute("SELECT UÇAK_KODU FROM UÇUŞ_TABLO").fetchall()
    TCDB = TC.get()

    if not isimDB or not soyİsimDB or not uçuşKodu2DB or not TCDB:
        showerror(title="Hata!",message="Lütfen Eksik Bilgileri Doldur!")
    elif uçuşKodu2DB == "Uçuş Seçiniz":
        showwarning(title="Uyarı!",message="Lütfen Uçuş Kodunu Seç!")
    else:
        try:
            for uçuş in uçuşKontrol:
                if uçuşKodu2DB == uçuş[0]:
                    veritabanı.execute(f"INSERT INTO YOLCU_TABLO (TC,İSİM,SOY_İSİM,UÇUŞ_KODU) VALUES(?,?,?,?)",(TCDB,isimDB,soyİsimDB,uçuşKodu2DB))
                    veritabanı.commit()
                    showinfo(title="Başarılı",message="Kayıt Ekleme İşlemi Tamamlandı!")
                    yolcuKayıtGöster()
                    break
            
        except sqlite3.IntegrityError:
            showerror(title="Hata!",message="Aynı Kimlik Numarasına Sahip Bir Yolcu Bulunmakta!")

def yolcuKayıtKaldır():
    if not altVeritabanı.selection():
        showwarning(title="Hata!",message="Herhangi Bir Kayıt Seçmeden Silme İşlemi Yapamazsın!")
    else:
        mevcutVeri = altVeritabanı.focus()
        veriler = altVeritabanı.item(mevcutVeri)
        seçim = veriler['values']
        
        altVeritabanı.delete(mevcutVeri)
        veritabanı.execute(f"DELETE FROM YOLCU_TABLO WHERE TC = {seçim[0]}")
        veritabanı.commit()


        showinfo(title="İşlem Başarılı",message="Kayıt Kaldırma İşlemi Tamamlandı")
        yolcuKayıtGöster()



root = tk.Tk()
root.geometry("1250x700")
root.title("Havalimanı Yönetim Sistemi")
photo = tk.PhotoImage(file = "Files/plane.png")
root.iconphoto(False, photo)
nereden = tk.StringVar()
nereye = tk.StringVar()
uçuşKodu = tk.StringVar()
uçuşKodu2 = tk.StringVar()
isim = tk.StringVar()
soyİsim = tk.StringVar()
TC = tk.StringVar()

root.resizable(False,False)
başlıkÇerçeve = tk.Frame(root,bg="#40444F")
başlıkÇerçeve.place(x=0,y=0,relheight=0.3,relwidth=1)
üstÇerçeve = tk.Frame(root,bg="#D12335")
üstÇerçeve.place(x=0,y=30,relheight=0.5,relwidth=0.5)
solÜstÇerçeve = tk.Frame(root,bg="#9D1B28")
solÜstÇerçeve.place(x=0,y=60,relheight=0.5,relwidth=0.25)
solOrtaÇerçeve = tk.Frame(root,bg="#009DDC")
solOrtaÇerçeve.place(x=0,y=380,relheight=0.5,relwidth=0.25)
solAltÇerçeve = tk.Frame(root,bg="#0075A3")
solAltÇerçeve.place(x=0,y=410,relheight=0.5,relwidth=0.25)
araÇerçeve = tk.Frame(root,bg="#2A2D34")
araÇerçeve.place(x=250,y=30,relheight=1,relwidth=0.3)
ortaÇerçeve = tk.Frame(root,bg="#D12335")
ortaÇerçeve.place(x=270,y=30,relheight=0.5,relwidth=1)
altÇerçeve = tk.Frame(root,bg="#009DDC")
altÇerçeve.place(x=270,y=380,relheight=0.5,relwidth=1)



isimYazı = ttk.Label(başlıkÇerçeve,text="HAVALİMANI YÖNETİM SİSTEMİ",font=("Calibri",17,"bold"),background="#40444F",foreground="White").place(x=500,y=0)
uçuşKayıtYazı = ttk.Label(üstÇerçeve,font=("Calibri",15,"bold"),text="Uçuş Kayıt",background="#D12335",foreground="White").place(x=79,y=0)

neredenYazı = ttk.Label(solÜstÇerçeve,text="Nereden",font=("Calibri",10,"bold"),background="#9D1B28",foreground="White").place(x=95,y=15)
neredenMenü = ttk.OptionMenu(solÜstÇerçeve,nereden,'Şehir Seçiniz','Adana','Ankara','Antalya','Hatay','Mersin','İstanbul','İzmir','Batman').place(x=48,y=35,relwidth=0.5)

nereyeYazı = ttk.Label(solÜstÇerçeve,text="Nereye",font=("Calibri",10,"bold"),background="#9D1B28",foreground="White").place(x=95,y=75)
nereyeMenü = ttk.OptionMenu(solÜstÇerçeve,nereye,'Şehir Seçiniz','Adana','Ankara','Antalya','Hatay','Mersin','İstanbul','İzmir','Batman').place(x=48,y=95,relwidth=0.5)

uçuşKoduYazı = ttk.Label(solÜstÇerçeve,text="Uçuş Kodu",font=("Calibri",10,"bold"),background="#9D1B28",foreground="White").place(x=95,y=135)
uçuşKoduMenü = ttk.OptionMenu(solÜstÇerçeve,uçuşKodu,'Uçuş Seçiniz','1','2','3','4','5','6','7').place(x=48,y=155,relwidth=0.5)

tarihYazı = ttk.Label(solÜstÇerçeve,text="Tarih",font=("Calibri",10,"bold"),background="#9D1B28",foreground="White").place(x=100,y=195)
tarihMenü = DateEntry(solÜstÇerçeve,width=15)
tarihMenü.place(x=48,y=215,relwidth=0.5)





rezervasyonYazı = ttk.Label(solOrtaÇerçeve,text="Yolcu Rezervasyon",background="#009DDC",font=("Calibri",15,"bold"),foreground="White").place(x=55,y=0)

isimYazı = ttk.Label(solAltÇerçeve,text="İsim",font=("Calibri",10,"bold"),background="#0075A3",foreground="White").place(x=110,y=15)
isimGiriş = ttk.Entry(solAltÇerçeve,textvariable=isim).place(x=48,y=35,relwidth=0.5)

soyİsimYazı = ttk.Label(solAltÇerçeve,text="Soy İsim",font=("Calibri",10,"bold"),background="#0075A3",foreground="White").place(x=100,y=75)
soyİsimGiriş = ttk.Entry(solAltÇerçeve,textvariable=soyİsim).place(x=48,y=100,relwidth=0.5)

TCYazı = ttk.Label(solAltÇerçeve,text="TC Kimlik Numarası",font=("Calibri",10,"bold"),background="#0075A3",foreground="White").place(x=77,y=140)
TCGiriş = ttk.Entry(solAltÇerçeve,textvariable=TC).place(x=48,y=160,relwidth=0.5)

uçuşKoduYazı2 = ttk.Label(solAltÇerçeve,text="Uçuş Kodu",font=("Calibri",10,"bold"),background="#0075A3",foreground="White").place(x=95,y=200)





menüGüncelle()

uçuşEkleButon = ttk.Button(solÜstÇerçeve,text="Uçuş Ekle",command=uçuşKayıtEkle).place(x=48,y=265)
uçuşKaldırButon = ttk.Button(solÜstÇerçeve,text="Uçuş Kaldır",command=uçuşKayıtKaldır).place(x=128,y=265)
yolcuEkleButon = ttk.Button(solAltÇerçeve,text="Yolcu Ekle",command=yolcuKayıtEkle).place(x=48,y=260)
yolcuKaldırButon = ttk.Button(solAltÇerçeve,text="Yolcu Kaldır",command=yolcuKayıtKaldır).place(x=128,y=260)

ortaVeritabanıYazı = ttk.Label(ortaÇerçeve,text="UÇUŞ VERİTABANI",font=("Calibri",17,"bold"),background="#D12335",foreground="white").place(x=380,y=0)
ortaVeritabanı = ttk.Treeview(ortaÇerçeve,height=100,selectmode=tk.BROWSE,columns=("Uçak Kodu","Nereden","Nereye","Tarih"))
ortaVeritabanı.place(x=0,y=30,relheight=1,relwidth=0.8)
yview = tk.YView
dikeyKaydırmaÇubuğu = tk.Scrollbar(ortaVeritabanı,orient=tk.VERTICAL,command=ortaVeritabanı.yview)
dikeyKaydırmaÇubuğu.pack(side=tk.RIGHT,fill=tk.Y)
ortaVeritabanı.config(yscrollcommand=dikeyKaydırmaÇubuğu.set)

ortaVeritabanı.heading("Uçak Kodu",text="Uçak Kodu",anchor=tk.CENTER)
ortaVeritabanı.heading("Nereden",text="Nereden",anchor=tk.CENTER)
ortaVeritabanı.heading("Nereye",text="Nereye",anchor=tk.CENTER)
ortaVeritabanı.heading("Tarih",text="Tarih",anchor=tk.CENTER)
ortaVeritabanı.column("#0",width=0,stretch=tk.NO)

altVeritabanıYazı = ttk.Label(altÇerçeve,text="YOLCU VERİTABANI",font=("Calibri",17,"bold"),background="#009DDC",foreground="White").place(x=378)
altVeritabanı = ttk.Treeview(altÇerçeve,height=100,selectmode=tk.BROWSE,columns=("TC Kimlik Numarası","İsim","Soy İsim","Uçuş Kodu"))
altVeritabanı.place(x=0,y=30,relheight=1,relwidth=0.8)
dikeyKaydırmaÇubuğu2 = tk.Scrollbar(altVeritabanı,orient=tk.VERTICAL,command=altVeritabanı.yview)
dikeyKaydırmaÇubuğu2.pack(side=tk.RIGHT,fill=tk.Y)
altVeritabanı.config(yscrollcommand=dikeyKaydırmaÇubuğu2.set)
altVeritabanı.heading("TC Kimlik Numarası",text="TC Kimlik Numarası",anchor=tk.CENTER)
altVeritabanı.heading("İsim",text="İsim",anchor=tk.CENTER)
altVeritabanı.heading("Soy İsim",text="Soy İsim",anchor=tk.CENTER)
altVeritabanı.heading("Uçuş Kodu",text="Uçuş Kodu",anchor=tk.CENTER)
altVeritabanı.column("#0",width=0,stretch=tk.NO)


try:
    veritabanı.execute("CREATE TABLE IF NOT EXISTS UÇUŞ_TABLO (UÇAK_KODU TEXT PRIMARY KEY NOT NULL, NEREDEN TEXT NOT NULL, NEREYE TEXT NOT NULL, TARİH TEXT)")
    veritabanı.execute("CREATE TABLE IF NOT EXISTS YOLCU_TABLO (TC INTEGER PRIMARY KEY NOT NULL,İSİM TEXT NOT NULL, SOY_İSİM TEXT NOT NULL, UÇUŞ_KODU TEXT NOT NULL)")
    uçuşKayıtGöster()
    yolcuKayıtGöster()
except Exception as e:
    showerror(title="Hata!",message="Bilinmeyen Bir Hata Oluştu!")


root.mainloop()


