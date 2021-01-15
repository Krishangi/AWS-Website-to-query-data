from flask import Flask, render_template, request
import mysql.connector as connector
from mysql.connector import Error
import time
import psycopg2


app = Flask(__name__)

@app.route('/')

def about():
        
    #variable declaration
    result = []
    execute=0
    print(request.args)
    startTime = 0
        
    if 'query' in request.args:
        try:
            if request.args['activeDB'] == "MySQL":

                # connect to db (HAVE TO CONNECT TO RDS)
                connection = connector.connect(user='****', password='dbds****', host='localhost', database='flaskapp')

                # declare cursor object
                cursor = connection.cursor()
                query1 = request.args['query'] + " LIMIT 0, 100;"

                #start timer
                startTime = time.time()

                # execute query through cursor
                cursor.execute(query1)

                # read query result
                records = cursor.fetchall()

                for x in records:
                    result.append(x)

                #store column names
                columns = mycursor.column_names

                #actual execution time
                execTime = time.time() - startTime

                #close connection
                connection.close()
                cursor.close()

            elif request.args['activeDB'] == "RedShift":
                
                #connect to redshift (HAVE TO CONNECT TO REDSHIFT)
                redshiftdb = psycopg2.connect(dbname='admin1', host='admin1.cbl6aq5ts0z4.us-east-2.redshift.amazonaws.com:',
                                              port='5439', user='admin', password='Dbds****')
                redshiftdb.autocommit = True

                # declare cursor object
                cur = redshiftdb.cursor()
                query1 = request.args['query'] + " LIMIT 100;"
                
                #start timer
                startTime = time.time()

                #execute query
                cur.execute(query)

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
        except Error as e:
            print("Error occured", e)

        return render_template('queryExplorer.html', resultPresent=True, columns=columns, data=result, mysqlActive=mysqlActive, 
            redShiftActive=redShiftActive, msg=request.args['query'] + " (Execution Time : " + str(execTime)[:7] + "s)",exectime=execTime status="success")


if __name__ == '__main__':
    app.run(debug=True)
