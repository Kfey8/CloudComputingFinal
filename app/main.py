!/usr/bin/env python3
from ebaysdk.finding import Connection
import datetime
import csv
api = Connection(domain='svcs.sandbox.ebay.com', debug=True, config_file='ebay.yaml')

from flask import Flask, render_template

request  = {'keywords' : 'Graphics Card'}
response = api.execute('findItemsByKeywords', request)



app = Flask(__name__)

filename = "/home/samjhennon/app/Clean Data revised.csv"
fields = []
rows = []
def setrequest(gpuname):
    request = {
        'keywords': gpuname,
    }
def getCards():
  best = 10
  worst = 0
  with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    fields = next(csvreader)
    x = 1
    for row in csvreader:
            row.append(x)
            x = x + 1
            coin = setrequest(row[2]) 
            rows[6] = round(coin[6] , 50)
            rows.append(row)
            if float(row[5]) < best:
                sendbest = row
                best = float(row[5])
            if float(row[5]) > worst:
                sendworst = row
                worst = float(row[5])
        
  return(fields , rows , sendbest , sendworst)


response = api.execute('findItemsByKeywords', request)

@app.route('/')
def root():
    # For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.
    titles , cards , bestcard , worstcard = getCards()
    # The outputs are like this [CardMake , CardName , Official Rank , Benchmark , MyRankt]
    return render_template('index.html',titles =  titles , cards = cards , bestcard = bestcard , worstcard = worstcard)



if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)