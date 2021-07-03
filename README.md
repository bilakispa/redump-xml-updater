# Redump XML Updater
## Introduction
Checks for the newest .dat files on redump.org and inserts them into a xml file to use with the clrmamepro's _WWW Profiler_ standard. The script also can run a simple local webserver using Python's http.server module, to update the xml into clrmamepro. Datfile URLs are also provided inside the XML.

## Requirements
1. Python 3
2. requests module (pip3 install requests)

## How to use
1. Edit the UserInfo.xml file with log-in data (if you have)
2. Run the script, if you chose the first option it will update the xml and start a local server too.
3. Add the site into clrmamepro's _WWW Profiler_
* Example configuration:
> URL of Dat: 127.0.0.1:8668/profile.xml
> 
> Site Alias: Redump Local XML

## Limitations
* Trying to download the BIOS datfiles will not work (for now)
