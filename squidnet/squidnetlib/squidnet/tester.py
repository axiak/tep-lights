import sexp
import time


N = 100

data = open('./data').read()

start = time.time()
for i in xrange(N):
    sexp.read_all(data)

print "Rate: %0.2d creates/sec" % (N / float(time.time() - start))
