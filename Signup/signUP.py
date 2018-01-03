#Generate HMAC for preventing length extension attack on MAC or Rainbow table attack on Hashes.

import hmac
from base64 import b64encode,b64decode
from hashlib import sha256
from PRNG import PRNG
from HBase_drive import HBaseDrive
from AES import AESCipher
from validations import *


class signUP:
    def generateGID(self,Y="1111",P="111",S="M"):
        # Common Key to Generate Hash for Group ID
        commonKey = "CEREBRO"
        string = Y+P+S
        GID = hmac.new(commonKey, msg = string,digestmod = sha256).digest()
        GID64 = b64encode(GID)
        return GID64
        
    def generateGUID(self,GID):
        hbd = HBaseDrive()
        # getLast returns a string starting with GID
        lastCount = hbd.getLast(GID)
        if last_Count is None:
            # Insert new string starting with GID inited with 1
            hbd.countPlus(GID+'1')
            lastCount = 1
        else:
            # Split the string with = and get last part
            try:
                last_Count = int(last_Count.split("=")[-1])
                
        GUID = PRNG(lastCount).nextRandom()
        # To increment last Count corresponding to that ID 
        hbd.countPlus(GID)
        return GUID

    def createHID(self,YPS="1111111M",UID="111111111111"):
        HID = hmac.new(YPS, msg = UID, digestmod = sha256).digest()
        HID64 = b64encode(HID)
        return HID64

    def retrieveBase(self,YPS="1111111M",UID="111111111111"):
        self.generateGID(YPS)
    #def cryptAID(self,Key,UID):
    #    agent = AESCipher(Key)
    #    return agent.encrypt(UID)
        
    #def decryptAID(self,Key,XID):
    #    agent = AESCipher(Key)
    #    return agent.decrypt(XID)
        
    
if __name__ == "__main__":
    inst = signUP()
    GID = inst.generateGID(Y="1996",P="209",S="M")
    GUID = inst.generateGUID(GID)
    HID = inst.createHID(YPS = "1996209M",UID = GID+str(GUID))
    #AID_enc = inst.cryptAID(HID,"903298497479")
    #decrypTry = inst.decryptAID(HID,AID_enc)
    
    print "GID",GID
    print "GUID",GUID
    print "HID",HID
    #print "AID_enc",AID_enc
    #print "decrypted",decrypTry
