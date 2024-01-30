#################################################
# SSPUtils.py
# Sensing Plus Application Utils
# 2022-06-15 YHWHman
#################################################

import os
import sys
import struct
import json
import datetime
import time

os.system("")

#
# defnie Ansi Color
#

#######################
# TEXT COLOR CODE
#######################
# 30, 90
#######################

ANORMAL="\033[0m"
ABLACK="\033[90m"
ARED="\033[91m"
AGREEN="\033[92m"
AYELLOW="\033[93m"
ABLUE="\033[94m"
APURPLE="\033[95m"
ASKY="\033[96m"
AWHITE="\033[97m"

#######################
# BACKGROUND COLOR CODE
#######################
# 7, 47
#######################
BBLOCK="\033[40m"
BRED="\033[41m"
BGREEN="\033[42m"
BYELLOW="\033[43m"
BBLUE="\033[44m"
BPURPLE="\033[45m"
BSKY="\033[46m"
BWHITE="\033[47m"


# end of class CAnsi

#------------------------------------------------------------------------------
def getNowStr(nMode=0):
#------------------------------------------------------------------------------

    try:
        
        now=datetime.datetime.now()
        strNow=now.strftime('%Y-%m-%d %H:%M:%S.%f')

        if(nMode==1):
            strNow=now.strftime('%Y%m%d%H%M%S%f')
            #strNow=strNow[:-3]

        if(nMode==2):
            strDate=f"{now.year:0>4}{now.month:0>2}{now.day:0>2}"
            strTime=f"{now.hour:0>2}{now.minute:0>2}{now.second:0>2}{now.microsecond:0>6}"
            strNow=f"{strDate}_{strTime}"

        if(nMode==3):
            strDate=f"{now.year:0>4}-{now.month:0>2}-{now.day:0>2}"
            strTime=f"{now.hour:0>2}:{now.minute:0>2}:{now.second:0>2}:{now.microsecond:0>6}"
            strNow=f"{strDate} {strTime}"

        #print(f"[DBG] strNow=[{strNow}]")
    
    except Exception as e:
        strErr=f"ModuleName=[{__name__}], FunctionName=[{sys._getframe().f_code.co_name}] {e}"
        return False, strErr

    return True, strNow

# end of getNowStr()

#------------------------------------------------------------------------------
def test_float():
#------------------------------------------------------------------------------

    # 4byte '16진수문자열'을 float로 변환
    
    #cdata='0x3C23D70A'
    #cdata='3C23D70A'
    #cdata='3c23d70a'
    cdata='3c00'
    print(f"cdata=[{cdata}]")


    # idata=int(cdata,16)
    # print(f"idata=[{idata}]")
    # 
    # hdata=float.hex(idata)
    # print(f"hdata=[{hdata}]")

    
    # string -> number format character
    # https://docs.python.org/ko/3/library/struct.html
    
    
    fdata=struct.unpack('!e', bytes.fromhex(cdata))[0]  # 4byte float
    #fdata=struct.unpack('!f', bytes.fromhex(cdata))[0]  # 4byte float
    #fdata=struct.unpack('<d', struct.pack("Q",int("0x"+hdata,16)))[0]
    print(f"hex=[{fdata}]")

# end of test_float()


#------------------------------------------------------------------------------
def byte2int(byteData,length):
#------------------------------------------------------------------------------
    
    # length : 4 ☞ 4byte integer
    # length : 2 ☞ 2byte integer
    # length : 1 ☞ 1byte integer

    try:    
        
        realLen=length*2
        
        #print(f"[DBG] {type(byteData)}")
        #print(f"[DBG] {byteData}")
        
        
        strData=f"{byteData.hex()}".upper()
        #print(f"[DBG] {strData}")
        
        if(length==4):
            v1=strData[realLen-2:realLen-0]
            v2=strData[realLen-4:realLen-2]
            v3=strData[realLen-6:realLen-4]
            v4=strData[realLen-8:realLen-6]
        
            hexValue=f"0x{v1}{v2}{v3}{v4}"
            #print(f"[DBG] hex:[{hexValue}]")
            intValue=int(hexValue,16)
            #print(f"[DBG] int(4) : [{intValue}]")
            
        elif(length==2):
            v1=strData[realLen-2:realLen-0]
            v2=strData[realLen-4:realLen-2]
        
            hexValue=f"0x{v1}{v2}"
            #print(f"[DBG] hex:[{hexValue}]")
            intValue=int(hexValue,16)
            #print(f"[DBG] int(2) : [{intValue}]")
            
        elif(length==1):
            v1=strData[realLen-2:realLen-0]
        
            hexValue=f"0x{v1}"
            #print(f"[DBG] hex:[{hexValue}]")
            intValue=int(hexValue,16)
            #print(f"[DBG] int(2) : [{intValue}]")

    except Exception as e:
        strErr=f"ModuleName=[{__name__}], FunctionName=[{sys._getframe().f_code.co_name}] {e}"
        return False, strErr

    return True, intValue # 정수 리턴

# end of def byte2int()

#------------------------------------------------------------------------------
def byte2hexstr(byteData,length):
#------------------------------------------------------------------------------    

    # length : 4 ☞ 4byte integer
    # length : 2 ☞ 2byte integer

    try:
        
        realLen=length*2
        
        strData=f"{byteData.hex()}".upper()
        #print(strData)
        
        if(length==4):
            v1=strData[realLen-2:realLen-0]
            v2=strData[realLen-4:realLen-2]
            v3=strData[realLen-6:realLen-4]
            v4=strData[realLen-8:realLen-6]
        
            strHexValue=f"{v1}{v2}{v3}{v4}"
            #print(f"[DBG] hex(4):[{strHexValue}]")
            
            
        elif(length==2):
            v1=strData[realLen-2:realLen-0]
            v2=strData[realLen-4:realLen-2]
        
            strHexValue=f"{v1}{v2}"
            #print(f"[DBG] hex(2):[{strHexValue}]")
        
    except Exception as e:
        strErr=f"ModuleName=[{__name__}], FunctionName=[{sys._getframe().f_code.co_name}] {e}"
        return False, strErr
    
    return True, strHexValue

# end of def byte2hexstr()

#------------------------------------------------------------------------------
def byte2float(byteData,length):
#------------------------------------------------------------------------------    

    # length : 4 ☞ 4byte float
    # length : 2 ☞ 2byte float
        
    try:
        
        realLen=length*2
            
        strData=f"{byteData.hex()}".upper()
        #print(strData)
        
        if(length==4):
            v1=strData[realLen-2:realLen-0]
            v2=strData[realLen-4:realLen-2]
            v3=strData[realLen-6:realLen-4]
            v4=strData[realLen-8:realLen-6]
        
            strHexValue=f"{v1}{v2}{v3}{v4}"
            #print(f"[DBG] hex:[{strHexValue}]")        
            floatValue=struct.unpack('!f', bytes.fromhex(strHexValue))[0]
            #print(f"[DBG] float(4) : [{floatValue}]")
            
        elif(length==2):
            v1=strData[realLen-2:realLen-0]
            v2=strData[realLen-4:realLen-2]
        
            strHexValue=f"{v1}{v2}"
            #print(f"[DBG] hex:[{strHexValue}]")     
            floatValue=struct.unpack('!f', bytes.fromhex(strHexValue))[0]
            #print(f"[DBG] float(2) : [{floatValue}]")

    except Exception as e:
        strErr=f"ModuleName=[{__name__}], FunctionName=[{sys._getframe().f_code.co_name}] {e}"
        return False, strErr

    return True, floatValue # 실수 리턴

# end of def byte2int()

#------------------------------------------------------------------------------
def int2bytes(nValue,nLen,byteorder="little", signed=True):
#------------------------------------------------------------------------------

    try:
        byteRlt=(nValue).to_bytes(nLen,byteorder=byteorder, signed=signed)

    except Exception as e:
        strErr=f"ModuleName=[{__name__}], FunctionName=[{sys._getframe().f_code.co_name}] {e}"
        return False, strErr
    return True, byteRlt
# end of int2bytes()

#------------------------------------------------------------------------------
def json2dict(jsonData):
#------------------------------------------------------------------------------
    try:
        
        dictData=json.loads(jsonData)

    except Exception as e:
        strErr=f"ModuleName=[{__name__}], FunctionName=[{sys._getframe().f_code.co_name}] {e}"
        return False, strErr

    return True, dictData
    
# end of json2dict()

#------------------------------------------------------------------------------
def dict2json(dictData):
#------------------------------------------------------------------------------
    try:
        
        #jsonData=json.dumps(dictData,ensure_ascii=False)
        jsonData=json.dumps(dictData,sort_keys=False,indent=4)

    except Exception as e:
        strErr=f"ModuleName=[{__name__}], FunctionName=[{sys._getframe().f_code.co_name}] {e}"
        return False, strErr
    
    return True, jsonData

# end of dict2json()

#------------------------------------------------------------------------------
def json2file(strTargetPath, strFileName, jsonData):
#------------------------------------------------------------------------------
    # 수신한 JSON 데이터 지정 위치에 .json 파일로 캡쳐

    try:
        
        
        # Capture Directory Check
        if(os.path.exists(strTargetPath)==False):
            os.makedirs(strTargetPath)

        # json file FULL Path
        strJsonFullPath=os.path.join(strTargetPath, strFileName)

        with open(strJsonFullPath,"w",encoding='utf-8') as jsonFile:
            #json.dump(jsonData,jsonFile)
            jsonFile.write(jsonData)
            jsonFile.flush()
        time.sleep(.001)

    except Exception as e:
        
        strErr=f"ModuleName=[{__name__}], FunctionName=[{sys._getframe().f_code.co_name}] {e}"
        return False, strErr
    
    return True, None

# end of json2file()

#------------------------------------------------------------------------------
def msg2file(strTargetPath, strFileName, byteMsg):
#------------------------------------------------------------------------------
    # 수신한 메시지 데이터 지정 위치에 .cap 파일로 캡쳐

    try: 
        
        
        # Capture Directory Check
        if(os.path.exists(strTargetPath)==False):
            os.makedirs(strTargetPath)

        # capture file FULL Path
        strCapFullPath=os.path.join(strTargetPath, strFileName)

        #with open(strCapFullPath,"wb",encoding='utf-8') as jsonFile:
        with open(strCapFullPath,"wb") as capFile:
            capFile.write(byteMsg)
            capFile.flush()
        time.sleep(.001)

    except Exception as e:
        strErr=f"ModuleName=[{__name__}], FunctionName=[{sys._getframe().f_code.co_name}] {e}"
        return False, strErr

    return True, None
    
# end of msg2cap()


# HxV
#------------------------------------------------------------------------------
def viewMsgHxV(strTargetPath, byteMsg):
#------------------------------------------------------------------------------
    # XXD View        
    # Hex View
    
    try:
    
        # Capture Directory Check
        if(os.path.exists(strTargetPath)==False):
            os.makedirs(strTargetPath)                    

        strTempFullPath=os.path.join(strTargetPath, f"{getNowStr(1)}.temp")
        with open(strTempFullPath,"wb") as fileTemp:
            fileTemp.write(byteMsg)
            fileTemp.flush()
            time.sleep(0.001)

        os.system(f"HxV {strTempFullPath}")        
        os.remove(strTempFullPath)

    except Exception as e:
        strErr=f"ModuleName=[{__name__}], FunctionName=[{sys._getframe().f_code.co_name}] {e}"
        return False, strErr
        
    return True, None

# end of viewMsgXXD()

#------------------------------------------------------------------------------
def cfg2json(strCfgPath, strCfgName, dictResult):
#------------------------------------------------------------------------------
    try:
        
        strCfgFPath=os.path.join(strCfgPath,strCfgName)

        with open(strCfgFPath, "r") as fileCfg:
            strFData=fileCfg.read()
        
        #print(f"[DBG]\n{SSPAnsi.AGREEN}{strFData}{SSPAnsi.ANORMAL}")
        #dictPreset={}
        
        listCfgLines=strFData.split('\n')
        #print(len(listCfgLines))
        
        # Command Count
        nCmdCnt=0
        for strLine in listCfgLines:
            strLine=strLine.strip()
            if strLine=="" or strLine[0]=="%":
                continue
            nCmdCnt+=1
        
        #print(f"[DBG] Command Count=[{nCmdCnt}]")        
        
        nSeq=0
        #dictPreset={}
        dictResult["cfginfo"]={}
        dictResult["cfginfo"]["cfgname"]=strCfgName
        dictResult["cfginfo"]["cmdcnt"]=nCmdCnt
        
        for strLine in listCfgLines:
            strLine=strLine.strip()
            if strLine=="" or strLine[0]=="%":            
                continue
            
            listTemp=strLine.split()
            dictResult["cfginfo"][f"cmd{nSeq}"]={}
            dictResult["cfginfo"][f"cmd{nSeq}"]["cmd"]=listTemp[0]
            
            nArgCnt=len(listTemp)-1
            dictResult["cfginfo"][f"cmd{nSeq}"]["argcnt"]=nArgCnt
            
            if(nArgCnt<1):
                nSeq+=1
                continue
                
            for nArgSeq in range(1,nArgCnt+1):
                dictResult["cfginfo"][f"cmd{nSeq}"][f"arg{nArgSeq-1}"]=float(listTemp[nArgSeq])
            
            nSeq+=1
            
        # end of for strLine in listCfgLines
        
        # 설정파일(cfg)을 읽어서 전달받은 dictResult 딕셔너리에 추가해서 리턴        

    except Exception as e:        
        strErr=f"ModuleName=[{__name__}], FunctionName=[{sys._getframe().f_code.co_name}] {e}"
        return False, strErr

    return True, dictResult

# end of cfg2json()

#------------------------------------------------------------------------------
def dispHexCon(byteMsg):
#------------------------------------------------------------------------------
    # HexCon.py 로 대체
    
    try:
        
        dispMsg=byteMsg.hex()    

        for pos in range(len(dispMsg)):

            # sequence display
            if(pos==0):
                print(f"{pos:0>8x}:\t", end="", flush=True)
            if(pos!=0 and pos%32==0):
                print(f"\n{pos//2:0>8x}:\t", end="", flush=True)
            
            # message display
            if(pos!=0 and pos%2==0 and pos%32!=0):
                print(" ",end="",flush=True)
            print(f"{dispMsg[pos]}", end="", flush=True)

        # end of for pos
        
    except Exception as e:
        strErr=f"ModuleName=[{__name__}], FunctionName=[{sys._getframe().f_code.co_name}] {e}"
        return False, strErr
        
    return True, None

# end of dispHexCon


#------------------------------------------------------------------------------
def parse_json_config(filename):
#------------------------------------------------------------------------------
    try:
        with open(filename, 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError as e:
        print(f'Error at parse_json_config(). {e}')
        raise e
    except Exception as e:
        print(f'Error at parse_json_config(). {e}')
        raise e
    
#___e___
