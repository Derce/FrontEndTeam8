# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 22:41:11 2022

@author: Eduar
"""

import tkinter as tk
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
import redshift_connector

import pandas as pd
from tkinter import *
import sqlite3
from tkinter.filedialog import asksaveasfile
from tkinter.messagebox  import showinfo
from tkinter import filedialog
import tkinter.scrolledtext as st
from tkinter import messagebox, ttk
from tkinter.tix import *

 
# Connecting with Redshift
conn = redshift_connector.connect(
     host='ds4a-final.c6vjo8xyv3b0.us-east-1.redshift.amazonaws.com',
     database='dev',
     user='awsuser_iman',
     password='Water12345!'
  )

cursor: redshift_connector.Cursor = conn.cursor()


# Connecting with sqlite3
conn = sqlite3.connect('Form1.db')

with conn:

    cursor1 = conn.cursor()

   

#Creating the root for the main window
root= tk.Tk()

# root.resizable(0, 0)

root.title("Air Fare Report Analysis")

root.resizable(True, True)

root.configure(background = 'white')

reg = Frame(root)

 

origin = StringVar()

destination = StringVar()



Dataframe=pd.DataFrame(columns = ['city1','airport_1','city2', 'airport_2','passengers', 'prices', 'date'])



def database():

          

        origin = combo1.get()

        destination = combo2.get()

        
        cursor1.execute('CREATE TABLE IF NOT EXISTS Search ( id_key integer primary key autoincrement,origin TEXT,destination TEXT)')

        cursor1.execute('INSERT INTO Search (origin,destination) VALUES(?,?)', (origin,destination))

        conn.commit()

        showinfo( title = "Search Record", message = "Data inserted sucessfully")
        
        

def display():
    

    text_area.config(state=NORMAL)

    text_area.delete(1.0,"end")
    
    origin = combo1.get()
    
    destination = combo2.get()
    
    
    if ((origin == '') or (destination == '') ):

          messagebox.showerror('error', 'Please check all the fields!')

          return
    database() #Calling this function and Saving the Search here 
    
    o=origin[0:3]
    d=destination[0:3]
    
    cursor.execute("select distinct city1,airport_1,city2,airport_2,passengers,fare,date from airfare.flight_data where date >= '2017-01-01'")
    test1 = cursor.fetchall()

    prices1=pd.DataFrame(test1, columns = ['city1','airport_1','city2', 'airport_2','passengers', 'prices', 'date'])

    prices2= prices1[(prices1['airport_1'] == o) & (prices1['airport_2'] == d)]
    prices2 = prices2.sort_values('date')
    
   
    # Inserting Text which is read only
    text_area.insert(tk.INSERT,prices2.to_string())
    text_area.configure(state ='disabled')
              
    # root= tk.Tk() 
    # root.resizable(100, 100)
    # root.title("Air Fare Report Analysis")
    # root.configure(background = 'white')
    
    
    figure1 = plt.Figure(figsize=(10,8), dpi=70)
    ax1 = figure1.add_subplot(111)
    bar1 = FigureCanvasTkAgg(figure1, root)
    bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    prices2.plot(x = 'date', y ='passengers', kind='bar', legend=True, ax=ax1, color='b')
    ax1.set_title('Year Vs. Passengers' + '   '+ o + '/' + d)
    # canvas1.create_window(100, 310, window=bar1)
    
     
    figure2 = plt.Figure(figsize=(10,8), dpi=70)
    ax2 = figure2.add_subplot(111)
    line2 = FigureCanvasTkAgg(figure2, root)
    line2.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH)
    prices2.plot(x = 'date', y = 'prices', kind='line', legend=True, ax=ax2, color='r',marker='o', fontsize=10)
    ax2.set_title('Year Vs. Air Fare Prices' + '   '+ o + '/' + d)
    # canvas1.create_window(550, 550, window=line2)
    
    return figure1,figure2
     
    # root.mainloop()
    
    

def Export():
    
    cursor.execute("select distinct city1,airport_1,city2,airport_2,passengers,fare,date from airfare.flight_data where date >= '2017-01-01'")
    test1 = cursor.fetchall()

    Dataframe=pd.DataFrame(test1, columns = ['city1','airport_1','city2', 'airport_2','passengers', 'prices', 'date'])

    files = [('EXCEL', '*.xlsx'),('All Files', '.csv')]

    try:

        file = asksaveasfile(filetypes = files, defaultextension = files)
    
        writerL = pd.ExcelWriter(file.name, engine='xlsxwriter')
    
        Dataframe.to_excel(writerL, sheet_name='Air fare data',index=False)
    
        writerL.save()
    
        showinfo( title = "Excel Export", message = "Data exported sucessfully")

    except:

         messagebox.showerror('Error', 'Data could not export! Try closing the file')   

    

def retrieve():

   
    clear()   

    cursor1.execute('SELECT origin FROM Search ORDER BY id_key DESC LIMIT 1')

    origin = cursor1.fetchone()

    combo1.insert('end'," ".join(origin))  

 

    cursor1.execute('SELECT destination FROM Search ORDER BY id_key DESC LIMIT 1')

    destination= cursor1.fetchone()

    combo2.insert('end', " ".join(destination))

    

    

def clear():

    combo1.set('')

    combo2.set('')

    text_area.config(state=NORMAL)

    text_area.delete(1.0,"end")

    text_area.config(state=DISABLED)
    
    # canvas.delete('all')
    # plt.cla()
       

 

canvas1 = tk.Canvas(root, width = 1300, height = 358,  relief = 'raised', bg="white")

canvas1.pack()

 
  

label1 = tk.Label(root, text='Air Fare Report Analysis ')

label1.config(font=("bold", 18),bg="white")

canvas1.create_window(250, 30, window=label1)

 

label2 = tk.Label(root, text='* Origin City:')

label2.config(font=('helvetica',14),bg="white")

canvas1.create_window(80, 90, window=label2)

 
combo1 = ttk.Combobox(root, width=35,

state="edit", #this can be "edit"

values=[ 'SLC-Salt Lake City, UT', 'LAS-Las Vegas, NV',   'LAX-Los Angeles, CA (Metropolitan Area)', 
  'ABQ-Albuquerque, NM',   'MDW-Chicago, IL',   'ALB-Albany, NY', 
  'AMA-Amarillo, TX',   'ASE-Aspen, CO', 
  'ATL-Atlanta, GA (Metropolitan Area)',   'AUS-Austin, TX', 
  'AVL-Asheville, NC',   'AZA-Phoenix, AZ',   'BDL-Hartford, CT', 
  'BHM-Birmingham, AL',   'BIS-Bismarck/Mandan, ND', 
  'BNA-Nashville, TN',   'MEM-Memphis, TN', 
  'MHT-Boston, MA (Metropolitan Area)',   'BOI-Boise, ID', 
  'BOS-Boston, MA (Metropolitan Area)', 
  'ONT-Los Angeles, CA (Metropolitan Area)',   'ORD-Chicago, IL', 
  'BTV-Burlington, VT',   'BUF-Buffalo, NY', 
  'BUR-Los Angeles, CA (Metropolitan Area)', 
  'ORF-Norfolk, VA (Metropolitan Area)',   'BZN-Bozeman, MT', 
  'CAE-Columbia, SC',   'CAK-Cleveland, OH (Metropolitan Area)', 
  'PHX-Phoenix, AZ',   'PIA-Peoria, IL',   'PIT-Pittsburgh, PA', 
  'PVD-Boston, MA (Metropolitan Area)',   'CHS-Charleston, SC', 
  'ROC-Rochester, NY',   'RSW-Fort Myers, FL', 
  'CLE-Cleveland, OH (Metropolitan Area)',   'SAV-Savannah, GA', 
  'SDF-Louisville, KY',   'SYR-Syracuse, NY',   'CLT-Charlotte, NC', 
  'CMH-Columbus, OH',   'COS-Colorado Springs, CO', 
  'CVG-Cincinnati, OH',   'DAL-Dallas/Fort Worth, TX', 
  'JFK-New York City, NY (Metropolitan Area)', 
  'DCA-Washington, DC (Metropolitan Area)',   'DEN-Denver, CO', 
  'DFW-Dallas/Fort Worth, TX',   'DSM-Des Moines, IA', 
  'DTW-Detroit, MI',   'EGE-Eagle, CO',   'ELP-El Paso, TX', 
  'EUG-Eugene, OR',   'EWR-New York City, NY (Metropolitan Area)', 
  'EYW-Key West, FL',   'FAT-Fresno, CA', 
  'FLL-Miami, FL (Metropolitan Area)',   'GRR-Grand Rapids, MI', 
  'GSO-Greensboro/High Point, NC',   'GSP-Greenville/Spartanburg, SC', 
  'HOU-Houston, TX',   'HPN-New York City, NY (Metropolitan Area)', 
  'HRL-Harlingen/San Benito, TX',   'HSV-Huntsville, AL', 
  'IAH-Houston, TX',   'IND-Indianapolis, IN', 
  'ISP-New York City, NY (Metropolitan Area)',   'JAC-Jackson, WY', 
  'JAX-Jacksonville, FL',   'ACK-Nantucket, MA',   'PNS-Pensacola, FL', 
  'BLI-Bellingham, WA',   'CHA-Chattanooga, TN', 
  'CRP-Corpus Christi, TX',   'DAB-Daytona Beach, FL', 
  'DAY-Dayton, OH',   'FCA-Kalispell, MT', 
  'IAD-Washington, DC (Metropolitan Area)',   'RDM-Bend/Redmond, OR', 
  'RDU-Raleigh/Durham, NC',   'RNO-Reno, NV',   'SAN-San Diego, CA', 
  'LGA-New York City, NY (Metropolitan Area)', 
  'LGB-Los Angeles, CA (Metropolitan Area)',   'LIT-Little Rock, AR', 
  'MCI-Kansas City, MO',   'MCO-Orlando, FL', 
  'MIA-Miami, FL (Metropolitan Area)',   'MKE-Milwaukee, WI', 
  'MSN-Madison, WI',   'MSP-Minneapolis/St. Paul, MN', 
  'MSY-New Orleans, LA',   'MVY-Marthas Vineyard, MA', 
  'MYR-Myrtle Beach, SC',   'OAK-San Francisco, CA (Metropolitan Area)', 
  'BIL-Billings, MT',   'FAR-Fargo, ND',   'FNT-Flint, MI', 
  'OKC-Oklahoma City, OK',   'LEX-Lexington, KY',   'OMA-Omaha, NE', 
  'PDX-Portland, OR',   'PHF-Norfolk, VA (Metropolitan Area)', 
  'PHL-Philadelphia, PA',   'PWM-Portland, ME',   'SAT-San Antonio, TX', 
  'SEA-Seattle, WA',   'SFO-San Francisco, CA (Metropolitan Area)', 
  'SJC-San Francisco, CA (Metropolitan Area)', 
  'SNA-Los Angeles, CA (Metropolitan Area)', 
  'SRQ-Sarasota/Bradenton, FL',   'STL-St. Louis, MO', 
  'SWF-New York City, NY (Metropolitan Area)',   'TYS-Knoxville, TN', 
  'XNA-Fayetteville, AR',   'ECP-Panama City, FL', 
  'BWI-Washington, DC (Metropolitan Area)',   'PSP-Palm Springs, CA', 
  'RIC-Richmond, VA', 'TUL-Tulsa, OK', 
  'TUS-Tucson, AZ',   'ACY-Atlantic City, NJ',   'BGR-Bangor, ME', 
  'GEG-Spokane, WA',   'USA-Concord, NC', 
  'TPA-Tampa, FL (Metropolitan Area)',   'VPS-Valparaiso, FL', 
  'CID-Cedar Rapids/Iowa City, IA',   'FWA-Fort Wayne, IN', 
  'JAN-Jackson/Vicksburg, MS',   'SBN-South Bend, IN', 
  'SMF-Sacramento, CA',   'LCK-Columbus, OH',   'BTR-Baton Rouge, LA', 
  'MOT-Minot, ND',   'PAE-Everett, WA',   'CHO-Charlottesville, VA', 
  'ABE-Allentown/Bethlehem/Easton, PA',   'IDA-Idaho Falls, ID', 
  'MDT-Harrisburg, PA',   'PIE-Tampa, FL (Metropolitan Area)', 
  'ATW-Appleton, WI',   'PSC-Pasco/Kennewick/Richland, WA', 
  'MFR-Medford, OR',   'SGF-Springfield, MO',   'MSO-Missoula, MT', 
  'FSD-Sioux Falls, SD',   'HHH-Hilton Head, SC',   'HTS-Ashland, WV', 
  'BLV-Belleville, IL']

 )

 
canvas1.create_window(272, 90, window=combo1)

 
 
label3 = tk.Label(root, text=' * Destination:')

label3.config(font=('helvetica',14),bg="white")

canvas1.create_window(65, 140, window=label3)

 

combo2 = ttk.Combobox(root, width=35,

state="edit", #this can be "readonly"

values=[ 'TPA-Tampa, FL (Metropolitan Area)', 'LAS-Las Vegas, NV',   'LAX-Los Angeles, CA (Metropolitan Area)', 
  'ABQ-Albuquerque, NM',   'MDW-Chicago, IL',   'ALB-Albany, NY', 
  'AMA-Amarillo, TX',   'ASE-Aspen, CO', 
  'ATL-Atlanta, GA (Metropolitan Area)',   'AUS-Austin, TX', 
  'AVL-Asheville, NC',   'AZA-Phoenix, AZ',   'BDL-Hartford, CT', 
  'BHM-Birmingham, AL',   'BIS-Bismarck/Mandan, ND', 
  'BNA-Nashville, TN',   'MEM-Memphis, TN', 
  'MHT-Boston, MA (Metropolitan Area)',   'BOI-Boise, ID', 
  'BOS-Boston, MA (Metropolitan Area)', 
  'ONT-Los Angeles, CA (Metropolitan Area)',   'ORD-Chicago, IL', 
  'BTV-Burlington, VT',   'BUF-Buffalo, NY', 
  'BUR-Los Angeles, CA (Metropolitan Area)', 
  'ORF-Norfolk, VA (Metropolitan Area)',   'BZN-Bozeman, MT', 
  'CAE-Columbia, SC',   'CAK-Cleveland, OH (Metropolitan Area)', 
  'PHX-Phoenix, AZ',   'PIA-Peoria, IL',   'PIT-Pittsburgh, PA', 
  'PVD-Boston, MA (Metropolitan Area)',   'CHS-Charleston, SC', 
  'ROC-Rochester, NY',   'RSW-Fort Myers, FL', 
  'CLE-Cleveland, OH (Metropolitan Area)',   'SAV-Savannah, GA', 
  'SDF-Louisville, KY',   'SYR-Syracuse, NY',   'CLT-Charlotte, NC', 
  'CMH-Columbus, OH',   'COS-Colorado Springs, CO', 
  'CVG-Cincinnati, OH',   'DAL-Dallas/Fort Worth, TX', 
  'JFK-New York City, NY (Metropolitan Area)', 
  'DCA-Washington, DC (Metropolitan Area)',   'DEN-Denver, CO', 
  'DFW-Dallas/Fort Worth, TX',   'DSM-Des Moines, IA', 
  'DTW-Detroit, MI',   'EGE-Eagle, CO',   'ELP-El Paso, TX', 
  'EUG-Eugene, OR',   'EWR-New York City, NY (Metropolitan Area)', 
  'EYW-Key West, FL',   'FAT-Fresno, CA', 
  'FLL-Miami, FL (Metropolitan Area)',   'GRR-Grand Rapids, MI', 
  'GSO-Greensboro/High Point, NC',   'GSP-Greenville/Spartanburg, SC', 
  'HOU-Houston, TX',   'HPN-New York City, NY (Metropolitan Area)', 
  'HRL-Harlingen/San Benito, TX',   'HSV-Huntsville, AL', 
  'IAH-Houston, TX',   'IND-Indianapolis, IN', 
  'ISP-New York City, NY (Metropolitan Area)',   'JAC-Jackson, WY', 
  'JAX-Jacksonville, FL',   'ACK-Nantucket, MA',   'PNS-Pensacola, FL', 
  'BLI-Bellingham, WA',   'CHA-Chattanooga, TN', 
  'CRP-Corpus Christi, TX',   'DAB-Daytona Beach, FL', 
  'DAY-Dayton, OH',   'FCA-Kalispell, MT', 
  'IAD-Washington, DC (Metropolitan Area)',   'RDM-Bend/Redmond, OR', 
  'RDU-Raleigh/Durham, NC',   'RNO-Reno, NV',   'SAN-San Diego, CA', 
  'LGA-New York City, NY (Metropolitan Area)', 
  'LGB-Los Angeles, CA (Metropolitan Area)',   'LIT-Little Rock, AR', 
  'MCI-Kansas City, MO',   'MCO-Orlando, FL', 
  'MIA-Miami, FL (Metropolitan Area)',   'MKE-Milwaukee, WI', 
  'MSN-Madison, WI',   'MSP-Minneapolis/St. Paul, MN', 
  'MSY-New Orleans, LA',   'MVY-Marthas Vineyard, MA', 
  'MYR-Myrtle Beach, SC',   'OAK-San Francisco, CA (Metropolitan Area)', 
  'BIL-Billings, MT',   'FAR-Fargo, ND',   'FNT-Flint, MI', 
  'OKC-Oklahoma City, OK',   'LEX-Lexington, KY',   'OMA-Omaha, NE', 
  'PDX-Portland, OR',   'PHF-Norfolk, VA (Metropolitan Area)', 
  'PHL-Philadelphia, PA',   'PWM-Portland, ME',   'SAT-San Antonio, TX', 
  'SEA-Seattle, WA',   'SFO-San Francisco, CA (Metropolitan Area)', 
  'SJC-San Francisco, CA (Metropolitan Area)', 
  'SNA-Los Angeles, CA (Metropolitan Area)', 
  'SRQ-Sarasota/Bradenton, FL',   'STL-St. Louis, MO', 
  'SWF-New York City, NY (Metropolitan Area)',   'TYS-Knoxville, TN', 
  'XNA-Fayetteville, AR',   'ECP-Panama City, FL', 
  'BWI-Washington, DC (Metropolitan Area)',   'PSP-Palm Springs, CA', 
  'RIC-Richmond, VA',   'SLC-Salt Lake City, UT',   'TUL-Tulsa, OK', 
  'TUS-Tucson, AZ',   'ACY-Atlantic City, NJ',   'BGR-Bangor, ME', 
  'GEG-Spokane, WA',   'USA-Concord, NC', 
  'VPS-Valparaiso, FL', 
  'CID-Cedar Rapids/Iowa City, IA',   'FWA-Fort Wayne, IN', 
  'JAN-Jackson/Vicksburg, MS',   'SBN-South Bend, IN', 
  'SMF-Sacramento, CA',   'LCK-Columbus, OH',   'BTR-Baton Rouge, LA', 
  'MOT-Minot, ND',   'PAE-Everett, WA',   'CHO-Charlottesville, VA', 
  'ABE-Allentown/Bethlehem/Easton, PA',   'IDA-Idaho Falls, ID', 
  'MDT-Harrisburg, PA',   'PIE-Tampa, FL (Metropolitan Area)', 
  'ATW-Appleton, WI',   'PSC-Pasco/Kennewick/Richland, WA', 
  'MFR-Medford, OR',   'SGF-Springfield, MO',   'MSO-Missoula, MT', 
  'FSD-Sioux Falls, SD',   'HHH-Hilton Head, SC',   'HTS-Ashland, WV', 
  'BLV-Belleville, IL']

 )

canvas1.create_window(272, 140, window=combo2)



button7 = tk.Button(text='   Display   ',command=display, bg='black', fg='white', font=('helvetica', 12, 'bold'))

canvas1.create_window(190, 230, window=button7)
 


button4 = tk.Button(text='   Retrieve   ',command=retrieve, bg='black', fg='white', font=('helvetica', 12, 'bold'))

canvas1.create_window(315, 230, window=button4)

 

button5 = tk.Button(text='   Export   ',command=Export, bg='black', fg='white', font=('helvetica', 12, 'bold'))

canvas1.create_window(190, 310, window=button5)



button3 = tk.Button(text='   Clear   ',command=clear, bg='black', fg='white', font=('helvetica', 12, 'bold'))

canvas1.create_window(315, 310, window=button3)

 

lblDisplay = tk.Label(root, text = "TABLES")

lblDisplay.config(font=('Helvetica',15,'bold'),fg='black',justify=CENTER,bg="white")

canvas1.create_window(900, 25, window=lblDisplay)

 

text_area = st.ScrolledText(root,

                            width = 90,

                            height = 16,

                            font = ("Helvetica",

                                    12))

canvas1.create_window(880, 190, window=text_area)



 

def iExit():

    iExit = tk.messagebox.askyesno("Exit","Do you want to exit ?")

    if iExit>0:

        root.destroy()

        return

   

 

def Data():

    root.resizable(width=True, height=True)

    root.geometry("1000x500+0+0")

 

 

def Form():

    root.resizable(width=True, height=True)

    root.geometry("500x500+0+0")

    root.config(font=('Helvetica',18,'bold'),fg='blue',justify=CENTER,bg="white")

 

 

def on_closing():

    if messagebox.askokcancel("Quit", "Do you want to quit?"):

        root.destroy()

 

root.protocol("WM_DELETE_WINDOW", on_closing)

 

   

menubar = Menu(reg)

 

filemenu = Menu(menubar, tearoff = 0)

menubar.add_cascade(label = 'Menu', menu = filemenu)

filemenu.add_command(label = "Exit",command = iExit)

root.config(menu=menubar)

 

 

mainloop()