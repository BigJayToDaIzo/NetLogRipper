#Welcome
Cable companies are trash.  All of them.  I've fought with them for quality internet for 20 years now and all they want to do to 'help' you is walk you through power cycling your modem and router.

With this tool I hope you will be able to set a ping log to run for a few hours, days, weeks or months and quickly parse out uptime, downtime, packet loss, etc. 

Armed with this data, when you call them you can ask for a helpdesk person who is smart enough to understand how to read ping logs, and show them these logs, and pass them the script to parse them too if they're still obstinate about fixing their garbage service.

##Notes
Script will fire and log the following:
1) ping -vD <your isp url here> > <yourPingLogTextFileName.txt here> which returns the following output:

* SUCCESS EXAMPLE: 
    * [1576711230.698411] 64 bytes from 216.239.34.117: icmp_seq=1455 ttl=51 time=1176 ms
* FAILURE EXAMPLE:
    * [1577117279.397268] From ubuntu-box (192.168.1.105) icmp_seq=4060 Destination Host Unreachable


The `datetime` library `fromtimestamp()` function wants an integer so I have to parse out the nanosecond data (after the .)

### Functionality Wishlist
1) Detect time gaps in logfiles so it doesn't skew uptime percentages with large gaps in the middle of data sets.