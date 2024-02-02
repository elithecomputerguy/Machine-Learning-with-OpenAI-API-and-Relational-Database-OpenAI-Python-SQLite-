import openai
import ai_function
import os
from gtts import gTTS 
import speech_recognition as sr
import sqlite3

client = openai.OpenAI(api_key='APIKEY',)


current_directory = os.path.dirname(os.path.abspath(__file__))
db_name = 'ai.db'
db_path = os.path.join(current_directory, db_name)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
create_table = '''
  create table if not exists decision(
    id integer primary key,
    query text,
    response text
  )
'''
cursor.execute(create_table)
conn.commit()

file_name = 'ai_function.py'
file_path = os.path.join(current_directory, file_name)
with open(file_path, 'r') as file_function:
  file_function = file_function.read()

def ai_request(file_function, query):
  response = client.chat.completions.create(
    messages=[
      {"role": "system", "content": "You are assisting in choosing the most suitable Python function for a user request."},
      {"role": "assistant", "content": "You will be provided with available function names for this program."},
      {"role": "assistant", "content": "Please only provide the name of the function, without additional information or responses."},
      {"role": "assistant", "content": "Do not provide any response other than the correct function name."},
      {"role": "assistant", "content": "If no functions is appropriate return 'dont_understand'"},
      {"role": "assistant", "content": file_function},
      {"role": "user", "content": query}
    ],
    model="gpt-3.5-turbo",
  )
  response = response.choices[0].message.content
  return  response

def speak(answer):
    language = 'en'
    try:
        myobj = gTTS(text=answer, lang=language, slow=False) 
        myobj.save("response.mp3")
        os.system("afplay response.mp3") 
    except:
            pass
   
def stt():
    query = ''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio).lower()
        print(f'Query: {query}')
    except sr.UnknownValueError:
        print("Google Speech Services - Unknown Error")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))    

    return query

os.system('clear')

while True:
    answer = ''
    query = ''
    response =''
  
    print("Say something!")

    query = stt()

    os.system('clear')

    if query == '':
        pass
    elif 'exit' in query:
        answer = 'goodbye'
        speak(answer)
        print(answer)
        break
    elif 'wrong answer' in query:
        answer = f'Sorry. What does {query_last} mean?'
        speak(answer)
        print(answer)
        try:
            learn = stt()
        except:
            print(f'There was an issue with Text to Speech')    
        try:
            sql = 'update decision set response=? where query=?'
            cursor.execute(sql,(learn, query_last))
            conn.commit()
            answer = f'I learned {query_last} means {learn}'
        except sqlite3.Error as e:
            print(f'error: {e}')
    else:
        query_last = query  
        try:
            sql_find = 'select * from decision where query = ?'
            cursor.execute(sql_find, (query,))
            result = cursor.fetchone()
        except sqlite3.Error as e:
            print(f'error: {e}')

        if result == None:
            response = ai_request(file_function, query)
            print(f'OpenAI Response:\n\t {response}')
            if 'understand' not in response:
                try:
                    sql = 'insert into decision(query,response) values(?,?)'
                    cursor.execute(sql,(query, response))
                    conn.commit()
                    print('Query Not in Database -- OpenAI Used')
                    print(f'Added to Database:\n\t {query} = {response}')
                except sqlite3.Error as e:
                    print(f'error: {e}')
            else:
                answer = f'What does "{query}" mean?'
                speak(answer)
                print(answer)
                learn = stt()
                try:
                    print(learn)
                    sql = 'insert into decision(query,response) values(?,?)'
                    cursor.execute(sql,(query, learn))
                    conn.commit()
                    answer = f'I learned {query} means {learn}'
                except sqlite3.Error as e:
                    print(f'error: {e}')
  
        else:
            response = result[2]
            print('Query in Database -- SQLite Used')
            print(f'Result Queryset:\n\t {result}')
            print(f'Result Definition:\n\t {result[1]} == {result[2]}')
            print(f'Response: {response}')

    if 'hello' in response:
        answer = ai_function.hello()
    elif 'goodbye' in response:
        answer = ai_function.goodbye() 
    elif 'time' in response:
        answer = ai_function.get_time()
    elif 'weather' in response:
        answer = ai_function.get_weather()
    elif 'joke' in response:
        answer = ai_function.get_joke(query)

    if answer != '':
        print(f'Message: {answer}')
        speak(answer)