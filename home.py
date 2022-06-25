from kivy.config import Config 
import pymysql
Config.set('graphics', 'resizable', True) 
import kivy 
import knn	
from kivy.app import App 
kivy.require('1.9.0') 
from kivy.uix.label import Label 
from kivy.uix.spinner import Spinner 
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
import nearby
from functools import partial
import main

conn=pymysql.connect(host='localhost',user='root',password='',db='guide')
a=conn.cursor()
sql='SELECT DISTINCT state from `localguide`;'
countrow=a.execute(sql)
state=[]
i=0
while(i<countrow):
    stated=a.fetchone()
    state.append(stated)
    i+=1

def listToString(s):  
    str1 = " "  
    return (str1.join(s))
# Make an App by deriving from the App class 
class SpinnerExample(App):
    def callback(self, layout):
        layout.clear_widgets()
        App().get_running_app().stop()
        main.abc()
        
    def build(self):
        layout = FloatLayout()
        self.btn = Button(text ="LOGOUT", 
           font_size ="10sp", 
           background_color =(1, 1, 1, 1), 
           color =(1, 1, 1, 1), 
           size =(1, 1), 
           size_hint =(.1, .1)) 
        self.btn.pos_hint ={'x': .88, 'y':.88}
        self.btn.bind(on_press=lambda x: self.callback(layout))
        layout.add_widget(self.btn)
        
        self.spinnerObject = Spinner(text ="Search by State",values =(listToString(statee) for statee in state), background_color =(0.784, 0.443, 0.216, 1)) 
        self.spinnerObject.size_hint = (0.27, 0.07) 
        self.spinnerObject.pos_hint ={'x': .45, 'y':.89}
        self.spinnerObject.size=(10, 4)

        self.spinnerObject5 = button = Button(text="Search nearby places",font_size ="20sp")
        button.background_color =(0.53,0.81,0.92, 1)
        button.color =(50, 50, 50, 50)
        button.size =(9, 9)
        button.size_hint =(0.27, 0.07)
        button.pos_hint ={'x': .10, 'y':.89}

        def show_selected_value(spinner, text):
            a1=conn.cursor()
            sql1="SELECT DISTINCT city from `localguide` where state='"+text+"';"
            countrow1=a1.execute(sql1)
            city=[]
            i=0
            while(i<countrow1):
                cityd=a1.fetchone()
                city.append(cityd)
                i+=1
            self.spinnerObject1 = Spinner(text ="Select City",values =(listToString(citye) for citye in city), background_color =(0.784, 0.443, 0.216, 1)) 
            self.spinnerObject1.size_hint = (0.27, 0.07) 
            self.spinnerObject1.pos_hint ={'x': .45, 'y':.81}
            def show_selected_value1(spinner, text1):
                a2=conn.cursor()
                sql2="SELECT DISTINCT intrest from `localguide` where state='"+text+"' and city='"+text1+"';"
                countrow2=a2.execute(sql2)
                intrest=[]
                i=0
                while(i<countrow2):
                    intrestd=a2.fetchone()
                    intrest.append(intrestd)
                    i+=1
                self.spinnerObject2 = Spinner(text ="Select your Intrest",values =(listToString(intreste) for intreste in intrest), background_color =(0.784, 0.443, 0.216, 1)) 
                self.spinnerObject2.size_hint = (0.27, 0.07) 
                self.spinnerObject2.pos_hint ={'x': .45, 'y':.72}
                def show_selected_value2(spinner, text2):
                    self.mylabel = Label(text='mylabel', color=[0.784, 0.443, 0.216, 1],size_hint = (0.3, 0.2),pos_hint ={'x': .35, 'y':.0})
                    layout.add_widget(self.mylabel)
                    sql3="SELECT * from `localguide` where state='"+text+"' and city='"+text1+"' and intrest='"+text2+"';"
                    print(sql3)
                    layout.clear_widgets()
                    App().get_running_app().stop()
                    knn.bb(sql3)    
               #| 
                self.spinnerObject2.bind(text=show_selected_value2)
                layout.add_widget(self.spinnerObject2)
           #|
            self.spinnerObject1.bind(text=show_selected_value1)
            layout.add_widget(self.spinnerObject1)
       #|
        self.spinnerObject.bind(text=show_selected_value)        
        layout.add_widget(self.spinnerObject)

        button.bind(on_press=lambda x: self.my_function(layout))
        layout.add_widget(self.spinnerObject5)
        return layout; 

    def my_function(self,layout):
        sql4="SELECT * from `localguide`;"
        layout.clear_widgets()
        App().get_running_app().stop()
        nearby.bb(sql4)

def home():
    SpinnerExample().run()	 
