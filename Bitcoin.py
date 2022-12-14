#Luke Coddington
#Final Project
#MS548 - Coding in blockchain
#Description: This program is designed to mine bitcoin while also prividing an interface to keep track of the status of the mining process.

import json
import time
from hashlib import sha256
from flask import Flask, request, render_template_string
from datetime import datetime

#global vars
nonce = 0
new_hash = "Initial"
found = False
startTime = time.time()


#encryption
def SHA256(text):
    return sha256(text.encode("ascii")).hexdigest()

#function to mine bitcoin
def mine(block_number, transactions, previous_hash, prefix_zeros):
    global nonce
    global new_hash
    global found
    prefix_str = '0'*prefix_zeros
    while(not found):
        text = str(block_number) + transactions + previous_hash + str(nonce)
        new_hash = SHA256(text)
        if new_hash.startswith(prefix_str):
            print(f"Successfully mined bitcoins with nonce value:{nonce}")
            found = True
            return new_hash
        nonce +=1

app = Flask(__name__)


#start mining route
@app.route('/start-mining', methods=['GET'])
def start():
    global new_hash
    print("Begining mining :: {0}".format(datetime.now()))
    difficulty=20
    transactions='''
    Luke Coddington->12-12-22
    '''
    new_hash = mine(1,transactions,'0000000xa036944e29568d0cff17edbe038f81208fecf9a66be9a2b8321c6ec7', difficulty)
    indexPage = """
    <html>
    <head>
    <title>Blockchain Running</title>
    </head>
    <body>
    <h1>Difficulty :: {0}</h1>
    <h1>Transactions :: {1}</h1>
    </body>
    </html> 
    """.format(difficulty, transactions)
    return render_template_string(indexPage)

#Status route
@app.route('/', methods=['GET'])
def mineBitcoinn():
    global nonce
    global new_hash
    global found
    global startTime
    total_time = time.time() - startTime
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    if(new_hash == "Initial"):
        mining = "Mining not Started; got to /start-mining to begin"
    else:
        mining = "Bitcoin Status"
    if(not found):
        indexPage = """
    <html>
    <head>
    <title>Bitcoin Status</title>
    </head>
    <body>
    <h1>{4}</h1>
    <h1>Last Updated :: {0}</h1>
    <h1>Current Hash :: {1}</h1>
    <h1>Elipsed Time :: {2}s</h1>
    <h1>Attempts :: {3}</h1>
    </body>
    </html> 
    """.format(now,new_hash,total_time, nonce, mining)
    else:
        indexPage = """
    <html>
    <head>
    <title>Blockchain Status</title>
    </head>
    <body>
    <h1>Blockchain Found!</h1>
    <h1>Hash Code :: {0}</h1>
    <h1>Total Time :: {1}</h1>
    <h1>Total attempts :: {2}</h1>
    </body>
    </html> 
    """.format(new_hash,total_time, nonce)
    return render_template_string(indexPage)

app.run(port=3000)
