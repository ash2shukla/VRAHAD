#Generate HMAC for preventing length extension attack on MAC or Rainbow table attack on Hashes.

import hmac
from base64 import b64encode,b64decode
from hashlib import sha256
from PRNG import PRNG
from HBase_drive import HBaseDrive
from AES import AESCipher


class signUP:
    def generateGID(self,Y="1111",P="111",S="M"):
        common_key = "SAM"
        string = Y+P+S
        GID = hmac.new(common_key, msg = string,digestmod = sha256).digest()
        GID64 = b64encode(GID)
        return GID64
        
    def generateGUID(self,GID):
        hbd = HBaseDrive()
        last_Count = hbd.getLast(GID)
        
        GUID = PRNG(last_Count).nextRandom()
        
        # To increment last Count corresponding to that ID 
        hbd.countPlus(GID)
        return GUID

    def createAID(self,YPS="1111111M",UID="111111111111"):
        AID = hmac.new(YPS, msg = UID, digestmod = sha256).digest()
        AID64 = b64encode(AID)
        return AID64

    def cryptAID(self,Key,UID):
        agent = AESCipher(Key)
        return agent.encrypt(UID)
        
    def decryptAID(self,Key,XID):
        agent = AESCipher(Key)
        return agent.decrypt(XID)
        
    
if __name__ == "__main__":
    inst = signUP()
    GID = inst.generateGID(Y="1996",P="209",S="M")
    GUID = inst.generateGUID(GID)
    AID = inst.createAID("1996209M","903298497479")
    AID_enc = inst.cryptAID(AID,"903298497479")
    decrypTry = inst.decryptAID(AID,AID_enc)
    
    print "GID",GID
    print "GUID",GUID
    print "AID",AID
    print "AID_enc",AID_enc
    print "decrypted",decrypTry
