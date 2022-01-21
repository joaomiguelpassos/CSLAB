# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 13:57:57 2022

@author: PMCV2
"""
import tkinter as tkinter
from tkinter import ttk
from tkinter.ttk import Progressbar
import time
import paho.mqtt.client as mqtt

def on_message(client, userdata, msg):
    global ID,ID_Reply,Pass_Reply,Pas,End_Flag,Expresso_Capsules_init,Latte_Capsules_init,Mocha_Capsules_init,Cappuccino_Capsules_init,Black_Capsules_init,Ristretto_Capsules_init

    mensagem = msg.payload.decode('utf-8')
    print("Reply =" + str(mensagem))
    
    if msg.topic == "login/idReply":
        print("login/idReply")
        if mensagem == "-2":
            print("Incorreto")
            ID = "-1"
            ID_Reply = 1
        elif mensagem == "-1":
            print("Correto")
            ID = "1"
            ID_Reply = 1
            
    elif msg.topic == "login/pinReply":
        print("login/pinReply")
        if mensagem == "-2":
            print("Pass Incorreto")
            Pas = "-1"
            Pass_Reply = 1
        elif mensagem == "-1":
            print("Pass Correto")
            Pas = "1"
            Pass_Reply = 1
            
    elif msg.topic == "capsules/result":
        print("capsules/result")
        if mensagem == "done":
            End_Flag = 1
    
    elif msg.topic == "capsules/refill":
        print("Stock refilled")
        Expresso_Capsules_init = 5
        Latte_Capsules_init = 5
        Mocha_Capsules_init = 5
        Cappuccino_Capsules_init = 5
        Black_Capsules_init = 5
        Ristretto_Capsules_init = 5
    
    
def Logout():
    global Third_Page
    
    Third_Page.destroy()
    Main()

def Ejetar_Capsulas():
    global P,Loading_Page,Third_Page,Number_Express_Capsules,Number_Latte_Capsules,Number_Mocha_Capsules,Number_Cappuccino_Capsules,Number_Black_Capsules,Number_Ristretto_Capsules,Expresso_Capsules_init,Latte_Capsules_init,Mocha_Capsules_init,Cappuccino_Capsules_init,Black_Capsules_init,Ristretto_Capsules_init
    
    Dispense_Flag = 0
    
    Selected_capsules_Expresso = str(Number_Express_Capsules)
    Selected_capsules_Latte = str(Number_Latte_Capsules)
    Selected_capsules_Mocha = str(Number_Mocha_Capsules)
    Selected_capsules_Cappuccino = str(Number_Cappuccino_Capsules)
    Selected_capsules_Black = str(Number_Black_Capsules)
    Selected_capsules_Ristretto = str(Number_Ristretto_Capsules)    
    
    
    # Error label
    if Number_Express_Capsules == 0 and Number_Latte_Capsules == 0 and Number_Mocha_Capsules == 0 and Number_Cappuccino_Capsules == 0 and Number_Black_Capsules == 0 and Number_Ristretto_Capsules == 0:
        Message = "No capsules selected"
    elif Expresso_Capsules_init - Number_Express_Capsules < 0:
        Message = "Expresso " + str(Expresso_Capsules_init) + " left"
    elif Latte_Capsules_init - Number_Latte_Capsules < 0:
        Message = "Latte " + str(Latte_Capsules_init) + " left"
    elif Mocha_Capsules_init - Number_Mocha_Capsules < 0:
        Message = "Mocha " + str(Mocha_Capsules_init) + " left"
    elif Cappuccino_Capsules_init - Number_Cappuccino_Capsules < 0:
        Message = "Cappuccino " + str(Cappuccino_Capsules_init) + " left"
    elif Black_Capsules_init - Number_Black_Capsules < 0:
        Message = "Black " + str(Black_Capsules_init) + " left"
    elif Ristretto_Capsules_init - Number_Ristretto_Capsules < 0:
        Message = "Ristretto " + str(Ristretto_Capsules_init) + " left"
    else:
        Dispense_Flag = 1 
        Message = ""
        
    if Dispense_Flag == 1:
        print("Aqui")
        Expresso_Capsules_init -= Number_Express_Capsules
        Latte_Capsules_init -= Number_Latte_Capsules
        Mocha_Capsules_init -= Number_Mocha_Capsules
        Cappuccino_Capsules_init -= Number_Cappuccino_Capsules
        Black_Capsules_init -= Number_Black_Capsules
        Ristretto_Capsules_init -= Number_Ristretto_Capsules
        
        Capsules_to_be_dispensed = Selected_capsules_Expresso + " " + Selected_capsules_Latte + " " + Selected_capsules_Mocha + " " + Selected_capsules_Cappuccino + " " + Selected_capsules_Black + " " + Selected_capsules_Ristretto + " "        
        print(Capsules_to_be_dispensed)
        client.publish("capsules/dispenser",Capsules_to_be_dispensed)
        print("Publiquei")
        
    Label_Error = tkinter.Label(Third_Page,text= Message, font=("Arial",10))    
    Label_Error.grid(row=12,column=2,columnspan=2)
    
    if Dispense_Flag == 1:
        
        Third_Page.destroy()
        Loading_Page = tkinter.Tk()
        Loading_Page.title("Dispensing capsules")
        Loading_Page.attributes('-fullscreen', True)
        Loading_Page.grid_rowconfigure(0, weight=13)
        Loading_Page.grid_rowconfigure(13, weight=13)
        Loading_Page.grid_columnconfigure(0, weight=13)
        Loading_Page.grid_columnconfigure(13, weight=13)
        
        # Objects creation
        Selected_capsules_Expresso_label = tkinter.Label(Loading_Page,text= "Expresso: " + Selected_capsules_Expresso, font=("Arial",15))
        Selected_capsules_Latte_label = tkinter.Label(Loading_Page,text= "Latte: " + Selected_capsules_Latte, font=("Arial",15))
        Selected_capsules_Mocha_label = tkinter.Label(Loading_Page,text= "Mocha: " + Selected_capsules_Mocha, font=("Arial",15))
        Selected_capsules_Cappuccino_label = tkinter.Label(Loading_Page,text= "Cappuccino: " + Selected_capsules_Cappuccino, font=("Arial",15))
        Selected_capsules_Black_label = tkinter.Label(Loading_Page,text= "Black: " + Selected_capsules_Black, font=("Arial",15))
        Selected_capsules_Ristretto_label = tkinter.Label(Loading_Page,text= "Ristretto: " + Selected_capsules_Ristretto, font=("Arial",15))
        P = Progressbar(Loading_Page,orient=tkinter.HORIZONTAL,length=200,mode="determinate",takefocus=True,maximum=100)  
        
        # Objects placement
        Selected_capsules_Expresso_label.grid(row=1, column=1, columnspan=1)
        Selected_capsules_Latte_label.grid(row=1, column=2, columnspan=1)
        Selected_capsules_Mocha_label.grid(row=2, column=1, columnspan=1)
        Selected_capsules_Cappuccino_label.grid(row=2, column=2, columnspan=1)
        Selected_capsules_Black_label.grid(row=3, column=1, columnspan=1)
        Selected_capsules_Ristretto_label.grid(row=3, column=2, columnspan=1)
        P.grid(row=5,column=1,columnspan=2)
        Bar()


def Bar():
    global P,Loading_Page,End_Flag
    
    End_Flag = 0
    
    Message_3 = tkinter.Label(Loading_Page,text="Waiting...", font=("Arial",15))
    Message_3.grid(row=6,column=1,columnspan=2)
    
    i = 0
    
    while i < 51:      
        #print(i)          
        P['value'] = i*2
        Loading_Page.update()
        time.sleep(0.1)
        i+=1
        if i*2 == 100:
            if End_Flag == 1:
                break;
            else:
                i = 0
    
    # Messages
    Message_1 = tkinter.Label(Loading_Page,text="All capsules have been dispensed", font=("Arial",15))
    Message_2 = tkinter.Label(Loading_Page,text="Have a nice day", font=("Arial",15))
    # Messages placement
    Message_1.grid(row=7,column=1,columnspan=2)
    Message_2.grid(row=8,column=1,columnspan=2)
    Loading_Page.update()
    time.sleep(2)
    
    Loading_Page.destroy()
    Main()

def Less_Express():
    global Number_Express_Capsules
    
    Destroy_Second_Page_Objects()
    
    Number_Express_Capsules -= 1
    if Number_Express_Capsules < 0:
        Number_Express_Capsules = 0
    Forth_Page_Generator()
    
def More_Express():
    global Number_Express_Capsules
    
    Destroy_Second_Page_Objects()
    
    Number_Express_Capsules += 1
    Forth_Page_Generator()
    
def Less_Latte():
    global Number_Latte_Capsules
    
    Destroy_Second_Page_Objects()
    
    Number_Latte_Capsules -= 1
    if Number_Latte_Capsules < 0:
        Number_Latte_Capsules = 0
    Forth_Page_Generator()
    
def More_Latte():
    global Number_Latte_Capsules
    
    Destroy_Second_Page_Objects()
    
    Number_Latte_Capsules += 1
    Forth_Page_Generator()
    
def Less_Mocha():
    global Number_Mocha_Capsules
    
    Destroy_Second_Page_Objects()
    
    Number_Mocha_Capsules -= 1
    if Number_Mocha_Capsules < 0:
        Number_Mocha_Capsules = 0
    Forth_Page_Generator()
    
def More_Mocha():
    global Number_Mocha_Capsules
    
    Destroy_Second_Page_Objects()
    
    Number_Mocha_Capsules += 1
    Forth_Page_Generator()
    
def Less_Cappuccino():
    global Number_Cappuccino_Capsules
    
    Destroy_Second_Page_Objects()
    
    Number_Cappuccino_Capsules -= 1
    if Number_Cappuccino_Capsules < 0:
        Number_Cappuccino_Capsules = 0
    Forth_Page_Generator()
    
def More_Cappuccino():
    global Number_Cappuccino_Capsules
    
    Destroy_Second_Page_Objects()
    
    Number_Cappuccino_Capsules += 1
    Forth_Page_Generator()
    
def Less_Black():
    global Number_Black_Capsules
    
    Destroy_Second_Page_Objects()
    
    Number_Black_Capsules -= 1
    if Number_Black_Capsules < 0:
        Number_Black_Capsules = 0
    Forth_Page_Generator()
    
def More_Black():
    global Number_Black_Capsules
    
    Destroy_Second_Page_Objects()
    
    Number_Black_Capsules += 1
    Forth_Page_Generator()
    
def Less_Ristretto():
    global Number_Ristretto_Capsules
    
    Destroy_Second_Page_Objects()
    
    Number_Ristretto_Capsules -= 1
    if Number_Ristretto_Capsules < 0:
        Number_Ristretto_Capsules = 0
    Forth_Page_Generator()
    
def More_Ristretto():
    global Number_Ristretto_Capsules
    
    Destroy_Second_Page_Objects()
    
    Number_Ristretto_Capsules += 1
    Forth_Page_Generator()

def Destroy_Second_Page_Objects():
    global Linha_em_branco_1,Linha_em_branco_2,Number_Express_Capsules,Number_Latte_Capsules,Number_Mocha_Capsules,Number_Cappuccino_Capsules,Number_Black_Capsules,Number_Ristretto_Capsules,Capsule_Express_Less,Capsule_Express,Capsule_Express_More,Capsule_Latte_Less,Capsule_Latte,Capsule_Latte_More,Capsule_Mocha_Less,Capsule_Mocha,Capsule_Mocha_More,Capsule_Cappuccino_Less,Capsule_Cappuccino,Capsule_Cappuccino_More,Capsule_Black_Less,Capsule_Black,Capsule_Black_More,Capsule_Ristretto_Less,Capsule_Ristretto,Capsule_Ristretto_More,Coluna_em_branco_1,Coluna_em_branco_2,Express_Label,Latte_Label,Mocha_Label,Cappuccino_Label,Black_Label,Ristretto_Label
    
    #Linha_em_branco_1.destroy()
    Capsule_Express_Less.destroy()
    Capsule_Express.destroy()
    Capsule_Express_More.destroy()
    Capsule_Latte_Less.destroy()
    Capsule_Latte.destroy()
    Capsule_Latte_More.destroy()
    Capsule_Mocha_Less.destroy()
    Capsule_Mocha.destroy()
    Capsule_Mocha_More.destroy()
    Capsule_Cappuccino_Less.destroy()
    Capsule_Cappuccino.destroy()
    Capsule_Cappuccino_More.destroy()
    Capsule_Black_Less.destroy()
    Capsule_Black.destroy()
    Capsule_Black_More.destroy()
    Capsule_Ristretto_Less.destroy()
    Capsule_Ristretto.destroy()
    Capsule_Ristretto_More.destroy()
    #Coluna_em_branco_1.destroy()
    #Coluna_em_branco_2.destroy()
    Express_Label.destroy()
    Latte_Label.destroy()
    Mocha_Label.destroy()
    Cappuccino_Label.destroy()
    Black_Label.destroy()
    Ristretto_Label.destroy()
    
    
def Number_1():
    global Caracter,Login,Caracter_2

    if Login == 1:
        Caracter_2 = 1
        Temp_Login()
    else:
        Caracter = 1
        Second_Page_Generator()
    
def Number_2():
    global Caracter,Login,Caracter_2

    if Login == 1:
        Caracter_2 = 2
        Temp_Login()
    else:
        Caracter = 2
        Second_Page_Generator()
        
def Number_3():
    global Caracter,Login,Caracter_2

    if Login == 1:
        Caracter_2 = 3
        Temp_Login()
    else:
        Caracter = 3
        Second_Page_Generator()
        
def Number_4():
    global Caracter,Login,Caracter_2

    if Login == 1:
        Caracter_2 = 4
        Temp_Login()
    else:
        Caracter = 4
        Second_Page_Generator()
        
def Number_5():
    global Caracter,Login,Caracter_2

    if Login == 1:
        Caracter_2 = 5
        Temp_Login()
    else:
        Caracter = 5
        Second_Page_Generator()
        
def Number_6():
    global Caracter,Login,Caracter_2

    if Login == 1:
        Caracter_2 = 6
        Temp_Login()
    else:
        Caracter = 6
        Second_Page_Generator()
        
def Number_7():
    global Caracter,Login,Caracter_2

    if Login == 1:
        Caracter_2 = 7
        Temp_Login()
    else:
        Caracter = 7
        Second_Page_Generator()
        
def Number_8():
    global Caracter,Login,Caracter_2

    if Login == 1:
        Caracter_2 = 8
        Temp_Login()
    else:
        Caracter = 8
        Second_Page_Generator()
        
def Number_9():
    global Caracter,Login,Caracter_2

    if Login == 1:
        Caracter_2 = 9
        Temp_Login()
    else:
        Caracter = 9
        Second_Page_Generator()
        
def Number_0():
    global Caracter,Login,Caracter_2

    if Login == 1:
        Caracter_2 = 0
        Temp_Login()
    else:
        Caracter = 0
        Second_Page_Generator()
        
def Number_DEL():
    global Caracter,Login,Caracter_2

    if Login == 1:
        Caracter_2 = "DEL"
        Temp_Login()
    else:
        Caracter = "DEL"
        Second_Page_Generator()
    
def Number_Cancel():
    global Caracter

    Caracter = "Cancel"
    Second_Page_Generator()
    
def Hide_PIN():
    global Hide_PIN_Flag, Caracter
    
    Caracter = "Inofensivo"
    
    if Hide_PIN_Flag == 1:
        Hide_PIN_Flag = 0
    else:
        Hide_PIN_Flag = 1
    Second_Page_Generator()

def Forth_Page_Generator():
    global First_Page,Second_Page_Flag,Linha_em_branco_1,Linha_em_branco_2,Number_Express_Capsules,Number_Latte_Capsules,Number_Mocha_Capsules,Number_Cappuccino_Capsules,Number_Black_Capsules,Number_Ristretto_Capsules,Capsule_Express_Less,Capsule_Express,Capsule_Express_More,Capsule_Latte_Less,Capsule_Latte,Capsule_Latte_More,Capsule_Mocha_Less,Capsule_Mocha,Capsule_Mocha_More,Capsule_Cappuccino_Less,Capsule_Cappuccino,Capsule_Cappuccino_More,Capsule_Black_Less,Capsule_Black,Capsule_Black_More,Capsule_Ristretto_Less,Capsule_Ristretto,Capsule_Ristretto_More,Coluna_em_branco_1,Coluna_em_branco_2,Express_Label,Latte_Label,Mocha_Label,Cappuccino_Label,Black_Label,Ristretto_Label,Third_page_first,Pas,User_Password,Third_page_first,Pass_Reply,PIN_send

        
    if Second_Page_Flag == 1:
        #First_Page.destroy()
        Number_Express_Capsules = 0
        Number_Latte_Capsules = 0
        Number_Mocha_Capsules = 0
        Number_Cappuccino_Capsules = 0
        Number_Black_Capsules = 0
        Number_Ristretto_Capsules = 0
        Second_Page_Flag = 0 
            
        client.publish("login/pin",PIN_send)
                
        print("Waiting for pass check")    
            
        while Pass_Reply != 1:
            time.sleep(0.1)
            
    if Pas == "-1":
        #print("Vou destruir")
        First_Page.destroy()
        Third_Page.destroy()
        Main()
    elif Pas == "1":
        #print("Vou prosseguir")
            
        # Objects creation
        # Express Menu
        Capsule_Express_Less = tkinter.Button(Third_Page,text="-", width=3 ,command= Less_Express)
        Capsule_Express = tkinter.Label(Third_Page,text = Number_Express_Capsules, width=4)
        Capsule_Express_More = tkinter.Button(Third_Page,text="+", width=3 ,command= More_Express)
        # Latte Menu
        Capsule_Latte_Less = tkinter.Button(Third_Page,text="-", width=3 ,command= Less_Latte)
        Capsule_Latte = tkinter.Label(Third_Page,text = Number_Latte_Capsules, width=4)
        Capsule_Latte_More = tkinter.Button(Third_Page,text="+", width=3 ,command= More_Latte)
        # Mocha Menu
        Capsule_Mocha_Less = tkinter.Button(Third_Page,text="-", width=3 ,command= Less_Mocha)
        Capsule_Mocha = tkinter.Label(Third_Page,text = Number_Mocha_Capsules, width=4)
        Capsule_Mocha_More = tkinter.Button(Third_Page,text="+", width=3 ,command= More_Mocha)
        # Cappuccino Menu
        Capsule_Cappuccino_Less = tkinter.Button(Third_Page,text="-", width=3 ,command= Less_Cappuccino)
        Capsule_Cappuccino = tkinter.Label(Third_Page,text = Number_Cappuccino_Capsules, width=4)
        Capsule_Cappuccino_More = tkinter.Button(Third_Page,text="+", width=3 ,command= More_Cappuccino)
        # Black Menu
        Capsule_Black_Less = tkinter.Button(Third_Page,text="-", width=3 ,command= Less_Black)
        Capsule_Black = tkinter.Label(Third_Page,text = Number_Black_Capsules, width=4)
        Capsule_Black_More = tkinter.Button(Third_Page,text="+", width=3 ,command= More_Black)
        # Ristretto Menu
        Capsule_Ristretto_Less = tkinter.Button(Third_Page,text="-", width=3 ,command= Less_Ristretto)
        Capsule_Ristretto = tkinter.Label(Third_Page,text = Number_Ristretto_Capsules, width=4)
        Capsule_Ristretto_More = tkinter.Button(Third_Page,text="+", width=3 ,command= More_Ristretto)
        # Empty Labels
        
        # Empty Columns
        Coluna_em_branco_1 = tkinter.Label(Third_Page, text="", width=3)
        Coluna_em_branco_2 = tkinter.Label(Third_Page, text="", width=3)    
        # Capsules Labels
        Express_Label = tkinter.Label(Third_Page, text="Express", font=("Arial",10))
        Latte_Label = tkinter.Label(Third_Page, text="Latte", font=("Arial",10))
        Mocha_Label = tkinter.Label(Third_Page, text="Mocha", font=("Arial",10))
        Cappuccino_Label = tkinter.Label(Third_Page, text="Capuccino", font=("Arial",10))
        Black_Label = tkinter.Label(Third_Page, text="Black", font=("Arial",10))
        Ristretto_Label = tkinter.Label(Third_Page, text="Ristretto", font=("Arial",10))
        # Logout button
        Logout_button = tkinter.Button(Third_Page, text="Logout", width=3, command= Logout)
        # Dispense Button
        Dispense_button = tkinter.Button(Third_Page, text="Dispense", width=5, command= Ejetar_Capsulas)
        
        # Objects placement
        # First row
        # Express capsules
        Express_Label.grid(row=1, column=1, columnspan=1)
        Capsule_Express_Less.grid(row=1,column=2,columnspan=1)
        Capsule_Express.grid(row=1,column=4,columnspan=1)
        Capsule_Express_More.grid(row=1,column=3,columnspan=1)
        
        #Linha_em_branco_1.grid(row=2)
        
        # Latte capsules
        Latte_Label.grid(row=3,column=1,columnspan=1)
        Capsule_Latte_Less.grid(row=3,column=2,columnspan=1)
        Capsule_Latte.grid(row=3,column=4,columnspan=1)
        Capsule_Latte_More.grid(row=3,column=3,columnspan=1)
        
        #Linha_em_branco_2.grid(row=4)
        #Coluna_em_branco_2.grid(column=8)
        
        # Mocha capsules
        Mocha_Label.grid(row=5,column=1,columnspan=1)
        Capsule_Mocha_Less.grid(row=5,column=2,columnspan=1)
        Capsule_Mocha.grid(row=5,column=4,columnspan=1)
        Capsule_Mocha_More.grid(row=5,column=3,columnspan=1)
        
        #Linha_em_branco_3.grid(row=6)
    
        # Second row
        # Cappuccino capsules
        Cappuccino_Label.grid(row=7,column=1,columnspan=1)
        Capsule_Cappuccino_Less.grid(row=7,column=2,columnspan=1)
        Capsule_Cappuccino.grid(row=7,column=4,columnspan=1)
        Capsule_Cappuccino_More.grid(row=7,column=3,columnspan=1)
        
        #Linha_em_branco_4.grid(row=8)
        
        # Black capsules
        Black_Label.grid(row=9,column=1,columnspan=1)
        Capsule_Black_Less.grid(row=9,column=2,columnspan=1)
        Capsule_Black.grid(row=9,column=4,columnspan=1)
        Capsule_Black_More.grid(row=9,column=3,columnspan=1)
        
        #Linha_em_branco_5.grid(row=10)
        
        # Ristretto capsules
        Ristretto_Label.grid(row=11,column=1,columnspan=1)
        Capsule_Ristretto_Less.grid(row=11,column=2,columnspan=1)
        Capsule_Ristretto.grid(row=11,column=4,columnspan=1)
        Capsule_Ristretto_More.grid(row=11,column=3,columnspan=1) 
        
        #Coluna_em_branco_1.grid(column=5)
        
        # Logout Button
        Logout_button.grid(row=12,column=1,columnspan=1)
        
        # Dispense Button
        Dispense_button.grid(row=12, column=4, columnspan=1)
    

def Third_Page_Generator():
    global Third_Page,User_Password,Pas,Pass_Reply,First_Page,Third_page_first
    
    Third_page_first = 1
    
    Third_Page = tkinter.Tk()
    Third_Page.title("Coffee capsules login page")
    Third_Page.attributes('-fullscreen', True)
    Third_Page.grid_rowconfigure(0, weight=13)
    Third_Page.grid_rowconfigure(13, weight=13)
    Third_Page.grid_columnconfigure(0, weight=13)
    Third_Page.grid_columnconfigure(13, weight=13)
    Forth_Page_Generator()
    Third_Page.mainloop()
    
def Second_Page_Generator():
    global Label_User_ID,User_ID,Button_Login,First_Page,Digit_1,Digit_2,Digit_3,Digit_4,Digit_1_Hiden,Digit_2_Hiden,Digit_3_Hiden,Digit_4_Hiden,Hide_PIN_Flag,Caracter,Second_Page_Flag,Label_User_Password,User_Password,User_Password,Hide_PIN_Button,Linha_em_branco_1,Button_1,Button_2,Button_3,Button_4,Button_5,Button_6,Button_7,Button_8,Button_9,Button_0,Button_del,Button_cancel,Linha_em_branco_2,ID_Reply,Login,ID,Third_page_first,PIN_send
    
    Login = "0"
    ID_Reply = "Nada"
    
    if Caracter == "Nada":

        User_ID_inserted = User_ID.get() 
        client.publish("login/id",User_ID_inserted)
        
        print("Waiting")    
        
        while ID_Reply == "Nada":
            time.sleep(0.1)
  
    
    if ID == "-1":
        First_Page.destroy()
        Main()
        
    elif ID == "1":
        
        Caracter_Inserted = str(Caracter)
        
        if Caracter_Inserted == "Cancel":
            First_Page.destroy()
            Main()
        
        elif Caracter_Inserted == "DEL":
            if Digit_4 != "":
                Digit_4 = ""
                Digit_4_Hiden = ""
            elif Digit_3 != "":
                Digit_3 = ""
                Digit_3_Hiden = ""
            elif Digit_2 != "":
                Digit_2 = ""
                Digit_2_Hiden = ""
            elif Digit_1 != "":
                Digit_1 = ""
                Digit_1_Hiden = ""
                
        elif Caracter_Inserted != "Nada" and Caracter_Inserted != "Inofensivo":
            if Digit_1 == "":
                Digit_1 = Caracter_Inserted
                Digit_1_Hiden = "•"
            elif Digit_2 == "":
                Digit_2 = Caracter_Inserted
                Digit_2_Hiden = "•"
            elif Digit_3 == "":
                Digit_3 = Caracter_Inserted
                Digit_3_Hiden = "•"
            elif Digit_4 == "":
                Digit_4 = Caracter_Inserted
                Digit_4_Hiden = "•"
                    
        if Hide_PIN_Flag == 1:
            PIN_reply = Digit_1_Hiden + Digit_2_Hiden + Digit_3_Hiden + Digit_4_Hiden
        elif Hide_PIN_Flag == 0:
            PIN_reply = Digit_1 + Digit_2 + Digit_3 + Digit_4
        PIN_send = Digit_1 + Digit_2 + Digit_3 + Digit_4
        if Caracter_Inserted == "Nada":
            # Destruction of the previosly created objects
            Label_User_ID.destroy()
            User_ID.destroy()
            Button_Login.destroy()
    
        # Objects creation
        Label_User_Password = tkinter.Label(First_Page, text="User PIN", font=("Arial",20))
        User_Password = tkinter.Entry(First_Page, width=10)
        User_Password.insert(0,str(PIN_reply))
        
        if Hide_PIN_Flag == 1:
            Hide_Message = "Ver PIN"
        elif Hide_PIN_Flag == 0:
            Hide_Message = "Esconder PIN"
        
        Hide_PIN_Button = tkinter.Button(First_Page, text=Hide_Message, width=10, command= Hide_PIN)
        
        Linha_em_branco_1 = tkinter.Label(First_Page, text="")
        
        Button_cancel = tkinter.Button(First_Page,text="Cancel", width=10, command=Number_Cancel)

        
        # Objects placement
        Label_User_Password.grid(row=4 ,column=4,columnspan=3)
        User_Password.grid(row=5,column=5,columnspan=1)
        Hide_PIN_Button.grid(row=5,column=4,columnspan=1)
            
        Linha_em_branco_1.grid(row=6,column=5)
            
        Button_cancel.grid(row=12,column=6,columnspan=1)
        
        Button_Login = tkinter.Button(First_Page, text="Login", width=10, command= Third_Page_Generator)
        Button_Login.grid(row=5,column=6)
    
def Temp_Login():
    global Label_User_ID,User_ID,Button_Login,First_Page,Digit_1,Digit_2,Digit_3,Digit_4,Digit_1_Hiden,Digit_2_Hiden,Digit_3_Hiden,Digit_4_Hiden,Caracter,Hide_PIN_Flag,Second_Page_Flag,Digit_1_ID,Digit_2_ID,Digit_3_ID,Digit_4_ID,Caracter_2
    
    Caracter_Inserted_2 = str(Caracter_2)
    
    
    if Caracter_Inserted_2 == "DEL":
        if Digit_4_ID != "":
            Digit_4_ID = ""
        elif Digit_3_ID != "":
            Digit_3_ID = ""
        elif Digit_2_ID != "":
            Digit_2_ID = ""
        elif Digit_1_ID != "":
            Digit_1_ID = ""
                
    elif Caracter_Inserted_2 != "Nada":
        if Digit_1_ID == "":
            Digit_1_ID = Caracter_Inserted_2
        elif Digit_2_ID == "":
            Digit_2_ID = Caracter_Inserted_2
        elif Digit_3_ID == "":
            Digit_3_ID = Caracter_Inserted_2
        elif Digit_4_ID == "":
            Digit_4_ID = Caracter_Inserted_2
        
    User_ID_reply = Digit_1_ID + Digit_2_ID + Digit_3_ID + Digit_4_ID
    
    # Objects creation
    Label_User_ID = tkinter.Label(First_Page, text="User ID", font=("Arial",15))
    User_ID = tkinter.Entry(First_Page)
    Button_Login = tkinter.Button(First_Page, text="Login", command= Second_Page_Generator)
    
    User_ID.insert(0,str(User_ID_reply))
    
    Linha_em_branco_1 = tkinter.Label(First_Page, text="")
        
    
    Button_1 = tkinter.Button(First_Page,text="1", width=10, command= Number_1) 
    Button_2 = tkinter.Button(First_Page,text="2", width=10, command= Number_2)
    Button_3 = tkinter.Button(First_Page,text="3", width=10, command= Number_3)
    Button_4 = tkinter.Button(First_Page,text="4", width=10, command= Number_4)
    Button_5 = tkinter.Button(First_Page,text="5", width=10, command= Number_5)
    Button_6 = tkinter.Button(First_Page,text="6", width=10, command= Number_6)
    Button_7 = tkinter.Button(First_Page,text="7", width=10, command= Number_7)
    Button_8 = tkinter.Button(First_Page,text="8", width=10, command= Number_8)
    Button_9 = tkinter.Button(First_Page,text="9", width=10, command= Number_9)
    Button_0 = tkinter.Button(First_Page,text="0", width=10, command= Number_0)
    Button_del = tkinter.Button(First_Page,text="DELETE", width=10, command= Number_DEL)

        
    # Objects placement
    Label_User_ID.grid(row=4 ,column=4,columnspan=3)
    User_ID.grid(row=5,column=5,columnspan=3)
    Button_Login.grid(row=5,column=4,columnspan=1)
            
    Linha_em_branco_1.grid(row=6,column=5)
            
    Button_1.grid(row=9,column=4,columnspan=1)
    Button_2.grid(row=9,column=5,columnspan=1)
    Button_3.grid(row=9,column=6,columnspan=1)
    Button_4.grid(row=10,column=4,columnspan=1)
    Button_5.grid(row=10,column=5,columnspan=1)
    Button_6.grid(row=10,column=6,columnspan=1)
    Button_7.grid(row=11,column=4,columnspan=1)
    Button_8.grid(row=11,column=5,columnspan=1)
    Button_9.grid(row=11,column=6,columnspan=1)
    Button_0.grid(row=12,column=4,columnspan=1)
    Button_del.grid(row=12,column=5,columnspan=1)
        
    
def Main():
    global Label_User_ID,User_ID,Button_Login,First_Page,Digit_1,Digit_2,Digit_3,Digit_4,Digit_1_Hiden,Digit_2_Hiden,Digit_3_Hiden,Digit_4_Hiden,Caracter,Hide_PIN_Flag,Second_Page_Flag,Digit_1_ID,Digit_2_ID,Digit_3_ID,Digit_4_ID,Login,Caracter_2,Pas,Pass_Reply
    
    Digit_1 = ""
    Digit_2 = ""
    Digit_3 = ""
    Digit_4 = ""
    Digit_1_Hiden = ""
    Digit_2_Hiden = ""
    Digit_3_Hiden = ""
    Digit_4_Hiden = ""
    Digit_1_ID = ""
    Digit_2_ID = ""
    Digit_3_ID = ""
    Digit_4_ID = ""
    Caracter= "Nada"
    Caracter_2= "Nada"
    Hide_PIN_Flag = 1
    Second_Page_Flag = 1
    Login = 1
    Pas = 0
    Pass_Reply = "Nada"
    First_Page = tkinter.Tk()
    First_Page.title("Coffee capsules login page")

    #First_Page.geometry("320x240")
    First_Page.attributes('-fullscreen', True)
    First_Page.grid_rowconfigure(0, weight=14)
    First_Page.grid_rowconfigure(14, weight=14)
    First_Page.grid_columnconfigure(0, weight=11)
    First_Page.grid_columnconfigure(11, weight=11)
    
    Temp_Login()
    
    First_Page.mainloop()

Expresso_Capsules_init = 5
Latte_Capsules_init = 5
Mocha_Capsules_init = 5
Cappuccino_Capsules_init = 5
Black_Capsules_init = 5
Ristretto_Capsules_init = 5
# Ligação ao broker
broker_adress= "localhost"
#broker_adress= "192.168.1.88"
broker_port = 1883
client = mqtt.Client("Machine_1")
print("Cliente criado com sucesso")
client.username_pw_set("user","lol123")
client.connect(broker_adress,broker_port)
print("cliente conectado com sucesso")
client.subscribe("login/idReply")
print("Tópico login/idReply subscrito com sucesso")
client.subscribe("login/pinReply")
print("Tópico login/pinReply subscrito com sucesso")
client.subscribe("capsules/result")
print("Tópico capsules/result subscrito com sucesso")
client.subscribe("capsules/refill")
print("Tópico capsules/refill subscrito com sucesso")
client.on_message = on_message
client.loop_start()
# Programa principal
Main()

