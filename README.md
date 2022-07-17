# BTC-Python-Webserver
 <h3> Python BTC Webserver</h3>
 
 <p>Main Features:<br>
 - Set any curve point with its respective coefficient as Generator point (default G of secp256k1)<br>
 - All three points with same y-coordinate and private keys thanks to lambda and lambda2 values in modal window by hex key click<br>
 - Check address balance from bloomfilter file database with play sound when found<br>
 - BloomFilter file creation (first download txt database from http://addresses.loyce.club/)<br>
 - Legacy(Compressed, Uncompressed), P2SH, Bech32 P2WPKH, Bech32 P2WSH addresses 
 </p>
 <h5>You can set it to lower values if you want more speed in auto and pilot mode</h5>
 <pre>let auto_speed = 500, pilot_speed = 300;  source(line=958)</pre>
 <h5>If columns overlap increase values as you feel necessary(they come in pairs(head and data - width values should be equal))</h5>
 <pre>
 #head_hex{display:inline-block;width:450px;text-align:center;}  source(line=852..867)
 #head_wifu{display:inline-block;width:360px;text-align:center;}
 #head_legu{display:inline-block;width:242px;text-align:center;}
 #head_legc{display:inline-block;width:242px;text-align:center;}
 #head_p2sh{display:inline-block;width:244px;text-align:center;}
 #head_p2wpkh{display:inline-block;width:298px;text-align:center;}
 #head_p2wsh{display:inline-block;width:436px;text-align:center;}
 #head_wifc{display:inline-block;width:368px;text-align:center;}
 .data_hex{display:inline-block;width:450px;color:#DE3163;}
 .data_wifu{display:inline-block;width:360px;color:#145A32;}
 .data_legu{display:inline-block;width:242px;color:#145A32;}
 .data_legc{display:inline-block;width:242px;color:#D35400;}
 .data_p2sh{display:inline-block;width:244px;color:#D35400;}
 .data_p2wpkh{display:inline-block;width:298px;color:#D35400;}
 .data_p2wsh{display:inline-block;width:436px;color:#D35400;}
 .data_wifc{display:inline-block;width:368px;color:#145A32;} 
 </pre>
 <h3>Python dependencies:</h3>
 <p>pip install bitcoinlib<br>
 pip install pygame<br>
 pip install mmh3<br>
 pip install xxhash<br>
 pip install bitarray<br>
 pip install base58</p>
 
 <h3>Usage:</h3>
 <pre>
 localhost:3333/1  -   go to page number 1
 localhost:3333/@1098761 - search page by private key in decimal
 localhost:3333/$FA783FFDE - search page by private key in hex
 localhost:3333/5JWuC9UYTYHrj9Rh8c64YSU1TAt5KDmY231vgghfBCvF8h171Zq  - search by WIF
 localhost:3333/KzJyNCQZr97QV2Bz8ZsLdmQCzWcS3RMZuZu5xAETW3c1P9yJvk9Z - search by WIF
 localhost:3333/[3384] - change step for next
 localhost:3333/(3456-9876) - set range for random</pre>
 <p>or just paste<p>
 <pre>
 1 - go to page number 1
 @1098761 - search page by private key in decimal
 $FA783FFDE - search page by private key in hex
 5JWuC9UYTYHrj9Rh8c64YSU1TAt5KDmY231vgghfBCvF8h171Zq - search by WIF
 KzJyNCQZr97QV2Bz8ZsLdmQCzWcS3RMZuZu5xAETW3c1P9yJvk9Z - search by WIF
 [3384] - change step for next
 (3456-9876) - set range for random</pre>
 <p>in the Search Field.</p>
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
