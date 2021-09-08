#D&D Discord Bot - For playing music and rolling dice
#Author: Z. Wool
 

import discord #discord lib
import giphy_client #gif lib
import os #token lib
import random #random lib
import requests #request lib
import json #json lib
import re


from replit import db #replit database lib

from giphy_client.rest import ApiException #api for giphy
from discord.ext import commands #discord bot commands

#initiate client call to discord
client =discord.Client()




#show we have logged into discord server
@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

#event reactions
@client.event
async def on_message(msg):
  api_key=os.getenv('GIFTOKEN')
  api_instance=giphy_client.DefaultApi()
  
  #Say nothing if bot sends
  if msg.author==client.user:
    return
  
  #respond to hello
  if msg.content.startswith('$hello'):
    await msg.channel.send('Hello')

  #turn responding on/off
  if msg.content.startswith("$responding"):
    value = msg.content.split("$responding ",1)[1]
    if value.lower()=="true":
      db["responding"]=True
      await msg.channel.send("Responding is on")
    else:
      db["responding"]=False
      await msg.channel.send("Responding is off")


   #rolls dice based on input
  if msg.content.startswith("$roll"):
    
    dice=msg.content.split("$roll ",1)[1]
    
    
    #for dice rolls with modifers
    try:
      numdice,dietype,mod=re.split("d|\+",dice)
      diceroll=int(mod);
      for x in range(int(numdice)):
        roll=random.randint(1,int(dietype))
        
        #send gif when rolling Nat 20
        if (dietype=="20") and (roll==20):
          try:
            api_response = api_instance.gifs_search_get(api_key,"Natural 20",limit=6)
            lst = list(api_response.data)
            giff=random.choice(lst)
            await msg.channel.send(giff.embed_url)
            await msg.channel.send("you rolled a Nat 20!")
          except ApiException as e:
            print("Exception when calling Api")
        
        #Send gif when rolling Nat 1
        elif (dietype=="20") and (roll==1):
          try:
            api_response = api_instance.gifs_search_get(api_key,"Natural 1",limit=6)
            lst = list(api_response.data)
            giff=random.choice(lst)
            await msg.channel.send(giff.embed_url)
            await msg.channel.send("you rolled a Nat 1...")
          except ApiException as e:
            print("Exception when calling Api")
        diceroll+=roll
        await msg.channel.send("you rolled "+str(diceroll))
      
    #for dice rolls without modifiers
    except:
      try:
        numdice,dietype=re.split("d",dice) 
        mod="0";
        diceroll=int(mod);
        for x in range(int(numdice)):
          roll=random.randint(1,int(dietype))
          
          #send gif when rolling Nat 20
          if (dietype=="20") and (roll==20):
            try:
              api_response = api_instance.gifs_search_get(api_key,"Natural 20",limit=6)
              lst = list(api_response.data)
              giff=random.choice(lst)
              await msg.channel.send(giff.embed_url)
              await msg.channel.send("you rolled a Nat 20!")
            except ApiException as e:
              print("Exception when calling Api")
          
          #Send gif when rolling Nat 1
          elif (dietype=="20") and (roll==1):
            try:
              api_response = api_instance.gifs_search_get(api_key,"Natural 1",limit=6)
              lst = list(api_response.data)
              giff=random.choice(lst)
              await msg.channel.send(giff.embed_url)
              await msg.channel.send("you rolled a Nat 1...")
            except ApiException as e:
              print("Exception when calling Api")
          diceroll+=roll
          await msg.channel.send("you rolled "+str(diceroll))
      except Exception:
        await msg.channel.send("Please enter dice roll in the format of '$roll XdY+Z'")
  #for dice rolls without modifiers
  #Edit so only works if file is uploaded to databace
  
  
  
   
    
    
    
    







  

  



#retried token ford discord
client.run(os.getenv('TOKEN'))
