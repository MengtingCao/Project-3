from tokenize import Double
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseRedirect
from .GroupMeAPI import groupmeapi as grme
from .DiscordAPI import discordapi as dapi
from .SlackAPI import slackapi as sapi
from datetime import datetime, date, time
from dateutil.parser import parse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from   django.contrib.messages import success
import json, requests
import psycopg2


from cryptography.fernet import Fernet

hostname = 'ec2-54-173-77-184.compute-1.amazonaws.com'
database = 'd2jg1tt725t1j4'
username = 'orysgydtilkzew'
pwd = '3c9add640649eec2525bc7871bcddebf38c054788f25ceee8e10b99d5fb40c62'
port_id = 5432

encryptionKey = "gRNCcDPDnSzqT2RT4nFJA6MYtsJkBG85sMEy9TogRYg="
fernet = Fernet(encryptionKey)

def storeGroupMeKey(name, authentication_key):

    #print(name+ " : " + authentication_key)
    encMessage = fernet.encrypt(authentication_key.encode())
    #print(name+ " : " + encMessage)
    conn = psycopg2.connect(
        host = hostname,
        dbname = database,
        user = username,
        password = pwd,
        port = port_id)
    cur = conn.cursor()
    db= "UPDATE  users SET groupme_auth = '" + encMessage.decode("utf-8")  + "' WHERE username = '" + name + "';"
    cur.execute(db)
    conn.commit()
    cur.close()
    conn.close()
    return 1



def returnGroupMeKey(name):
    conn = psycopg2.connect(
        host = hostname,
        dbname = database,
        user = username,
        password = pwd,
        port = port_id)
    cur = conn.cursor()
    db = "SELECT * FROM users WHERE username = '" + name +"';"
    cur.execute(db)
    conn.commit()
    encMessage = cur.fetchall()
    cur.close()
    conn.close()
    for message in encMessage:
        encoded = message[3]
    return fernet.decrypt(encoded.encode('utf-8')).decode()