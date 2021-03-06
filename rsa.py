#238b754103cae5c695164710719d3e0ffbc6fec67d6c2f3158d0d16935cfb1dda6f97c3e43d7b8bc26e0dc238320a56883df334ef60d35ff3a63f1bba607f04eb60c3f4400b6358f4b7753512a7677567436cfd622a9312ce1f1f0737113fe905eebe99faaa5d106282a1483c017d8d095b3d1b64979a88798fad8bf69278bafc4b0a9056af55284cba8c7b069139918814c893764836582ec76f374fe3b30a523414bb158a53198292eee0497748f8a9cea490ccc507c15c39b0c85b11794cc6679bc845a18fc253cfa066f14ff9c4b59ece0fdc35edf7d0e9c16274cd58530767ee81ff753ffd70d42bee285674ff3a1623acc9f4c80c7812e3d5b33bca09
import random, hashlib, sys

nrsa = 378922943703416474947928969264028101081244532593163128779113280000695502368522842323214207098737569552266709775501455739872485802463471077267530862634002298886073434547797214795222991372258936705287453862117361661422211113858103209923233881656197316247097851837892085055931104229902135242018973464737658437809683715221546549427607858965173900781538062090819670897686110103859527757357827744430547307677377747685387737194581122257788862637431062201061835959153001407281406626560395359818688203422258782964844312816750530133952004565271534082715244306967752247864802374734006415998027988324634159517536216527230497869L

def bin2num(x):
  res = 0
  for c in x:
    res = (res<<8) ^ ord(c)
  return res

def num2bin(x):
  res = ''
  while x > 0:
    res = chr(x % 256) + res
    x /= 256
  return res

def digital2num(x):
  res = 0
  for c in x:
    if ord(c) >= 48 and ord(c) <= 57:
      res = (res*10) + ord(c) - 48
  return res

def hextxt2num(x):
  res = 0
  for c in x:
    if ord(c) < 58 and ord(c) >= 48:
       res = (res<<4) + ord(c) - 48
    elif ord(c) <= ord('f') and ord(c) >= ord('a'):
       res = (res<<4) + ord(c) - 87
  return res

def num2hextxt(x):
  res = ''
  h__ = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
  while x > 0:
    res = h__[x % 16] + res
    x /= 16
  return res

def gcd(a,b):
  if b > a:
    a,b = b,a
  while b > 0:
    a,b = b,a % b
  return a

def issmooth(n,m):
  g = gcd(n,m)
  while True:
    n = n / g
    g = gcd(n,m)
    if g == 1:
      break
  return n == 1

def pp(x):
 i = ii = 1
 while i < x:
   i = i + 1
   if gcd(ii,i) == 1:
     ii = i * ii
 return ii
 
def nextPrime(p):
 if p % 2 == 0:
   p = p + 1
 return nextPrime_odd(p)

def nextPrime_odd(p):
  m_ = 3*5*7*11*13*17*19*23*29
  while gcd(p,m_) != 1:
    p = p + 2 
  if (pow(2,p-1,p) != 1):
      return nextPrime_odd(p + 2)
  if (pow(3,p-1,p) != 1):
      return nextPrime_odd(p + 2)
  if (pow(5,p-1,p) != 1):
      return nextPrime_odd(p + 2)
  if (pow(17,p-1,p) != 1):
      return nextPrime_odd(p + 2)
  return p
  
def writeNumber(number, fnam):
  f = open(fnam, 'wb')
  n = number
  while n > 0:
    byte = n % 256
    n = n / 256
    f.write(chr(byte))
  f.close()

def readNumber(fnam):
  f = open(fnam, 'rb')
  n = 0
  snum = f.read()
  for i in range(len(snum)):
    n = (n << 8) ^ ord(snum[len(snum)-i-1])   
  f.close()
  return n

def random512():
  md = hashlib.sha512("RANDOM-SEED")
  md.update('large key value for generation of random number')
  md.update( str(random.random()) )
  md.update( str(random.random()) )
  result = 0
  largestr = md.digest()
  for i in range(len(largestr)):
      result = (result << 8) ^ ord(largestr[i])
  return result

def random1024():
  return random512() * random512()

def h(x):
  dx1 = hashlib.sha512(x).digest()
  dx2 = hashlib.sha512(dx1+x).digest()
  dx3 = hashlib.sha512(x+dx2).digest()
  dx4 = hashlib.sha512(x+dx3).digest()
  dx5 = hashlib.sha512(x+dx4).digest()
  res = 0
  for cx in (dx1+dx2+dx3+dx4+dx5):
    res = (res<<8) ^ ord(cx)
  return res % (nrsa)

def hF(fnam):
  f = open(fnam,'r')
  return h(f.read())

def sF(fnam):
  f = open(fnam,'r')
  s = pow (h(f.read()), readNumber('gxxx'), nrsa)
  f.close()
  return s

def vF(fnam,s):
  f = open(fnam,'r')
  return  h(f.read()) == pow (s, rsa129, nrsa)
 
def inv(b,m):
  s = 0
  t = 1
  a = m
  while b != 1:
    q = a/b
    aa = b
    b = a % b
    a = aa
    ss = t
    t = s - q*t
    s = ss
  if t < 0:
    t = t + m
  return t

# My public key
#>>> readNumber('n')
n = 132158664968768490782960847799015406036650767779277459921379897867566679587724524521987896737725523269165395751923267303738641975289767617733673183719848122664620561025225091299282924584871878765772994798839194882625865916048662867255808940326382392925259371837094024054492616735167070129273991602554868281260403078931758978042320828712406521136768937860224472073584018384229887268232999555522044285586888065207215194190028245326972822338830044710482833241494104291299248101801097861695990218731328867880865825220780717582330616093628187888772860304794060649785037872959663106341572544892592180043533578078543073813L
#>>> readNumber('e')
e = 3705065645512927316321462305254520982876035314505654008283722719433928258945868606816193707934157371759177881042853386436215164383893639793003538863209251L
#>>> 
rsa129 = 114381625757888867669235779976146612010218296721242362562561842935706935245733897830597123563958705058989075147599290026879543541
p1 = 3490529510847650949147849619903898133417764638493387843990820577
p2 = 32769132993266709549961988190834461413177642967992942539798288533


print "\n\n rsacrypt - copyright Scheerer Software 2017 - all rights reserved\n\n"
print "First parameter is V,S,E or D\n\n"
print "\n\n verify signature (3 parameters):"
print "   > python rsacrypt.py V <filename> <digital signature> "

print " create signature S (2 parameter):"
print "   > python rsacrypt.py S <filename> \n\n"
print " encrypt E (2 parameter):"
print "   > python rsacrypt.py E <text> \n\n"
print " decrypt D (2 parameter):"
print "   > python rsacrypt.py D <bigInteger> \n\n"

print " number of parameters is " + str(len(sys.argv)-1)
print " "
print " "

if len(sys.argv) == 3 and sys.argv[1] == "E":
  print "encrypted text: \n" + str (pow(bin2num(sys.argv[2]), rsa129, nrsa))

if len(sys.argv) == 3 and sys.argv[1] == "D":
  print " decrypt text:\n " + num2bin(pow (digital2num(sys.argv[2]),readNumber('gxxx'),nrsa)) 

if  len(sys.argv) == 4 and sys.argv[1] == "V":
  print "result of verification: " + str(vF(sys.argv[2], hextxt2num(sys.argv[3])))

if len(sys.argv) == 3 and sys.argv[1] == "S":
  print " digital signature:\n " + num2hextxt(sF(sys.argv[2]))
     
