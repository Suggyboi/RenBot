import discord 
import os
import requests 
import json 
import weather

# function names are gathered from discord.py library

client = discord.Client()
# defining weather token
weather_token = os.environ['WEATHERTOKEN']

#Returning the quote of the day from zenquotes.io
def get_quoteofday(): 
  response = requests.get("https://zenquotes.io/api/today") #Generate quote of day
  json_data = json.loads(response.text)
  quoteofday = json_data[0]['q'] + " -" + json_data[0]['a']#q = quote
  return(quoteofday)

#Returning the random quote from zenquotes.io
def get_randomquote(): 
  response = requests.get("https://zenquotes.io/api/random") #Generate random quote
  json_data = json.loads(response.text)
  randomquote = json_data[0]['q'] + " -" + json_data[0]['a']#q = quote
  return(randomquote)

#Returning a dadjoke in JSON format 
def get_dadjoke():
  headers = {
    'x-rapidapi-key': "c52c2964famshad8b00a4de6f0aap169565jsn6b154b90ab87",
    'x-rapidapi-host': "dad-jokes.p.rapidapi.com"
    }
  url = "https://dad-jokes.p.rapidapi.com/random/jokes"
  response = requests.request("GET", url, headers=headers)
  return(response.text)


#decorator to register an event 
@client.event 
async def on_ready(): #called when bot is ready to be used
  print('We have logged in as {0.user}'.format(client)) #prints username
  # shows discord bot status as "Listening to $commands"
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='$commands'))

@client.event
#when message is recieved
async def on_message(message): 
  if message.author == client.user:
    return 
  
  #when bot sees this command it will send a message
  if message.content.startswith('$hello'):
    await message.channel.send('Hello! {}'.format(message.author))

  #when bot sees this command it will send quote of the day 
  elif message.content.startswith('$quoteofday'): 
    quoteofday = get_quoteofday()
    await message.channel.send(quoteofday)

  #when bot sees this command it will send a random quote 
  elif message.content.startswith('$quoterandom'): 
    randomquote = get_randomquote()
    await message.channel.send(randomquote)
  
  #when bot sees this command it will send a dad joke
  elif message.content.startswith('$dadjoke'): 
    dadjoke = get_dadjoke()
    await message.channel.send(dadjoke)

  # Get the weather of any city. 
  if message.content.startswith('$'):
    location = message.content.replace('$', '').lower()
    if len(location) >= 1:
      url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_token}&units=metric'

      try:
        data = json.loads(requests.get(url).content)
        data = weather.parse_data(data)
        await message.channel.send(embed=weather.weather_message(data, location))
      except KeyError:
        await message.channel.send(embed=weather.error_message(location))






client.run(os.getenv('TOKEN')) # run bot
