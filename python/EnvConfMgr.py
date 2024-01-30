#
# EnvConfMgr.py
# ssp sensor mw Application Environment Configure Manager
# 2022-06-20 YHWHman
#

#import os
#import sys
from SU_Common import SSPUtils
#os.system("")

class CEnvConfMgr:

    className="EnvConfMgr"
    
    #strEnvFilename="SSPEnvConf.cfg"
    strEnvFilename=None
    
    
    def __init__(self,strEnvFilename):
        
        methodName="init"    
        try:
            self.strEnvFilename=strEnvFilename
            
        except Exception as e:
            print(f"[EXP] {self.className}:{methodName}",e)

        finally:
            pass
            
    # end of init()

    def getEnvCfg(self):
    
        methodName="getEnvCfg"
        try:
            
            with open(self.strEnvFilename,"r",encoding='utf-8') as f:
                strRMsg=f.read()
                f.close()
    
            readmsg=strRMsg.split('\n')
            #print(readmsg)
    
            # Debugging Msg        
            #for msg in readmsg:
            #    print(f"[DBG]\t{msg}")
            #print()
    
    
            dictEnvInfo={}
    
            for msg in readmsg:
    
                if(len(msg)<=0):
                    continue
    
                if(msg[0]=="#"):
                    continue
                
                #key,value=msg.upper().split("=")
                key,value=msg.split("=")
                dictEnvInfo[key]=value
                
                # print(f"[DBG] key=[{key.strip()}], value=[{value.strip()}]")
    
            # end of for msg in readmsg
    
        except Exception as e:
            print(f"[EXP] {self.className}:{methodName}",e)
            return False, None

        finally:
            pass
    
        return True, dictEnvInfo
    
    # end of getEnvCfg()
    
    def dispEnvInfo(self,dictEnvInfo=None):
        
        methodName="dispEnvInfo"
        
        try:
            if dictEnvInfo==None:
                bRtc, dictEnvInfo=self.getEnvCfg()
                if(bRtc==False):
                    print(f"[DBG] {SSPUtils.AGREEN}EnvConfMgr{SSPUtils.ANORMAL} {SSPUtils.ARED}Error!{SSPUtils.ANORMAL}")
        
            listEnvKeys=dictEnvInfo.keys()
            nSeq=0
            for strKey in listEnvKeys:
                nSeq+=1
                print(f"{nSeq:>10d}\t{strKey}={SSPUtils.AGREEN}[{SSPUtils.ANORMAL}{dictEnvInfo[strKey]}{SSPUtils.AGREEN}]{SSPUtils.ANORMAL}")
            
            # end of for()
            
            #print(f"{SSPUtils.AGREEN}Done{SSPUtils.ANORMAL}")
            
        except Exception as e:
            print(f"[EXP] {self.className}:{methodName}",e)

        finally:
            pass
    
    # end of dispEnvInfo()    
    
    
# end of class EnvConfMgr


if __name__=="__main__":

    strEnvConfFilename="SSPEnvConf.cfg"
    envConfMgr=CEnvConfMgr(strEnvConfFilename)
    
    bRtc, dictEnvInfo=envConfMgr.getEnvCfg()
    if(bRtc==False):
        print(f"[DBG] {SSPUtils.AGREEN}EnvConfMgr{SSPUtils.ANORMAL} {SSPUtils.ARED}Error!{SSPUtils.ANORMAL}")

    listEnvKeys=dictEnvInfo.keys()
    nSeq=0
    for strKey in listEnvKeys:
        nSeq+=1
        print(f"{nSeq:>10d}\t{strKey}={SSPUtils.AGREEN}[{SSPUtils.ANORMAL}{dictEnvInfo[strKey]}{SSPUtils.AGREEN}]{SSPUtils.ANORMAL}")
    
    # end of for()
    
    print(f"{SSPUtils.AGREEN}Done{SSPUtils.ANORMAL}")

# end of __main__()

#___e___