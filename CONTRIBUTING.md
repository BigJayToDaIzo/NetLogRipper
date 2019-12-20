#Welcome

##Notes
I'm going to parse 2 types of ping logs at first
1) ping -vD www.google.com which returns the following
* SUCESS EXAMPLE: 
   * Tue 17 Dec 2019 07:04:00 PM CST: 64 bytes from ord38s19-in-f4.1e100.net (172.217.5.4): icmp_seq=33107 ttl=51 time=17.4 ms
* FAILURE EXAMPLE:
   * Tue 17 Dec 2019 09:51:55 AM CST: From ubuntu-box (192.168.1.105) icmp_seq=94 Destination Host Unreachable
2) ping -nD www.google.com which returns the following
* SUCCESS EXAMPLE: 
    * [1576711230.698411] 64 bytes from 216.239.34.117: icmp_seq=1455 ttl=51 time=1176 ms
* FAILURE EXAMPLE:
    * [1576711215.538075] From 192.168.1.105 icmp_seq=1439 Destination Host Unreachable

The `datetime` library `fromtimestamp()` function wants an integer so I have to parse out the nanosecond data (after the .)

### Functionality Wishlist
1) Detect time gaps in logfiles so it doesn't skew uptime percentages with large gaps in the middle of data sets.