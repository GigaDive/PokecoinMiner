import hashlib
from _sha256 import sha256
from datetime import datetime
import math
import requests
import calendar
from multiprocessing import Pool
# parallelisierung
from multiprocessing import Process, freeze_support
threads = []
threadnum = 16

"""
threads.append(Thread(target=self.recRaytracing,
                                          args=(widthPerThread * x, x * widthPerThread + widthPerThread,)))
login = 
print("LOGIN: ",login.json())
"""



class Worker:
  loginToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Ij4-IEpFRkYgQkVaT1MgPDwiLCJpYXQiOjE1NzY4ODIyNDUsImV4cCI6MTU3Njk2ODY0NX0.vhuwmLUfUcVWcTQRAlc_11jGhEEqhePpPWmVt8rp0EQ"
  w_id = 0
  amount=0
  def __init__(self,workerID,amount,loginToken):
    self.loginToken = loginToken
    self.w_id = workerID
    self.amount = amount

  def getLastBlockHash(self):
    return requests.get('https://rocky-lowlands-35145.herokuapp.com/blockchain/lastBlock').json()["hash"]


  def getDifficulty(self):
    return requests.get('https://rocky-lowlands-35145.herokuapp.com/blockchain/currentDifficulty',
                        headers={"accept": "application/json"}).json()


  def getTime(self):
    return calendar.timegm(datetime.now().timetuple())


  def sha256(self,message):
    return hashlib.sha256(message.encode('utf-8')).hexdigest()

  def mine(self, joke, difficulty=1):
    assert difficulty >= 1
    r = requests.get('https://icanhazdadjoke.com/', headers={"accept": "application/json"})
    prefix = '0' * difficulty
    nonce = 0
    lastBlockHash = self.getLastBlockHash()
    currentDiff = self.getDifficulty()
    time = self.getTime()
    while (True):
      blockString = str(lastBlockHash) + str(time) + str(joke) + str(nonce)
      cryptoHash = self.sha256(blockString)
      # print("Current Hash: ",cryptoHash[0:currentDiff], "Diff: ", prefix, " Nonce: ",nonce)
      if cryptoHash[0:currentDiff] == prefix:
        block = {"lastBlockHash": lastBlockHash,
                 "data": joke,
                 "timestamp":  time,
                 "nonce": nonce}
        return block
      else:
        nonce += 1;
        if nonce % 300000 == 0:
          lastBlockHash =  self.getLastBlockHash()
          #print("Request Latest Blockhash: ", lastBlockHash)

  def run(self):
    iterations = 0
    while (iterations < self.amount):
      #Authenticate me
      authMe = requests.get('https://rocky-lowlands-35145.herokuapp.com/auth/me', headers={"token": self.loginToken})
      print(authMe.json())
      if "code" in authMe.json():
        self.loginToken = requests.post('https://rocky-lowlands-35145.herokuapp.com/auth/login', json={
          "username": ">> JEFF BEZOS <<",
          "password": "ohdamnboidatsallotadamage1337"
        }).json()["token"]
        print("LOGIN TOKEN UPDATED", self.loginToken)
      else:
        print("TOKEN STILL VALID")
      #start mining
      newB = self.mine(str(requests.get('https://icanhazdadjoke.com/', headers={"accept": "application/json"}).json()["joke"]), requests.get('https://rocky-lowlands-35145.herokuapp.com/blockchain/currentDifficulty',
                                        headers={"accept": "application/json"}).json())
      finalReq = requests.post("https://rocky-lowlands-35145.herokuapp.com/blockchain/blocks", json={
        "previousHash": newB["lastBlockHash"],
        "data": newB["data"],
        "timestamp": newB["timestamp"],
        "nonce": newB["nonce"]}
                               , headers={"token": self.loginToken})
      if "code" not in finalReq.json():
        print("Balance: ",requests.get("https://rocky-lowlands-35145.herokuapp.com/wallet/balance", headers={"token": self.loginToken}).json()["amount"], "FOUND: ", finalReq.json()["block"]["hash"]," - ",finalReq.json()["block"]["data"] )
      iterations+=1



if __name__ == '__main__':
  for i in range(0, threadnum):
    w = Worker(i, 1000,
               "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Ij4-IEpFRkYgQkVaT1MgPDwiLCJpYXQiOjE1NzY4ODIyNDUsImV4cCI6MTU3Njk2ODY0NX0.vhuwmLUfUcVWcTQRAlc_11jGhEEqhePpPWmVt8rp0EQ")
    threads.append(Process(target=w.run,
                           args=()))

  for t in threads:
    t.start()
  for p in threads:
    p.join()

  """
  print(requests.get('https://rocky-lowlands-35145.herokuapp.com/auth/me',headers={"Accept":"application/json",
                                                                                   "username": "Pokinator", "password": "snitchig"}).json())"""