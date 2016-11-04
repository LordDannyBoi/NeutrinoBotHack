# NeutrinoBotHack
Blind SQL injection in Neutrino panel

## Neutrino now uses POST request, but just as badly as before.
They added a 'ban' feature that blocks you upon ANY invalid request, meaning you can no longer abuse the POST variable 'ip'.
You can still set your ip via this variable however and can XSS and blind SQLi inject via the 'user-agent' header in the same request, this adds you to the banned list, with your ip set as the 'ip' variable.

This module fills in your ip as a random number and completes requests with a binary search rather than brute-forcing. 
This means less requests, less noise and takes less time.
