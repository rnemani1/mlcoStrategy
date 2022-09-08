from pickle import TRUE
from re import A
from telnetlib import DO
from termios import TIOCPKT_DOSTOP
from dotenv import load_dotenv
from requests import TooManyRedirects
load_dotenv(".env", override=True)
from google.cloud import firestore
import pandas as pd
import twilioManager
from datetime import datetime
import os

credential_path = "/Users/rnemani/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Keep/Projects/Vegas/mlcoStrategy/Nemani_Pro_Vegas-mlcoStrategy-key.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

firestoreRef = firestore.Client(project='vegas-mlcostrategy')

def open(league, uTeam, fTeam, fSpread):
    
    collection = firestoreRef.collection('open case')
    document = collection.document()

    oCollection = {}

    for d in collection.stream():

        if(d.get('league') == league and d.get('uTeam') == uTeam):
            oCollection[d.id] = d.get('fSpread')
    
    oCollection_sorted = sorted(oCollection, key=oCollection.get)

    if(len(oCollection) < 2):
        document.set({
            u'league': league,
            u'uTeam': uTeam,
            u'fTeam': fTeam,
            u'fSpread': fSpread,
            u'ts_open': str(datetime.now().strftime('%m/%d/%Y %H:%M:%S'))
        })
    elif(oCollection[oCollection_sorted[0]] < fSpread):
        collection.document(oCollection_sorted[0]).set({
            u'fSpread': fSpread,
            u'ts_open': str(datetime.now().strftime('%m/%d/%Y %H:%M:%S'))
        }, merge=True)
    elif(oCollection[oCollection_sorted[1]] < fSpread): 
        collection.document(oCollection_sorted[1]).set({
            u'fSpread': fSpread,
            u'ts_open': str(datetime.now().strftime('%m/%d/%Y %H:%M:%S'))
        }, merge=True)

def in_(league, uTeam, fTeam, uScore, fScore, umLine, fmLine):
    
    collection = firestoreRef.collection('open case')
    document_in = firestoreRef.collection('in case').document()
    
    for d in collection.stream():

        if(d.get('league') == league and (d.get('uTeam') == uTeam or d.get('uTeam') == fTeam)):

            if(d.get('fTeam') == fTeam):
                uLead = float(uScore) - float(fScore)
            else:
                uLead = fScore - uScore

            if(uLead > d.get('fSpread')):
                
                if(d.get('fTeam') == fTeam):
                    fmlTarget = (1/((fmLine/100)+1))+0.10
                    twilioManager.text('In', league, fTeam, '-'+str(fmLine))
                else:
                    fTeam = uTeam
                    fmLine = umLine
                    twilioManager.text('In', league, fTeam, '+'+str(fmLine))
                    fmlTarget = (1/((100/fmLine)+1))+0.10

                document_in.set({
                    u'league': d.get('league'),
                    u'uTeam': d.get('uTeam'),
                    u'fTeam': d.get('fTeam'),
                    u'fSpread': d.get('fSpread'),
                    u'ts_open': d.get('ts_open'),
                    u'uLead': uLead,
                    u'fmLine_in': fmLine,
                    u'fmlTarget': fmlTarget,
                    u'ts_in': str(datetime.now().strftime('%m/%d/%Y %H:%M:%S'))
                })

                collection.document(d.id).delete()

                for e in collection.stream():

                    if(e.get('league') == league and e.get('fTeam') == fTeam):
                        collection.document(e.id).delete()

def out(league, uTeam, fTeam, umLine, fmLine):
    
    collection = firestoreRef.collection('in case')
    document_out = firestoreRef.collection('out case').document()

    for d in collection.stream():

        if(d.get('league') == league and (d.get('uTeam') == uTeam or d.get('uTeam') == fTeam)):

            if(d.get('fTeam') == fTeam):
                fmLine_odds = 1/((fmLine/100)+1)
            else:
                fTeam = uTeam
                fmLine = umLine
                fmLine_odds = 1/((100/fmLine)+1)

            if(fmLine_odds > d.get('fmlTarget')):
                
                if(d.get('fTeam') == fTeam):
                    twilioManager.text('Out', league, fTeam, '-'+str(fmLine))
                else:
                    twilioManager.text('Out', league, fTeam, '+'+str(fmLine))

                document_out.set({
                    u'league': d.get('league'),
                    u'uTeam': d.get('uTeam'),
                    u'fTeam': d.get('fTeam'),
                    u'fSpread': d.get('fSpread'),
                    u'ts_open': d.get('ts_open'),
                    u'uLead': d.get('uLead'),
                    u'fmLine_in': d.get('fmLine_in'),
                    u'fmlTarget': d.get('fmlTarget'),
                    u'ts_in': d.get('ts_in'),
                    u'fmLine≤_out': fmLine_odds,
                    u'ts_out': str(datetime.now().strftime('%m/%d/%Y %H:%M:%S'))
                })

                collection.document(d.id).delete()
        
def archive():
    collection_open = firestoreRef.collection('open case')
    collection_in = firestoreRef.collection('in case')
    document_archive = firestoreRef.collection('archive case').document()

    for d in collection_open.stream():
        
        if(datetime.now() - datetime.strptime(d.get('ts_open'), '%m/%d/%Y %H:%M:%S') > 86400):
            collection_open.document(d.id).delete()

    for d in collection_in.stream():
        
        if(datetime.now() - datetime.strptime(d.get('ts_in'), '%m/%d/%Y %H:%M:%S') > 86400):
           
            document_archive.set({
                u'league': d.get('league'),
                u'uTeam': d.get('uTeam'),
                u'fTeam': d.get('fTeam'),
                u'fSpread': d.get('fSpread'),
                u'ts_open': d.get('ts_open'),
                u'uLead': d.get('uLead'),
                u'fmLine_in': d.get('fmLine_in'),
                u'fmlTarget': d.get('fmlTarget'),
                u'ts_in': d.get('ts_in')
            })
            
            collection_in.document(d.id).delete()

def export():
    #export in, archive, out
    
    archive()

    df = pd.DataFrame()
    data = []

    collection_in = firestoreRef.collection('in case')
    collection_archive = firestoreRef.collection('archive case')
    collection_out = firestoreRef.collection('out case')

    for d in collection_in.stream():
        #'collection','league', 'uTeam', 'fTeam', 'fSpread', 'ts_open', 'uLead', 'fmLine_in', 'fmlTarget', 'ts_in', 'fmLine_out', 'ts_out'
        data.append(['in', d.get('league'), d.get('uTeam'), d.get('fTeam'), d.get('fSpread'), d.get('ts_open'), d.get('uLead'), d.get('fmLine_in'), d.get('fmlTarget'), d.get('ts_in'), "NULL", "NULL"])

    for d in collection_archive.stream():
        data.append(['in', d.get('league'), d.get('uTeam'), d.get('fTeam'), d.get('fSpread'), d.get('ts_open'), d.get('uLead'), d.get('fmLine_in'), d.get('fmlTarget'), d.get('ts_in'), "NULL", "NULL"])

    for d in collection_out.stream():
        data.append(['in', d.get('league'), d.get('uTeam'), d.get('fTeam'), d.get('fSpread'), d.get('ts_open'), d.get('uLead'), d.get('fmLine_in'), d.get('fmlTarget'), d.get('ts_in'), d.get('fmLine_out'), d.get('ts_out')])

    df = pd.DataFrame(data, columns=['collection','league', 'uTeam', 'fTeam', 'fSpread', 'ts_open', 'uLead', 'fmLine_in', 'fmlTarget', 'ts_in', 'fmLine_out', 'ts_out'])
    df.to_csv(f'export.csv', index=False)