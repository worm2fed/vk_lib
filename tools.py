import time

# Class to elapse time
class LeadTime(object):
    def __enter__(self):
        self._startTime = time.time()
         
    def __exit__(self, type, value, traceback):
        print('Elapsed time: {:.3f} sec '.format(time.time() - self._startTime))
