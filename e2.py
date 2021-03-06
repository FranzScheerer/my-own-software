import math, hashlib, random
# must be of the form 4k + 3 = 4(k+1) - 1
# prime from NIST
#prime = 2**256 - 2**224 + 2**192 + 2**96 - 1
prime = 115792089237316195423570985008687907853269984665640564039457584007913130018587
#  n_ = 115792089210356248762697446949407573529996955224135760342422259061068512044369
n_ = prime + 1
a = prime - 31
c = 17
y0 = 0
 
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

def gcd(a,b):
  if b > a:
    a,b = b,a
  while b > 0:
    a,b = b,a % b
  return a

def nextPrime(p):
 while p % 8 != 3:
   p = p + 1
 return nextPrime_odd(p)

def nextPrime_odd(p):
  m_ = 3*5*7*11*13*17*19*23*29
  while True:
    while gcd(p,m_) != 1:
      p = p + 8 
    q = (p+1)/4
    if (pow(2,p-1,p) != 1 or pow(2,q-1,q) != 1):
       p = p + 8
       continue
    if (pow(3,p-1,p) != 1 or pow(3,q-1,q) != 1):
       p = p + 8
       continue
    if (pow(5,p-1,p) != 1 or pow(5,q-1,q) != 1):
       p = p + 8
       continue
    if (pow(17,p-1,p) != 1 or pow(17,q-1,q) != 1):
       p = p + 8
       continue
    break
  return p

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

def E(m, key, prime):
  return pow(m, key, prime)

def D(c, key, prime):
  key = inv(key, prime - 1)
  return pow(c, key, prime)

def hextxt2num(x):
  res = 0
  for c in x:
    if ord(c) < 58 and ord(c) >= 48:
       res = (res<<4) + ord(c) - 48
    elif ord(c) <= ord('f') and ord(c) >= ord('a'):
       res = (res<<4) + ord(c) - 87
  return res

bhex = "5ac635d8 aa3a93e7 b3ebbd55 769886bc 651d06b0 cc53b0f6 3bce3c3e 27d2604b" 
b = hextxt2num(bhex)
#prime = nextPrime(2**500)
b = 0
def code2num(x):
  res = 0
  for c in x:
     if ord(c) >= 48 and ord(c) < 58:
       res = (res << 6) + ord(c) - 48
     if ord(c) >= 65 and ord(c) < 91:
       res = (res << 6) + ord(c) - 55
     if ord(c) >= 97 and ord(c) < 123:
       res = (res << 6) + ord(c) - 61
     if c == '#': 
       res = (res << 6) + 62
     if c == '/': 
       res = (res << 6) + 63
  return res

def num2code(x):
  res = ''
  while x > 0:
    y = x % 64
    if y < 10:
       res = chr( y + 48 ) + res
    elif y < 36:
       res = chr( y + 55 ) + res
    elif y < 62:
       res = chr( y + 61 ) + res 
    elif y == 62:
       res = '#' + res 
    elif y == 63:
       res = '/' + res 
    x /= 64
  return res


def h(x):
  dx1 = hashlib.md5(x).digest()
  dx2 = hashlib.md5(x+x).digest()
  res = 0
  for cx in (dx1+dx2):
    res = (res<<8) ^ ord(cx)
  return res

def random256():
  md = hashlib.sha256("RANDOM-SEED_X")
  md.update('large key value for generation of random number')
  md.update( str(random.random()) )
  md.update( str(random.random()) )
  result = 0
  largestr = md.digest()
  for i in range(len(largestr)):
      result = (result << 8) ^ ord(largestr[i])
  return result

def genP(x,a,b):
   if (4*a*a*a + 27*b*b) % prime == 0:
      b = b + 1
   while pow(c*x**3 + a*x + b, (prime - 1)/2, prime) != 1:
     x = x + 1
   y = pow(c*x**3 + a*x + b, (prime + 1)/4, prime)
   return [x % prime, (y+y0) % prime]

def dpoint(P):
  x = P[0]
  y = P[1] - y0
  s = ((3*c*(x**2) + a) * inv(2*y, prime)) % prime
  xr = (cinv*s**2 - 2*x) % prime
  yr = (-y + s * (x-xr) + y0) % prime
  return [xr , yr]

def addP(P,Q):
  if P == Q:
    return dpoint(P)
  x1 = P[0]
  x2 = Q[0]
  y1 = P[1] - y0
  y2 = Q[1] - y0
  while x1 < x2:
     x1 = x1 + prime
  while y1 < y2:
     y1 = y1 + prime
  s = ((y1-y2) * inv(x1-x2, prime)) % prime
  xr = cinv*s**2 - x1 - x2
  yr = s * (x1-xr) - y1 + y0
  return [xr % prime, yr % prime]

def mulP(P,n):
  isFirst = True
  resP = P
  if n < 0:
    resP[1] = prime - resP[1]
    n = (-1)*n 
  bsize = 20
  while 2**bsize < n:
     bsize = bsize + 1
  PP = resP
  for b in range(bsize + 1):
     if (n & (1 << b) != 0):   
         if isFirst:
            resP = PP
            isFirst = False
         else:
            resP = addP(resP,PP)
     PP = dpoint(PP) 
  return resP

def signSchnorr(G,m,x):
  k = random256()
  R = mulP(G,k)
  e = h(str(R[0]) + m)
  return [k - x*e, e]

def verifySchnorr(G,s,Y,e,m):
  return e == h(str(addP(mulP(G,s),mulP(Y,e))[0]) + m)


# x-value of the starting point  
x = a + 17

# The starting point which is added many times to itself 
P = genP(x,a,b)
cinv = inv(c, prime)
#Q = P = [2,2]
#for xx in range(10):
#  if mulP(P,xx+2) == P: 
#    print "ERROR ", xx

# mulP(P,n_) to test mulP(P,b_) is infty :)

f = open('e2.py','r')
message = f.read()
x = 1234
y = mulP(P,x)
f.close()

sig = signSchnorr(P, message, x)

print "Schnorr's signature: ", sig
print "The verification of Schnorr's signature ", verifySchnorr(P, sig[0], y, sig[1], message)

# The public keys
privAlice = 85743857348573489891704994859049170499485904
privBob = 455457456346534563457893499994859049170499485904*1111
# We calulate the public keys
pubkAlice = mulP(P, privAlice)
print "Public Key from Alice \n", pubkAlice  
pubkBob = mulP(P, privBob)
print "Public Key from Bob \n", pubkBob  

shareBob   = mulP(pubkAlice, privBob)
shareAlice = mulP(pubkBob, privAlice)

print "\n\nThe shared key as calculated from Alice\n", shareAlice 

print "\n\n"
print "Verification: Are the shared keys equal? ", shareAlice == shareBob

key = 12344567
ikey = inv( key, prime + 1 )
Pm = mulP(pubkAlice, h('Karo Ass'))
print "encrypt/decrypt test: ", mulP(mulP(Pm, key),ikey) == Pm
# test Schnorr Identifikacation
G = Pm
x=1231234354545645
y = mulP(G,x)
e = 8878578945748989578
k = 5849547584657846777
r = mulP(G,k)
s = (k + e*x) % n_
print " Schnorr-Identifikation: test ... ", mulP(G, s) == addP(r,mulP(y,e))
#
# Die Primzahl von Hans Riesel ;)
#
p = 2**3217 - 1
k = 1785968598548549*2**80 + 1
k_inv = inv(k, prime + 1)
kk = 1777777777777*2**99 + 1
kk_inv = inv(kk, prime + 1)

print "The secret ... ", k,kk
m = "Secret message from Bob to Alice"
print "Message: ", m

number = bin2num(m)
print "Message converted to a number: \n", number
x = number
if pow (c*x**3 + a*x, (prime-1)/2, prime) != 1:
  x = prime - x
P_ = [x, pow (c*x**3 + a*x, (prime+1)/4, prime)]
e_ = mulP(P_,k)
print "\n encrypted point is sent to Alice\n", e_
ee_ = mulP(e_,kk)
print "\n Point sent to Bob, encrypted twice\n", ee_
d1 = mulP(ee_,k_inv)
print "\n Single encrypted point is send to Alice: \n", d1
mm = mulP(d1, kk_inv)[0]
if mm > (prime+1)/2:
  mm = prime - mm
mm = num2bin(mm)
print "\n Encrypred by Alice: ", mm

print "Does it work, is mm = m? ", mm == m
