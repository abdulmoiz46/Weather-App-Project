from tkinter import *
import tkinter as tk
import pytz
from geopy.geocoders import Nominatim
from datetime import datetime , timedelta
import requests
from PIL import Image , ImageTk
from tkinter import messagebox , ttk
from timezonefinder import TimezoneFinder


root=Tk()
root.title("Weather App")
root.geometry("800x500+300+200")
root.resizable(False,False)
root.config(bg="#202731")


def getweather():
    city = textfield.get()
    geolocator = Nominatim(user_agent="new")

    try:
        location = geolocator.geocode(city)
        if location is None:
            timezone.config(text="Location not found")
            return

        tf = TimezoneFinder()  
        result = tf.timezone_at(lat=location.latitude, lng=location.longitude)

        if result:
            timezone.config(text=result)
        else:
            timezone.config(text="Timezone not found")
    except Exception as e:
        timezone.config(text=f"Error: {e}")

    long_lat.config(text=f"{round(location.latitude,4)}°N{round(location.longitude,4)}°E")

    lat_suffix = "N" if location.latitude >= 0 else "S"
    lon_suffix = "E" if location.longitude >= 0 else "W"
    long_lat.config(text=f"{abs(round(location.latitude, 4))}°{lat_suffix} {abs(round(location.longitude, 4))}°{lon_suffix}")


    home=pytz.timezone(result)
    local_time=datetime.now(home)
    current_time=local_time.strftime("%I:%M %p")
    clock.config(text=current_time)


    api_key="a5be4bd8b30cd625ebff7db8a7dcf5f8"
    api=f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    


    try:
        response = requests.get(api)
        response.raise_for_status()
        json_data = response.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("API Error", f"Failed to get weather data:\n{e}")
        return
     
     
    if "list" not in json_data or not json_data["list"]:
         messagebox.showerror("Data Error", "Weather data is not available for this location.")
         return

    current = json_data['list'][0]
    temp = current['main']['temp']
    humidity = current['main']['humidity']
    pressure = current['main']['pressure']
    wind_speed = current['wind']['speed']
    description = current['weather'][0]['description']
    condition = current['weather'][0]['main']
    
  
    wind_speed_kmph = round(wind_speed * 3.6, 2)
    
    t.config(text=f"{temp}°C")
    h.config(text=f"{humidity}%")
    p.config(text=f"{pressure}hpa")
    w.config(text=f"{wind_speed_kmph} km/h")
    d.config(text=f"{description}")

    
    
    c.config(text=f"{condition} | FEELS LIKE {temp}°")

    daily_data = []
    for entry in json_data['list']:
        if "12:00:00" in entry['dt_txt']:
            daily_data.append(entry)


    icons = []
    temps = []

    for i in range(5):
        if i >= len(daily_data):
            break
        icon_code = daily_data[i]['weather'][0]['icon']
        try:
            img = Image.open(f"icon/{icon_code}@2x.png").resize((50, 50))
        except FileNotFoundError:
            img = Image.open("icon/default.png").resize((50, 50))  

        icons.append(ImageTk.PhotoImage(img))
        temps.append((daily_data[i]['main']['temp_max'], daily_data[i]['main']['feels_like']))




    for i, (img_label, day_label, temp_label) in enumerate(day_widget):
        if i >= len(icons):  
            break
        img_label.config(image=icons[i])
        img_label.image = icons[i]  
        temp_label.config(text=f"Day: {temps[i][0]}°C\nNight: {temps[i][1]}°C")
        future_date = datetime.now() + timedelta(days=i)
        day_label.config(text=future_date.strftime("%A"))
#
#
# 
    
def getweather_with_loading():
    loading_label.place(x=400, y=100)
    root.update_idletasks()
    try:
        getweather()
    finally:
        loading_label.place_forget()  

#
#
#

logo_image=PhotoImage(file="weather-icon-png-11081.png")
logo=Label(image=logo_image,bg="#202731")
logo.place(x=1,y=1)


frame=Frame(root,width=900,height=180,bg="#202731")
frame.pack(side=BOTTOM)


firstbox=PhotoImage(file="Rounded Rectangle 2.png")
secondbox=PhotoImage(file="Rounded Rectangle 2 copy.png")


Label(frame,image=firstbox,bg="#202731").place(x=30,y=20)
Label(frame,image=secondbox,bg="#202731").place(x=300,y=30)
Label(frame,image=secondbox,bg="#202731").place(x=425,y=30)
Label(frame,image=secondbox,bg="#202731").place(x=550,y=30)
Label(frame,image=secondbox,bg="#202731").place(x=675,y=30)


frame_image=PhotoImage(file="Copy of box.png")
frame_myimage=Label(image=frame_image,bg="#202731")
frame_myimage.pack(padx=5,pady=5,side=BOTTOM)


label1=Label(root,text="WIND",font=("helvetica",14,"italic"),fg="white",bg="#1aa1d2")
label1.place(x=100,y=225)

label2=Label(root,text="HUMIDITY",font=("Helvetica",14,"italic"),fg="white",bg="#1aa1d2")
label2.place(x=230,y=225)

label3=Label(root,text="PRESSURE",font=("Helvetica",14,"italic"),fg="white",bg="#1aa1d2")
label3.place(x=400,y=225)

label4=Label(root,text="DESCRIPTION",font=("Helvetica",14,"italic"),fg="white",bg="#1aa1d2")
label4.place(x=580,y=225)


t=Label(root,font=("helvetica",20,"italic"),bg="#202731",fg="white")
t.place(x=300,y=110)

c=Label(font=("arial",15,"italic"),bg="#202731",fg="#FFFFFF")
c.place(x=275,y=150)

w=Label(text="...",font=("arial",15,"italic"),bg="#1aa1d2")
w.place(x=100,y=250)

h=Label(text="...",font=("arial",15,"italic"),bg="#1aa1d2")
h.place(x=250,y=250)

p=Label(text="...",font=("arial",15,"italic"),bg="#1aa1d2")
p.place(x=400,y=250)

d=Label(text="...",font=("arial",15,"italic"),bg="#1aa1d2")
d.place(x=580,y=250)


Search_image=PhotoImage(file="Rounded Rectangle 3.png")
myimage=Label(root,image=Search_image,bg="#202731")
myimage.place(x=280,y=20)


Search_icon=PhotoImage(file="layer 6.png")
#myimage_icon=Button(root,image=Search_icon,borderwidth=0,cursor= "hand2",bg="#333c4c",command=getweather)
myimage_icon = Button(root, image=Search_icon, borderwidth=0, cursor="hand2", bg="#333c4c", command=getweather_with_loading)

myimage_icon.place(x=670,y=30)

loading_label = Label(root, text="Loading...", font=("Helvetica", 14, "italic"), fg="white", bg="#202731")
loading_label.place(x=383, y=75)  
loading_label.place_forget()



textfield=tk.Entry(root,justify="center",width=15,font=("poppins",25,"italic"),bg="#333c4c",border=0,fg="white")
textfield.place(x=383,y=32)


weat_image=PhotoImage(file="Layer 7.png")
weatherimage=Label(root,image=weat_image,bg="#333c4c")
weatherimage.place(x=312,y=23)


clock=Label(root,font=("helvetica",20,"italic"),bg="#202731",fg="white")
clock.place(x=1,y=1)

timezone=Label(root,font=("helvetica",20,"italic"),bg="#202731",fg="white")
timezone.place(x=550,y=100)

long_lat=Label(root,font=("helvetica",10),bg="#202731",fg="white")
long_lat.place(x=550,y=135)


firstframe=Frame(root,width=230,height=132,bg="#323661")
firstframe.place(x=35,y=345)

firstimage=Label(firstframe,bg="#323661")
firstimage.place(x=10,y=25)

day1=Label(firstframe,font=("Arial 20"),bg="#323661",fg="white")
day1.place(x=95,y=15)

day1temp=Label(firstframe,font=("Arial 15 italic"),bg="#323661",fg="white")
day1temp.place(x=90,y=60)


secondframe=Frame(root,width=70,height=115,bg="#eeefea")
secondframe.place(x=305,y=355)

secondimage=Label(secondframe,bg="#eeefea")
secondimage.place(x=3,y=20)


day2=Label(secondframe,font=("Arial 9"),bg="#eeefea",fg="#000")
day2.place(x=2,y=5)

day2temp=Label(secondframe,font=("Arial 8 italic"),bg="#eeefea",fg="#000")
day2temp.place(x=1,y=75)


thirdframe=Frame(root,width=70,height=115,bg="#eeefea")
thirdframe.place(x=430,y=355)

thirdimage=Label(thirdframe,bg="#eeefea")
thirdimage.place(x=3,y=20)


day3=Label(thirdframe,font=("Arial 9"),bg="#eeefea",fg="#000")
day3.place(x=2,y=5)

day3temp=Label(thirdframe,font=("Arial 8 italic"),bg="#eeefea",fg="#000")
day3temp.place(x=1,y=75)


fourthframe=Frame(root,width=70,height=115,bg="#eeefea")
fourthframe.place(x=555,y=355)

fourthimage=Label(fourthframe,bg="#eeefea")
fourthimage.place(x=3,y=20)


day4=Label(fourthframe,font=("Arial 9"),bg="#eeefea",fg="#000")
day4.place(x=2,y=5)

day4temp=Label(fourthframe,font=("Arial 8 italic"),bg="#eeefea",fg="#000")
day4temp.place(x=1,y=75)


fifthframe=Frame(root,width=70,height=115,bg="#eeefea")
fifthframe.place(x=680,y=355)

fifthimage=Label(fifthframe,bg="#eeefea")
fifthimage.place(x=3,y=20)


day5=Label(fifthframe,font=("Arial 9"),bg="#eeefea",fg="#000")
day5.place(x=2,y=5)

day5temp=Label(fifthframe,font=("Arial 8 italic"),bg="#eeefea",fg="#000")
day5temp.place(x=1,y=75)

day_widget= [
        (firstimage,day1,day1temp),
        (secondimage,day2,day2temp),
        (thirdimage,day3,day3temp),
        (fourthimage,day4,day4temp),
        (fifthimage,day5,day5temp),
]



root.mainloop()
