import discord

key_features = {
  'feels_like':'Feels Like', 
  'temp':'Temparature', 
  'temp_min':'Minimum Temperature',
  'temp_max':'Maximum Temperature'
}

# taking data from weather api, and parsing what we want. 
def parse_data(data):
  data = data['main']
  del data['humidity']
  del data['pressure']
  return data

# using imbedded messages to output data to Discord
def weather_message(data, location):
  location = location.title()
  message = discord.Embed(
    title=f'Weather in {location}',
    description=f'Here is the weather in {location}'
  )
  for key in data:
    message.add_field(
      name=key_features[key], 
      value=str(data[key]), 
      inline=False #formats into a vertical table
    )
  return message 

#error message if someone types in invalid location
def error_message(location):
  location = location.title()
  return discord.embed(
    title='Error', 
    description=f'There was an error retrieving weather data for {location}.'
    
  )