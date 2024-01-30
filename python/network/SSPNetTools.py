#################################################
# SSPNetTools.py
# SSP Network Tools Module
# 2022-06-30 YHWHman
#################################################

import os
import socket
import platform

moduleName="SSPNetTools"

#------------------------------------------------------------------------------
def chkHost(strTargetIP):
#------------------------------------------------------------------------------

    methodName="chkHost"
    try:
        strPlatform=platform.system()
        if(strPlatform=="Linux"):
            result = os.system(f"ping -c 1 -i 1 {strTargetIP} >/dev/null")
        elif(strPlatform=="Windows"):
            result = os.system(f"ping -w 100 -n 1 {strTargetIP} >nul")
        else:
            print(f"[ERR] Unknown Platform [{strPlatform}] Error!")
            
        if(result==0):
            #print(f"[DBG] Target Host [{strTargetIP}] is On...[{result}]")
            bRtc=True
        else:
            #print(f"[DBG] Target Host [{strTargetIP}] is Off..[{result}]")
            bRtc=False
        
    except Exception as e:
        print(f"[EXP] {moduleName}:{methodName} {e}")
        return False
        
    return bRtc

# end of chkIP()

#------------------------------------------------------------------------------
def chkPort(strTargetIP, nPort, nTimeout):
#------------------------------------------------------------------------------

    methodName="chkPort"
    #sock=None

    try:

        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(nTimeout)

        result=sock.connect_ex((strTargetIP,nPort))
        #print(f"[DBG] result type=[{type(result)}], result value=[{result}]")

        if(result==0):
            #print(f"[DBG] Target Host [{strTargetIP}] Port [{nPort}] [True]")
            bRtc=True
        else:
            #print(f"[DBG] Target Host [{strTargetIP}] Port [{nPort}] [False]")
            bRtc=False

        #sock.close()

    except Exception as e:
        print(f"[EXP] {moduleName}:{methodName} {e}")        
        return False

    finally:
        sock.close

    return bRtc

# end of chkPort()

# end of class CNetTools()

#------------------------------------------------------------------------------
if __name__=='__main__':
#------------------------------------------------------------------------------

    #strTargetIP="172.30.1.33"
    strTargetIP="127.0.0.1"
    nTargetPort=8888
    nTimeout=1 # second

    bHealth=chkHost(strTargetIP)
    print(f"[DBG] Target Host [{strTargetIP}] Health [{bHealth}]")
    print()
    
    bHealthPort=chkPort(strTargetIP, nTargetPort, nTimeout)
    print(f"[DBG] Target Host [{strTargetIP}] Port [{nTargetPort}] Health [{bHealthPort}]")
    print()
    
    print("Done.")

# end of main()

#___e___
