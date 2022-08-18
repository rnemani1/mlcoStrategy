from pickle import TRUE
from telnetlib import DO
from termios import TIOCPKT_DOSTOP
from this import d
from dotenv import load_dotenv
from requests import TooManyRedirects
load_dotenv(".env", override=True)
from google.cloud import firestore
import pandas as pd
import twilioManager
from datetime import datetime

firestoreRef = firestore.Client(project='vegas-mlcostrategy')
collection = firestoreRef.collection('open case').orderBy("uSpread", "asc")

print(collection)

    