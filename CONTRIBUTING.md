#Welcome

##Notes
Script will fire and log the following:
1) ping -vD www.google.com which returns the following

* SUCCESS EXAMPLE: 
    * [1576711230.698411] 64 bytes from 216.239.34.117: icmp_seq=1455 ttl=51 time=1176 ms
* FAILURE EXAMPLE:
    * [1577117279.397268] From ubuntu-box (192.168.1.105) icmp_seq=4060 Destination Host Unreachable


The `datetime` library `fromtimestamp()` function wants an integer so I have to parse out the nanosecond data (after the .)

### Functionality Wishlist
1) Detect time gaps in logfiles so it doesn't skew uptime percentages with large gaps in the middle of data sets.