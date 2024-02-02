import datetime
import requests
import openai

client = openai.OpenAI(api_key='APIKEY',)
api_weather = 'APIKEY'

#Say Hello
def hello():
    message = 'hello'
    return message

#Say Goodbye
def goodbye():
    message = 'goodbye'
    return message

#Say I Don't Understand
def dont_understand():
    message = 'I dont understand'
    return message

#Get Current Time
def get_time():
    current_time = datetime.datetime.now()
    message = str(current_time.strftime("%A %H:%M"))
    return message

#Get Current Weather
def get_weather():
    #ip_address = requests.get('https://api.ipify.org').text	
    ip_address = '72.250.236.50'
    ip_data = requests.get(f'http://ip-api.com/json/{ip_address}').json()
    weather = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={ip_data["lat"]}&lon={ip_data["lon"]}&units=imperial&appid={api_weather}').json()
    message = f'Current temp: {weather["main"]["temp"]} degrees  - High: {weather["main"]["temp_max"]}  Low: {weather["main"]["temp_min"]}\n{weather["weather"][0]["main"]} -- {weather["weather"][0]["description"]}  '
    return message

#Get a Joke
def get_joke(phrase):
    response = client.chat.completions.create(
         messages=[
        {"role": "system", "content": "you are a comedian"},
        {"role": "assistant", "content": "answer in less than 25 words"},
        {"role": "user", "content": phrase}
        ],
        model="gpt-3.5-turbo",
    )
    message = response.choices[0].message.content
    return message
