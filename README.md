# BTC-Python-Webserver
 <h3> Python BTC Webserver</h3>
 
 <p>Main Features:<br>
 - Set any curve point with its respective coefficient as Generator point (default G of secp256k1)<br>
 - All three points with same y-coordinate and private keys thanks to lambda and lambda2 values in modal window by hex key click<br>
 - Check address balance from bloomfilter file database with play sound when found<br>
 - BloomFilter file creation (first download txt database from http://addresses.loyce.club/)<br>
 - Legacy(Compressed, Uncompressed), P2SH, Bech32 P2WPKH, Bech32 P2WSH addresses 
 </p>
 
 <h3>Python dependencies:</h3>
 <p>pip install bitcoinlib<br>
 pip install pygame<br>
 pip install mmh3<br>
 pip install xxhash<br>
 pip install bitarray<br>
 pip install base58</p>
 
<h3>Usage:</h3>
 <p>localhost:3333/1  -   go to page number 1 </p>
 <p>localhost:3333/@1098761 - search page by private key in decimal </p>
 <p>localhost:3333/$FA783FFDE - search page by private key in hex </p>
 <p>localhost:3333/5JWuC9UYTYHrj9Rh8c64YSU1TAt5KDmY231vgghfBCvF8h171Zq  - search by WIF</p>
 <p>localhost:3333/KzJyNCQZr97QV2Bz8ZsLdmQCzWcS3RMZuZu5xAETW3c1P9yJvk9Z - search by WIF</p>
 <p>localhost:3333/[3384] - change step for next</p>
 <p>localhost:3333/(3456-9876) - set range for random</p>
 <p>or just paste
 1 - go to page number 1
 @1098761 - search page by private key in decimal
 $FA783FFDE - search page by private key in hex
 5JWuC9UYTYHrj9Rh8c64YSU1TAt5KDmY231vgghfBCvF8h171Zq - search by WIF
 KzJyNCQZr97QV2Bz8ZsLdmQCzWcS3RMZuZu5xAETW3c1P9yJvk9Z - search by WIF
 [3384] - change step for next
 (3456-9876) - set range for random
 in the Search Field</p>
 <br>
 <h4>You can download fresh txt database with addresses from here: http://addresses.loyce.club/</h4>
 <p>Download. Unpack. Name it address.txt</p>
 <p>Start create_bloom_file.py and wait untill done.</p>
 <p>Then just start webserver.py</p>
 
 ![Screenshot (2)](https://user-images.githubusercontent.com/46902666/178923003-c80f9e30-c161-4e4b-9235-af4c0329fd8b.png)
 ![Screenshot (3)](https://user-images.githubusercontent.com/46902666/178923019-a5428d55-59b0-43cc-b614-4dcc63676ce6.png)
 ![Screenshot (4)](https://user-images.githubusercontent.com/46902666/178923031-d3b14967-11f5-4efb-a612-f4c4b0d49f0d.png)

<br>
<p>Donations Welcome Bitcoin Address: https://www.blockchain.com/btc/address/3Fnc4w98wF5mRMpNyK4DooHw5gELLXj5Hd</p>
