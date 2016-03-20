# Endpoints
------------
## For login

* Event managers will be signed up through their emails and password will be sent to their mail id
* Other endpoints will be as follows :-
* Every endpoint except /login mentioned in this file needs a header "Authorization" with its value set as token

| Endpoint      | Request                                             | Response                               |
|:--------------|:---------------------------------------------------:|:--------------------------------------:|
|/login         |POST<br>Body Keylist [username, password]            | On success<br>{"status": 200, "token"} |
|/participants  |POST Keylist[names, mobileNumber]                    |On success<br>{"status": 200, "id"}     |
|/participants  |GET<br> urlencoded keys [{round}]             |On success<br>{"status": 200, "message":[{_id, names, mobileNumber, receiptId, smsStatus}]}|
|/sendsms       |POST<br>Body Keylist[teams[id, receipt_id, names, mobileNumber], date, time, venue]|On success<br>{"status": 200, "message": "Smses sent and teams promoted"}|
