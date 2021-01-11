//Node.js 12.x
//For LAMBDA FUNCTION DEFINATION- ALEXA CONNECT

'use strict';
const { Parser } = require('node-sql-parser');
var mysql = require('mysql');

exports.handler =  function(event,context) {

    try {
        var request = event.request;

        if (request.type === "LaunchRequest") {

            let options = {};
            options.speechText = "Welcome to Query Dashboard. Tell me the query";

            options.repromptText = "Hello...Tell me the query";
            options.endSession = false;
            context.succeed(buildResponse(options));

        } else if (request.type === "IntentRequest") {

            let options = {};
            if (request.intent.name === "HelloIntent") {
                let name = request.intent.slots.query.value.toLowerCase().replace("all ","*");
                name = name.replace("is equal to","=");
                name = name.replace("is greater than",">=");
                name = name.replace("is less than","<=");
                name = name.replace("five"," 5 ");
                name = name.replace("department's","departments");
                name = name.replace("product's","products");
                name = name.replace("order's","orders");
                name = name.replace("order products","order_products");


                //LET'S VALIDATE & PARSE THE SQL
                const parser = new Parser();
                let ast ={}
                try {
                    ast = parser.astify(name);
                } catch (e) {
                    options.speechText="Sequel does not look right bad syntax. Please try again";
                    options.endSession = false;
                    context.succeed(buildResponse(options));
                }

                let newFormattedName="'"+name+"'";
                let sql = "update alexa set sql_query="+newFormattedName+",time_asked=CURRENT_TIMESTAMP";

                var connection = mysql.createConnection({

                    host: "finalrds.c5k076gxzohl.us-east-2.rds.amazonaws.com",
                    user: "admin",
                    password: "Dbds2k19",
                    database : "finalrds",
                    port: 3306
                });

                //LETS SEE THE SQL EXECUTES RIGHT
                connection.query(name, function (error, results, fields) {

                    if (error) {
                        connection.end();
                        options.speechText = "Sequel does not look right bad syntax. Please try again";
                        options.endSession = false;
                        context.succeed(buildResponse(options));
                    }

                    if (results) {
                        connection.query(sql, function (error, results, fields) {
                            connection.end();
                            options.speechText="Ok Done. See the output now.";
                            options.endSession = true;
                            context.succeed(buildResponse(options));
                        });
                    }
                });

            } else {
                throw "Unknown Intent";
            }
        } else if (request.type === "SessionEndedRequest") {
        } else {
            throw "Unknown Intent";
        }
    } catch(e) {
        context.fail("Exception: "+e);
    }
};

function buildResponse(options){

    var response = {
        version: "1.0",
        response: {
            outputSpeech: {
                type: "PlainText",
                text: options.speechText
            },
            shouldEndSession: options.endSession
        }
    };

    if(options.repromptText){
        response.response.reprompt = {
            outputSpeech: {
                type: "PlainText",
                text: options.repromptText
            }
        }
    }
    return response;
}
