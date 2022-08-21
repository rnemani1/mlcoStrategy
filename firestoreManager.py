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
import os

credential_path = "/Users/rnemani/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Keep/Documents/Projects/Vegas/mlcoStrategy/Nemani_Pro_Vegas-mlcoStrategy-key.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

def open(league, uTeam, fTeam, uSpread, uLead):
    firestoreRef = firestore.Client(project='vegas-mlcostrategy')
    document = firestoreRef.collection(u'open case').document()

    document.set({
        u'league': league,
        u'uTeam': uTeam,
        u'fTeam': fTeam,
        u'uSpread': uSpread,
        u'uLead': uLead,
        u'open_ts': str(datetime.now().strftime('%m/%d/%Y %H:%M:%S'))

    })

    remDuplicates('open case')

    for document in firestoreRef.collection(u'open case').stream():
        docID = document.id

        for doc2 in firestoreRef.collection(u'open case').stream():
            doc2ID = doc2.id
            
            if(docID != doc2ID):
                if(document.get('fTeam') == doc2.get('fTeam') and
                    document.get('league') == doc2.get('league') and
                    float(document.get('uSpread')[1:]) > float(doc2.get('uSpread')[1:]) and
                    document.get('uTeam') == doc2.get('uTeam')):
                        firestoreRef.collection(u'open case').document(doc2.id).delete()

def fmlTarget(fmLine):
    
    target = 0.2

    fmLine_float = float(fmLine[1:])
    fmlTarget = (1/((fmLine_float/100)+1))+target

    return fmlTarget

def in_(uTeam, uLead, fLead, umLine, fmLine):
    
    firestoreRef = firestore.Client(project='vegas-mlcostrategy')
    collection = firestoreRef.collection('open case')

    for document in collection.stream():
    
        document_id = document.id
        uSpread = float(document.get('uSpread')[1:])

        if uTeam == document.get('uTeam'):
            i_uLead = uLead
            i_fmLine = fmLine
        elif uTeam == document.get('fTeam'):
            i_uLead = fLead
            i_fmLine = umLine
        else:
            continue

        i_fmlTarget = fmlTarget(i_fmLine)

        if i_uLead > uSpread:
            document_in = firestoreRef.collection(u'in case').document()

            document_in.set({
                u'i_uLead': i_uLead, 
                u'i_fmLine': i_fmLine,
                u'i_fmlTarget': i_fmlTarget,
                u'isQ4': 'FALSE',
                u'league': document.get('league'),
                u'uTeam': document.get('uTeam'),
                u'fTeam': document.get('fTeam'),
                u'uSpread': document.get('uSpread'),
                u'uLead': document.get('uLead'),
                u'open_ts': document.get('open_ts'),
                u'in_ts': str(datetime.now().strftime('%m/%d/%Y %H:%M:%S'))
                
            })

            twilioManager.in_(document.get('fTeam'), i_fmLine)
            collection.document(document_id).delete()

def out(uTeam, umLine, fmLine):
    #set fmLine_iOdds
    firestoreRef = firestore.Client(project='vegas-mlcostrategy')
    collection = firestoreRef.collection('in case')

    for document in collection.stream():
    
        document_id = document.id

        if uTeam == document.get('uTeam'):
            fmLine_sign = fmLine[0]
            fmLine_float = float(fmLine[1:])
        elif uTeam == document.get('fTeam'):
            fmLine_sign = umLine[0]
            fmLine_float = float(umLine[1:])
        else:
            continue

        if fmLine_sign == "+": 
            fmLine_iOdds = 1/((fmLine_float/100)+1)
        else:
            fmLine_iOdds = 1/((100/fmLine_float)+1)

        if fmLine_iOdds > document.get('i_fmlTarget'):
            #in -> out
            document_out = firestoreRef.collection(u'out case').document()

            document_out.set({
                u'o_caseHit': "TRUE",
                u'o_fmLine': fmLine_iOdds,
                u'i_uLead': document.get('i_uLead'), 
                u'i_fmLine': document.get('i_fmLine'),
                u'i_fmlTarget': document.get('i_fmlTarget'),
                u'league': document.get('league'),
                u'uTeam': document.get('uTeam'),
                u'fTeam': document.get('fTeam'),
                u'uSpread': document.get('uSpread'),
                u'uLead': document.get('uLead'),
                u'open_ts': document.get('open_ts'),
                u'in_ts': document.get('in_ts'),
                u'isQ4': document.get('isQ4'),
                u'out_ts': str(datetime.now().strftime('%m/%d/%Y %H:%M:%S'))
                
            })
            
            twilioManager.out(document.get('fTeam'), document.get('i_fmLine'), str(fmLine_sign) + str(fmLine_float))
            collection.document(document_id).delete()

def export():
    df = pd.DataFrame()
    data = []

    firestoreRef = firestore.Client(project='vegas-mlcostrategy')
    collection_open = firestoreRef.collection('open case')
    collection_archive = firestoreRef.collection('archive')

    for document in collection_open.stream():
        #['collection','league', 'uTeam', 'fTeam', 'uSpread', 'uLead', 'i_uLead', 'i_fmLine', 'i_fmlTarget', 'o_caseHit', 'o_fmLine']
        data.append(['open', document.get('league'), document.get('uTeam'), document.get('fTeam'), document.get('uSpread'), document.get('uLead'), "NULL", "NULL", "NULL", "NULL", "NULL", document.get('open_ts'), "NULL", "NULL", "NULL"])
   
    collection_in = firestoreRef.collection('in case')

    for document in collection_in.stream():
        #['collection','league', 'uTeam', 'fTeam', 'uSpread', 'uLead', 'i_uLead', 'i_fmLine', 'i_fmlTarget', 'o_caseHit', 'o_fmLine']
        data.append(['in', document.get('league'), document.get('uTeam'), document.get('fTeam'), document.get('uSpread'), document.get('uLead'), document.get('i_uLead'), document.get('i_fmLine'), document.get('i_fmlTarget'), "NULL", "NULL", document.get('open_ts'), document.get('in_ts'), "NULL", document.get('isQ4')])

    collection_out = firestoreRef.collection('out case')

    for document in collection_out.stream():
        #['collection','league', 'uTeam', 'fTeam', 'uSpread', 'uLead', 'i_uLead', 'i_fmLine', 'i_fmlTarget', 'o_caseHit', 'o_fmLine']
        data.append(['out', document.get('league'), document.get('uTeam'), document.get('fTeam'), document.get('uSpread'), document.get('uLead'), document.get('i_uLead'), document.get('i_fmLine'), document.get('i_fmlTarget'), document.get('o_caseHit'), document.get('o_fmLine'), document.get('open_ts'), document.get('in_ts'), document.get('out_ts'), document.get('isQ4')])

    df = pd.DataFrame(data, columns=['collection','league', 'uTeam', 'fTeam', 'uSpread', 'uLead', 'i_uLead', 'i_fmLine', 'i_fmlTarget', 'o_caseHit', 'o_fmLine', 'open_ts', 'in_ts', 'out_ts', 'isQ4'])
    df.to_csv(f'export.csv', index=False)

    #col_list = df["Courses"].values.tolist()
    #dict(map(lambda el  : (el, list(nums).count(el)), nums))

    league_list = df['league'].values.tolist()
    print(dict(map(lambda x  : (x, list(league_list).count(x)), league_list)))

def remDuplicates(collection):

    firestoreRef = firestore.Client(project='vegas-mlcostrategy')
    collection = firestoreRef.collection(collection)

    docList = []

    for document in collection.stream():
        docID = document.id

        for doc2 in collection.stream():
            doc2ID = doc2.id

            if(docID != doc2ID):
                if(document.get('fTeam') == doc2.get('fTeam') and
                    document.get('league') == doc2.get('league') and
                    document.get('uSpread') == doc2.get('uSpread') and
                    document.get('uTeam') == doc2.get('uTeam')):
                        docList.append(doc2ID)

    docList = [*set(docList)]

    for d in docList[1:]:
        collection.document(d).delete()

#CALL: 
#export()

