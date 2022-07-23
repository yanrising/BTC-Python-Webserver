from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
import secp256k1 as ice
import bitcoinlib
import base58
import binascii
import random
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer
from bloomfilter import *

hostName,serverPort,version,found_sound = "localhost",3333,"v5.1.7",'success.mp3'
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337
N1,N2 = 37718080363155996902926221483475020450927657555482586988616620542887997980018,78074008874160198520644763525212887401909906723592317393988542598630163514318
G = bytes(bytearray.fromhex('0479be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8'))
Point_Coefficient = 1
#G = bytes(bytearray.fromhex('0479be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798b7c52588d95c3b9aa25b0403f1eef75702e84bb7597aabe663b82f6f04ef2777'))
#Point_Coefficient = 115792089237316195423570985008687907852837564279074904382605163141518161494336

#G = bytes(bytearray.fromhex('04c6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7abac09b95c709ee51ae168fea63dc339a3c58419466ceaeef7f632653266d0e1236431a950cfe52a'))
#Point_Coefficient = 2
#G = bytes(bytearray.fromhex('04c6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7abac09b95c709ee5e51e970159c23cc65c3a7be6b99315110809cd9acd992f1edc9bce55af301705'))
#Point_Coefficient = 115792089237316195423570985008687907852837564279074904382605163141518161494335

#G = bytes(bytearray.fromhex('04f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9388f7b0f632de8140fe337e62a37f3566500a99934c2231b6cb9fd7584b8e672'))
#Point_Coefficient = 3
#G = bytes(bytearray.fromhex('04e493dbf1c10d80f3581e4904930b1404cc6c13900ee0758474fa94abe8c4cd1351ed993ea0d455b75642e2098ea51448d967ae33bfbdfe40cfe97bdc47739922'))
#Point_Coefficient = 4

#G = bytes(bytearray.fromhex('0400000000000000000000003b78ce563f89a0ed9414f5aa28ad0d96d6795f9c633f3979bf72ae8202983dc989aec7f2ff2ed91bdd69ce02fc0700ca100e59ddf3'))
#Point_Coefficient = 57896044618658097711785492504343953926418782139537452191302581570759080747168
#G = bytes(bytearray.fromhex('0400000000000000000000003b78ce563f89a0ed9414f5aa28ad0d96d6795f9c63c0c686408d517dfd67c2367651380d00d126e4229631fd03f8ff35eef1a61e3c'))
#Point_Coefficient = 57896044618658097711785492504343953926418782139537452191302581570759080747169

#G = bytes(bytearray.fromhex('04a6b594b38fb3e77c6edf78161fade2041f4e09fd8497db776e546c41567feb3c71444009192228730cd8237a490feba2afe3d27d7cc1136bc97e439d13330d55'))
#Point_Coefficient = 28948022309329048855892746252171976963209391069768726095651290785379540373584
#G = bytes(bytearray.fromhex('04a6b594b38fb3e77c6edf78161fade2041f4e09fd8497db776e546c41567feb3c8ebbbff6e6ddd78cf327dc85b6f0145d501c2d82833eec943681bc61eccceeda'))
#Point_Coefficient = 86844066927987146567678238756515930889628173209306178286953872356138621120753

def modinv(a,n):
    lm = 1
    hm = 0
    low = a%n
    high = n
    while low > 1:
        ratio = high//low
        nm = hm-lm*ratio
        new = high-low*ratio
        high = low
        low = new
        hm = lm
        lm = nm
    return lm % n

def inv(a):
    return N - a
    
def add(a,b):
    return (a + b) % N

def sub(a,b):
    return (a + inv(b)) % N

def mul(a,b):
    return (a * b) % N
    
def div(a,b):
    return (a * modinv(b,N)) % N 
   
class WebServer(BaseHTTPRequestHandler):
    num=startPrivKey=random=random5H=random5J=random5K=randomKw=randomKx=randomKy=randomKz=0
    randomL1=randomL2=randomL3=randomL4=randomL5=previous=next=0
    max,middle = 904625697166532776746648320380374280100293470930272690489102837043110636675,452312848583266388373324160190187140050146735465136345244551418521555318338 
    hj,jk = 85966769946697919304477156997851416897897452779964215616135418886216209408,551340488851368173693535237984541213163631919119002481700768830238824024064
    Kx,Ky = 82331037767755182942062640740142902864571402261690479162349220360023960857,187767270957094537452083612213689809831026867291628836322148977619599168865
    L1,L2 = 398639737335773246472125555160783623763937797351505550641748492138749584881,504075970525112600982146526634330530730393262381443907801548249398324792889
    L3,L4 = 609512203714451955492167498107877437696848727411382264961348006657900000897,714948436903791310002188469581424344663304192441320622121147763917475208905
    L5,Kz = 820384670093130664512209441054971251629759657471258979280947521177050416913,293203504146433891962104583687236716797482332321567193481948734879174376873
    randomMax=rndMax=max
    randomMin=rndMin=first=stride=p1=p2=p3=p4=p5=p6=1    
    p7,p8,p9,p10,p11,p12,p13,p14,p15,p16,p17,p18,p19 = 2,3,5,9,17,33,65,129,257,513,1025,2049,4097
    p20,p21,p22,p23,p24,p25,p26,p27,p28 = 8193,16385,32769,65537,131073,262145,524289,1048577,2097153
    p29,p30,p31,p32,p33,p34,p35 = 4194305,8388609,16777217,33554433,67108865,134217729,268435457
    p36,p37,p38,p39,p40,p41 = 536870913,1073741825,2147483649,4294967297,8589934593,17179869185
    p42,p43,p44,p45,p46,p47 = 34359738369,68719476737,137438953473,274877906945,549755813889,1099511627777
    p48,p49,p50,p51,p52 = 2199023255553,4398046511105,8796093022209,17592186044417,35184372088833
    p53,p54,p55,p56,p57 = 70368744177665,140737488355329,281474976710657,562949953421313,1125899906842625
    p58,p59,p60,p61,p62 = 2251799813685249,4503599627370497,9007199254740993,18014398509481985,36028797018963969
    p63,p64,p65,p66 = 72057594037927937,144115188075855873,288230376151711745,576460752303423489
    p67,p68,p69,p70 = 1152921504606846977,2305843009213693953,4611686018427387905,9223372036854775809
    p71,p72,p73,p74 = 18446744073709551617,36893488147419103233,73786976294838206465,147573952589676412929
    p75,p76,p77,p78 = 295147905179352825857,590295810358705651713,1180591620717411303425,2361183241434822606849
    p79,p80,p81,p82 = 4722366482869645213697,9444732965739290427393,18889465931478580854785,37778931862957161709569
    p83,p84,p85,p86 = 75557863725914323419137,151115727451828646838273,302231454903657293676545,604462909807314587353089
    p87,p88,p89,p90 = 1208925819614629174706177,2417851639229258349412353,4835703278458516698824705,9671406556917033397649409
    p91,p92,p93,p94 = 19342813113834066795298817,38685626227668133590597633,77371252455336267181195265,154742504910672534362390529
    p95,p96,p97 = 309485009821345068724781057,618970019642690137449562113,1237940039285380274899124225
    p98,p99,p100 = 2475880078570760549798248449,4951760157141521099596496897,9903520314283042199192993793
    p101,p102,p103 = 19807040628566084398385987585,39614081257132168796771975169,79228162514264337593543950337
    p104,p105,p106 = 158456325028528675187087900673,316912650057057350374175801345,633825300114114700748351602689
    p107,p108,p109 = 1267650600228229401496703205377,2535301200456458802993406410753,5070602400912917605986812821505
    p110,p111,p112 = 10141204801825835211973625643009,20282409603651670423947251286017,40564819207303340847894502572033
    p113,p114,p115 = 81129638414606681695789005144065,162259276829213363391578010288129,324518553658426726783156020576257
    p116,p117,p118 = 649037107316853453566312041152513,1298074214633706907132624082305025,2596148429267413814265248164610049
    p119,p120,p121 = 5192296858534827628530496329220097,10384593717069655257060992658440193,20769187434139310514121985316880385
    p122,p123,p124 = 41538374868278621028243970633760769,83076749736557242056487941267521537,166153499473114484112975882535043073
    p125,p126,p127 = 332306998946228968225951765070086145,664613997892457936451903530140172289,1329227995784915872903807060280344577
    p128,p129,p130 = 2658455991569831745807614120560689153,5316911983139663491615228241121378305,10633823966279326983230456482242756609
    p131,p132,p133 = 21267647932558653966460912964485513217,42535295865117307932921825928971026433, 85070591730234615865843651857942052865
    p134,p135,p136 = 170141183460469231731687303715884105729,340282366920938463463374607431768211457,680564733841876926926749214863536422913
    p137,p138,p139 = 1361129467683753853853498429727072845825,2722258935367507707706996859454145691649,5444517870735015415413993718908291383297
    p140,p141 = 10889035741470030830827987437816582766593,21778071482940061661655974875633165533185
    p142,p143 = 43556142965880123323311949751266331066369,87112285931760246646623899502532662132737
    p144,p145 = 174224571863520493293247799005065324265473,348449143727040986586495598010130648530945
    p146,p147 = 696898287454081973172991196020261297061889,1393796574908163946345982392040522594123777
    p148,p149 = 2787593149816327892691964784081045188247553,5575186299632655785383929568162090376495105
    p150,p151 = 11150372599265311570767859136324180752990209,22300745198530623141535718272648361505980417
    p152,p153 = 44601490397061246283071436545296723011960833,89202980794122492566142873090593446023921665
    p154,p155 = 178405961588244985132285746181186892047843329,356811923176489970264571492362373784095686657
    p156,p157 = 713623846352979940529142984724747568191373313,1427247692705959881058285969449495136382746625
    p158,p159 = 2854495385411919762116571938898990272765493249,5708990770823839524233143877797980545530986497
    p160,p161 = 11417981541647679048466287755595961091061972993,22835963083295358096932575511191922182123945985
    p162,p163 = 45671926166590716193865151022383844364247891969,91343852333181432387730302044767688728495783937
    p164,p165 = 182687704666362864775460604089535377456991567873,365375409332725729550921208179070754913983135745
    p166,p167 = 730750818665451459101842416358141509827966271489,1461501637330902918203684832716283019655932542977
    p168,p169 = 2923003274661805836407369665432566039311865085953,5846006549323611672814739330865132078623730171905
    p170,p171 = 11692013098647223345629478661730264157247460343809,23384026197294446691258957323460528314494920687617
    p172,p173 = 46768052394588893382517914646921056628989841375233,93536104789177786765035829293842113257979682750465
    p174,p175 = 187072209578355573530071658587684226515959365500929,374144419156711147060143317175368453031918731001857
    p176,p177 = 748288838313422294120286634350736906063837462003713,1496577676626844588240573268701473812127674924007425
    p178,p179 = 2993155353253689176481146537402947624255349848014849,5986310706507378352962293074805895248510699696029697
    p180,p181 = 11972621413014756705924586149611790497021399392059393,23945242826029513411849172299223580994042798784118785
    p182,p183 = 47890485652059026823698344598447161988085597568237569,95780971304118053647396689196894323976171195136475137
    p184,p185 = 191561942608236107294793378393788647952342390272950273,383123885216472214589586756787577295904684780545900545
    p186,p187 = 766247770432944429179173513575154591809369561091801089,1532495540865888858358347027150309183618739122183602177
    p188,p189 = 3064991081731777716716694054300618367237478244367204353,6129982163463555433433388108601236734474956488734408705
    p190,p191 = 12259964326927110866866776217202473468949912977468817409,24519928653854221733733552434404946937899825954937634817
    p192,p193 = 49039857307708443467467104868809893875799651909875269633,98079714615416886934934209737619787751599303819750539265
    p194,p195 = 196159429230833773869868419475239575503198607639501078529,392318858461667547739736838950479151006397215279002157057
    p196,p197 = 784637716923335095479473677900958302012794430558004314113,1569275433846670190958947355801916604025588861116008628225
    p198,p199 = 3138550867693340381917894711603833208051177722232017256449,6277101735386680763835789423207666416102355444464034512897
    p200,p201 = 12554203470773361527671578846415332832204710888928069025793,25108406941546723055343157692830665664409421777856138051585
    p202,p203 = 50216813883093446110686315385661331328818843555712276103169,100433627766186892221372630771322662657637687111424552206337
    p204,p205 = 200867255532373784442745261542645325315275374222849104412673,401734511064747568885490523085290650630550748445698208825345
    p206,p207 = 803469022129495137770981046170581301261101496891396417650689,1606938044258990275541962092341162602522202993782792835301377
    p208,p209 = 3213876088517980551083924184682325205044405987565585670602753,6427752177035961102167848369364650410088811975131171341205505
    p210,p211 = 12855504354071922204335696738729300820177623950262342682411009,25711008708143844408671393477458601640355247900524685364822017
    p212,p213 = 51422017416287688817342786954917203280710495801049370729644033,102844034832575377634685573909834406561420991602098741459288065
    p214,p215 = 205688069665150755269371147819668813122841983204197482918576129,411376139330301510538742295639337626245683966408394965837152257
    p216,p217 = 822752278660603021077484591278675252491367932816789931674304513,1645504557321206042154969182557350504982735865633579863348609025
    p218,p219 = 3291009114642412084309938365114701009965471731267159726697218049,6582018229284824168619876730229402019930943462534319453394436097
    p220,p221 = 13164036458569648337239753460458804039861886925068638906788872193,26328072917139296674479506920917608079723773850137277813577744385
    p222,p223 = 52656145834278593348959013841835216159447547700274555627155488769,105312291668557186697918027683670432318895095400549111254310977537
    p224,p225 = 210624583337114373395836055367340864637790190801098222508621955073,421249166674228746791672110734681729275580381602196445017243910145
    p226,p227 = 842498333348457493583344221469363458551160763204392890034487820289,1684996666696914987166688442938726917102321526408785780068975640577
    p228,p229 = 3369993333393829974333376885877453834204643052817571560137951281153,6739986666787659948666753771754907668409286105635143120275902562305
    p230,p231 = 13479973333575319897333507543509815336818572211270286240551805124609,26959946667150639794667015087019630673637144422540572481103610249217
    p232,p233 = 53919893334301279589334030174039261347274288845081144962207220498433,107839786668602559178668060348078522694548577690162289924414440996865
    p234,p235 = 215679573337205118357336120696157045389097155380324579848828881993729,431359146674410236714672241392314090778194310760649159697657763987457
    p236,p237 = 862718293348820473429344482784628181556388621521298319395315527974913,1725436586697640946858688965569256363112777243042596638790631055949825
    p238,p239 = 3450873173395281893717377931138512726225554486085193277581262111899649,6901746346790563787434755862277025452451108972170386555162524223799297
    p240,p241 = 13803492693581127574869511724554050904902217944340773110325048447598593,27606985387162255149739023449108101809804435888681546220650096895197185
    p242,p243 = 55213970774324510299478046898216203619608871777363092441300193790394369,110427941548649020598956093796432407239217743554726184882600387580788737
    p244,p245 = 220855883097298041197912187592864814478435487109452369765200775161577473,441711766194596082395824375185729628956870974218904739530401550323154945
    p246,p247 = 883423532389192164791648750371459257913741948437809479060803100646309889,1766847064778384329583297500742918515827483896875618958121606201292619777
    p248,p249 = 3533694129556768659166595001485837031654967793751237916243212402585239553,7067388259113537318333190002971674063309935587502475832486424805170479105
    p250,p251 = 14134776518227074636666380005943348126619871175004951664972849610340958209,28269553036454149273332760011886696253239742350009903329945699220681916417
    p252,p253 = 56539106072908298546665520023773392506479484700019806659891398441363832833,113078212145816597093331040047546785012958969400039613319782796882727665665
    p254,p255 = 226156424291633194186662080095093570025917938800079226639565593765455331329,452312848583266388373324160190187140051835877600158453279131187530910662657
    idx1=idx2=idx3=0                                               #searchKeyU when we search for page by pasting privatekey decimal in url localhost:3333/@10985746
    privKey=privKey_C=bitAddr=bitAddr_C=searchKey=searchKey_U = "" #searchKey when we search for page by pasting privatekey hex in url localhost:3333/$fff 
    starting_key_hex=ending_key_hex=privateKey=privateKey_C=publicKey=publicKey_C=addr_count=foundling=""                                          
    balance_on_page = "False"
    addresses = list()
    bloomfile = 'bloomfile_btc.bf'
    bloom = BloomFilter(420000000, 0.007, bloomfile)
    with open('count.txt', 'r') as in_file:
        for line in in_file:
            addr_count = line
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    print(f"[{time}] Addresses loaded: " + str(addr_count))

    def isHex(s):
        for ch in s:
            if ((ch < '0' or ch > '9') and (ch < 'A' or ch > 'F') and (ch < 'a' or ch > 'f')):                 
                return False
        return True
     
    def RandomInteger(minN, maxN):
        return random.randrange(minN, maxN)
        
    #def log_message(self, format, *args):
        #pass

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
#--------------AJAX Modal Fetch Page PART---------------------------------------
        str_url = self.path[1:] #removing / from url as we do not need it
        if str_url.startswith("!"): # handle ajax request to get all data for modal popup window
            idxN = str_url.index("!") #find ! after goes the number we need
            G1 = bytes(bytearray.fromhex('0479be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8'))
            numb = int(str_url[idxN+1:],10) #get the number from url
            addrC_one = ice.privatekey_to_address(0, True, (numb))
            addrU_one = ice.privatekey_to_address(0, False, (numb))
            addrP2sh_one = ice.privatekey_to_address(1, True, (numb))
            addrbech32_one = ice.privatekey_to_address(2, True, (numb)) 
            a1 = list()
            b_word1 = "No"
            a1.append(addrC_one)
            a1.append(addrU_one)
            for addr in a1:
                if __class__.bloom.lookup_mm(addr):
                    b_word1 = "Yes"
            a12 = list()
            b_word12 = "No"
            a12.append(addrP2sh_one)
            a12.append(addrbech32_one)
            for addr in a12:
                if __class__.bloom.lookup_mm(addr):
                    b_word12 = "Yes"
            P = ice.point_multiplication(numb, G1).hex() #getting point coordinates
            P_X = P[2:66]
            P_Y = P[66:]
            add_inv = N - numb
            addrC = ice.privatekey_to_address(0, True, (add_inv))
            addrU = ice.privatekey_to_address(0, False, (add_inv))
            addrP2sh_inv = ice.privatekey_to_address(1, True, (add_inv))
            addrbech32_inv = ice.privatekey_to_address(2, True, (add_inv))
            a2 = list()
            b_word = "No"
            a2.append(addrC)
            a2.append(addrU)
            for addr in a2:
                if __class__.bloom.lookup_mm(addr):
                    b_word = "Yes"
            a2pb = list()
            b_word_pb_inv = "No"
            a2pb.append(addrP2sh_inv)
            a2pb.append(addrbech32_inv)
            for addr in a2pb:
                if __class__.bloom.lookup_mm(addr):
                    b_word_pb_inv = "Yes"
            AP = ice.point_multiplication(add_inv, G).hex()            
            AP_X = AP[2:66]
            AP_Y = AP[66:]
            n1 = mul(N1,numb)
            n2 = mul(N2,numb)
            if n1 < n2:
                same1n = n1
                same2n = n2
            else:
                same1n = n2
                same2n = n1
            samey1P = ice.scalar_multiplication(same1n)
            samey2P = ice.scalar_multiplication(same2n)
            sameaddr1U = ice.pubkey_to_address(0, False, bytes.fromhex(samey1P.hex()))
            sameaddr1C = ice.pubkey_to_address(0, True, bytes.fromhex(samey1P.hex()))
            addrP2sh_same1 = ice.privatekey_to_address(1, True, (same1n)) #p2sh
            addrbech32_same1 = ice.privatekey_to_address(2, True, (same1n)) #bech32
            same_1 = list()
            b_word_same1 = "No"
            same_1.append(sameaddr1U)
            same_1.append(sameaddr1C)
            for addr in same_1:
                if __class__.bloom.lookup_mm(addr):
                    b_word_same1 = "Yes"
            same_1pb = list()
            b_word_same1pb = "No"
            same_1pb.append(addrP2sh_same1)
            same_1pb.append(addrbech32_same1)
            for addr in same_1pb:
                if __class__.bloom.lookup_mm(addr):
                    b_word_same1pb = "Yes"
            sameaddr2U = ice.pubkey_to_address(0, False, bytes.fromhex(samey2P.hex()))
            sameaddr2C = ice.pubkey_to_address(0, True, bytes.fromhex(samey2P.hex()))
            addrP2sh_same2 = ice.privatekey_to_address(1, True, (same2n)) #p2sh
            addrbech32_same2 = ice.privatekey_to_address(2, True, (same2n)) #bech32
            same_2 = list()
            b_word_same2 = "No"
            same_2.append(sameaddr2U)
            same_2.append(sameaddr2C)
            for addr in same_2:
                if __class__.bloom.lookup_mm(addr):
                    b_word_same2 = "Yes"
            same_2pb = list()
            b_word_same2pb = "No"
            same_2pb.append(addrP2sh_same2)
            same_2pb.append(addrbech32_same2)
            for addr in same_2pb:
                if __class__.bloom.lookup_mm(addr):
                    b_word_same2pb = "Yes"
            #----getting compressed public key format
            if (ord(bytearray.fromhex(P[-2:])) % 2 == 0):
                pubkey_compressed = '02'
            else:
                pubkey_compressed = '03'
            pubkey_compressed += P[2:66]
            #-----getting ripemd160 hash----------------------
            rmdU = ice.privatekey_to_h160(0, False, numb).hex()  #Uncompressed RIPEMD160
            rmdC = ice.privatekey_to_h160(0, True, numb).hex()  #Compressed RIPEMD160
            #---sending ajax response (" " to split data elements)
            self.wfile.write(bytes(P_X+" "+P_Y+" " \
            +str(int(P_X,16))+" "+str(int(P_Y,16))+" " \
            +rmdU+" "+rmdC+" "+str(bin(numb)[2:])+" " \
            +pubkey_compressed+ " "+AP_X+" "+AP_Y+ " "+addrU+" "+addrC+" " \
            +str(hex(add_inv)[2:].zfill(64))+" "+b_word+" " \
            +samey1P.hex()[2:66]+" "+sameaddr1U+" "+sameaddr1C+" "+b_word_same1+" " \
            +samey2P.hex()[2:66]+" "+sameaddr2U+" "+sameaddr2C+" "+b_word_same2+" "+str(numb)+" "+str(hex(numb)[2:].zfill(64))+" " \
            +str(hex(same1n)[2:].zfill(64))+" "+str(hex(same2n)[2:].zfill(64))+" " \
            +b_word_pb_inv+" "+addrP2sh_inv+" "+addrbech32_inv+" "+b_word_same1pb+" "+addrP2sh_same1+" "+addrbech32_same1+" " \
            +b_word_same2pb+" "+addrP2sh_same2+ " "+addrbech32_same2+" "+b_word1+" "+addrU_one+" "+addrC_one+" " \
            +b_word12+" "+addrP2sh_one+" " +addrbech32_one,"utf-8"))
#---------Pilot Mode---------------------------------------------------------------------------------------------
        elif str_url.startswith("P"):
            addresses = list()
            page_num = int(self.path[2:],10)               
            startPrivKey = (page_num - 1) * 128+1
            for i in range(128):
                pub = ice.point_multiplication(startPrivKey,G).hex()
                dec = int((startPrivKey*Point_Coefficient)%N)
                privKey_C = ice.btc_pvk_to_wif(hex(dec)[2:].zfill(64))
                privKey = ice.btc_pvk_to_wif(hex(dec)[2:].zfill(64), False)
                bitAddr = ice.pubkey_to_address(0, False, bytes(bytearray.fromhex(pub)))
                bitAddr_C = ice.pubkey_to_address(0, True, bytes(bytearray.fromhex(pub)))
                addrP2sh = ice.privatekey_to_address(1, True, dec)
                addrbech32 = ice.privatekey_to_address(2, True, dec)
                addrbech32_p2wsh = bitcoinlib.keys.Address(ice.point_to_cpub(ice.point_multiplication(startPrivKey,G)),encoding='bech32',script_type='p2wsh').address                
                addresses.append(bitAddr)
                addresses.append(bitAddr_C)
                addresses.append(addrP2sh)
                addresses.append(addrbech32)
                addresses.append(addrbech32_p2wsh)
                if startPrivKey == 115792089237316195423570985008687907852837564279074904382605163141518161494336:
                     break
                startPrivKey += 1
            status = 'No'
            for addr in addresses:
                if __class__.bloom.lookup_mm(addr):
                    status = 'Yes'
                    with open("found.txt", "a", encoding="utf-8") as f:
                        f.write(f"Bitcoin Address: {addr} Page# {page_num} \n")
            if status == "Yes":
                mixer.init()
                mixer.music.load(found_sound)
                mixer.music.play()
            self.wfile.write(bytes(status, "utf-8"))
            addresses.clear()
#---------Search Field---------------------------------------------------------------------------------------------            
        elif str_url.startswith("S"):
            str_url = self.path[2:] #gettin / outta way from url we do not need
            if str_url.startswith('5H') or str_url.startswith('5J') or str_url.startswith('5K'): # if url starts with 5H 5J 5K we request page by 5WIF
                first_encode = base58.b58decode(self.path[2:])
                private_key_full = binascii.hexlify(first_encode)
                private_key = private_key_full[2:-8]
                private_key_hex = private_key.decode("utf-8")
                keyU = int(private_key_hex,16)
                __class__.searchKey = ice.privatekey_to_address(0, False, keyU)
                __class__.num = int(private_key_hex,16)
                __class__.num = __class__.num // 128
                __class__.num = __class__.num + 1
                __class__.previous = __class__.num - 1
                if (__class__.previous == 0):
                    __class__.previous = 1
                __class__.next = __class__.num + __class__.stride;                
                if (__class__.next > __class__.max):
                    __class__.next = __class__.max
                __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
            elif str_url.startswith('K') or str_url.startswith('L'): # if url starts with L K we request page by LWIF KWIF
                first_encode = base58.b58decode(self.path[2:])
                private_key_full = binascii.hexlify(first_encode)
                private_key = private_key_full[2:-8]
                private_key_hex = private_key.decode("utf-8")
                keyC = int(private_key_hex[0:64],16)
                __class__.searchKey = ice.privatekey_to_address(0, True, keyC)
                __class__.num = int(private_key_hex[0:64],16);
                __class__.num = __class__.num // 128
                __class__.num = __class__.num + 1
                __class__.previous = __class__.num - 1
                if (__class__.previous == 0):
                    __class__.previous = 1
                __class__.next = __class__.num + __class__.stride                
                if (__class__.next > __class__.max):
                    __class__.next = __class__.max
                __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
            else:
                if str_url.find("[") >= 0: # if url has [ after page number localhost:3333/123[33]  we want to change increment for next 
                    __class__.idx1 = str_url.index("[")
                    __class__.idx2 = str_url.index("]")
                    __class__.num = 1
                    __class__.stride = int(str_url[__class__.idx1+1:__class__.idx2],10)
                    self.wfile.write(bytes("<script>$('#cur_inc').html(BigInt("+str(__class__.stride)+"));</script>", "utf-8"))
                    __class__.previous = __class__.num - 1
                    if __class__.previous == 0:
                        __class__.previous = 1
                    __class__.next = __class__.num + __class__.stride                
                    if __class__.next > __class__.max:
                        __class__.next = __class__.max
                    __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
                elif str_url.find("(") >= 0: # if url has ( after page number localhost:3333/123(100-333) we want to change random range for pages starting with 100 up to 333              
                    __class__.idx1 = str_url.index("(")
                    __class__.idx2 = str_url.index("-")
                    __class__.idx3 = str_url.index(")")
                    __class__.randomMin = int(str_url[__class__.idx1+1:__class__.idx2],10)
                    __class__.randomMax = int(str_url[__class__.idx2+1:__class__.idx3],10)
                    self.wfile.write(bytes("<script>$('#rand_min').html(BigInt("+str(__class__.randomMin)+"));</script>", "utf-8"))
                    self.wfile.write(bytes("<script>$('#rand_max').html(BigInt("+str(__class__.randomMax)+"));</script>", "utf-8"))
                    __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
                    __class__.num = 1
                    __class__.previous = __class__.num - 1
                    if __class__.previous == 0:
                        __class__.previous = 1
                    __class__.next = __class__.num + __class__.stride                
                    if __class__.next > __class__.max:
                        __class__.next = __class__.max
                elif str_url.find("$") >= 0:  #if url starts with $ localhost:3333/$f78feb18a  we want to search page by hex value of privatekey              
                    __class__.idx1 = str_url.index("$")
                    if __class__.isHex(str_url[__class__.idx1+1:]) and len(str_url[__class__.idx1+1:]) > 0:                    
                        __class__.num = int(str_url[__class__.idx1+1:],16)
                        __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
                        __class__.searchKey_U = ice.privatekey_to_address(0, False, __class__.num)
                        __class__.num = __class__.num // 128
                        __class__.num = __class__.num + 1                
                        __class__.previous = __class__.num - 1
                        if __class__.previous == 0:
                            __class__.previous = 1
                        __class__.next = __class__.num + __class__.stride                
                        if __class__.next > __class__.max:
                            __class__.next = __class__.max
                    else:
                        __class__.num = 1
                        __class__.previous = __class__.num - 1;
                        if __class__.previous == 0:
                            __class__.previous = 1
                        __class__.next = __class__.num + __class__.stride                
                        if __class__.next > __class__.max:
                            __class__.next = __class__.max
                        __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
                elif str_url.find("@") >= 0: #if url starts with @ localhost:3333/@186732 we want to search page by decimal value of privatekey               
                    __class__.idx1 = str_url.index("@")
                    if str_url[__class__.idx1+1:].isnumeric():                    
                        __class__.num = int(str_url[__class__.idx1+1:],10)
                        __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
                        __class__.searchKey_U = ice.privatekey_to_address(0, False, __class__.num)
                        __class__.num = __class__.num // 128
                        __class__.num = __class__.num + 1                
                        __class__.previous = __class__.num - 1
                        if __class__.previous == 0:
                            __class__.previous = 1
                        __class__.next = __class__.num + __class__.stride                
                        if __class__.next > __class__.max:
                            __class__.next = __class__.max
                    else:
                        __class__.num = 1
                        __class__.previous = __class__.num - 1;
                        if __class__.previous == 0:
                            __class__.previous = 1
                        __class__.next = __class__.num + __class__.stride                
                        if __class__.next > __class__.max:
                            __class__.next = __class__.max
                        __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
                else:
                    if str_url == 'favicon.ico': #favicon.ico request gag
                        pass
                    else:
                        if str_url.isnumeric(): #if url contains just page number in decimal localhost:3333/123456 that is correct
                            __class__.num = int(str_url,10)
                            if __class__.num > __class__.max: #if requested page number more than max(last) we set it to max(last)
                                __class__.num = __class__.max
                            __class__.previous = __class__.num - 1;
                            if __class__.previous == 0:
                                 __class__.previous = 1
                            __class__.next = __class__.num + __class__.stride                
                            if __class__.next > __class__.max:
                                 __class__.next = __class__.max
                            __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
                        else: # if page number has not just decimal numbers we set it to first 
                            __class__.num = 1
                            __class__.previous = __class__.num - 1;
                            if __class__.previous == 0:
                                 __class__.previous = 1
                            __class__.next = __class__.num + __class__.stride                
                            if __class__.next > __class__.max:
                                 __class__.next = __class__.max
                            __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
            __class__.startPrivKey = (__class__.num - 1) * 128+1
            __class__.random5H = __class__.RandomInteger(__class__.rndMin,__class__.hj)
            __class__.random5J = __class__.RandomInteger(__class__.hj,__class__.jk)
            __class__.random5K = __class__.RandomInteger(__class__.jk,__class__.rndMax)
            __class__.randomKw = __class__.RandomInteger(__class__.rndMin,__class__.Kx)
            __class__.randomKx = __class__.RandomInteger(__class__.Kx,__class__.Ky)
            __class__.randomKy = __class__.RandomInteger(__class__.Ky,__class__.Kz)
            __class__.randomKz = __class__.RandomInteger(__class__.Kz,__class__.L1)
            __class__.randomL1 = __class__.RandomInteger(__class__.L1,__class__.L2) 
            __class__.randomL2 = __class__.RandomInteger(__class__.L2,__class__.L3)
            __class__.randomL3 = __class__.RandomInteger(__class__.L3,__class__.L4)
            __class__.randomL4 = __class__.RandomInteger(__class__.L4,__class__.L5)
            __class__.randomL5 = __class__.RandomInteger(__class__.L5,__class__.rndMax)                            
            self.wfile.write(bytes("<h3><span id='page_span'>Page #</span><span id='current_page'>" + str(__class__.num) + "</span><span id='out_of'><< out of >></span><span id='last_page'>904625697166532776746648320380374280100293470930272690489102837043110636675</span></h3>", "utf-8"))
            self.wfile.write(bytes("<pre>[&nbsp;<span class='ajax' page='/"+str(__class__.previous)+"'>previous</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.next)+"'>next</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.random)+"'>random</span>&nbsp;]&nbsp;&nbsp;&nbsp;<=>&nbsp;&nbsp;&nbsp;", "utf-8"))
            self.wfile.write(bytes("[&nbsp;<span class='ajax' page='/"+str(__class__.first)+"'>first</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.middle)+"'>middle</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.max)+"'>last</span>&nbsp;]</pre>", "utf-8"))
            self.wfile.write(bytes("<pre>[&nbsp;<span class='ajax' page='/"+str(__class__.random5H)+"'>5H_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.random5J)+"'>5J_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.random5K)+"'>5K_random</span>&nbsp;]&nbsp;&nbsp;&nbsp;<=>&nbsp;&nbsp;&nbsp;", "utf-8"))
            self.wfile.write(bytes("[&nbsp;<span class='ajax' page='/"+str(__class__.randomKw)+"'>Kw_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.randomKx)+"'>Kx_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.randomKy)+"'>Ky_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.randomKz)+"'>Kz_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.randomL1)+"'>L1_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.randomL2)+"'>L2_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.randomL3)+"'>L3_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.randomL4)+"'>L4_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.randomL5)+"'>L5_random</span>&nbsp;]</pre>", "utf-8"))
            __class__.starting_key_hex = hex((__class__.startPrivKey*Point_Coefficient)%N)[2:].zfill(64)
            if __class__.startPrivKey == 115792089237316195423570985008687907852837564279074904382605163141518161494273:
                __class__.ending_key_hex = hex((__class__.startPrivKey*Point_Coefficient+63*Point_Coefficient)%N)[2:].zfill(64)
            else:
                __class__.ending_key_hex = hex((__class__.startPrivKey*Point_Coefficient+127*Point_Coefficient)%N)[2:].zfill(64)
            self.wfile.write(bytes("<p class='key_hex'>*Starting Private Key Hex: " + str(__class__.starting_key_hex) + "</p>", "utf-8"))
            self.wfile.write(bytes("<p class='key_hex'>**Ending Private Key Hex: " + str(__class__.ending_key_hex) + "</p>", "utf-8"))
            self.wfile.write(bytes("<p id='balance' class='balance_on_page'>Balance on this Page: False</p>", "utf-8"))
            self.wfile.write(bytes("<pre><strong id='head_hex'>Private Key Hex</strong><strong id='head_wifu'>WIF Private Key Uncompressed</strong><strong id='head_legu'>Legacy Uncompressed Address</strong><strong id='head_legc'>Legacy Compressed Address</strong><strong id='head_p2sh'>Segwit P2SH Address</strong><strong id='head_p2wpkh'>Bech32 P2WPKH Address</strong><strong id='head_p2wsh'>Bech32 P2WSH Address</strong><strong id='head_wifc'>WIF Private Key Compressed</strong><br>", "utf-8"))
            for i in range(128):
                pub = ice.point_multiplication(__class__.startPrivKey,G).hex()
                dec = int((__class__.startPrivKey*Point_Coefficient)%N)
                __class__.privKey_C = ice.btc_pvk_to_wif(hex(dec)[2:].zfill(64))
                __class__.privKey = ice.btc_pvk_to_wif(hex(dec)[2:].zfill(64), False)
                __class__.bitAddr = ice.pubkey_to_address(0, False, bytes(bytearray.fromhex(pub)))
                __class__.bitAddr_C = ice.pubkey_to_address(0, True, bytes(bytearray.fromhex(pub)))
                addrP2sh = ice.privatekey_to_address(1, True, dec)
                addrbech32 = ice.privatekey_to_address(2, True, dec)
                addrbech32_p2wsh = bitcoinlib.keys.Address(ice.point_to_cpub(ice.point_multiplication(__class__.startPrivKey,G)),encoding='bech32',script_type='p2wsh').address
                __class__.addresses.append(__class__.bitAddr)
                __class__.addresses.append(__class__.bitAddr_C)
                __class__.addresses.append(addrP2sh)
                __class__.addresses.append(addrbech32)
                __class__.addresses.append(addrbech32_p2wsh)
                __class__.starting_key_hex = hex((__class__.startPrivKey*Point_Coefficient)%N)[2:].zfill(64)                    
                if __class__.bitAddr == __class__.searchKey or __class__.bitAddr_C == __class__.searchKey:
                    self.wfile.write(bytes("<span class='data_hex' rel='popup1' style='font-weight:bold;' num='"+str(i+1)+"' value='"+__class__.starting_key_hex+"'>"+__class__.starting_key_hex+"</span><span class='data_wifu' style='color:#DE3163;'>" + __class__.privKey + "</span><span class='data_legu'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr + "'>" + __class__.bitAddr + "</a></span><span class='data_legc'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr_C + "'>" + __class__.bitAddr_C + "</a></span><span class='data_p2sh'><a target='_blank' href='https://bitaps.com/"+addrP2sh+"'>"+addrP2sh+"</a></span><span class='data_p2wpkh'><a target='_blank' href='https://bitaps.com/"+addrbech32+"'>"+addrbech32+"</a></span><span class='data_p2wsh'><a target='_blank' href='https://bitaps.com/"+addrbech32_p2wsh+"'>"+addrbech32_p2wsh+"</a></span><span class='data_wifc' style='color:#DE3163'>" + __class__.privKey_C + "</span></br>", "utf-8"))
                    __class__.searchKey = ""
                elif __class__.bitAddr == __class__.searchKey_U:
                    self.wfile.write(bytes("<span class='data_hex' rel='popup1' style='font-weight:bold;' num='"+str(i+1)+"' value='"+__class__.starting_key_hex+"'>"+__class__.starting_key_hex+"</span><span class='data_wifu' style='color:#DE3163;'>" + __class__.privKey + "</span><span class='data_legu'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr + "'>" + __class__.bitAddr + "</a></span><span class='data_legc'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr_C + "'>" + __class__.bitAddr_C + "</a></span><span class='data_p2sh'><a target='_blank' href='https://bitaps.com/"+addrP2sh+"'>"+addrP2sh+"</a></span><span class='data_p2wpkh'><a target='_blank' href='https://bitaps.com/"+addrbech32+"'>"+addrbech32+"</a></span><span class='data_p2wsh'><a target='_blank' href='https://bitaps.com/"+addrbech32_p2wsh+"'>"+addrbech32_p2wsh+"</a></span><span class='data_wifc' style='color:#DE3163'>" + __class__.privKey_C + "</span></br>", "utf-8"))
                    __class__.searchKey_U = ""
                elif  __class__.num == 452312848583266388373324160190187140050146735465136345244551418521555318338 and i == 31 or __class__.num == 452312848583266388373324160190187140050146735465136345244551418521555318338 and i == 32:
                    self.wfile.write(bytes("<span class='data_hex' rel='popup1' style='font-weight:bold;' num='"+str(i+1)+"' value='"+__class__.starting_key_hex+"'>"+__class__.starting_key_hex+"</span><span class='data_wifu'>" + __class__.privKey + "</span><span class='data_legu'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr + "'>" + __class__.bitAddr + "</a></span><span class='data_legc'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr_C + "'>" + __class__.bitAddr_C + "</a></span><span class='data_p2sh'><a target='_blank' href='https://bitaps.com/"+addrP2sh+"'>"+addrP2sh+"</a></span><span class='data_p2wpkh'><a target='_blank' href='https://bitaps.com/"+addrbech32+"'>"+addrbech32+"</a></span><span class='data_p2wsh'><a target='_blank' href='https://bitaps.com/"+addrbech32_p2wsh+"'>"+addrbech32_p2wsh+"</a></span><span class='data_wifc'>" + __class__.privKey_C + "</span></br>", "utf-8"))
                else:
                    self.wfile.write(bytes("<span class='data_hex' rel='popup1' num='"+str(i+1)+"' value='"+__class__.starting_key_hex+"'>"+__class__.starting_key_hex+"</span><span class='data_wifu'>" + __class__.privKey + "</span><span class='data_legu'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr + "'>" + __class__.bitAddr + "</a></span><span class='data_legc'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr_C + "'>" + __class__.bitAddr_C + "</a></span><span class='data_p2sh'><a target='_blank' href='https://bitaps.com/"+addrP2sh+"'>"+addrP2sh+"</a></span><span class='data_p2wpkh'><a target='_blank' href='https://bitaps.com/"+addrbech32+"'>"+addrbech32+"</a></span><span class='data_p2wsh'><a target='_blank' href='https://bitaps.com/"+addrbech32_p2wsh+"'>"+addrbech32_p2wsh+"</a></span><span class='data_wifc'>" + __class__.privKey_C + "</span></br>", "utf-8"))
                if __class__.startPrivKey == 115792089237316195423570985008687907852837564279074904382605163141518161494336:
                     break
                __class__.startPrivKey += 1
            for addr in __class__.addresses:
                if __class__.bloom.lookup_mm(addr):
                    __class__.balance_on_page = "True"
                    __class__.foundling += addr + " "
                    with open("found.txt", "a", encoding="utf-8") as f:
                        f.write(f"Bitcoin Address: {addr} Page# {__class__.num} \n")
            if __class__.balance_on_page == "True":
                mixer.init()
                mixer.music.load(found_sound)
                mixer.music.play()
            self.wfile.write(bytes("</pre><pre>[&nbsp;<span class='ajax' page='/"+str(__class__.previous)+"'>previous</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.next)+"'>next</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.random)+"'>random</span>&nbsp;]</pre>", "utf-8"))
            self.wfile.write(bytes("<p class='balance_on_page'>Balance on this Page: " + __class__.balance_on_page + " " + __class__.foundling + "</p>", "utf-8"))
            self.wfile.write(bytes("<script>var elem = document.getElementById('balance');elem.innerHTML = 'Balance on this Page: " + __class__.balance_on_page + " " + __class__.foundling + "'</script>", "utf-8"))
            __class__.addresses.clear()         
            __class__.balance_on_page = "False"
            __class__.foundling = ""
#-------#--------Search Field End-----------------------------------------------------------
        elif str_url.startswith("A"): #AJAX Page Refresh     
            __class__.num = int(self.path[2:],10)
            __class__.previous = __class__.num - 1;
            if __class__.previous == 0:
                __class__.previous = 1
            __class__.next = __class__.num + __class__.stride                
            if __class__.next > __class__.max:
                __class__.next = __class__.max
            __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)                
            __class__.startPrivKey = (__class__.num - 1) * 128+1
            __class__.random5H = __class__.RandomInteger(__class__.rndMin,__class__.hj)
            __class__.random5J = __class__.RandomInteger(__class__.hj,__class__.jk)
            __class__.random5K = __class__.RandomInteger(__class__.jk,__class__.rndMax)
            __class__.randomKw = __class__.RandomInteger(__class__.rndMin,__class__.Kx)
            __class__.randomKx = __class__.RandomInteger(__class__.Kx,__class__.Ky)
            __class__.randomKy = __class__.RandomInteger(__class__.Ky,__class__.Kz)
            __class__.randomKz = __class__.RandomInteger(__class__.Kz,__class__.L1)
            __class__.randomL1 = __class__.RandomInteger(__class__.L1,__class__.L2) 
            __class__.randomL2 = __class__.RandomInteger(__class__.L2,__class__.L3)
            __class__.randomL3 = __class__.RandomInteger(__class__.L3,__class__.L4)
            __class__.randomL4 = __class__.RandomInteger(__class__.L4,__class__.L5)
            __class__.randomL5 = __class__.RandomInteger(__class__.L5,__class__.rndMax)
            self.wfile.write(bytes("<h3><span id='page_span'>Page #</span><span id='current_page'>" + str(__class__.num) + "</span><span id='out_of'><< out of >></span><span id='last_page'>904625697166532776746648320380374280100293470930272690489102837043110636675</span></h3>", "utf-8"))
            self.wfile.write(bytes("<pre>[&nbsp;<span class='ajax' page='/"+str(__class__.previous)+"'>previous</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.next)+"'>next</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.random)+"'>random</span>&nbsp;]&nbsp;&nbsp;&nbsp;<=>&nbsp;&nbsp;&nbsp;", "utf-8"))
            self.wfile.write(bytes("[&nbsp;<span class='ajax' page='/"+str(__class__.first)+"'>first</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.middle)+"'>middle</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.max)+"'>last</span>&nbsp;]</pre>", "utf-8"))
            self.wfile.write(bytes("<pre>[&nbsp;<span class='ajax' page='/"+str(__class__.random5H)+"'>5H_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.random5J)+"'>5J_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.random5K)+"'>5K_random</span>&nbsp;]&nbsp;&nbsp;&nbsp;<=>&nbsp;&nbsp;&nbsp;", "utf-8"))
            self.wfile.write(bytes("[&nbsp;<span class='ajax' page='/"+str(__class__.randomKw)+"'>Kw_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.randomKx)+"'>Kx_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.randomKy)+"'>Ky_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.randomKz)+"'>Kz_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.randomL1)+"'>L1_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.randomL2)+"'>L2_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.randomL3)+"'>L3_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.randomL4)+"'>L4_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.randomL5)+"'>L5_random</span>&nbsp;]</pre>", "utf-8"))
            __class__.starting_key_hex = hex((__class__.startPrivKey*Point_Coefficient)%N)[2:].zfill(64)
            if __class__.startPrivKey == 115792089237316195423570985008687907852837564279074904382605163141518161494273:
                __class__.ending_key_hex = hex((__class__.startPrivKey*Point_Coefficient+63*Point_Coefficient)%N)[2:].zfill(64)
            else:
                __class__.ending_key_hex = hex((__class__.startPrivKey*Point_Coefficient+127*Point_Coefficient)%N)[2:].zfill(64)
            self.wfile.write(bytes("<p class='key_hex'>*Starting Private Key Hex: " + str(__class__.starting_key_hex) + "</p>", "utf-8"))
            self.wfile.write(bytes("<p class='key_hex'>**Ending Private Key Hex: " + str(__class__.ending_key_hex) + "</p>", "utf-8"))
            self.wfile.write(bytes("<p id='balance' class='balance_on_page'>Balance on this Page: False</p>", "utf-8"))
            self.wfile.write(bytes("<pre><strong id='head_hex'>Private Key Hex</strong><strong id='head_wifu'>WIF Private Key Uncompressed</strong><strong id='head_legu'>Legacy Uncompressed Address</strong><strong id='head_legc'>Legacy Compressed Address</strong><strong id='head_p2sh'>Segwit P2SH Address</strong><strong id='head_p2wpkh'>Bech32 P2WPKH Address</strong><strong id='head_p2wsh'>Bech32 P2WSH Address</strong><strong id='head_wifc'>WIF Private Key Compressed</strong><br>", "utf-8"))
            for i in range(128):
                pub = ice.point_multiplication(__class__.startPrivKey,G).hex()
                dec = int((__class__.startPrivKey*Point_Coefficient)%N)
                __class__.privKey_C = ice.btc_pvk_to_wif(hex(dec)[2:].zfill(64))
                __class__.privKey = ice.btc_pvk_to_wif(hex(dec)[2:].zfill(64), False)
                __class__.bitAddr = ice.pubkey_to_address(0, False, bytes(bytearray.fromhex(pub)))
                __class__.bitAddr_C = ice.pubkey_to_address(0, True, bytes(bytearray.fromhex(pub)))
                addrP2sh = ice.privatekey_to_address(1, True, dec)
                addrbech32 = ice.privatekey_to_address(2, True, dec)
                addrbech32_p2wsh = bitcoinlib.keys.Address(ice.point_to_cpub(ice.point_multiplication(__class__.startPrivKey,G)),encoding='bech32',script_type='p2wsh').address
                __class__.addresses.append(__class__.bitAddr)
                __class__.addresses.append(__class__.bitAddr_C)
                __class__.addresses.append(addrP2sh)
                __class__.addresses.append(addrbech32)
                __class__.addresses.append(addrbech32_p2wsh)
                __class__.starting_key_hex = hex((__class__.startPrivKey*Point_Coefficient)%N)[2:].zfill(64)
                if  __class__.num == 452312848583266388373324160190187140050146735465136345244551418521555318338 and i == 31 or __class__.num == 452312848583266388373324160190187140050146735465136345244551418521555318338 and i == 32:
                    self.wfile.write(bytes("<span class='data_hex' rel='popup1' style='font-weight:bold;'  num='"+str(i+1)+"' value='"+__class__.starting_key_hex+"'>"+__class__.starting_key_hex+"</span><span class='data_wifu'>" + __class__.privKey + "</span><span class='data_legu'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr + "'>" + __class__.bitAddr + "</a></span><span class='data_legc'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr_C + "'>" + __class__.bitAddr_C + "</a></span><span class='data_p2sh'><a target='_blank' href='https://bitaps.com/"+addrP2sh+"'>"+addrP2sh+"</a></span><span class='data_p2wpkh'><a target='_blank' href='https://bitaps.com/"+addrbech32+"'>"+addrbech32+"</a></span><span class='data_p2wsh'><a target='_blank' href='https://bitaps.com/"+addrbech32_p2wsh+"'>"+addrbech32_p2wsh+"</a></span><span class='data_wifc'>" + __class__.privKey_C + "</span></br>", "utf-8")) 
                else:
                    self.wfile.write(bytes("<span class='data_hex' rel='popup1' num='"+str(i+1)+"' value='"+__class__.starting_key_hex+"'>"+__class__.starting_key_hex+"</span><span class='data_wifu'>" + __class__.privKey + "</span><span class='data_legu'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr + "'>" + __class__.bitAddr + "</a></span><span class='data_legc'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr_C + "'>" + __class__.bitAddr_C + "</a></span><span class='data_p2sh'><a target='_blank' href='https://bitaps.com/"+addrP2sh+"'>"+addrP2sh+"</a></span><span class='data_p2wpkh'><a target='_blank' href='https://bitaps.com/"+addrbech32+"'>"+addrbech32+"</a></span><span class='data_p2wsh'><a target='_blank' href='https://bitaps.com/"+addrbech32_p2wsh+"'>"+addrbech32_p2wsh+"</a></span><span class='data_wifc'>" + __class__.privKey_C + "</span></br>", "utf-8"))
                if __class__.startPrivKey == 115792089237316195423570985008687907852837564279074904382605163141518161494336:
                     break
                __class__.startPrivKey += 1
            for addr in __class__.addresses:
                if __class__.bloom.lookup_mm(addr):
                    __class__.balance_on_page = "True"
                    __class__.foundling += addr + " "
                    with open("found.txt", "a", encoding="utf-8") as f:
                        f.write(f"Bitcoin Address: {addr} Page# {__class__.num} \n")
            if __class__.balance_on_page == "True":
                mixer.init()
                mixer.music.load(found_sound)
                mixer.music.play()
            self.wfile.write(bytes("</pre><pre>[&nbsp;<span class='ajax' page='/"+str(__class__.previous)+"'>previous</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.next)+"'>next</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.random)+"'>random</span>&nbsp;]</pre>", "utf-8"))
            self.wfile.write(bytes("<p class='balance_on_page'>Balance on this Page: " + __class__.balance_on_page + " " + __class__.foundling + "</p>", "utf-8"))
            self.wfile.write(bytes("<script>var elem = document.getElementById('balance');elem.innerHTML = 'Balance on this Page: " + __class__.balance_on_page + " " + __class__.foundling + "'</script>", "utf-8"))
            __class__.addresses.clear()
            __class__.balance_on_page = "False"
            __class__.foundling = ""
#---------------------------------------------------------Full Page(Without Ajax(when sending requests from url))---------------------
        else:
            str_url = self.path[1:] #gettin / outta way from url we do not need
            if str_url.startswith('5H') or str_url.startswith('5J') or str_url.startswith('5K'): # if url starts with 5H 5J 5K we request page by 5WIF
                first_encode = base58.b58decode(self.path[1:])
                private_key_full = binascii.hexlify(first_encode)
                private_key = private_key_full[2:-8]
                private_key_hex = private_key.decode("utf-8")
                keyU = int(private_key_hex,16)
                __class__.searchKey = ice.privatekey_to_address(0, False, keyU)
                __class__.num = int(private_key_hex,16)
                __class__.num = __class__.num // 128
                __class__.num = __class__.num + 1
                __class__.previous = __class__.num - 1
                if (__class__.previous == 0):
                    __class__.previous = 1
                __class__.next = __class__.num + __class__.stride;                
                if (__class__.next > __class__.max):
                    __class__.next = __class__.max
                __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
            elif str_url.startswith('K') or str_url.startswith('L'): # if url starts with L K we request page by LWIF KWIF
                first_encode = base58.b58decode(self.path[1:])
                private_key_full = binascii.hexlify(first_encode)
                private_key = private_key_full[2:-8]
                private_key_hex = private_key.decode("utf-8")
                keyC = int(private_key_hex[0:64],16)
                __class__.searchKey = ice.privatekey_to_address(0, True, keyC)
                __class__.num = int(private_key_hex[0:64],16);
                __class__.num = __class__.num // 128
                __class__.num = __class__.num + 1
                __class__.previous = __class__.num - 1
                if (__class__.previous == 0):
                    __class__.previous = 1
                __class__.next = __class__.num + __class__.stride                
                if (__class__.next > __class__.max):
                    __class__.next = __class__.max
                __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
            else:
                if str_url.find("[") >= 0: # if url has [ after page number localhost:3333/123[33]  we want to change increment for next 
                    __class__.idx1 = str_url.index("[")
                    __class__.idx2 = str_url.index("]")
                    numm = str_url[0:__class__.idx1]
                    if bool(numm):
                        __class__.num = int(numm,10)
                    else:
                        __class__.num = 1
                    __class__.stride = int(str_url[__class__.idx1+1:__class__.idx2],10)
                    __class__.previous = __class__.num - 1
                    if __class__.previous == 0:
                        __class__.previous = 1
                    __class__.next = __class__.num + __class__.stride                
                    if __class__.next > __class__.max:
                        __class__.next = __class__.max
                    __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
                elif str_url.find("(") >= 0: # if url has ( after page number localhost:3333/123(100-333) we want to change random range for pages starting with 100 up to 333              
                    __class__.idx1 = str_url.index("(")
                    __class__.idx2 = str_url.index("-")
                    __class__.idx3 = str_url.index(")")
                    __class__.randomMin = int(str_url[__class__.idx1+1:__class__.idx2],10)
                    __class__.randomMax = int(str_url[__class__.idx2+1:__class__.idx3],10)
                    __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
                    numm = str_url[0:__class__.idx1]
                    if bool(numm):
                        __class__.num = int(numm,10)
                    else:
                        __class__.num = 1
                    __class__.previous = __class__.num - 1
                    if __class__.previous == 0:
                        __class__.previous = 1
                    __class__.next = __class__.num + __class__.stride                
                    if __class__.next > __class__.max:
                        __class__.next = __class__.max
                elif str_url.find("$") >= 0:  #if url starts with $ localhost:3333/$f78feb18a  we want to search page by hex value of privatekey              
                    __class__.idx1 = str_url.index("$")
                    if __class__.isHex(str_url[__class__.idx1+1:]) and len(str_url[__class__.idx1+1:]) > 0:                    
                        __class__.num = int(str_url[__class__.idx1+1:],16)
                        __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
                        __class__.searchKey_U = ice.privatekey_to_address(0, False, __class__.num)
                        __class__.num = __class__.num // 128
                        __class__.num = __class__.num + 1                
                        __class__.previous = __class__.num - 1
                        if __class__.previous == 0:
                            __class__.previous = 1
                        __class__.next = __class__.num + __class__.stride                
                        if __class__.next > __class__.max:
                            __class__.next = __class__.max
                    else:
                        __class__.num = 1
                        __class__.previous = __class__.num - 1;
                        if __class__.previous == 0:
                            __class__.previous = 1
                        __class__.next = __class__.num + __class__.stride                
                        if __class__.next > __class__.max:
                            __class__.next = __class__.max
                        __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
                elif str_url.find("@") >= 0: #if url starts with @ localhost:3333/@186732 we want to search page by decimal value of privatekey               
                    __class__.idx1 = str_url.index("@")
                    if str_url[__class__.idx1+1:].isnumeric():                    
                        __class__.num = int(str_url[__class__.idx1+1:],10)
                        __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
                        __class__.searchKey_U = ice.privatekey_to_address(0, False, __class__.num)
                        __class__.num = __class__.num // 128
                        __class__.num = __class__.num + 1                
                        __class__.previous = __class__.num - 1
                        if __class__.previous == 0:
                            __class__.previous = 1
                        __class__.next = __class__.num + __class__.stride                
                        if __class__.next > __class__.max:
                            __class__.next = __class__.max
                    else:
                        __class__.num = 1
                        __class__.previous = __class__.num - 1;
                        if __class__.previous == 0:
                            __class__.previous = 1
                        __class__.next = __class__.num + __class__.stride                
                        if __class__.next > __class__.max:
                            __class__.next = __class__.max
                        __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
                else:
                    if str_url == 'favicon.ico': #favicon.ico request gag
                        pass
                    else:
                        if str_url.isnumeric(): #if url contains just page number in decimal localhost:3333/123456 that is correct
                            __class__.num = int(str_url,10)
                            if __class__.num > __class__.max: #if requested page number more than max(last) we set it to max(last)
                                __class__.num = __class__.max
                            __class__.previous = __class__.num - 1;
                            if __class__.previous == 0:
                                 __class__.previous = 1
                            __class__.next = __class__.num + __class__.stride                
                            if __class__.next > __class__.max:
                                 __class__.next = __class__.max
                            __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
                        else: # if page number has not just decimal numbers we set it to first 
                            __class__.num = 1
                            __class__.previous = __class__.num - 1;
                            if __class__.previous == 0:
                                 __class__.previous = 1
                            __class__.next = __class__.num + __class__.stride                
                            if __class__.next > __class__.max:
                                 __class__.next = __class__.max
                            __class__.random = __class__.RandomInteger(__class__.randomMin,__class__.randomMax)
            self.wfile.write(bytes("""
<!DOCTYPE html>
<html>
<head>
            """, "utf-8"))
            self.wfile.write(bytes("<title>BTC Web Server "+version+"</title>", "utf-8"))
            self.wfile.write(bytes("""
<link rel='shortcut icon' href='data:image/x-icon;,' type='image/x-icon'> 
<style>
body{font-size:9.4pt;font-family:'Open Sans',sans-serif;}
a{text-decoration:none}
a:hover {text-decoration: underline}
.overlay_popup {display:none;position:fixed;z-index: 999;top:0;right:0;left:0;bottom:0;background:#000;opacity:0.5;}
.popup {display: none;position: relative;z-index: 1000;margin:0 25% 0 25%;width:50%;}
.object{z-index: 2;background-color: #eee;margin: 0 auto;position: fixed;top: 50%;left: 50%;transform: translate(-50%, -50%);width:700px;height:100%;text-align:center;}
.ajax{color:blue;}
.ajax:hover {cursor:pointer;text-decoration: underline;}
.arrow:hover {cursor:pointer;box-shadow:0 0 3px #656D9E;cursor:pointer;border:2px solid white;}
.auto_button:hover {box-shadow:0 0 3px #656D9E;cursor:pointer;border:2px solid white;}
.auto_button{height:30px;width:120px;padding:4px;}
#up{float:left;margin-bottom:12px;text-align:center;width:80px;height:30px;}
#up:hover{box-shadow:0 0 3px #656D9E;cursor:pointer;border:2px solid white;}
.arrow:focus {outline: none;}
input[type=text], select {width:640px;padding:8px 10px;margin: 2px 0;display: inline-block;border: 1px solid #ccc;border-radius: 4px;box-sizing: border-box;text-align:center;}
#search_line:focus{outline: none !important;border:1px solid #D5DBDB;box-shadow: 0 0 4px #719ECE;}
#page_span{color:#145A32;background-color:#f2f3f4;padding:2px;border-radius: 2px;}
#current_page{color:#145A32;padding:2px;background-color:#f2f3f4;border-radius: 2px;}
#last_page{color:#145A32;padding:2px;background-color:#f2f3f4;border-radius: 2px;}
#out_of{color:#145A32;padding:2px;background-color:#f2f3f4;border-radius: 2px;}
.key_hex{color:gray;font-weight:bold;}
.balance_on_page{color:#9A2A2A;font-weight:bold;}
.page_inc_rand{color:#9A2A2A;font-weight:bold;}
.gen_point{color:#6C3483;font-weight:bold;}
.data_hex:hover {cursor:pointer;text-decoration: underline;}
#head_hex{display:inline-block;width:450px;text-align:center;}
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
</style>""", "utf-8"))
            self.wfile.write(bytes("<script src='https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js'></script>", "utf-8"))
            self.wfile.write(bytes("<script>var point_coefficient=BigInt('"+str(Point_Coefficient)+"');</script>", "utf-8"))
            self.wfile.write(bytes("<script>var N = BigInt('115792089237316195423570985008687907852837564279074904382605163141518161494337');</script>", "utf-8"))
            self.wfile.write(bytes("""
</head>
<body link='#0000FF' vlink='#0000FF' alink='#0000FF'>""", "utf-8"))
            self.wfile.write(bytes("<p class='gen_point'>Generator Point (G) |&nbsp;<span style='color:#F1C40F;'>" + str(G.hex()[0:2]) + "</span><span style='color:#21618C;'>"+str(G.hex()[2:66])+"</span><span style='color:#239B56;'>"+str(G.hex()[66:])+"</span>&nbsp;|</p>", "utf-8"))
            self.wfile.write(bytes("<p class='gen_point'><span>Point Coefficient *** |&nbsp;<span style='color:#DE3163;'>"+str(Point_Coefficient)+"</span>&nbsp;|</span></p>", "utf-8"))
            self.wfile.write(bytes("<h2><span style='color:#34495E;'><input type='text' id='search_line' name='lastname' placeholder='Search Field' autocomplete='off'>&nbsp;&nbsp;&nbsp;Bitcoin addresses database&nbsp;***|&nbsp;" + str(__class__.addr_count) + " |</span></h2>", "utf-8")) 
            self.wfile.write(bytes("<p class='page_inc_rand'>Current page increment for next = <span id='cur_inc'>" + str(__class__.stride) + "</span></p>", "utf-8"))
            self.wfile.write(bytes("<p class='page_inc_rand'>Current random range = <span id='rand_min'>" + str(__class__.randomMin) + "</span> - <span id='rand_max'>" + str(__class__.randomMax) + "</span></p>", "utf-8"))            
            self.wfile.write(bytes("<pre><a class='ajax' page='/"+str(__class__.p255)+"'>2^255</a>|<a class='ajax' page='/"+str(__class__.p254)+"'>2^254</a>|<a class='ajax' page='/"+str(__class__.p253)+"'>2^253</a>|<a class='ajax' page='/"+str(__class__.p252)+"'>2^252</a>|<a class='ajax' page='/"+str(__class__.p251)+"'>2^251</a>|<a class='ajax' page='/"+str(__class__.p250)+"'>2^250</a>", "utf-8"))
            self.wfile.write(bytes("|<a class='ajax' page='/"+str(__class__.p249)+"'>2^249</a>|<a class='ajax' page='/"+str(__class__.p248)+"'>2^248</a>|<a class='ajax' page='/"+str(__class__.p247)+"'>2^247</a>|<a class='ajax' page='/"+str(__class__.p246)+"'>2^246</a>|<a class='ajax' page='/"+str(__class__.p245)+"'>2^245</a>|<a class='ajax' page='/"+str(__class__.p244)+"'>2^244</a>", "utf-8"))
            self.wfile.write(bytes("|<a class='ajax' page='/"+str(__class__.p243)+"'>2^243</a>|<a class='ajax' page='/"+str(__class__.p242)+"'>2^242</a>|<a class='ajax' page='/"+str(__class__.p241)+"'>2^241</a>|<a class='ajax' page='/"+str(__class__.p240)+"'>2^240</a>|<a class='ajax' page='/"+str(__class__.p239)+"'>2^239</a>|<a class='ajax' page='/"+str(__class__.p238)+"'>2^238</a>", "utf-8"))
            self.wfile.write(bytes("|<a class='ajax' page='/"+str(__class__.p237)+"'>2^237</a>|<a class='ajax' page='/"+str(__class__.p236)+"'>2^236</a>|<a class='ajax' page='/"+str(__class__.p235)+"'>2^235</a>|<a class='ajax' page='/"+str(__class__.p234)+"'>2^234</a>|<a class='ajax' page='/"+str(__class__.p233)+"'>2^233</a>|<a class='ajax' page='/"+str(__class__.p232)+"'>2^232</a>", "utf-8"))
            self.wfile.write(bytes("|<a class='ajax' page='/"+str(__class__.p231)+"'>2^231</a>|<a class='ajax' page='/"+str(__class__.p230)+"'>2^230</a>|<a class='ajax' page='/"+str(__class__.p229)+"'>2^229</a>|<a class='ajax' page='/"+str(__class__.p228)+"'>2^228</a>|<a class='ajax' page='/"+str(__class__.p227)+"'>2^227</a>|<a class='ajax' page='/"+str(__class__.p226)+"'>2^226</a>", "utf-8"))
            self.wfile.write(bytes("|<a class='ajax' page='/"+str(__class__.p225)+"'>2^225</a>|<a class='ajax' page='/"+str(__class__.p224)+"'>2^224</a>|<a class='ajax' page='/"+str(__class__.p223)+"'>2^223</a>|<a class='ajax' page='/"+str(__class__.p222)+"'>2^222</a>|<a class='ajax' page='/"+str(__class__.p221)+"'>2^221</a>|<a class='ajax' page='/"+str(__class__.p220)+"'>2^220</a><br>", "utf-8"))
            self.wfile.write(bytes("<a class='ajax' page='/"+str(__class__.p219)+"'>2^219</a>|<a class='ajax' page='/"+str(__class__.p218)+"'>2^218</a>|<a class='ajax' page='/"+str(__class__.p217)+"'>2^217</a>|<a class='ajax' page='/"+str(__class__.p216)+"'>2^216</a>|<a class='ajax' page='/"+str(__class__.p215)+"'>2^215</a>|<a class='ajax' page='/"+str(__class__.p214)+"'>2^214</a>", "utf-8"))
            self.wfile.write(bytes("|<a class='ajax' page='/"+str(__class__.p213)+"'>2^213</a>|<a class='ajax' page='/"+str(__class__.p212)+"'>2^212</a>|<a class='ajax' page='/"+str(__class__.p211)+"'>2^211</a>|<a class='ajax' page='/"+str(__class__.p210)+"'>2^210</a>|<a class='ajax' page='/"+str(__class__.p209)+"'>2^209</a>|<a class='ajax' page='/"+str(__class__.p208)+"'>2^208</a>", "utf-8"))
            self.wfile.write(bytes("|<a class='ajax' page='/"+str(__class__.p207)+"'>2^207</a>|<a class='ajax' page='/"+str(__class__.p206)+"'>2^206</a>|<a class='ajax' page='/"+str(__class__.p205)+"'>2^205</a>|<a class='ajax' page='/"+str(__class__.p204)+"'>2^204</a>|<a class='ajax' page='/"+str(__class__.p203)+"'>2^203</a>|<a class='ajax' page='/"+str(__class__.p202)+"'>2^202</a>", "utf-8"))
            self.wfile.write(bytes("|<a class='ajax' page='/"+str(__class__.p201)+"'>2^201</a>|<a class='ajax' page='/"+str(__class__.p200)+"'>2^200</a>|<a class='ajax' page='/"+str(__class__.p199)+"'>2^199</a>|<a class='ajax' page='/"+str(__class__.p198)+"'>2^198</a>|<a class='ajax' page='/"+str(__class__.p197)+"'>2^197</a>|<a class='ajax' page='/"+str(__class__.p196)+"'>2^196</a>", "utf-8"))
            self.wfile.write(bytes("|<a class='ajax' page='/"+str(__class__.p195)+"'>2^195</a>|<a class='ajax' page='/"+str(__class__.p194)+"'>2^194</a>|<a class='ajax' page='/"+str(__class__.p193)+"'>2^193</a>|<a class='ajax' page='/"+str(__class__.p192)+"'>2^192</a>|<a class='ajax' page='/"+str(__class__.p191)+"'>2^191</a>|<a class='ajax' page='/"+str(__class__.p190)+"'>2^190</a>", "utf-8"))
            self.wfile.write(bytes("|<a class='ajax' page='/"+str(__class__.p189)+"'>2^189</a>|<a class='ajax' page='/"+str(__class__.p188)+"'>2^188</a>|<a class='ajax' page='/"+str(__class__.p187)+"'>2^187</a>|<a class='ajax' page='/"+str(__class__.p186)+"'>2^186</a>|<a class='ajax' page='/"+str(__class__.p185)+"'>2^185</a>|<a class='ajax' page='/"+str(__class__.p184)+"'>2^184</a><br>", "utf-8"))
            self.wfile.write(bytes("<a class='ajax' page='/"+str(__class__.p183)+"'>2^183</a>|<a class='ajax' page='/"+str(__class__.p182)+"'>2^182</a>|<a class='ajax' page='/"+str(__class__.p181)+"'>2^181</a>|<a class='ajax' page='/"+str(__class__.p180)+"'>2^180</a>|<a class='ajax' page='/"+str(__class__.p179)+"'>2^179</a>|<a class='ajax' page='/"+str(__class__.p178)+"'>2^178</a>", "utf-8"))
            self.wfile.write(bytes("|<a class='ajax' page='/"+str(__class__.p177)+"'>2^177</a>|<a class='ajax' page='/"+str(__class__.p176)+"'>2^176</a>|<a class='ajax' page='/"+str(__class__.p175)+"'>2^175</a>|<a class='ajax' page='/"+str(__class__.p174)+"'>2^174</a>|<a class='ajax' page='/"+str(__class__.p173)+"'>2^173</a>|<a class='ajax' page='/"+str(__class__.p172)+"'>2^172</a>", "utf-8"))
            self.wfile.write(bytes("|<a class='ajax' page='/"+str(__class__.p171)+"'>2^171</a>|<a class='ajax' page='/"+str(__class__.p170)+"'>2^170</a>|<a class='ajax' page='/"+str(__class__.p169)+"'>2^169</a>|<a class='ajax' page='/"+str(__class__.p168)+"'>2^168</a>|<a class='ajax' page='/"+str(__class__.p167)+"'>2^167</a>|<a class='ajax' page='/"+str(__class__.p166)+"'>2^166</a>", "utf-8"))
            self.wfile.write(bytes("|<a class='ajax' page='/"+str(__class__.p165)+"'>2^165</a>|<a class='ajax' page='/"+str(__class__.p164)+"'>2^164</a>|<a class='ajax' page='/"+str(__class__.p163)+"'>2^163</a>|<a class='ajax' page='/"+str(__class__.p162)+"'>2^162</a>|<a class='ajax' page='/"+str(__class__.p161)+"'>2^161</a>|<a class='ajax' page='/"+str(__class__.p160)+"'>2^160</a>", "utf-8"))
            self.wfile.write(bytes("|<a class='ajax' page='/"+str(__class__.p159)+"'>2^159</a>|<a class='ajax' page='/"+str(__class__.p158)+"'>2^158</a>|<a class='ajax' page='/"+str(__class__.p157)+"'>2^157</a>|<a class='ajax' page='/"+str(__class__.p156)+"'>2^156</a>|<a class='ajax' page='/"+str(__class__.p155)+"'>2^155</a>|<a class='ajax' page='/"+str(__class__.p154)+"'>2^154</a>", "utf-8"))
            self.wfile.write(bytes("|<a class='ajax' page='/"+str(__class__.p153)+"'>2^153</a>|<a class='ajax' page='/"+str(__class__.p152)+"'>2^152</a>|<a class='ajax' page='/"+str(__class__.p151)+"'>2^151</a>|<a class='ajax' page='/"+str(__class__.p150)+"'>2^150</a>|<a class='ajax' page='/"+str(__class__.p149)+"'>2^149</a>|<a class='ajax' page='/"+str(__class__.p148)+"'>2^148</a><br>", "utf-8"))
            self.wfile.write(bytes("<a class='ajax' page='/"+str(__class__.p147)+"'>2^147</a>|<a class='ajax' page='/"+str(__class__.p146)+"'>2^146</a>|<a class='ajax' page='/"+str(__class__.p145)+"'>2^145</a>|<a class='ajax' page='/"+str(__class__.p144)+"'>2^144</a>|<a class='ajax' page='/"+str(__class__.p143)+"'>2^143</a>|<a class='ajax' page='/"+str(__class__.p142)+"'>2^142</a>", "utf-8"))
            self.wfile.write(bytes("|<a class='ajax' page='/"+str(__class__.p141)+"'>2^141</a>|<a class='ajax' page='/"+str(__class__.p140)+"'>2^140</a>|<a class='ajax' page='/"+str(__class__.p139)+"'>2^139</a>|<a class='ajax' page='/"+str(__class__.p138)+"'>2^138</a>|<a class='ajax' page='/"+str(__class__.p137)+"'>2^137</a>|<a class='ajax' page='/"+str(__class__.p136)+"'>2^136</a>", "utf-8"))
            self.wfile.write(bytes("|<a class='ajax' page='/"+str(__class__.p135)+"'>2^135</a>|<a class='ajax' page='/"+str(__class__.p134)+"'>2^134</a>|<a class='ajax' page='/"+str(__class__.p133)+"'>2^133</a>|<a class='ajax' page='/"+str(__class__.p132)+"'>2^132</a>|<a class='ajax' page='/"+str(__class__.p131)+"'>2^131</a>|<a class='ajax' page='/"+str(__class__.p130)+"'>2^130</a>", "utf-8"))
            self.wfile.write(bytes("|<a class='ajax' page='/"+str(__class__.p129)+"'>2^129</a>|<a class='ajax' page='/"+str(__class__.p128)+"'>2^128</a>|<a class='ajax' page='/"+str(__class__.p127)+"'>2^127</a>|<a class='ajax' page='/"+str(__class__.p126)+"'>2^126</a>|<a class='ajax' page='/"+str(__class__.p125)+"'>2^125</a>|<a class='ajax' page='/"+str(__class__.p124)+"'>2^124</a>", "utf-8"))
            self.wfile.write(bytes("|<a class='ajax' page='/"+str(__class__.p123)+"'>2^123</a>|<a class='ajax' page='/"+str(__class__.p122)+"'>2^122</a>|<a class='ajax' page='/"+str(__class__.p121)+"'>2^121</a>|<a class='ajax' page='/"+str(__class__.p120)+"'>2^120</a>|<a class='ajax' page='/"+str(__class__.p119)+"'>2^119</a>|<a class='ajax' page='/"+str(__class__.p118)+"'>2^118</a>", "utf-8"))
            self.wfile.write(bytes("|<a class='ajax' page='/"+str(__class__.p117)+"'>2^117</a>|<a class='ajax' page='/"+str(__class__.p116)+"'>2^116</a>|<a class='ajax' page='/"+str(__class__.p115)+"'>2^115</a>|<a class='ajax' page='/"+str(__class__.p114)+"'>2^114</a>|<a class='ajax' page='/"+str(__class__.p113)+"'>2^113</a>|<a class='ajax' page='/"+str(__class__.p112)+"'>2^112</a><br>", "utf-8"))
            self.wfile.write(bytes("<a class='ajax' page='/"+str(__class__.p111)+"'>2^111</a>|<a class='ajax' page='/"+str(__class__.p110)+"'>2^110</a>|<a class='ajax' page='/"+str(__class__.p109)+"'>2^109</a>|<a class='ajax' page='/"+str(__class__.p108)+"'>2^108</a>|<a class='ajax' page='/"+str(__class__.p107)+"'>2^107</a>|<a class='ajax' page='/"+str(__class__.p106)+"'>2^106</a>", "utf-8"))
            self.wfile.write(bytes("|<a class='ajax' page='/"+str(__class__.p105)+"'>2^105</a>|<a class='ajax' page='/"+str(__class__.p104)+"'>2^104</a>|<a class='ajax' page='/"+str(__class__.p103)+"'>2^103</a>|<a class='ajax' page='/"+str(__class__.p102)+"'>2^102</a>|<a class='ajax' page='/"+str(__class__.p101)+"'>2^101</a>|<a class='ajax' page='/"+str(__class__.p100)+"'>2^100</a>", "utf-8"))
            self.wfile.write(bytes("|<a class='ajax' page='/"+str(__class__.p99)+"'>2^99</a>|<a class='ajax' page='/"+str(__class__.p98)+"'>2^98</a>|<a class='ajax' page='/"+str(__class__.p97)+"'>2^97</a>|<a class='ajax' page='/"+str(__class__.p96)+"'>2^96</a>|<a class='ajax' page='/"+str(__class__.p95)+"'>2^95</a>|<a class='ajax' page='/"+str(__class__.p94)+"'>2^94</a>", "utf-8"))
            self.wfile.write(bytes("|<a class='ajax' page='/"+str(__class__.p93)+"'>2^93</a>|<a class='ajax' page='/"+str(__class__.p92)+"'>2^92</a>|<a class='ajax' page='/"+str(__class__.p91)+"'>2^91</a>|<a class='ajax' page='/"+str(__class__.p90)+"'>2^90</a>|<a class='ajax' page='/"+str(__class__.p89)+"'>2^89</a>|<a class='ajax' page='/"+str(__class__.p88)+"'>2^88</a>", "utf-8"))
            self.wfile.write(bytes("|<a class='ajax' page='/"+str(__class__.p87)+"'>2^87</a>|<a class='ajax' page='/"+str(__class__.p86)+"'>2^86</a>|<a class='ajax' page='/"+str(__class__.p85)+"'>2^85</a>|<a class='ajax' page='/"+str(__class__.p84)+"'>2^84</a>|<a class='ajax' page='/"+str(__class__.p83)+"'>2^83</a>|<a class='ajax' page='/"+str(__class__.p82)+"'>2^82</a>", "utf-8"))
            self.wfile.write(bytes("|<a class='ajax' page='/"+str(__class__.p81)+"'>2^81</a>|<a class='ajax' page='/"+str(__class__.p82)+"'>2^82</a>|<a class='ajax' page='/"+str(__class__.p81)+"'>2^81</a>|<a class='ajax' page='/"+str(__class__.p80)+"'>2^80</a>|<a class='ajax' page='/"+str(__class__.p79)+"'>2^79</a>|<a class='ajax' page='/"+str(__class__.p78)+"'>2^78</a>", "utf-8"))
            self.wfile.write(bytes("|<a class='ajax' page='/"+str(__class__.p77)+"'>2^77</a>|<a class='ajax' page='/"+str(__class__.p76)+"'>2^76</a>|<a class='ajax' page='/"+str(__class__.p75)+"'>2^75</a>|<a class='ajax' page='/"+str(__class__.p74)+"'>2^74</a>|<a class='ajax' page='/"+str(__class__.p73)+"'>2^73</a><br><a class='ajax' page='/"+str(__class__.p72)+"'>2^72</a>", "utf-8"))
            self.wfile.write(bytes("|<a class='ajax' page='/"+str(__class__.p71)+"'>2^71</a>|<a class='ajax' page='/"+str(__class__.p70)+"'>2^70</a>|<a class='ajax' page='/"+str(__class__.p69)+"'>2^69</a>|<a class='ajax' page='/"+str(__class__.p68)+"'>2^68</a>|<a class='ajax' page='/"+str(__class__.p67)+"'>2^67</a>|<a class='ajax' page='/"+str(__class__.p66)+"'>2^66</a>", "utf-8"))
            self.wfile.write(bytes("|<a class='ajax' page='/"+str(__class__.p65)+"'>2^65</a>|<a class='ajax' page='/"+str(__class__.p64)+"'>2^64</a>|<a class='ajax' page='/"+str(__class__.p63)+"'>2^63</a>|<a class='ajax' page='/"+str(__class__.p62)+"'>2^62</a>|<a class='ajax' page='/"+str(__class__.p61)+"'>2^61</a>|<a class='ajax' page='/"+str(__class__.p60)+"'>2^60</a>", "utf-8"))
            self.wfile.write(bytes("|<a class='ajax' page='/"+str(__class__.p59)+"'>2^59</a>|<a class='ajax' page='/"+str(__class__.p58)+"'>2^58</a>|<a class='ajax' page='/"+str(__class__.p57)+"'>2^57</a>|<a class='ajax' page='/"+str(__class__.p56)+"'>2^56</a>|<a class='ajax' page='/"+str(__class__.p55)+"'>2^55</a>|<a class='ajax' page='/"+str(__class__.p54)+"'>2^54</a>", "utf-8"))
            self.wfile.write(bytes("|<a class='ajax' page='/"+str(__class__.p53)+"'>2^53</a>|<a class='ajax' page='/"+str(__class__.p52)+"'>2^52</a>|<a class='ajax' page='/"+str(__class__.p51)+"'>2^51</a>|<a class='ajax' page='/"+str(__class__.p50)+"'>2^50</a>|<a class='ajax' page='/"+str(__class__.p49)+"'>2^49</a>|<a class='ajax' page='/"+str(__class__.p48)+"'>2^48</a>", "utf-8"))
            self.wfile.write(bytes("|<a class='ajax' page='/"+str(__class__.p47)+"'>2^47</a>|<a class='ajax' page='/"+str(__class__.p46)+"'>2^46</a>|<a class='ajax' page='/"+str(__class__.p45)+"'>2^45</a>|<a class='ajax' page='/"+str(__class__.p44)+"'>2^44</a>|<a class='ajax' page='/"+str(__class__.p43)+"'>2^43</a>|<a class='ajax' page='/"+str(__class__.p42)+"'>2^42</a>", "utf-8"))
            self.wfile.write(bytes("|<a class='ajax' page='/"+str(__class__.p41)+"'>2^41</a>|<a class='ajax' page='/"+str(__class__.p40)+"'>2^40</a>|<a class='ajax' page='/"+str(__class__.p39)+"'>2^39</a>|<a class='ajax' page='/"+str(__class__.p38)+"'>2^38</a>|<a class='ajax' page='/"+str(__class__.p37)+"'>2^37</a>|<a class='ajax' page='/"+str(__class__.p36)+"'>2^36</a>", "utf-8"))
            self.wfile.write(bytes("|<a class='ajax' page='/"+str(__class__.p35)+"'>2^35</a>|<a class='ajax' page='/"+str(__class__.p34)+"'>2^34</a>|<a class='ajax' page='/"+str(__class__.p33)+"'>2^33</a>|<a class='ajax' page='/"+str(__class__.p32)+"'>2^32</a>|<a class='ajax' page='/"+str(__class__.p31)+"'>2^31</a>|<a class='ajax' page='/"+str(__class__.p30)+"'>2^30</a><br>", "utf-8"))
            self.wfile.write(bytes("<a class='ajax' page='/"+str(__class__.p29)+"'>2^29</a>|<a class='ajax' page='/"+str(__class__.p28)+"'>2^28</a>|<a class='ajax' page='/"+str(__class__.p27)+"'>2^27</a>|<a class='ajax' page='/"+str(__class__.p26)+"'>2^26</a>|<a class='ajax' page='/"+str(__class__.p25)+"'>2^25</a>|<a class='ajax' page='/"+str(__class__.p24)+"'>2^24</a>", "utf-8"))
            self.wfile.write(bytes("|<a class='ajax' page='/"+str(__class__.p23)+"'>2^23</a>|<a class='ajax' page='/"+str(__class__.p22)+"'>2^22</a>|<a class='ajax' page='/"+str(__class__.p21)+"'>2^21</a>|<a class='ajax' page='/"+str(__class__.p20)+"'>2^20</a>|<a class='ajax' page='/"+str(__class__.p19)+"'>2^19</a>|<a class='ajax' page='/"+str(__class__.p18)+"'>2^18</a>", "utf-8"))
            self.wfile.write(bytes("|<a  class='ajax' page='/"+str(__class__.p17)+"'>2^17</a>|<a class='ajax' page='/"+str(__class__.p16)+"'>2^16</a>|<a class='ajax' page='/"+str(__class__.p15)+"'>2^15</a>|<a class='ajax' page='/"+str(__class__.p14)+"'>2^14</a>|<a class='ajax' page='/"+str(__class__.p13)+"'>2^13</a>|<a class='ajax' page='/"+str(__class__.p12)+"'>2^12</a>", "utf-8"))
            self.wfile.write(bytes("|<a class='ajax' page='/"+str(__class__.p11)+"'>2^11</a>|<a class='ajax' page='/"+str(__class__.p10)+"'>2^10</a>|<a class='ajax' page='/"+str(__class__.p9)+"'>2^9</a>|<a class='ajax' page='/"+str(__class__.p8)+"'>2^8</a>|<a class='ajax' page='/"+str(__class__.p7)+"'>2^7</a>|<a class='ajax' page='/"+str(__class__.p6)+"'>2^6</a>", "utf-8"))
            self.wfile.write(bytes("|<a class='ajax' page='/"+str(__class__.p5)+"'>2^5</a>|<a class='ajax' page='/"+str(__class__.p4)+"'>2^4</a>|<a class='ajax' page='/"+str(__class__.p3)+"'>2^3</a>|<a class='ajax' page='/"+str(__class__.p2)+"'>2^2</a>|<a class='ajax' page='/"+str(__class__.p1)+"'>2^1</a></pre>", "utf-8"))
            self.wfile.write(bytes("<pre>[&nbsp;<span class='ajax' page='/"+str(__class__.hj)+"'>5H(end)-5J(start)</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.jk)+"'>5J(end)-5K(start)</span>&nbsp;]&nbsp;&nbsp;&nbsp;<=>&nbsp;&nbsp;&nbsp;", "utf-8"))
            self.wfile.write(bytes("[&nbsp;<span class='ajax' page='/"+str(__class__.Kx)+"'>Kw(end)_Kx(start)</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.Ky)+"'>Kx(end)_Ky(start)</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.Kz)+"'>Ky(end)_Kz(start)</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.L1)+"'>Kz(end)-L1(start)</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.L2)+"'>L1(end)_L2(start)</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.L3)+"'>L2(end)_L3(start)</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.L4)+"'>L3(end)_L4(start)</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.L5)+"'>L4(end)_L5(start)</span>&nbsp;]</pre>", "utf-8"))
            self.wfile.write(bytes("""
<div id='auto' style='padding-bottom:3px;'> 
<button class='auto_button' id='start_auto'>Auto Start</button>
<button class='auto_button' id='stop_auto'>Auto Stop</button> &nbsp;&nbsp;&nbsp;
<span id='status_str' style='color:brown;font-weight: bold;'>Found [&nbsp;<span id='found_num'>0</span>&nbsp;]&nbsp;
Pages checked:&nbsp;<span id='p_checked'>0</span></span>&nbsp;&nbsp;&nbsp;&nbsp;
<button class='auto_button' id='start_auto_seq'>Start AutoSeq</button>
<button class='auto_button' id='stop_auto_seq'>Stop AutoSeq</button> &nbsp;&nbsp;&nbsp;
<span id='status_str_seq' style='color:brown;font-weight: bold;'>Found [&nbsp;<span id='found_num_seq'>0</span>&nbsp;]&nbsp;&nbsp;&nbsp;
Pages checked:&nbsp;<span id='p_checked_seq'>0</span></span>&nbsp;&nbsp;&nbsp;&nbsp;
<button class='auto_button' id='start_auto_pilot'>Start AutoPilot</button>
<button class='auto_button' id='stop_auto_pilot'>Stop AutoPilot</button> &nbsp;&nbsp;&nbsp;
<span id='status_str_pilot' style='color:brown;font-weight: bold;'>Found [&nbsp;<span id='found_num_pilot'>0</span>&nbsp;]&nbsp;&nbsp;&nbsp;
Pages checked:&nbsp;<span id='p_checked_pilot'>0</span> &nbsp;&nbsp;Total addresses scanned: <span id='t_scanned_pilot'></span></span>&nbsp;&nbsp;&nbsp;&nbsp;
<button class='auto_button' id='start_auto_pilot_seq'>Start PilotSeq</button>
<button class='auto_button' id='stop_auto_pilot_seq'>Stop PilotSeq</button> &nbsp;&nbsp;&nbsp;
<span id='status_str_pilot_seq' style='color:brown;font-weight: bold;'>Found [&nbsp;<span id='found_num_pilot_seq'>0</span>&nbsp;]&nbsp;&nbsp;&nbsp;
Pages checked:&nbsp;<span id='p_checked_pilot_seq'>0</span> &nbsp;&nbsp;Total addresses scanned: <span id='t_scanned_pilot_seq'></span><br>
<span id='status_page' style='margin-left:592px'>Current page: <span id='pilot_page_seq_num'></span></span></span></div>
            """, "utf-8"))
            self.wfile.write(bytes("""
<script>
let auto_speed = 500, pilot_speed = 300;
let play_random = 0, play_sequence = 0, play_pilot = 0, play_pilot_sequence = 0, difference = 0, f_num = 0;
let page_number = BigInt(0), checked_pages = BigInt(0), increment = BigInt(0);
let RandomMin = BigInt(0), RandomMax = BigInt(0), numPage = BigInt(0), randomDifference = BigInt(0); 
let differenceLength = '', multiplier = '', divisor = '', found_str = '', status_str = ''; 
document.getElementById("status_str").style.display = "none";
document.getElementById("status_str_seq").style.display = "none";
document.getElementById("status_str_pilot").style.display = "none";
document.getElementById("status_str_pilot_seq").style.display = "none";
document.getElementById("stop_auto").style.display = "none";
document.getElementById("stop_auto_pilot").style.display = "none";
document.getElementById("stop_auto_pilot_seq").style.display = "none";
document.getElementById("stop_auto_seq").style.display = "none";
$('#search_line').focus(function() {
   $('#search_line').val("");
})
$('#search_line').blur(function() {
   var input_val = $('#search_line').val();
   $.get("http://localhost:3333/S"+ input_val.trim(), function(data, status){
            document.getElementById("main_content").innerHTML = data;
            history.pushState({}, null, "http://localhost:3333/"+$('#current_page').html());
    })
})
function generateRandomBigInt(lowBigInt, highBigInt) {
    difference = highBigInt - lowBigInt;
    differenceLength = difference.toString().length;
    multiplier = '';
    while (multiplier.length < differenceLength) {
        multiplier += Math.random().toString().split('.')[1];
    }
    multiplier = multiplier.slice(0, differenceLength);
    divisor = '1' + '0'.repeat(differenceLength);
    randomDifference = (BigInt(difference) * BigInt(multiplier)) / BigInt(divisor);
    return (BigInt(lowBigInt) + BigInt(randomDifference)).toString();
}
function rolling(){                
    numPage = generateRandomBigInt(RandomMin,RandomMax);
    $.get("http://localhost:3333/A"+numPage, function(data){        
        document.getElementById("main_content").innerHTML = data;
        history.pushState({}, null, "http://localhost:3333/"+numPage);
        f_num = parseInt(document.getElementById("found_num").innerHTML); 
        found_str = document.getElementById("balance").innerHTML;
        if(found_str.includes("False") && f_num == 0 ) { 
            document.getElementById("found_num").innerHTML = "0"; 
        }
        if(found_str.includes("False") && f_num > 0 ) {
            document.getElementById("found_num").innerHTML = f_num;
        }
        if(found_str.includes("True")) {                    
            document.getElementById("found_num").innerHTML = f_num + 1; 
        }
    })
    document.getElementById("p_checked").innerHTML = ++checked_pages;
}
$('#start_auto').click(function() {
    play_random = setInterval(rolling, auto_speed);
    document.getElementById("start_auto").style.display = "none";
    document.getElementById("stop_auto").style.display = "inline";     
    checked_pages = 0;
    RandomMin = BigInt(document.getElementById("rand_min").innerHTML)
    RandomMax = BigInt(document.getElementById("rand_max").innerHTML)
    document.getElementById("start_auto_seq").disabled = "true";
    document.getElementById("start_auto_pilot").disabled = "true";
    document.getElementById("start_auto_pilot_seq").disabled = "true";
    document.getElementById("search_line").disabled = "true";
    document.getElementById("p_checked").innerHTML = "0";
    document.getElementById("found_num").innerHTML = "0";        
    document.getElementById("status_str").style.display = "inline";
})
$('#stop_auto').click(function() {
    clearInterval(play_random);                    
    document.getElementById("start_auto_seq").removeAttribute("disabled");
    document.getElementById("start_auto_pilot").removeAttribute("disabled");
    document.getElementById("start_auto_pilot_seq").removeAttribute("disabled");
    document.getElementById("search_line").removeAttribute("disabled");
    document.getElementById("stop_auto").style.display = "none";
    document.getElementById("start_auto").style.display = "inline";
    $('#status_str').fadeOut(1000);     
})
function sequence() {
    page_number += increment;                
    if (page_number > BigInt("904625697166532776746648320380374280100293470930272690489102837043110636675")) {
        clearInterval(play_sequence);
        document.getElementById("search_line").removeAttribute("disabled");
        document.getElementById("start_auto_pilot").removeAttribute("disabled");
        document.getElementById("start_auto_pilot_seq").removeAttribute("disabled");
        document.getElementById("start_auto").removeAttribute("disabled");
        document.getElementById("stop_auto_seq").style.display = "none";
        document.getElementById("start_auto_seq").style.display = "inline";
        $('#status_str_seq').fadeOut(1500);
        checked_pages = 0;
        return false;
    }
    else {
        $.get("http://localhost:3333/A"+ page_number, function(data, status){
            document.getElementById("main_content").innerHTML = data;
            history.pushState({}, null, "http://localhost:3333/"+$('#current_page').html());
            f_num = parseInt(document.getElementById("found_num_seq").innerHTM);             
            found_str = document.getElementById("balance").innerHTM;                    
            if(found_str.includes("False") && f_num == 0 ) { 
                document.getElementById("found_num_seq").innerHTML = "0"; 
            }
            if(found_str.includes("False") && f_num > 0 ) {
                document.getElementById("found_num_seq").innerHTML = f_num;
            }
            if(found_str.includes("True")) {                    
                document.getElementById("found_num_seq").innerHTML = f_num + 1;
            }
        })
    }
    $('#p_checked_seq').html(++checked_pages);                                              
}
$('#start_auto_seq').click(function() {
    play_sequence = setInterval(sequence, auto_speed);
    $(this).hide();
    $('#stop_auto_seq').show();
    checked_pages = 0;
    page_number = BigInt(document.getElementById("current_page").innerHTML);                
    increment = BigInt(document.getElementById("cur_inc").innerHTML);
    $('#start_auto').prop('disabled', true);
    $('#start_auto_pilot').prop('disabled', true);
    $('#start_auto_pilot_seq').prop('disabled', true);
    $('#search_line').prop('disabled', true);               
    document.getElementById("p_checked_seq").innerHTML = "0";
    document.getElementById("found_num_seq").innerHTML = "0";
    $('#status_str_seq').show();     
})
$('#stop_auto_seq').click(function() {
    clearInterval(play_sequence);    
    $('#start_auto').prop('disabled', false);
    $('#start_auto_seq').prop('disabled', false);
    $('#start_auto_pilot').prop('disabled', false);
    $('#start_auto_pilot_seq').prop('disabled', false);
    $('#search_line').prop('disabled', false);
    $(this).hide();
    $('#start_auto_seq').show();
    $('#status_str_seq').fadeOut(1000);                               
})
function pilot(){                
    numPage = generateRandomBigInt(RandomMin,RandomMax);
    $.get("http://localhost:3333/P"+numPage, function(data, status){
        status_str = data;
        f_num = parseInt(document.getElementById("found_num_pilot").innerHTML);
        if(status_str == "Yes" ) { 
            document.getElementById("found_num_pilot").innerHTML = f_num + 1; 
        }
        if(status_str == "No" ) {
            document.getElementById("found_num_pilot").innerHTML = f_num ;
        }
    })
    $('#p_checked_pilot').html(++checked_pages);
    $('#t_scanned_pilot').html((checked_pages*640));
}
$('#start_auto_pilot').click(function() {
    play_pilot = setInterval(pilot, pilot_speed);
    RandomMin = BigInt(document.getElementById("rand_min").innerHTML)
    RandomMax = BigInt(document.getElementById("rand_max").innerHTML)
    $('#start_auto').prop('disabled', true);
    $('#start_auto_seq').prop('disabled', true);
    $('#start_auto_pilot_seq').prop('disabled', true);
    checked_pages = 0;
    document.getElementById("p_checked_pilot").innerHTML = "0";
    document.getElementById("found_num_pilot").innerHTML = "0";
    document.getElementById("t_scanned_pilot").innerHTML = "0";
    $('#status_str_pilot').show();
    $(this).hide();
    $('#stop_auto_pilot').show();
})
$('#stop_auto_pilot').click(function() {
    clearInterval(play_pilot);
    $('#start_auto').prop('disabled', false);
    $('#start_auto_seq').prop('disabled', false);
    $('#start_auto_pilot_seq').prop('disabled', false);    
    $(this).hide();
    $('#start_auto_pilot').show();    
    $('#status_str_pilot').fadeOut(1000);                                                        
})
function pilot_sequence() {
    page_number += increment;                
    if (page_number > BigInt("904625697166532776746648320380374280100293470930272690489102837043110636675")) {
        clearInterval(play_pilot_sequence);
        $('#start_auto_seq').prop('disabled', false);
        $('#start_auto').prop('disabled', false);
        $('#start_auto_pilot').prop('disabled', false);
        $('#stop_auto_pilot_seq').hide();
        $('#start_auto_pilot_seq').show();
        $('#status_str_pilot_seq').fadeOut(1500);
        $('#pilot_page_seq_num').html('904625697166532776746648320380374280100293470930272690489102837043110636675');
        checked_pages = 0;                 
        return false;
    }
    else {
        $.get("http://localhost:3333/P"+ page_number, function(data, status){
            status_str = data;
            f_num = parseInt(document.getElementById("found_num_pilot_seq").innerHTML);
            if(status_str == "Yes" ) { 
                f_num = f_num + 1;
                $('#found_num_pilot_seq').html(f_num); 
            }
            if(status_str == "No" ) {
                $('#found_num_pilot_seq').html(f_num);
            }
        })
    }
    document.getElementById("p_checked_pilot_seq").innerHTML = ++checked_pages;
    document.getElementById("t_scanned_pilot_seq").innerHTML = checked_pages*640;
    document.getElementById("pilot_page_seq_num").innerHTML = page_number;                                              
}
$('#start_auto_pilot_seq').click(function() {
    play_pilot_sequence = setInterval(pilot_sequence, pilot_speed);
    $(this).hide();
    $('#stop_auto_pilot_seq').show();
    checked_pages = 0;
    page_number = BigInt(document.getElementById("current_page").innerHTML);                
    increment = BigInt(document.getElementById("cur_inc").innerHTML);
    $('#start_auto').prop('disabled', true);
    $('#start_auto_seq').prop('disabled', true);
    $('#start_auto_pilot').prop('disabled', true);               
    document.getElementById("p_checked_pilot_seq").innerHTML = "0";
    document.getElementById("found_num_pilot_seq").innerHTML = "0";
    document.getElementById("t_scanned_pilot_seq").innerHTML = "0";
    $('#status_str_pilot_seq').show();
})
$('#stop_auto_pilot_seq').click(function() {
    clearInterval(play_pilot_sequence);
    $('#start_auto').prop('disabled', false);
    $('#start_auto_seq').prop('disabled', false);
    $('#start_auto_pilot').prop('disabled', false);
    $(this).hide();
    $('#start_auto_pilot_seq').show();    
    $('#status_str_pilot_seq').fadeOut(1000);                               
})
</script>""", "utf-8"))
            self.wfile.write(bytes("""
<div class='overlay_popup'></div>
<div class='popup' id='popup1'>
<div class='object' style='overflow-y:auto;overflow-x:hidden;'>
<h4 style='color:brown;font-weight:bold;text-align:right;'>
<button class='arrow' id='arrow_left' style='color:blue;margin-left:132px;'><<<</button>&nbsp;&nbsp;
<span style='color:brown;' id='arrow_num'>1</span> <span style='color:brown;'>of</span> <span  id='all_num' style='color:brown;'>128</span>&nbsp;&nbsp;
<button class='arrow' id='arrow_right' style='color:blue;'>>>></button>&nbsp;&nbsp;</h4>
<h4 style='color:brown;font-weight:bold;'>Private and Public ECDSA Key</h4>          
<p id='funbin' style='color:#DE3163;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;word-wrap: break-word;'></p>            
<p id='funhex' style='color:#DE3163;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='fun' style='color:#DE3163;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='fun2x' style='color:#21618C;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='fun2y' style='color:#239B56;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='fun3x' style='color:#21618C;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='fun3y' style='color:#239B56;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='fun5' style='color:#21618C;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='fun4' style='color:#34495E ;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='funaddr1' style='color:blue;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='funaddr2' style='color:blue;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>           
<h4 style='color:brown;font-weight:bold;'>Additive Inverse Point</h4>
<p id='addinvn' style='color:#DE3163;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='addinvx' style='color:#21618C;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='addinvy' style='color:#239B56;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='addrinv' style='color:blue;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='addrinvpb' style='color:blue;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<h4 style='color:brown;font-weight:bold;'>Two More Points same Y different X</h4>
<p id='same1n' style='color:#DE3163;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='same1x' style='color:#21618C;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='same1y' style='color:#239B56;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='same1addr' style='color:blue;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='same1addrpb' style='color:blue;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='same2n' style='color:#DE3163;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='same2x' style='color:#21618C;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='same2y' style='color:#239B56;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='same2addr' style='color:blue;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
<p id='same2addrpb' style='color:blue;background:#D7DBDD;padding:3px;font-weight:bold;font-size: 12px;'></p>
</div></div>""", "utf-8"))
            self.wfile.write(bytes("<div id='main_content'>", "utf-8"))
            __class__.startPrivKey = (__class__.num - 1) * 128+1
            __class__.random5H = __class__.RandomInteger(__class__.rndMin,__class__.hj)
            __class__.random5J = __class__.RandomInteger(__class__.hj,__class__.jk)
            __class__.random5K = __class__.RandomInteger(__class__.jk,__class__.rndMax)             
            __class__.randomKw = __class__.RandomInteger(__class__.rndMin,__class__.Kx)
            __class__.randomKx = __class__.RandomInteger(__class__.Kx,__class__.Ky)
            __class__.randomKy = __class__.RandomInteger(__class__.Ky,__class__.Kz)
            __class__.randomKz = __class__.RandomInteger(__class__.Kz,__class__.L1)            
            __class__.randomL1 = __class__.RandomInteger(__class__.L1,__class__.L2) 
            __class__.randomL2 = __class__.RandomInteger(__class__.L2,__class__.L3)
            __class__.randomL3 = __class__.RandomInteger(__class__.L3,__class__.L4)
            __class__.randomL4 = __class__.RandomInteger(__class__.L4,__class__.L5)
            __class__.randomL5 = __class__.RandomInteger(__class__.L5,__class__.rndMax)                                        
            self.wfile.write(bytes("<h3><span id='page_span'>Page #</span><span id='current_page'>" + str(__class__.num) + "</span><span id='out_of'><< out of >></span><span id='last_page'>904625697166532776746648320380374280100293470930272690489102837043110636675</span></h3>", "utf-8"))
            self.wfile.write(bytes("<pre>[&nbsp;<span class='ajax' page='/"+str(__class__.previous)+"'>previous</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.next)+"'>next</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.random)+"'>random</span>&nbsp;]&nbsp;&nbsp;&nbsp;<=>&nbsp;&nbsp;&nbsp;", "utf-8"))
            self.wfile.write(bytes("[&nbsp;<span class='ajax' page='/"+str(__class__.first)+"'>first</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.middle)+"'>middle</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.max)+"'>last</span>&nbsp;]</pre>", "utf-8"))           
            self.wfile.write(bytes("<pre>[&nbsp;<span class='ajax' page='/"+str(__class__.random5H)+"'>5H_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.random5J)+"'>5J_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.random5K)+"'>5K_random</span>&nbsp;]&nbsp;&nbsp;&nbsp;<=>&nbsp;&nbsp;&nbsp;", "utf-8"))
            self.wfile.write(bytes("[&nbsp;<span class='ajax' page='/"+str(__class__.randomKw)+"'>Kw_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.randomKx)+"'>Kx_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.randomKy)+"'>Ky_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.randomKz)+"'>Kz_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.randomL1)+"'>L1_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.randomL2)+"'>L2_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.randomL3)+"'>L3_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.randomL4)+"'>L4_random</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.randomL5)+"'>L5_random</span>&nbsp;]</pre>", "utf-8"))         
            __class__.starting_key_hex = hex((__class__.startPrivKey*Point_Coefficient)%N)[2:].zfill(64)
            if __class__.startPrivKey == 115792089237316195423570985008687907852837564279074904382605163141518161494273:
                __class__.ending_key_hex = hex((__class__.startPrivKey*Point_Coefficient+63*Point_Coefficient)%N)[2:].zfill(64)
            else:
                __class__.ending_key_hex = hex((__class__.startPrivKey*Point_Coefficient+127*Point_Coefficient)%N)[2:].zfill(64)
            self.wfile.write(bytes("<p class='key_hex'>*Starting Private Key Hex: " + str(__class__.starting_key_hex) + "</p>", "utf-8"))
            self.wfile.write(bytes("<p class='key_hex'>**Ending Private Key Hex: " + str(__class__.ending_key_hex) + "</p>", "utf-8"))
            self.wfile.write(bytes("<p id='balance' class='balance_on_page'>Balance on this Page: False</p>", "utf-8"))
            self.wfile.write(bytes("<pre><strong id='head_hex'>Private Key Hex</strong><strong id='head_wifu'>WIF Private Key Uncompressed</strong><strong id='head_legu'>Legacy Uncompressed Address</strong><strong id='head_legc'>Legacy Compressed Address</strong><strong id='head_p2sh'>Segwit P2SH Address</strong><strong id='head_p2wpkh'>Bech32 P2WPKH Address</strong><strong id='head_p2wsh'>Bech32 P2WSH Address</strong><strong id='head_wifc'>WIF Private Key Compressed</strong><br>", "utf-8"))
            for i in range(128):
                pub = ice.point_multiplication(__class__.startPrivKey,G).hex()
                dec = int((__class__.startPrivKey*Point_Coefficient)%N)
                __class__.privKey_C = ice.btc_pvk_to_wif(hex(dec)[2:].zfill(64))
                __class__.privKey = ice.btc_pvk_to_wif(hex(dec)[2:].zfill(64), False)
                __class__.bitAddr = ice.pubkey_to_address(0, False, bytes(bytearray.fromhex(pub)))
                __class__.bitAddr_C = ice.pubkey_to_address(0, True, bytes(bytearray.fromhex(pub)))
                addrP2sh = ice.privatekey_to_address(1, True, dec)
                addrbech32 = ice.privatekey_to_address(2, True, dec)
                addrbech32_p2wsh = bitcoinlib.keys.Address(ice.point_to_cpub(ice.point_multiplication(__class__.startPrivKey,G)),encoding='bech32',script_type='p2wsh').address               
                __class__.addresses.append(__class__.bitAddr)
                __class__.addresses.append(__class__.bitAddr_C)
                __class__.addresses.append(addrP2sh)
                __class__.addresses.append(addrbech32)
                __class__.addresses.append(addrbech32_p2wsh)
                __class__.starting_key_hex = hex((__class__.startPrivKey*Point_Coefficient)%N)[2:].zfill(64)                    
                if __class__.bitAddr == __class__.searchKey or __class__.bitAddr_C == __class__.searchKey:
                    self.wfile.write(bytes("<span class='data_hex' rel='popup1' style='font-weight:bold;' num='"+str(i+1)+"' value='"+__class__.starting_key_hex+"'>"+__class__.starting_key_hex+"</span><span class='data_wifu' style='color:#DE3163;'>" + __class__.privKey + "</span><span class='data_legu'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr + "'>" + __class__.bitAddr + "</a></span><span class='data_legc'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr_C + "'>" + __class__.bitAddr_C + "</a></span><span class='data_p2sh'><a target='_blank' href='https://bitaps.com/"+addrP2sh+"'>"+addrP2sh+"</a></span><span class='data_p2wpkh'><a target='_blank' href='https://bitaps.com/"+addrbech32+"'>"+addrbech32+"</a></span><span class='data_p2wsh'><a target='_blank' href='https://bitaps.com/"+addrbech32_p2wsh+"'>"+addrbech32_p2wsh+"</a></span><span class='data_wifc' style='color:#DE3163'>" + __class__.privKey_C + "</span></br>", "utf-8"))
                    __class__.searchKey = ""
                elif __class__.bitAddr == __class__.searchKey_U:
                    self.wfile.write(bytes("<span class='data_hex' rel='popup1' style='font-weight:bold;' num='"+str(i+1)+"' value='"+__class__.starting_key_hex+"'>"+__class__.starting_key_hex+"</span><span class='data_wifu' style='color:#DE3163;'>" + __class__.privKey + "</span><span class='data_legu'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr + "'>" + __class__.bitAddr + "</a></span><span class='data_legc'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr_C + "'>" + __class__.bitAddr_C + "</a></span><span class='data_p2sh'><a target='_blank' href='https://bitaps.com/"+addrP2sh+"'>"+addrP2sh+"</a></span><span class='data_p2wpkh'><a target='_blank' href='https://bitaps.com/"+addrbech32+"'>"+addrbech32+"</a></span><span class='data_p2wsh'><a target='_blank' href='https://bitaps.com/"+addrbech32_p2wsh+"'>"+addrbech32_p2wsh+"</a></span><span class='data_wifc' style='color:#DE3163'>" + __class__.privKey_C + "</span></br>", "utf-8"))
                    __class__.searchKey_U = ""
                elif  __class__.num == 452312848583266388373324160190187140050146735465136345244551418521555318338 and i == 31 or __class__.num == 452312848583266388373324160190187140050146735465136345244551418521555318338 and i == 32:
                    self.wfile.write(bytes("<span class='data_hex' rel='popup1' style='font-weight:bold;' num='"+str(i+1)+"' value='"+__class__.starting_key_hex+"'>"+__class__.starting_key_hex+"</span><span class='data_wifu'>" + __class__.privKey + "</span><span class='data_legu'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr + "'>" + __class__.bitAddr + "</a></span><span class='data_legc'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr_C + "'>" + __class__.bitAddr_C + "</a></span><span class='data_p2sh'><a target='_blank' href='https://bitaps.com/"+addrP2sh+"'>"+addrP2sh+"</a></span><span class='data_p2wpkh'><a target='_blank' href='https://bitaps.com/"+addrbech32+"'>"+addrbech32+"</a></span><span class='data_p2wsh'><a target='_blank' href='https://bitaps.com/"+addrbech32_p2wsh+"'>"+addrbech32_p2wsh+"</a></span><span class='data_wifc'>" + __class__.privKey_C + "</span></br>", "utf-8"))
                else:
                    self.wfile.write(bytes("<span class='data_hex' rel='popup1' num='"+str(i+1)+"' value='"+__class__.starting_key_hex+"'>"+__class__.starting_key_hex+"</span><span class='data_wifu'>" + __class__.privKey + "</span><span class='data_legu'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr + "'>" + __class__.bitAddr + "</a></span><span class='data_legc'><a target='_blank' href='https://bitaps.com/" + __class__.bitAddr_C + "'>" + __class__.bitAddr_C + "</a></span><span class='data_p2sh'><a target='_blank' href='https://bitaps.com/"+addrP2sh+"'>"+addrP2sh+"</a></span><span class='data_p2wpkh'><a target='_blank' href='https://bitaps.com/"+addrbech32+"'>"+addrbech32+"</a></span><span class='data_p2wsh'><a target='_blank' href='https://bitaps.com/"+addrbech32_p2wsh+"'>"+addrbech32_p2wsh+"</a></span><span class='data_wifc'>" + __class__.privKey_C + "</span></br>", "utf-8"))
                if __class__.startPrivKey == 115792089237316195423570985008687907852837564279074904382605163141518161494336:
                     break
                __class__.startPrivKey += 1
            for addr in __class__.addresses:
                if __class__.bloom.lookup_mm(addr):
                    __class__.balance_on_page = "True"
                    __class__.foundling += addr + " "
                    with open("found.txt", "a", encoding="utf-8") as f:
                        f.write(f"Bitcoin Address: {addr} Page# {__class__.num} \n")
            if __class__.balance_on_page == "True":
                mixer.init()
                mixer.music.load(found_sound)
                mixer.music.play()
            self.wfile.write(bytes("</pre><pre>[&nbsp;<span class='ajax' page='/"+str(__class__.previous)+"'>previous</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.next)+"'>next</span> | ", "utf-8"))
            self.wfile.write(bytes("<span class='ajax' page='/"+str(__class__.random)+"'>random</span>&nbsp;]", "utf-8"))
            self.wfile.write(bytes("</pre>", "utf-8"))
            self.wfile.write(bytes("<p class='balance_on_page'>Balance on this Page: " + __class__.balance_on_page + " " + __class__.foundling + "</p>", "utf-8"))
            self.wfile.write(bytes("<script>var elem = document.getElementById('balance');elem.innerHTML = 'Balance on this Page: " + __class__.balance_on_page + " " + __class__.foundling + "'</script>", "utf-8"))
            self.wfile.write(bytes("</div>", "utf-8"))
            self.wfile.write(bytes("""
<script>
$(document).on('click', '.ajax', function() { 
    var pnum = $(this).attr('page');
    pnum = pnum.substring(1);
    $.get("http://localhost:3333/A"+pnum, function(data, status){
        document.getElementById("main_content").innerHTML = data;
        history.pushState({}, null, "http://localhost:3333/"+pnum); 
    })
})                                                                                
$(function() {
    $('#up').click(function(){
        $('html,body').animate({scrollTop:0},400);
    });    
})
$(document).on('click', '.data_hex', function() {
    var path = window.location.pathname;
    if(path == '/904625697166532776746648320380374280100293470930272690489102837043110636675') { $('#all_num').html(64); } 
<<<<<<< HEAD:webserver_5.1.8.py
    else {$('#all_num').html(128);}          
=======
    else {$('#all_num').html(128);}
>>>>>>> 0e40d40430320b962152a19a28e10a9421261d87:webserver_5.1.7.py
    var val = $(this).attr('value');
    var num = $(this).attr('num');
    $('#arrow_num').html(num);
    var decNum = BigInt("0x"+val);
    $('#arrow_num').attr('dec', decNum);
    $.get("http://localhost:3333/!"+decNum, function(data, status){
        const myArray = data.split(" ");
        $('#fun2x').html('x: '+myArray[0]);
        $('#fun2y').html('y: '+myArray[1]);
        $('#fun3x').html('x: '+myArray[2]);
        $('#fun3y').html('y: '+myArray[3]);
        $('#fun4').html("U: " +myArray[4]+ "&nbsp;&nbsp;C: " +myArray[5]);
        if(myArray[6].length > 1) { $('#funbin').html(myArray[6]+"<br>("+myArray[6].length+" bits)"); }
        else { $('#funbin').html(myArray[6]+"<br>("+myArray[6].length+" bit)"); }
        $('#fun5').html('x: ' +myArray[7]);
        $('#addinvx').html('x: ' +myArray[8]);
        $('#addinvy').html('y: ' +myArray[9]);
        $('#addrinv').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[13]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[10]+"'>" +myArray[10]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[11]+"'>" +myArray[11]+"</a>");
        $('#addinvn').html(myArray[12]);
        $('#same1x').html('x: ' +myArray[14]);
        $('#same1y').html('y: ' +myArray[1]);
        $('#same1addr').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[17]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[15]+"'>" +myArray[15]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[16]+"'>" +myArray[16]+"</a>");
        $('#same2x').html('x: ' +myArray[18]);
        $('#same2y').html('y: ' +myArray[1]);
        $('#same2addr').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[21]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[19]+"'>" +myArray[19]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[20]+"'>" +myArray[20]+"</a>");
        $('#fun').html(myArray[22]);
        $('#funhex').html(myArray[23]);
        $('#same1n').html(myArray[24]);
        $('#same2n').html(myArray[25]);
        $('#addrinvpb').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[26]+"</span>&nbsp;&nbsp;P: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[27]+"'>" +myArray[27]+ "</a>&nbsp;&nbsp;B: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[28]+"'>" +myArray[28]+"</a>");
        $('#same1addrpb').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[29]+"</span>&nbsp;&nbsp;P: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[30]+"'>" +myArray[30]+ "</a>&nbsp;&nbsp;B: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[31]+"'>" +myArray[31]+"</a>");
        $('#same2addrpb').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[32]+"</span>&nbsp;&nbsp;P: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[33]+"'>" +myArray[33]+ "</a>&nbsp;&nbsp;B: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[34]+"'>" +myArray[34]+"</a>");
        $('#funaddr1').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[35]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[36]+"'>" +myArray[36]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[37]+"'>" +myArray[37]+"</a>");
        $('#funaddr2').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[38]+"</span>&nbsp;&nbsp;P: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[39]+"'>" +myArray[39]+ "</a>&nbsp;&nbsp;B: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[40]+"'>" +myArray[40]+"</a>");
    })            
    var popup_id = $('#' + $(this).attr('rel'));
    $(popup_id).show();
    $('.overlay_popup').show();
    $(this).attr('style',  'color:#DE3163;display:inline-block;width:450px;font-weight:bold;');
})
$(document).on('click', '.overlay_popup', function() {
    $('.overlay_popup, .popup').hide();
})
$(document).on('click', '#arrow_left', function() {
    var item_num = parseInt($('#arrow_num').html());
    if(item_num > 1) { 
        $('#arrow_num').html(item_num - 1);
        var decNum = $('#arrow_num').attr('dec');
        var bigNum = BigInt(decNum);
        var j = (bigNum - point_coefficient) % N
        if (j < 0) { j = j < 0n ? -j : j; j = N - j; }
        $.get("http://localhost:3333/!"+(j), function(data, status){
            const myArray = data.split(" ");
            $('#fun2x').html('x: '+myArray[0]);
            $('#fun2y').html('y: '+myArray[1]);
            $('#fun3x').html('x: '+myArray[2]);
            $('#fun3y').html('y: '+myArray[3]);
            $('#fun4').html("U: " +myArray[4]+ "&nbsp;&nbsp;C: " +myArray[5]);
            if(myArray[6].length > 1) { $('#funbin').html(myArray[6]+"<br>("+myArray[6].length+" bits)"); }
            else { $('#funbin').html(myArray[6]+"<br>("+myArray[6].length+" bit)"); }
            $('#fun5').html('x: ' +myArray[7]);
            $('#addinvx').html('x: ' +myArray[8]);
            $('#addinvy').html('y: ' +myArray[9]);
            $('#addrinv').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[13]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[10]+"'>" +myArray[10]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[11]+"'>" +myArray[11]+"</a>");
            $('#addinvn').html(myArray[12]);
            $('#same1x').html('x: ' +myArray[14]);
            $('#same1y').html('y: ' +myArray[1]);
            $('#same1addr').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[17]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[15]+"'>" +myArray[15]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[16]+"'>" +myArray[16]+"</a>");
            $('#same2x').html('x: ' +myArray[18]);
            $('#same2y').html('y: ' +myArray[1]);
            $('#same2addr').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[21]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[19]+"'>" +myArray[19]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[20]+"'>" +myArray[20]+"</a>");
            $('#fun').html(myArray[22]);
            $('#funhex').html(myArray[23]);
            $('#same1n').html(myArray[24]);
            $('#same2n').html(myArray[25]);
            $('#addrinvpb').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[26]+"</span>&nbsp;&nbsp;P: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[27]+"'>" +myArray[27]+ "</a>&nbsp;&nbsp;B: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[28]+"'>" +myArray[28]+"</a>");
            $('#same1addrpb').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[29]+"</span>&nbsp;&nbsp;P: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[30]+"'>" +myArray[30]+ "</a>&nbsp;&nbsp;B: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[31]+"'>" +myArray[31]+"</a>");
            $('#same2addrpb').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[32]+"</span>&nbsp;&nbsp;P: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[33]+"'>" +myArray[33]+ "</a>&nbsp;&nbsp;B: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[34]+"'>" +myArray[34]+"</a>");
            $('#funaddr1').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[35]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[36]+"'>" +myArray[36]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[37]+"'>" +myArray[37]+"</a>");
            $('#funaddr2').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[38]+"</span>&nbsp;&nbsp;P: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[39]+"'>" +myArray[39]+ "</a>&nbsp;&nbsp;B: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[40]+"'>" +myArray[40]+"</a>");
        })
        var j = (bigNum - point_coefficient) % N
        if (j < 0) { j = j < 0n ? -j : j; j = N - j;$('#arrow_num').attr('dec', j); }
        else { $('#arrow_num').attr('dec', (bigNum - point_coefficient) % N); }
        var set_style = parseInt($('#arrow_num').html());
        $('*[num="'+(set_style)+'"]').attr('style',  'color:#DE3163;display:inline-block;width:450px;font-weight:bold;');
        $('html, body').animate({scrollTop: $('*[num="'+(set_style)+'"]').offset().top}, 200); 
    }
    else { 
        $('#arrow_num').html(item_num); 
    }
})
$(document).on('click', '#arrow_right', function() {
    var last = 128;
    var path = window.location.pathname;
    if(path == '/904625697166532776746648320380374280100293470930272690489102837043110636675') { last = 64; $('#all_num').html(64); }
    var item_num = parseInt($('#arrow_num').html());
    if(item_num != last) { 
        $('#arrow_num').html(item_num + 1);
        var decNum = $('#arrow_num').attr('dec');
        var bigNum = BigInt(decNum);
        $.get("http://localhost:3333/!"+((bigNum + point_coefficient) % N), function(data, status){
            const myArray = data.split(" ");
            $('#fun2x').html('x: '+myArray[0]);
            $('#fun2y').html('y: '+myArray[1]);
            $('#fun3x').html('x: '+myArray[2]);
            $('#fun3y').html('y: '+myArray[3]);
            $('#fun4').html("U: " +myArray[4]+ "&nbsp;&nbsp;C: " +myArray[5]);
            if(myArray[6].length > 1) { $('#funbin').html(myArray[6]+"<br>("+myArray[6].length+" bits)"); }
            else { $('#funbin').html(myArray[6]+"<br>("+myArray[6].length+" bit)"); }
            $('#fun5').html('x: ' +myArray[7]);
            $('#addinvx').html('x: ' +myArray[8]);
            $('#addinvy').html('y: ' +myArray[9]);
            $('#addrinv').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[13]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[10]+"'>" +myArray[10]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[11]+"'>" +myArray[11]+"</a>");
            $('#addinvn').html(myArray[12]);
            $('#same1x').html('x: ' +myArray[14]);
            $('#same1y').html('y: ' +myArray[1]);
            $('#same1addr').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[17]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[15]+"'>" +myArray[15]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[16]+"'>" +myArray[16]+"</a>");
            $('#same2x').html('x: ' +myArray[18]);
            $('#same2y').html('y: ' +myArray[1]);
            $('#same2addr').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[21]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[19]+"'>" +myArray[19]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[20]+"'>" +myArray[20]+"</a>");
            $('#fun').html(myArray[22]);
            $('#funhex').html(myArray[23]);
            $('#same1n').html(myArray[24]);
            $('#same2n').html(myArray[25]);
            $('#addrinvpb').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[26]+"</span>&nbsp;&nbsp;P: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[27]+"'>" +myArray[27]+ "</a>&nbsp;&nbsp;B: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[28]+"'>" +myArray[28]+"</a>");
            $('#same1addrpb').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[29]+"</span>&nbsp;&nbsp;P: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[30]+"'>" +myArray[30]+ "</a>&nbsp;&nbsp;B: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[31]+"'>" +myArray[31]+"</a>");
            $('#same2addrpb').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[32]+"</span>&nbsp;&nbsp;P: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[33]+"'>" +myArray[33]+ "</a>&nbsp;&nbsp;B: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[34]+"'>" +myArray[34]+"</a>");
            $('#funaddr1').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[35]+"</span>&nbsp;&nbsp;U: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[36]+"'>" +myArray[36]+ "</a>&nbsp;&nbsp;C: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[37]+"'>" +myArray[37]+"</a>");
            $('#funaddr2').html("<span style='color:brown;font-weight:bold;'>B:"+myArray[38]+"</span>&nbsp;&nbsp;P: <a target='_blank'  href='https://www.blockchain.com/btc/address/"+myArray[39]+"'>" +myArray[39]+ "</a>&nbsp;&nbsp;B: <a target='_blank' href='https://www.blockchain.com/btc/address/"+myArray[40]+"'>" +myArray[40]+"</a>");
        })
        $('#arrow_num').attr('dec', (bigNum + point_coefficient) % N);
        var set_style = parseInt($('#arrow_num').html());
        $('*[num="'+(set_style)+'"]').attr('style',  'color:#DE3163;display:inline-block;width:450px;font-weight:bold;');
        $('html, body').animate({scrollTop: $('*[num="'+(set_style)+'"]').offset().top}, 200);
    }
    else { 
        $('#arrow_num').html(last); 
    }
})
</script>""", "utf-8"))
            __class__.addresses.clear()        
            __class__.balance_on_page = "False"
            __class__.foundling = ""
            self.wfile.write(bytes("<button id='up'>&#x2191&#x2191&#x2191</button>", "utf-8"))             
            self.wfile.write(bytes("</body></html>", "utf-8"))

if __name__ == "__main__":
    now = datetime.now()
    time = now.strftime("%H:%M:%S")    
    webServer = HTTPServer((hostName, serverPort), WebServer)
    print(f"[{time}] Server started at http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
