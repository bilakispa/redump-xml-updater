# Redump XML Updater
## Introduction
Check for the newest .dat files on Redump.org and insert them into a xml file to use with the clrmamepro's _WWW Mode_ standard. The script also can run a simple local webserver using Python's http.server module, to update the xml into clrmamepro.

## How to use
1. Install Python 3 (and the requests module)
2. Edit the UserInfo.xml file with log-in data (if you have)
3. Run the script, if you chose the first option it will update the xml and start a local server too.
4. Insert the remote xml file url into clrmamepro's _WWW Mode_
> Default URL: 127.0.0.1/profile.xml

## Limitations
* The port should left at 80 because, clrmamepro only works with that port.
* The script doesn't insert any links to download the dats inside the clrmamepro
