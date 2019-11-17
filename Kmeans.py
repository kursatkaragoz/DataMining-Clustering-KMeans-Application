#-------------------------------------------------------------------------------
# Name:        KMeansAlgorithm
# Purpose:
#
# Author:      Kursat
#
# Created:     26.10.2019
# Copyright:   (c) Kursat 2019
# Licence:     <10400336210>
#-------------------------------------------------------------------------------
from tkinter import *
from tkinter import Tk, Label, Button
from tkinter import ttk
from tkinter import filedialog
import openpyxl
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
import math


class Kmeans():

    def dosyaSec(self):
        try:
            self.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                  filetypes=(("CSV field", "*.csv"), ("all files", "*.*")))
            if(self.filename!=""):
                self.listekutusu.insert(0,"Dosya Yolu : {}".format(self.filename))
                self.degerleri_oku(self.filename)
                k_max_deger = []
                for i in range (2,uzunluk+1):
                    k_max_deger.append(i)
                self.kdeger["values"] = k_max_deger
# okunan x ve y değerleri grafik üzerinde gösteriliyor
                plt.xlabel("x1")
                plt.ylabel("x2")
                bc2=plt.scatter(x_degerler,y_degerler)
                plt.grid(True)
                plt.show()
        except:
            messagebox.showerror("HATA","HATALI SECİM YAPTINIZ")

    def degerleri_oku(self,yol):
        global x_degerler
        global y_degerler
        global uzunluk
        dataset = pd.read_csv(self.filename)
        x_degerler = (dataset.iloc[:,0].values)
        y_degerler =(dataset.iloc[:,1].values)
        uzunluk = x_degerler.__len__()
        self.listekutusu.insert(END,"")
        self.listekutusu.insert(END,"""Gözlem  Degisken1 Degisken2 """)
        for i in range(0,uzunluk):
            self.listekutusu.insert(END,"X{:<10}{:^15}{:^25}".format(i+1,x_degerler[i],y_degerler[i]))

        self.kdeger.configure(state="readonly")

    def k_deger(self,event=None):

            self.cendroidx=[]
            self.cendroidy=[]
            self.renkler=["red","black","purple","navy","DARKGREEN","cyan","AQUAMARINE","AZURE","BISQUE","BISQUE","BISQUE","BLANCHEDALMOND","BLUE","BLUEVIOLET"]
            k_degeri =int(self.kdeger.get())
            self.x_degerler = x_degerler
            self.y_degerler = y_degerler
            self.listekutusu.insert(END,"")
            self.listekutusu.insert(END,"K degeri {} olarak belirlendi".format(self.kdeger.get()))
            self.listekutusu.insert(END,"")

# grafik üzerinde maximum  k sayısı kadar merkez oluşturmak için x ve y noktalarının aralığı belirleniyor
# belirlenen bu iki aralık arasında k sayısı kadar random olarak merzkez nokta oluşturulacak

            xmax = max(self.x_degerler)    #x değerlerinin maximumu
            ymax = max(self.y_degerler)    #y değerlerinin maximumu

            # k adet merkez oluşturuluyor
            i=0
            self.random_merkezler = {
                i+1: [np.random.randint(1,xmax) , np.random.randint(1,ymax)]
                for i in range(k_degeri)
            }
            print(self.random_merkezler[1])
            self.listekutusu.insert(END,"")
            self.listekutusu.insert(END,"Rastgele Oluşan Merkezler")
            for i in  self.random_merkezler:
                self.listekutusu.insert(END,"Cendroid{:<10} = {:^10}".format(i,str(self.random_merkezler[i])))
            self.listekutusu.insert(END,"")
            self.gozlemGrafik.configure(state="active")

            print(self.random_merkezler)
            for i in self.random_merkezler:
                self.cendroidx.append(self.random_merkezler[i][0])
                self.cendroidy.append(self.random_merkezler[i][1])

            ##### Merkez hesapla fonksiyonu kullanılarak rastgele oluşan merkezler değerlerin uzaklığı hesaplandı ve atamalar yapıldı sonuçta yeni üyelikler bulundu
            first_cluster_membership = self.merkez_hesapla(self.cendroidx,self.cendroidy)
            self.kontrol_kume=[]
            self.kontrol_kume.append(first_cluster_membership)
            self.first_cluster_membership = first_cluster_membership

            fig = plt.figure()
            plt.xlabel("x1")
            plt.ylabel("x2")
            bc2=plt.scatter(x_degerler,y_degerler)
            i=0
            for i in self.random_merkezler.keys():
                print(self.random_merkezler[i])
                plt.scatter(*self.random_merkezler[i], color=self.renkler[i-1], s=80)

            plt.grid(True)


            fig = plt.figure()
            ax = plt.axes()
            plt.xlabel("x1")
            plt.ylabel("x2")
            plt.scatter(x_degerler, y_degerler,s=20,c=first_cluster_membership)
            plt.scatter(self.cendroidx,self.cendroidy)

            for i in range(0,len(self.cendroidx)):
                cizgi_baslangicx=self.cendroidx[i]-0.5
                cizgi_baslangicy=self.cendroidy[i]-0.5
                ax.annotate(" ",xy=(self.cendroidx[i],self.cendroidy[i]),xytext=(cizgi_baslangicx,cizgi_baslangicy),
                arrowprops=dict(arrowstyle="->"))
                text="C{}".format(i+1)
                ax.text(self.cendroidx[i]+0.2,self.cendroidy[i]+0.2,text ,ha="center",fontsize=9)
                ax.set(title="Rastgele Oluşan Merkezlere Göre Dağılım")

            plt.grid(True)
            plt.show()




    def kmeans(self):

        self.kmeans_Hesapla(self.cendroidx,self.cendroidy,self.first_cluster_membership)

    def sonGrafGoster(self):

        self.grafgoster(self.centroit_degerlerix,self.centroit_degerleriy,self.kontrol_kume)




    def gozlemDegerGrafigi(self):

        fig, ax = plt.subplots()

        plt.xlabel("x1")
        plt.ylabel("x2")
        plt.scatter(x_degerler,y_degerler)

        plt.grid(True)
        ax.set(title="Gözlem Değerlerinin Grafik Üzerinde Dağılımı")
        plt.show()


    def __init__(self,pencere):

            self.pencere = pencere
            pencere.iconbitmap(r'data.ico')
            pencere.title(""" K MEANS ALGORİTHM                                                                                    by KürşadKARAGÖZ""")
            pencere.configure(background='black')
            pencere.geometry("800x450+275+120")

            pencere.resizable(0,0)
            self.scrollbar = Scrollbar(pencere)
            self.listekutusu = Listbox(pencere , width = 127 , height = 25 ,background="black", fg="white",selectbackground="Red", yscrollcommand = self.scrollbar.set)
            self.listekutusu.place(x=10 , y = 40)
            self.scrollbar.pack(side=RIGHT , fill=Y)
            self.scrollbar.config(command=self.listekutusu.yview)

            self.dosyasecButton = Button(pencere,bg="red",font='arial 9 bold',fg="black", text = "Dosya Yolunu Belirleyiniz" ,width=21 , height = 1,command = self.dosyaSec)
            self.dosyasecButton.place(x=10,y=10)
            self.kdegerLabel = Label(pencere ,fg="black",text="K Degeri",bg="red",font='arial 9 bold')
            self.kdegerLabel.place(x=180,y=13)

            combostyle = ttk.Style()

            combostyle.theme_create('combostyle', parent='alt',
                             settings = {'TCombobox':
                                         {'configure':
                                          {'selectbackground': 'blue',
                                           'fieldbackground': 'red',
                                           'background': 'blue'
                                           }}}
                             )
    # ATTENTION: this applies the new style 'combostyle' to all ttk.Combobox
            combostyle.theme_use('combostyle')


            self.kdeger = ttk.Combobox(pencere, width=8 ,height=5, state="disabled" )
            self.kdeger.bind('<<ComboboxSelected>>',self.k_deger)
            self.kdeger.place(x=250,y=13)

            self.gozlemGrafik = Button(pencere,bg="red",font='arial 9 bold',fg="black",text= "Gözlem Değerleri Grafiği",width=25,height=1,state="disabled",command=self.gozlemDegerGrafigi)
            self.gozlemGrafik.place(x=330,y=10)

            self.cözümeBasla = Button(pencere,bg="red",font='arial 9 bold',fg="black",text="Çözüme Başla",width=15,height=1,command=self.kmeans)
            self.cözümeBasla.place(x=540,y=10)

            self.sonGraf = Button(pencere,text="Son Grafik",width=12,height=1,command=self.sonGrafGoster,bg="red",font='arial 9 bold',fg="black")
            self.sonGraf.place(x=680,y=10)




    def merkez_hesapla(self,centroit_degerlerix,centroit_degerleriy):

        kume_uyelikleri=[]
        min_index= 0
        m_uzaklik =[]
        m_uzakliklar=[]
        m_uzaklikdeger=0
        i=0
        y=0
        z=0
        print("cendroit değerleri x : {}".format(centroit_degerlerix))
        print("cendroit değerleri y : {}".format(centroit_degerleriy))
        for y in range(0,len(centroit_degerlerix)):
            for i in range(0,len(self.x_degerler)):
                self.x_degerler[i] = float(self.x_degerler[i])
                self.y_degerler[i] = float(self.y_degerler[i])
                m_uzaklikdeger=math.sqrt (pow((self.x_degerler[i])-(centroit_degerlerix[z]),2) +
                pow ((self.y_degerler[i])-(centroit_degerleriy[z]),2))
                m_uzaklik.append("{:.2f}".format(m_uzaklikdeger))
            m_uzakliklar.append(m_uzaklik)
            z +=1
            m_uzaklik = []

        self.listekutusu.insert(END,"")
        self.listekutusu.insert(END,"Merkezlerden olan uzaklıklar Hesaplandı")
        self.listekutusu.itemconfig(END,bg="black",fg="white")
        self.listekutusu.insert(END,"")
        self.listekutusu.insert(END,"""Gözlemler - Merkezlerden Uzaklıklar""")
        self.listekutusu.itemconfig(END,bg="black",fg="white")

        gecici_siralanacak_merkezler = []
        print(" Merkezden uzaklıklar: ")
        print(m_uzakliklar[0])
        print(m_uzakliklar[1])
       # print(m_uzakliklar[2])
        print("uzaklık taam")
        z=0
        i=0
        y=0
        for i in range(0,len(self.x_degerler)):
            for y in range(0,len(m_uzakliklar)):
                gecici_siralanacak_merkezler.append(float(m_uzakliklar[y][i]))

            min_index = gecici_siralanacak_merkezler.index(min(gecici_siralanacak_merkezler))
            min_index = min_index + 1
            del gecici_siralanacak_merkezler[:]
            kume_uyelikleri.append(min_index)

        print("Küme Üyeliği : {}".format(kume_uyelikleri))

        z=0
        renkler=["red","black","purple","navy","DARKGREEN","cyan","AQUAMARINE","AZURE","BISQUE","BISQUE","BISQUE","BLANCHEDALMOND","BLUE","BLUEVIOLET"]
        for y in range (0,len(centroit_degerlerix)):
            for i in range (0,len(self.x_degerler)):

                sonuc = "X{:<15}  d(M{:<1},X{:<1}) = {:^15}".format(i+1,z+1,i+1,m_uzakliklar[z][i])
                self.listekutusu.insert(END,sonuc)
                self.listekutusu.itemconfig(END,bg=renkler[z],fg="white")
                if z==14:
                    z=-1
            z +=1


        self.listekutusu.insert(END,"")
        self.listekutusu.insert(END,"Rastgele Atanan Merkezlere Göre Gözlem Değerlerinin Üyelikleri :")
        self.listekutusu.itemconfig(END,bg="purple",fg="white")
        self.listekutusu.insert(END,"")
        for i in range(0,len(kume_uyelikleri)):
            self.listekutusu.insert(END,"X{:<15} {:^15} {:^15} C{:<15}".format(i+1,self.x_degerler[i],self.y_degerler[i],kume_uyelikleri[i]))

        return kume_uyelikleri

    def kmeans_Hesapla(self,merkezx,merkezy,kumeler1):

        devamEt=True
        iterasyon = 1
        gozlem_uzunluk = len(self.x_degerler)

        while devamEt ==True:

            gecici=[]
            self.kume_gruplari = []   #aynı sınıflara ait elemanların sınıf indexleri
            self.kare_hatalari=[]
            self.centroit_degerlerix = []
            self.centroit_degerleriy = []

            self.listekutusu.insert(END,"")
            self.listekutusu.insert(END,"""
                                                                                            Çözüm için {}. iterasyon Başladı
                                             """.format(iterasyon))
            self.listekutusu.itemconfig(END,bg="purple",fg="white")
            self.listekutusu.insert(END,"")
            self.listekutusu.insert(END,"a.) Centroit Değerleri (Küme Merkezleri) Hesaplandı")
            self.listekutusu.itemconfig(END,bg="black",fg="white")
            self.listekutusu.insert(END,"")

            # aynı sınıflara ait elemanlar belirlendi ve indeksleri bir diziye aktarıldı

            print("gözlem kümeleri . {}".format(kumeler1))
            for i in range(0,gozlem_uzunluk):
                for y in range(0,gozlem_uzunluk):
                    if (i==kumeler1[y]):
                        gecici.append(y)

                if len(gecici)!=0:
                    self.kume_gruplari.append(gecici)
                gecici=[]
            print("küme grupları : {}".format(self.kume_gruplari))

            uzunluk_y_z=0
            gecici = 0
            gecicix =0
            geciciy =0

            for i in range(0,len(self.kume_gruplari)):              #merkez sayısı
                uzunluk_y_z =self.kume_gruplari[i].__len__()
                for y in range(0,uzunluk_y_z):      #merkez içindeki  i'nci dizi eleman sayısı
                    gecici = self.kume_gruplari[i][y]
                    gecicix = gecicix + self.x_degerler[gecici]
                    geciciy = geciciy + self.y_degerler[gecici]
                #print("{}'nci küme bitti".format(i))
                self.centroit_degerlerix.append("{:.2f}".format(gecicix/uzunluk_y_z))
                self.centroit_degerleriy.append("{:.2f}".format(geciciy/uzunluk_y_z))
                gecicix=0
                geciciy=0

            i=0
            # sonuçlar yazdırılıyor.
            for i in range(0,self.centroit_degerlerix.__len__()):
                sonuc="Centroit M{0} = [{1},{2}]".format(i+1,self.centroit_degerlerix[i],self.centroit_degerleriy[i])
                self.listekutusu.insert(END,sonuc)
            print("{}. iterasyon Cendroid Degerlerix : {}".format(iterasyon,self.centroit_degerlerix))
            print("{}.iterasyon Cendroid Degerleriy : {}".format(iterasyon,self.centroit_degerleriy))
            print("{}. iterasyon Küme Üyelikleri : {}".format(iterasyon,kumeler1))


            #Cendroidlerin objeler olan uzaklıkları (Küme içi Değişmeler) Hesaplanıyor
            self.listekutusu.insert(END,"")
            self.listekutusu.insert(END,"b.) Toplam Kare Hata Hesaplandı")
            self.listekutusu.itemconfig(END,bg="black",fg="white")
            self.listekutusu.insert(END,"")

            uzunluk_y_z=0
            gecici = 0
            gecicix =0
            geciciy =0
            toplam =0.0
            toplam2=0.0
            dizi1 =[]
            dizi2 =[]
            dizi1x=[]
            dizi2x=[]
            kare_hata1 = 0
            kare_hata2 = 0
            kare_hata = 0
            for i in range(0,len(self.kume_gruplari)):              #merkez sayısı
                uzunluk_y_z =self.kume_gruplari[i].__len__()
                for y in range(0,uzunluk_y_z):      #merkez içindeki  i'nci dizi eleman sayısı
                    gecici = self.kume_gruplari[i][y]
                    gecicix =self.x_degerler[gecici]
                    geciciy = self.y_degerler[gecici]
                    dizi1.append(gecicix)
                    dizi2.append(geciciy)
                dizi1x.append(dizi1)
                dizi2x.append(dizi2)
                #self.kare_hatalari.append(toplam)
                #self.kare_hatalari.append(toplam2)
                dizi1=[]
                dizi2=[]
                gecicix=0
                geciciy=0
            #print(self.kare_hatalari)

            for i in range (0,len(self.centroit_degerlerix)):
                self.centroit_degerlerix[i] = float(self.centroit_degerlerix[i])
                self.centroit_degerleriy[i] = float(self.centroit_degerleriy[i])

            e1 = 0.0
            kare_hatalar=[]
            z=0
            for i in range (0,len(dizi1x)):
                for y in range (0,len(dizi2x[i])):
                    e1 = e1 + float(pow((float(dizi1x[i][y]) - self.centroit_degerlerix[z]),2) + pow((float(dizi2x[i][y]) - self.centroit_degerleriy[z]),2))
                z=z+1
                kare_hatalar.append("{:.2f}".format(e1))
                e1= 0.0
            print("{}. iterasyon Kare Hatalar : {}".format(iterasyon,kare_hatalar))
            i=0
            toplam_karehata = 0
            for i in range (0,len(kare_hatalar)):
                toplam_karehata += float(kare_hatalar[i])
            for i in range (0,len(kare_hatalar)):
                self.listekutusu.insert(END,"e{} kare = {}".format(i+1,kare_hatalar[i]))
            self.listekutusu.insert(END,"E (Toplam Kare Hata) = {}".format(toplam_karehata))
            self.listekutusu.itemconfig(END,bg="blue",fg="black")
            print("{}. iterasyon toplam Kare Hata : {}".format(iterasyon,toplam_karehata))


            # Uzaklıklar hesaplanıyor , Minimum uzaklığa göre gruplamalar yapılıyor
                # uzaklıkların hesaplanmasında yararlanılan öklid uzaklık formuludür
            m_uzaklik =[]
            self.m_uzakliklar=[]
            m_uzaklikdeger=0

            z=0
            for y in range(0,len(self.centroit_degerlerix)):
                for i in range(0,len(self.x_degerler)):
                    self.x_degerler[i] = float(self.x_degerler[i])
                    self.y_degerler[i] = float(self.y_degerler[i])
                    m_uzaklikdeger=math.sqrt (pow((self.x_degerler[i])-(self.centroit_degerlerix[z]),2) +
                    pow ((self.y_degerler[i])-(self.centroit_degerleriy[z]),2))
                    m_uzaklik.append("{:.2f}".format(m_uzaklikdeger))
                self.m_uzakliklar.append(m_uzaklik)
                z +=1
                m_uzaklik = []
            print("{}. iterasyon Merkezden Uzaklıklar : {}".format(iterasyon,self.m_uzakliklar))

            self.listekutusu.insert(END,"")
            self.listekutusu.insert(END,"c. Merkezlerden olan uzaklıklar Hesaplandı")
            self.listekutusu.itemconfig(END,bg="black",fg="white")
            self.listekutusu.insert(END,"")
            self.listekutusu.insert(END,"""Gözlemler Merkezlerden Uzaklıklar""")
            self.listekutusu.itemconfig(END,bg="black",fg="white")


            son_kume_uyelikleri=[]
            min_index=0
            gecici_siralanacak_merkezler=[]


            for i in range(0,len(self.x_degerler)):
                for y in range(0,len(self.m_uzakliklar)):
                    gecici_siralanacak_merkezler.append(float(self.m_uzakliklar[y][i]))

                min_index = gecici_siralanacak_merkezler.index(min(gecici_siralanacak_merkezler))
                min_index = min_index + 1
                del gecici_siralanacak_merkezler[:]
                son_kume_uyelikleri.append(min_index)


            self.son_kume_uyelikleri = son_kume_uyelikleri
            print("{} . iterasyon Küme Üyeliği : {}".format(iterasyon,son_kume_uyelikleri))

            z=0
            renkler=["red","blue","gray","purple","aliceblue","ANTIQUEWHITE","AQUA","AQUAMARINE","AZURE","BISQUE","BISQUE","BISQUE","BLANCHEDALMOND","BLUE","BLUEVIOLET"]
            for y in range (0,len(self.centroit_degerlerix)):
                for i in range (0,len(self.x_degerler)):

                    sonuc = "X{:<15}  d(M{:<1},X{:<1}) = {:^15}".format(i+1,z+1,i+1,self.m_uzakliklar[z][i])
                    self.listekutusu.insert(END,sonuc)
                    self.listekutusu.itemconfig(END,bg=renkler[z],fg="white")
                    if z==14:
                        z=-1
                z +=1




            i=0
            self.listekutusu.insert(END,"")
            self.listekutusu.insert(END,"{}. iterasyon sonucu oluşan küme üyelikleri :".format(iterasyon))
            self.listekutusu.itemconfig(END,bg="purple",fg="white")
            self.listekutusu.insert(END,"")
            for i in range(0,len(self.son_kume_uyelikleri)):
                self.listekutusu.insert(END,"X{:<15} {:^15} {:^15} C{:<15}".format(i+1,self.x_degerler[i],self.y_degerler[i],self.son_kume_uyelikleri[i]))

            print("{}. iterasyon son ".format(iterasyon))
            print(self.son_kume_uyelikleri)



            if(self.son_kume_uyelikleri == kumeler1):
                    devamEt=False
                    self.listekutusu.insert(END,"")
                    self.listekutusu.insert(END,"Bu Durumda Son Kümeler: ")
                    self.listekutusu.itemconfig(END,bg="purple",fg="white")
                    self.listekutusu.insert(END,"")

                    sonuc=""
                    print(self.kume_gruplari)

                    for i in range(0,len(self.kume_gruplari)):
                        for y in range(0,len(self.kume_gruplari[i])):
                            sonuc =sonuc + """, X{}""".format(self.kume_gruplari[i][y]+1)
                        sonuc=sonuc[1:len(sonuc)]
                        self.listekutusu.insert(END,"C{0} = {1}".format(i+1,sonuc))
                        sonuc=""
                    self.kontrol_kume = self.son_kume_uyelikleri
                    self.listekutusu.insert(END,"")
                    self.listekutusu.insert(END,"En Son Oluşan Merkezler :")
                    self.listekutusu.itemconfig(END,bg="black",fg="white")
                    self.listekutusu.insert(END,"")
                    i=0
                    for i in range(0,self.centroit_degerlerix.__len__()):
                        sonuc="Centroit M{0} = [{1},{2}]".format(i+1,self.centroit_degerlerix[i],self.centroit_degerleriy[i])
                        self.listekutusu.insert(END,sonuc)

                    self.listekutusu.insert(END,"")
                    self.listekutusu.insert(END,"""
                                                                                        {}. İterasyon'da Sonuca ulaşıldı
                                """.format(iterasyon))
                    self.listekutusu.itemconfig(END,bg="purple",fg="white")
                    self.listekutusu.insert(END,"")



            else:
                print("devam ediyor")
                print(self.kontrol_kume)
                print("devam ediyor")
                self.kontrol_kume = self.son_kume_uyelikleri
                kumeler1 = self.son_kume_uyelikleri
                devamEt=True
                self.listekutusu.insert(END,"")
                self.listekutusu.insert(END,"""
                                                                                {}. İterasyon Tamamlandı, Devam Ediyor
                        """.format(iterasyon))
                self.listekutusu.itemconfig(END,bg="purple",fg="white")

            iterasyon +=1




    def grafgoster(self,centroitx=[],centroity=[],uyelikler=[]):

        ax = plt.axes()
        print("GRAFF GOSTER")
        print(centroitx)
        print(centroity)
        print(uyelikler)
        print("tm")
        plt.xlabel("x1")
        plt.ylabel("x2")
        plt.scatter(x_degerler, y_degerler,s=20,c=uyelikler)
        plt.scatter(centroitx,centroity)
        gecici = [x for i, x in enumerate(uyelikler) if i ==uyelikler.index(x)]

        print(gecici)
        print(len(gecici))
        print("tm")
        if(gecici[0] !=1):
            gecici.reverse()
        i=0
        print(centroitx)
        for i in range(0,len(centroitx)):
            print(i)
            cizgi_baslangicx=centroitx[i]-0.5
            cizgi_baslangicy=centroity[i]-0.5
            ax.annotate(" ",xy=(centroitx[i],centroity[i]),xytext=(cizgi_baslangicx,cizgi_baslangicy),
            arrowprops=dict(arrowstyle="->"))
            text="C{}".format(i+1)
            ax.text(centroitx[i]+0.2,centroity[i]+0.2,text ,ha="center",fontsize=9)
            ax.set(title="K-Means Algoritması Sonucu Oluşan Grafik")

        plt.grid(True)
        plt.show()




pencere = Tk()
basla = Kmeans(pencere)
pencere.colormapwindows()

pencere.mainloop()