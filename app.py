from flask import Flask, render_template, request
import mysql.connector as connector
from mysql.connector import Error
import time
import psycopg2
import urlparse


app = Flask(__name__,template_folder='Template')
print("Step -1")
@app.route('/')
@app.route('/querydb')

def about():
    print("Step 0")
    #variable declaration
    result = []
    columns = []
    execute=0
    startTime = 0
    execTime=0
    print ("Step1")

    queryFromWeb = request.args.get('query')

    if 'query' in request.args:
        if request.args.get('activeDB') == "MySQL":
            connection = connector.connect(user='admin', password='********', host='finalrds.c5k076gxzohl.us-east-2.rds.amazonaws.com',port='3306', database='finalrds')

            # declare cursor object
            cursor = connection.cursor()
            # queryFromWeb = request.args.get('query')

            print("**********Query Below*****************")
            print(queryFromWeb)
            #start timer
            startTime = time.time()

            # execute query through cursor
            # cursor.execute(query1,multi=True)
            cursor.execute(queryFromWeb)

            # read query result
            records = cursor.fetchall()

            for x in records:
                result.append(x)

            #store column names
            columns = cursor.column_names

            #actual execution time
            execTime = time.time() - startTime

            #close connection
            connection.close()
            cursor.close()

        elif request.args.get('activeDB') == "RedShift":
            print ("Step 3")
            #connect to redshift (HAVE TO CONNECT TO REDSHIFT)
            redshiftdb = psycopg2.connect(dbname='admin1', host='admin1.cbl6aq5ts0z4.us-east-2.redshift.amazonaws.com',
                                              port='5439', user='admin', password='*******')

            # declare cursor object
            cur = redshiftdb.cursor()
            # query1 = request.args['query'] + " LIMIT 100;"

            #start timer
            startTime = time.time()

            #execute query
            cur.execute(queryFromWeb)

            #fetch all records
            myresult = cur.fetchall()

            #store all column names in list
            columns = list(zip(*cur.description))[0]

            for x in myresult:
                result.append(x)

            #close connection
            cur.close()

            #actual execution time
            execTime = time.time() - startTime

    # print ("Step 4")       
    return render_template('home.html', resultPresent=True, data=result,columns=columns, exectime=execTime,  status="success")


if __name__ == '__main__':
    app.run(debug=True)
#    app.run(debug=True,host="0.0.0.0", port=5000)


