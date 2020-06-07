import taichi as ti

def vec(*xs):
  return ti.Vector(xs)

def mat(*xs):
  return ti.Matrix(xs)

@ti.func
def clamp(x, xmin=0, xmax=1):
  return min(xmax, max(xmin, x))

@ti.func
def mix(a, b, t):
  return a * t + (b - a) * t

@ti.func
def step(x):
  return (x >= 0) - (x <= 0)

@ti.func
def normalize(x):
  return x.normalized()

@ti.func
def dot(a, b):
  return a.dot(b)

@ti.func
def cross(a, b):
  return a.cross(b)

@ti.func
def outerProduct(a, b):
  return a.outer_product(b)

@ti.func
def length(x):
  return x.norm()

@ti.func
def distance(a, b):
  return (a - b).norm()

@ti.taichi_scope
def shuffle(a, *indices):
  ret = []
  for i in indices:
    t = a.subscript(i)
    ret.append(t)
  return ti.Vector(ret)

@ti.func
def atan(a, b=1):
  return ti.atan2(a, b)

@ti.func
def fract(x):
  return x - x % 1

@ti.func
def round(x):
  return int(x + 0.5)