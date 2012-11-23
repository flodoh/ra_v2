# coding=utf-8
'''
Created on 04.12.2011
@author: Eric
@funktion: Dies ist die alte Klasse für die CRUD-Operationen an der Datenbank.
Ersetzt wird dieses durch die Verwendung der sqlobject-Library
'''

import sqlite3

from time import gmtime, strftime

DBNAME = "../database/db1.db"         


def new_policy(name, text, url):
    # Connect to existing DB
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    
    date = strftime("%Y-%m-%d", gmtime())
    name =  str(name)
    text =  str(text)
    url = str(url)
    values = (name, text, url, date)
    query = "INSERT INTO Policies (name, policy, url, date) VALUES (?, ?, ?, ?)"
    cursor.execute(query, values)
    row = cursor.lastrowid
    connection.commit()

    return row

def get_policy_by_rowid(row):
    # Connect to existing DB
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    
    query = """SELECT * FROM Policies WHERE rowid = '""" + str(row) + """';"""
    cursor.execute(query)
    data = cursor.fetchone()
    
    return data

def get_policy_by_name(name):
    # Connect to existing DB
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
        
    query = """SELECT * FROM Policies WHERE name = '""" + name + """';"""
    cursor.execute(query)   
    r =  cursor.fetchall() 
        
    return r

def get_policies_by_names(list):
    names_query = ""
    for item in list:
        names_query = names_query + """'""" + item + """' OR name =  """
    
    names_query = names_query[:-11]
    
    # Connect to existing DB
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()   
    query = """SELECT * FROM Policies WHERE name = """ + names_query + """;"""  
    cursor.execute(query)   
    r =  cursor.fetchall() 
    data = {}
    
    for row in r:
        name = row[1]
        name = str(name)
        
        text = row[2]
        text = str(text.encode('utf-8'))
            
        url = row[0]
        url = str(url)
            
        date = row[3]
        date = str(date)
            
        data[name] = {}
        data[name]["name"] = name
        data[name]["text"] = text
        data[name]["url"] = url
        data[name]["date"] = date
    
    return data
    
def get_all_names():
    # Connect to existing DB
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    
    query = """SELECT * FROM Policies;"""
    cursor.execute(query)
    data = cursor.fetchall()
    name_list = []
    
    for row in data:
        name = row[1]
        name_list.append(name)
        
    print name_list


def get_all_policies():
    # Connect to existing DB    
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
        
    query = """SELECT * FROM Policies;"""
    cursor.execute(query)   
    r =  cursor.fetchall() 
    data = {}

    for row in r:
        name = row[1]
        name = str(name)
        
        text = row[2]
        text = str(text.encode('utf-8'))
            
        url = row[0]
        url = str(url)
            
        date = row[3]
        date = str(date)
            
        data[name] = {}
        data[name]["name"] = name
        data[name]["text"] = text
        data[name]["url"] = url
        data[name]["date"] = date
        
    return data