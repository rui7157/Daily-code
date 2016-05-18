# -*- coding: utf-8 -*-
"""
rsakey.py
新浪微博提交数据时的签名类RSAKey:(PC端js方法转为python)
"""
import time
import math
import random

"""
#28 represents the user_agent 
if (c && navigator.appName == "Microsoft Internet Explorer") {
d.prototype.am = g;
a = 30
} else if (c && navigator.appName != "Netscape") {
d.prototype.am = f;
a = 26
} else {
d.prototype.am = h;
a = 28
}
d.prototype.DB = a;
d.prototype.DM = (1 << a) - 1;
d.prototype.DV = 1 << a
var i = 52;
d.prototype.FV = Math.pow(2, i);
d.prototype.F1 = i - a;
d.prototype.F2 = 2 * a - i;
"""
DB = 28
DM = (1 << DB) -1
DV = 1 << DB
I = 52
FV = 2**I
F1 = I - DB
F2 = 2*DB - I
bc = None
bb, bc, bd, be, bh = 256,None,[],0,0
while be < bb:
  """
  bh = Math.floor(65536 * Math.random());
  bd[be++] = bh >>> 8;
  bd[be++] = bh & 255"""
  bh = int(math.floor(random.random() * 65536))
  bd.append(bh >> 8)
  be += 1
  bd.append(bh & 0xff)
  be += 1
be = 0
"""
function bg() {
bf((new Date).getTime())
}
function bf(a) {
bd[be++] ^= a & 255;
bd[be++] ^= a >> 8 & 255;
bd[be++] ^= a >> 16 & 255;
bd[be++] ^= a >> 24 & 255;
be >= bb && (be -= bb)
}"""
def bg():
  global bd,be,be,bb
  t = int(time.time() * 1000)
  bd[be] ^= t & 255
  be += 1
  bd[be] ^= t >> 8 & 255
  be += 1
  bd[be] ^= t >> 16 & 255
  be += 1
  bd[be] ^= t >> 24 & 255
  be += 1
  if be >= bb:
    be -= bb
bg()
e = int('10001',16)


class RSAKey():
  def __init__(self):
    #this.n=null;this.e=0;this.d=null;this.p=null;this.q=null;this.dmp1=null;this.dmq1=null;this.coeff=null
    this = self
    this.n = None
    this.e = 0
    this.d = None
    this.p = None
    this.q = None
    this.dmp1 = None
    this.dmq1 = None
    this.coeff = None

  def doPublic(self,a):
    #function bs(a){return a.modPowInt(this.e,this.n)}
    this = self
    return a.modPowInt(this.e, this.n)


  def setPublic(self,a,b):
    #"function br(a,b){if(a!=null&&b!=null&&a.length>0&&b.length>0){this.n=bm(a,16);this.e=parseInt(b,16)}else alert("Invalid RSA publickey")}"
    this = self
    if a is not None and len(a) > 0 and len(b) > 0:
      pubkey_dict, t, s = encryptpk_fromstring(a,16)
      this.n = E(pubkey_dict, t, s)
      this.e = int(b,16)
      return this
    else:
      print "Invalid RSA publickey"
      return None
      

  def encrypt(self,a,**kwargs):
    global bb,bc,bd,be
    bb = kwargs['bb'] if kwargs.has_key('bb') else bb
    bc = kwargs['bc'] if kwargs.has_key('bc') else bc
    bd = kwargs['bd'] if kwargs.has_key('bd') else bd
    be = kwargs['be'] if kwargs.has_key('be') else be
    """var b = bp(a, this.n.bitLength() + 7 >> 3);
    if (b == null )
      return null ;
    var c = this.doPublic(b);
    if (c == null )
      return null ;
    var d = c.toString(16);
    return (d.length & 1) == 0 ? d : "0" + d
    """
    def bp(a,b):
      if b < len(a) + 11:
        print "Message too long for RSA"
        return None
      c,e = [0] * b,len(a)-1
      while e>=0 and b>0:
        """var f = a.charCodeAt(e--);"""
        f = ord(a[e])
        e -= 1
        if f < 128:
          """c[--b] = f;"""
          b -= 1
          c[b] = f
        elif f > 127 and f < 2048:
          """c[--b] = f & 63 | 128;
          c[--b] = f >> 6 | 192"""
          b -= 1
          c[b] = f & 63 | 128
          b -= 1
          c[b] = f >> 6 | 192
        else:
          """c[--b] = f & 63 | 128;
          c[--b] = f >> 6 & 63 | 128;
          c[--b] = f >> 12 | 224"""
          b -= 1
          c[b] = f & 63 | 128
          b -= 1
          c[b] = f >> 6 & 63 | 128
          b -= 1
          c[b] = f >> 12 | 224
      #end of the loop
      b -= 1
      c[b] = 0
      g,h = Z(),[0]
      while b > 2:
        h[0] = 0
        while h[0] == 0:
          nextbytes(h)
        b -= 1
        c[b] = h[0]
      b -= 1
      c[b] = 2
      b -= 1
      c[b] = 0
      dict, t, s = encryptpk_fromstring(c,256)
      return E(dict, t, s)
    this = self
    b = bp(a, self.n.bit_length() + 7 >> 3)
    if b is None:
      return None
    c = this.doPublic(b)
    if c is None:
      return None
    d = c.toString(16)
    return d if (len(d) & 1) == 0 else "0"+d

class E:
  def __init__(self, pubkey_dict=None, t=0, s=0):
      self.array = pubkey_dict
      self.t = t
      self.s = s

  def __getitem__(self, key):
    if type(key) == int and self.array is not None:
      return self.array[key]
    return None

  def __setitem__(self, key, value):
    if type(key) == int and self.array is not None:
      self.array[key] = value
    elif type(key) == int and self.array is None:
      self.array = {}
      self.array[key] = value
    else:
      raise Exception('an error occured in __setitem__ with key:%s and value:%s' % (key,value))
  
  def toString(self,a):
    def n(i):
      str = "0123456789abcdefghijklmnopqrstuvwxyz"
      try:
        return str[i]
      except:
        return ""
    this = self
    if this.s < 0:
      return "-" + this.negate().toString(a)
    b = math.log(a,2)
    if b.is_integer() and int(b) in (1,2,3,4,5):
      b = int(b)
    c = (1 << b) - 1
    e = False
    f = ""
    g = this.t
    h = DB - g * DB % b
    d = None
    if g-1 > 0:
      g -= 1
      d = this[g] >> h
      if h < DB and d > 0:
        e = True
        f = n(d)
      while g >= 0:
        if h < b:
          """d = (this[g] & (1 << h) - 1) << b - h;"""
          """d |= this[--g] >> (h += this.DB - b)"""
          d = (this[g] & (1 << h) - 1) << b -h
          g -= 1
          h += DB -b
          d |= this[g] >> h
        else:
          """d = this[g] >> (h -= b) & c;"""
          h -= b
          d = this[g] >> h & c
          if h <= 0:
            h += DB
            g -= 1
        """d > 0 && (e = !0);e && (f += n(d))"""
        e = True if d > 0 else e
        f += n(d) if e else f
    return f if e else "0" 

  def y(self,a):
    b,c=1,None
    c = a >> 16
    if c != 0:
      a = c
      b += 16
    c = a >> 8
    if c != 0:
      a = c
      b += 8
    c = a >> 4
    if c != 0:
      a = c
      b += 4
    c = a >> 2
    if c != 0:
      a = c
      b += 2
    c = a >> 1
    if c != 0:
      a = c
      b += 1
    return b

  def bit_length(self):
    return 0 if self.t <= 0 else DB * (self.t-1) + self.y(self[self.t-1] ^ self.s & DM)

  def abs(self):
    this = self
    return this.negate() if this.s < 0 else this

  def negate(self):
    a = E()
    E.ZERO.subTo(self,a)
    return a

  def subTo(self,a,b):
    this = self
    #a=>an instance of E,b=>another instance of E
    c,d,e = 0,0,min(a.t,this.t)
    while c < e:
      d += this[c] - a[c]
      b[c] = d & DM
      c += 1
      d >>= DB
    if a.t < this.t:
      d -= a.s
      while c < this.t:
        d += this[c]
        b[c] = d & DM
        c += 1
        d >>= DB
      d += this.s
    else:
      d += this.s
      while c < a.t:
        d -= a[c]
        b[c] = d & DM
        c += 1
        d >>= DB
      d -= a.s
    """
    b.s = d < 0 ? -1 : 0;
    d < -1 ? b[c++] = this.DV + d : d > 0 && (b[c++] = d);
    b.t = c;
    b.clamp()
    """
    b.s = -1 if d < 0 else 0
    if d < -1:
      b[c] = DV + d
      c += 1
    elif d > 0:
      b[c] = d
      c += 1
    b.t = c
    b.clamp()

  def clamp(self):
    this = self
    a = this.s & DM
    while this.t > 0 and this[this.t - 1] == a:
      this.t -= 1

  def copyTo(self,a):
    this = self
    for b in range(this.t - 1, -1, -1):
      a[b] = this[b]
    a.t = this.t
    a.s = this.s

  def squareTo(self,a):
    this = self
    b = this.abs()
    c = a.t = 2 * b.t
    while c-1 >= 0:
      c -= 1
      a[c] = 0
    for i in range(0, b.t-1):
      d = b.am(i, b[i], a, 2 * i, 0, 1)
      """if ((a[i + b.t] += b.am(i + 1, 2 * b[i], a, 2 * i + 1, d, b.t - i - 1)) >= b.DV) {"""
      a[i+b.t] += b.am(i+1, 2 * b[i], a, 2*i+1, d, b.t-i-1)
      if a[i+b.t] >= DV:
        """a[i + b.t] -= b.DV;a[i + b.t + 1] = 1"""
        a[i+b.t] -= DV
        a[i+b.t+1] = 1
    """a.t > 0 && (a[a.t - 1] += b.am(c, b[c], a, 2 * c, 0, 1));"""
    c = b.t - 1# c == 36
    if a.t > 0:
      a[a.t-1] += b.am(c, b[c], a, 2*c, 0, 1)
    a.s = 0
    a.clamp()

  def am(self,a, b, c, d, e, f):
    this = self
    g = b & 16383
    h = b >> 14
    while f-1 >= 0:
      f -= 1
      i,j = this[a] & 16383, this[a] >> 14
      k = h * i + j * g
      a += 1
      """i = g * i + ((k & 16383) << 14) + c[d] + e;
        e = (i >> 28) + (k >> 14) + h * j;
        c[d++] = i & 268435455
      """
      i = g * i + ((k & 16383) << 14) + c[d] + e
      e = (i >> 28) + (k >> 14) + h * j
      c[d] = i & 268435455
      d += 1
    return e

  def multiplyTo(self,a,b):
    """
    function F(a, b) {
      var c = this.abs(),
      e = a.abs(),
      f = c.t;
      b.t = f + e.t;
      while (--f >= 0)
        b[f] = 0;
      for (f = 0; f < e.t; ++f)
        b[f + c.t] = c.am(0, e[f], b, f, 0, c.t);
      b.s = 0;
      b.clamp();
      this.s != a.s && d.ZERO.subTo(b, b)
    }"""
    this = self
    c,e = this.abs(),a.abs()
    f = c.t
    b.t = f + e.t
    while f-1 >= 0:
      f -= 1
      b[f] = 0
    for i in range(0,e.t):
      b[i + c.t] = c.am(0, e[i], b, i, 0, c.t)
    b.s = 0
    b.clamp()
    if this.s != a.s:
      E.ZERO.subTo(b,b)
  
  def mod(self,a):
    this = self
    b = E()
    this.abs().divRemTo(a, None, b)
    this.s < 0 and b.compareTo(E.ZERO) > 0 and a.subTo(b,b) 
    
  def compareTo(self,a):
    this = self
    b = this.s - a.s
    if b != 0:
      return b
    c = this.t
    b = c - a.t
    if b != 0:
      return b
    while c-1 >= 0:
      c -= 1
      b = this[c] - a[c]
      if b != 0:
        return b
    return 0

  def divRemTo(self, a, b, c):
    this = self
    f = a.abs()
    if not f.t <= 0:
      g = this.abs()
      if g.t < f.t:
        b != None and b.fromInt(0)
        c != None and this.copyTo(c)
        return
      if c == None:
        c = E()
      h,i,j,k = E(), this.s, a.s, DB-self.y(f[f.t - 1])
      if k > 0:
        f.lShiftTo(k, h)
        g.lShiftTo(k, c)
      else:
        f.copyTo(h)
        g.copyTo(c)
      l = h.t
      m = h[l - 1]
      if m == 0:
        return
      """var n = m * (1 << this.F1) + (l > 1 ? h[l - 2] >> this.F2 : 0),
        o = this.FV / n,
          p = (1 << this.F1) / n,
            q = 1 << this.F2,
              r = c.t,
                s = r - l,
                  t = b == null ? e() : b;"""
      n = m * (1 << F1) + (h[l - 2] >> F2 if l > 1 else 0)
      o = FV / float(n)
      p = (1 << F1) / float(n)
      q = 1 << F2
      r = c.t
      s = r - l
      t = E() if b == None else b
      h.dlShiftTo(s, t)
      if c.compareTo(t) >= 0:
        c[c.t] = 1
        c.t += 1
        c.subTo(t, c)
      E.ONE.dlShiftTo(l, t)
      t.subTo(h, h)
      while h.t < l:
        h[h.t] = 0
        h.t += 1
      while s-1 >= 0:
        s -= 1
        """var u = c[--r] == m ? this.DM : Math.floor(c[r] * o + (c[r - 1] + q) * p);"""
        r -= 1
        u = DM if c[r] == m else int(c[r] * o + p * (c[r - 1] + q))
        """if ((c[r] += h.am(0, u, c, s, 0, l)) < u) {"""
        c[r] += h.am(0, u, c, s, 0, l)
        if c[r] < u:
          """h.dlShiftTo(s, t);c.subTo(t, c);while (c[r] < --u)c.subTo(t, c)"""
          h.dlShiftTo(s,t)
          c.subTo(t,c)
          while c[r] < u - 1:
            u -= 1
            c.subTo(t,c)
      if b != None:
        c.drShiftTo(l, b)
        i != j and E.ZERO.subTo(b, b)
      """c.t = l;c.clamp();k > 0 && c.rShiftTo(k, c);i < 0 && d.ZERO.subTo(c, c)"""
      c.t = l
      c.clamp()
      k > 0 and c.rShiftTo(k, c)
      i < 0 and E.ZERO.subTo(c, c)
  
  def dlShiftTo(self, a, b):
    this = self
    for i in range(this.t - 1, -1, -1):
      b[i + a] = this[i]
    for j in range(a - 1, -1, -1):
      b[j] = 0
    b.t = this.t + a
    b.s = this.s

  def drShiftTo(self, a, b):
    this = self
    for i in range(a, this.t):
      b[i - a] = this[i]
    b.t = max(this.t - a, 0)
    b.s = this.s

  def lShiftTo(self, a, b):
    """
    var c = a % this.DB, d = this.DB - c, e = (1 << d) - 1, f = Math.floor(a / this.DB), g = this.s << c & this.DM, h;
    for (h = this.t - 1; h >= 0; --h) {
      b[h + f + 1] = this[h] >> d | g;
      g = (this[h] & e) << c
    }
    for (h = f - 1; h >= 0; --h)
      b[h] = 0;
    b[f] = g; b.t = this.t + f + 1; b.s = this.s; b.clamp()"""
    this = self
    c = a % DB
    d = DB - c
    e = (1 << d) - 1
    f = int(a / DB)
    g = this.s << c & DM 
    for i in range(this.t - 1, -1, -1):
      b[i + f + 1] = this[i] >> d | g
      g = (this[i] & e) << c
    for j in range(f - 1, -1, -1):
      b[j] = 0
    b[f] = g
    b.t = this.t + f + 1
    b.s = this.s
    b.clamp()

  def rShiftTo(self, a, b):
    """
    function rShiftTo(a, b) {
      b.s = this.s;
      var c = Math.floor(a / this.DB);
      if (c >= this.t) b.t = 0;
      else {
       var d = a % this.DB, e = this.DB - d, f = (1 << d) - 1;
       b[0] = this[c] >> d;
       for (var g = c + 1; g < this.t; ++g) {
         b[g - c - 1] |= (this[g] & f) << e;
         b[g - c] = this[g] >> d
       }
       d > 0 && (b[this.t - c - 1] |= (this.s & f) << e);
       b.t = this.t - c;
       b.clamp()
     }
    }
    """
    this = self
    b.s = this.s
    c = int(a / DB)
    if c >= this.t:
      b.t = 0
    else:
      d = a % DB
      e = DB - d
      f = (1 << d) - 1
      b[0] = this[c] >> d
      for g in range(c + 1, this.t):
        b[g - c - 1] |= (this[g] & f) << e
        b[g - c] = this[g] >> d
      if d > 0:
        b[this.t - c - 1] |= (this.s & f) << e
      b.t = this.t - c
      b.clamp()

  def fromInt(self,a):
    """this.t = 1;
       this.s = a < 0 ? -1 : 0;
       a > 0 ? this[0] = a : a < -1 ? this[0] = a + DV : this.t = 0"""
    this = self
    this.t = 1
    this.s = -1 if a < 0 else 0
    if a > 0:
      this[0] = a
    elif a < -1:
      this[0] = a + DV
    else:
      this.t = 0
        
  def exp(self,a,b):
    if a > 4294967295 or a < 1:
      return E.ONE
    c = E()
    f = E()
    g = b.convert(self)
    h = self.y(a) - 1
    g.copyTo(c)
    while h-1 >= 0:
      h -= 1
      b.sqrTo(c,f)
      if (a & 1 << h) > 0:
        b.mulTo(f, g, c)
      else:
        c,f = f,c
    return b.revert(c)

  def isEven(self):
    this = self
    return (this[0] & 1 if this.t > 0 else this.s) == 0
     
  def modPowInt(self,a,b):
    this = self
    if a < 256 or b.isEven():
      c = J(b)
    else:
      c = Q(b)
    return this.exp(a,c)

  def invDigit(self):
    this = self
    if this.t < 1:
      return 0
    a = this[0]
    if (a & 1) == 0:
      return 0
    b = a & 3;
    b = b * (2 - (a & 15) * b) & 15
    b = b * (2 - (a & 255) * b) & 255
    b = b * (2 - ((a & 65535) * b & 65535)) & 65535
    b = b * (2 - a * b % DV) % DV
    return DV - b if b > 0 else -b
  
  def get_zero(self):
    self.s = 0
    self.t = 0
    self.array = None
    return self
  
  def get_one(self):
    self.s = 0
    self.t = 1
    self.array = {0:1}
    return self

E.ZERO = E().get_zero()
E.ONE = E().get_one()
E.e = e

class Q:
  def __init__(self, a):
    this = self
    this.m = a 
    this.mp = a.invDigit()
    this.mpl = this.mp & 32767
    this.mph = this.mp >> 15
    this.um = (1 << DB - 15) - 1
    this.mt2 = 2 * a.t
  
  def convert(self,instance_E):
    """var b = e();
    a.abs().dlShiftTo(this.m.t, b);
    b.divRemTo(this.m, null , b);
    a.s < 0 && b.compareTo(d.ZERO) > 0 && this.m.subTo(b, b);
    return b"""
    this = self
    b = E()
    instance_E.abs().dlShiftTo(this.m.t,b)
    b.divRemTo(this.m, None, b)
    if instance_E.s < 0 and b.compareTo(E.ZERO) > 0:
      this.instance_E.subTo(b, b)
    return b
    
  def revert(self,a):
    this = self
    b = E()
    a.copyTo(b)
    this.reduce(b)
    return b

  def reduce(self,a):
    """
    while (a.t <= this.mt2)
      a[a.t++] = 0;
    for (var b = 0; b < this.m.t; ++b) {
      var c = a[b] & 32767,
      d = c * this.mpl + ((c * this.mph + (a[b] >> 15) * this.mpl & this.um) << 15) & a.DM;
      c = b + this.m.t;
      a[c] += this.m.am(0, d, a, b, 0, this.m.t);
      while (a[c] >= a.DV) {
        a[c] -= a.DV;
        a[++c]++
      }
    }
    a.clamp();
    a.drShiftTo(this.m.t, a);
    a.compareTo(this.m) >= 0 &&
    a.subTo(this.m, a)
    """
    this = self
    while a.t <= this.mt2:
      a[a.t] = 0
      a.t += 1
    for b in range(0,this.m.t):
      c = a[b] & 32767
      d = c * this.mpl + ((c * this.mph + (a[b] >> 15) * this.mpl & this.um) << 15) & DM
      c = b + this.m.t
      a[c] += this.m.am(0, d, a, b, 0, this.m.t)
      while a[c] >= DV:
        a[c] -= DV
        c += 1
        a[c] += 1
    a.clamp()
    a.drShiftTo(this.m.t, a)
    if a.compareTo(this.m) >= 0:
      a.subTo(this.m, a)

  def mulTo(self, a, b, c):
    this = self
    a.multiplyTo(b, c)
    this.reduce(c)

  def sqrTo(self,a,b):
    this = self
    a.squareTo(b)
    this.reduce(b) 

class J:
  def __init__(self,instance_E):
    this = self
    this.m = instance_E

  def convert(self,a):
    """return a.s < 0 || a.compareTo(this.m) >= 0 ? a.mod(this.m) : a"""
    this = self
    return a.s < 0 or a.mod(this.m) if a.compareTo(this.m) >= 0 else a

  def revert(self,a):
    return a

  def reduce(self,a):
    this = self
    a.divRemTo(this.m, None, a)

  def mulTo(self, a, b, c): 
    this = self
    a.multiplyTo(b,c)
    this.reduce(c)

  def sqrTo(self, a, b):
    this = self
    a.squareTo(b)
    this.reduce(b)

class Z:
  def __init__(self):
    self.i = 0
    self.j = 0
    self.S = []
  
  def init(self,bd):
    """var b, c, d;
    for (b = 0; b < 256; ++b)
    this.S[b] = b;
    c = 0;
    for (b = 0; b < 256; ++b) {
    c = c + this.S[b] + a[b % a.length] & 255;
    d = this.S[b];
    this.S[b] = this.S[c];
    this.S[c] = d
    }
    this.i = 0;
    this.j = 0"""
    c,d = 0,0
    for b in range(0,256):
      self.S.append(b)
    for b in range(0,256):
      c = c + self.S[b] + bd[b % len(bd)] & 255
      d = self.S[b]
      self.S[b] = self.S[c]
      self.S[c] = d
    self.i = 0
    self.j = 0

  def next(self):
    """
    var a;
    this.i = this.i + 1 & 255;
    this.j = this.j + this.S[this.i] & 255;
    a = this.S[this.i];
    this.S[this.i] = this.S[this.j];
    this.S[this.j] = a;
    return this.S[a + this.S[this.i] & 255]"""
    self.i = self.i + 1 & 255
    self.j = self.j + self.S[self.i] & 255
    a = self.S[self.i]
    self.S[self.i] = self.S[self.j]
    self.S[self.j] = a
    return self.S[a + self.S[self.i] & 255]

def main():
  pubkey="EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443"
  str = '1449678890\tCYYZN5\n009000'
  instance_RSAKey = RSAKey()
  instance_RSAKey.setPublic(pubkey,'10001')
  """b = e.encrypt([me.servertime, me.nonce].join("\t") + "\n" + b)"""
  ret = instance_RSAKey.encrypt(str)
  print ret

def nextbytes(array):
  global bc,be
  for b in range(0,len(array)):
    if bc is None:
      #get bc
      bg()
      bc = Z()
      bc.init(bd)
      for i in range(0, len(bd)):
        bd[i] = 0
      be = 0
    array[b] = bc.next()

def encryptpk_fromstring(pubkey,bit=16):
  if pubkey is None:
    return (0,1,0) #ret,t,s
  import math
  c = math.log(bit,2)
  if c.is_integer() and c>=1 and c<=8:
    c = int(c)
    ret = {}
    t,s,g,e,f=0,0,0,len(pubkey),False
    while e-1 >= 0:
      e -= 1
      char,h = pubkey[e],0
      ischar = type(char) == str
      if c==8 and ischar:
        h = 0
      elif c==8 and not ischar:
        h = int(char)
      else:
        """
        function o(a,b){var c=k[a.charCodeAt(b)];return c==null?-1:c}
        """
        charcode = ord(char)
        if charcode>=48 and charcode<=57:
          h = charcode-48
        elif charcode>=65 and charcode<=90:
          h = charcode-55
        elif charcode>=97 and charcode<=122:
          h = charcode-87
        else:
          f = char=='-'
          e = e-1
          continue
      if g==0:
        ret[t] = h
        t = t+1
      elif (g+c) > DB:
        ret[t-1] |= (h & (1 << DB-g) - 1) << g
        ret[t] = h >> DB -g
        t = t+1
      else:
        ret[t-1] |= h << g
      g += c
      g = g - DB if g >= DB else g
    #end of the loop
    fl = ord(pubkey[0]) if type(pubkey[0]) == str else int(pubkey[0])
    #fl should be in range(0,123),if fl & 128 !=0 the fl should between(128,256)
    if c==8 and (fl & 128) !=0:
      s = -1
      if g > 0:
        ret[t-1] |= (1 << DB -g) -1 << g
    a = s & DM
    while t>0 and ret[t-1] == a:
      t -= 1
    if f == True:
      """f && d.ZERO.subTo(this, this)"""
      """
      //subTo function defination:
      function E(a, b) {
      var c = 0,
      d = 0,
      e = Math.min(a.t, this.t);
      while (c < e) {
      d += this[c] - a[c];
      b[c++] = d & this.DM;
      d >>= this.DB
      }
      if (a.t < this.t) {
      d -= a.s;
      while (c < this.t) {
      d += this[c];
      b[c++] = d & this.DM;
      d >>= this.DB
      }
      d += this.s
      } else {
      d += this.s;
      while (c < a.t) {
      d -= a[c];
      b[c++] = d & this.DM;
      d >>= this.DB
      }
      d -= a.s
      }
      b.s = d < 0 ? -1 : 0;
      d < -1 ? b[c++] = this.DV + d : d > 0 && (b[c++] = d);
      b.t = c;
      b.clamp()
      }
      """
      #TODO:not implemented!
      return None
    else:
      return (ret,t,s)
  else:
    return None

if __name__ == '__main__':
  main()