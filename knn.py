import pymysql
import pandas as pd
import geopy,os
import warnings
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.base import runTouchApp
from kivy.lang import Builder
import webbrowser
from functools import partial
warnings.filterwarnings("ignore")
from numpy import cos, sin, arcsin, sqrt
from math import radians
from geopy.geocoders import Nominatim
os.listdir()
nom=Nominatim()
conn=pymysql.connect(host='localhost',user='root',password='',db='guide')
a=conn.cursor()
import home

def bb(sql):
    countrow=a.execute(sql)
    print("no of rows",countrow)

    i=0
    places=[]
    site=[]
    latitude=[]
    longitude=[]
    while(i<countrow):
        data=a.fetchone()
        latitude.append(float(data[4]))
        longitude.append(float(data[5]))
        site.append(data[0])
        i+=1
        
    i=0
    latt=[]
    longg=[]
    global cord_list
    cord_list=[]
    while(i<countrow):    
        latt.append(latitude[i])
        longg.append(longitude[i])
        cord_list.append(str(latitude[i])+','+str(longitude[i]))
        i+=1
    global df
    df = pd.DataFrame(site,columns =['PLACES']) 
    df['LAT']=pd.DataFrame(latt)
    df['LON']=pd.DataFrame(longg)
    print(df)

    def haversine(row):
        lon1 = 74.5119014
        lat1 = 15.8814388
        lon2 = row['LON']
        lat2 = row['LAT']
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * arcsin(sqrt(a)) 
        km = 6367 * c
        return km

    df['DISTANCE'] = df.apply(lambda row: haversine(row), axis=1)
    df.sort_values("DISTANCE", axis = 0, ascending = True,inplace = True, na_position ='last')
    print('\n',df)
    MyApp().run()

     
class MyGrid(GridLayout):
    def callback(self, event):
        self.clear_widgets()
        App().get_running_app().stop()
        home.home()
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.btn = Button(text ="BACK", 
        font_size ="20sp", 
        background_color =(1, 1, 1, 1), 
        color =(1, 1, 1, 1), 
        size =(2, 2), 
        size_hint =(.2, .7), 
        pos =(300, 250)) 

        self.btn.bind(on_press = self.callback) 
        self.add_widget(self.btn)
        self.cols = 1
        self.inside = GridLayout()
        self.inside.cols = 1
        self.inside.add_widget(Label(text="       Select a place to Navigate through Google Maps"))
        self.add_widget(self.inside)
        pplace=df['PLACES'].values.tolist()
        LAT=df['LAT'].values.tolist()
        LON=df['LON'].values.tolist()
        print("LAT",LAT,"lon",LON)
        i=0
        #print("cord_list",cord_list)
        for w in pplace:
            ADDRESS=str(LAT[i])+","+str(LON[i])
            url = "https://www.google.co.in/maps/place/" + ADDRESS
            self.button = Button(text= pplace[i], on_press=partial(webbrowser.open, url),background_color =(0.784, 0.443, 0.216, 1))       
            self.add_widget(self.button)
            i+=1

class MyApp(App):
    def build(self):
        return MyGrid()        
