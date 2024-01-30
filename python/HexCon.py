#
# HexCon
# Hex Message Display Console
# 
import sys

def dispHexCon(byteMsg):

    try:
        print()
        
        totalMsg=byteMsg.hex()    
        
        nLineLen=32
        nCopyLen=0
        nTotalLen=len(totalMsg)
        
        #print(nTotalLen)
        
        for nMsgPos in range(0,nTotalLen,nLineLen):
                
            #print(nMsgPos)
            if(nMsgPos+nLineLen)<=nTotalLen :
                nCopyLen=nLineLen
            else:
                nCopyLen=nTotalLen-nMsgPos
        
            print("\033[36m",end="",flush=True)
            if(nMsgPos==0):
                print(f"{nMsgPos:010X}    ",end="",flush=True)
            else:
                print(f"{nMsgPos//2:010X}    ",end="",flush=True)
            print("\033[0m",end="",flush=True)
             
            dispMsg=totalMsg[nMsgPos:nMsgPos+nCopyLen]
            
            # display HEX code
            for nDispPos in range(len(dispMsg)):
                print(dispMsg[nDispPos],end="",flush=True)
                if(nDispPos!=0 and (nDispPos+1)%4==0):
                    print(" ",end="",flush=True)
            
            if(len(dispMsg)<nLineLen):
                nSpace=(nLineLen-len(dispMsg))
                nSpace=nSpace+(nSpace//4)
                print(" "* nSpace,end="",flush=True)
                
            print("    ",end="",flush=True)
            
            # disp ASCII code
            print("\033[33m",end="",flush=True)
            for nDispPos in range(0,len(dispMsg),2):
                hexNum=dispMsg[nDispPos]+dispMsg[nDispPos+1]
                
                nCode=int(hexNum,16)
                if(nCode<0x21 or nCode>0x7f):
                    charX="."
                else:
                    charX=chr(nCode)                
                print(charX,end="",flush=True)
            print("\033[0m",end="",flush=True)
            print()
            
        print()
        
    except Exception as e:
        print(f"[EXP] ModuleName=[{__name__}], FunctionName=[{sys._getframe().f_code.co_name}] {e}") 
        return None

    return True

# end of dispHexCon


if __name__=='__main__':

    with open("LD2410_ACK.dat","rb") as f:
        byteMsg=f.read()
    dispHexCon(byteMsg)
    print("Done")

#___e___