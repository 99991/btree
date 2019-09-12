from btree import BTreeSet
import time
import random
random.seed(0)

def test():
    # insert and remove 0..99
    t = BTreeSet()
    for i in range(100):
        t.add(i)
        t.check()
        assert(list(t) == list(range(i + 1)))
    for i in range(100):
        t.remove(i)
        t.check()
        assert(list(t) == list(range(i + 1, 100)))

    # insert and remove 99..0
    t = BTreeSet()
    for i in reversed(range(100)):
        t.add(i)
        t.check()
        assert(list(t) == list(range(i, 100)))
    
    for i in range(100):
        assert(i in t)
    
    for i in reversed(range(100)):
        t.remove(i)
        t.check()
        assert(list(t) == list(range(i)))

    # test inserting and removing randomly
    s = set()
    t = BTreeSet()
    for _ in range(10_000):
        if random.random() < 0.5 or len(s) == 0:
            value = random.randrange(100)
            s.add(value)
            t.add(value)
        else:
            value = random.choice(list(s))
            s.remove(value)
            t.remove(value)
        
        if len(s) > 0:
            assert(t.min() == min(s))
            assert(t.max() == max(s))
        
        t.check()
        
        assert(list(t) == list(sorted(s)))

class Timer(object):
    def __init__(self):
        self.t = time.perf_counter()
    
    def log(self, what):
        t = time.perf_counter()
        dt = t - self.t
        self.t = t
        print(f"{what}: {dt} seconds")

def benchmark():
    n = 10_000
    values = list(range(n))
    random.shuffle(values)

    s = set()
    t = BTreeSet()
    
    timer = Timer()
    
    for i in range(n):
        s.add(i)

    timer.log("insert ascending      set")

    for i in range(n):
        t.add(i)

    timer.log("insert ascending BTreeSet")

    for i in range(n):
        s.remove(i)

    timer.log("remove ascending      set")

    for i in range(n):
        t.remove(i)

    timer.log("remove ascending BTreeSet")

    for i in range(n):
        s.add(i)

    timer.log("insert random order      set")

    for i in range(n):
        t.add(i)

    timer.log("insert random order BTreeSet")
    
    s_sorted = sorted(s)
    
    timer.log("sorting      set")
    
    t_sorted = list(t)
    
    timer.log("sorting BTreeSet")
    
    assert(s_sorted == t_sorted)

    timer.log("testing equality")

    random.shuffle(values)
    
    timer.log("shuffling")

    for i in range(n):
        s.remove(i)

    timer.log("remove random order      set")

    for i in range(n):
        t.remove(i)

    timer.log("remove random order BTreeSet")

    test()

    timer.log("test")
    
    t.check()
    
    print("")

for _ in range(10):
    benchmark()
