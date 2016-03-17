# Endpoints
------------
## For login

* Event managers will be signed up through their emails and password will be sent to their mail id
* Other endpoints will be as follows :-

| Endpoint      | Request                                             | Response                               |
|:--------------|:---------------------------------------------------:|:--------------------------------------:|
|/login         |POST<br>Body Keylist [username, password]            | On success<br>{"status": 200, "token"} |
|/participants  |POST Keylist[names, mobileNumber]                    |On success<br>{"status": 200, "id"}     |
|/participants  |GET<br> urlencoded keys [token, {round}]             |On success<br>{"status": 200, "message":[{id, names, mobileNumber}]}|
|/sendsms       |POST<br>Body Keylist[token, teams[id, receipt_id, names, mobileNumber], message]|On success<br>{"status": 200, "message": "Smses sent and teams promoted"}|

