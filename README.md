# Machine-Learning-with-OpenAI-API-and-Relational-Database-OpenAI-Python-SQLite-
Machine Learning with OpenAI API and Relational Database (OpenAI, Python, SQLite)

YouTube Video - https://youtu.be/QRdxtO1PU3w

This project uses SQLite as a cacheing mechanism for OpenAI API requests.  When a user makes a request from OpenAI the request and the response is inserted into a SQLite table.  The script checks the if a request is already stored in the database and if it is then the database is read from instead of doing an API call.

## Modules

OpenAI

sqlite3

gtts

speechrecognition

For Voice Recognition you also need to install pyaudio
