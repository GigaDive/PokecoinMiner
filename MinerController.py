from pokeMiner import Worker
from multiprocessing import Process

# parallelisierung

threads = []
threadnum = 16

def initiateWorker(id, amount, token):
  return Worker(id, amount, token)

for i in range(0,threadnum):
    w = Worker(i,50,"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Ij4-IEpFRkYgQkVaT1MgPDwiLCJpYXQiOjE1NzY4ODIyNDUsImV4cCI6MTU3Njk2ODY0NX0.vhuwmLUfUcVWcTQRAlc_11jGhEEqhePpPWmVt8rp0EQ")
    threads.append(Process(target=w.run,
                          args=()))

for t in threads:
  t.start()
for p in threads:
   p.join()
