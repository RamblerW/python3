#!/usr/bin/env python
#-*- coding:utf-8 -*-

# 抓取王者荣耀比赛数据
# author: rambler
# datetime: 2018/11/26 23:08
# software: PyCharm
import datetime
import os
import random
import time
import urllib
import ssl
import threading
from numpy import long
import sys
import json
from copy import deepcopy
import pymongo
import traceback
import warnings
# 不输出警告信息
warnings.filterwarnings("ignore")

def getDB():
    conn = pymongo.MongoClient('mongodb://localhost:27017/')
    db = conn.pvp # 连接数据库名
    return conn,db
# 保存数据到mongoDB
def saveData(list,connectionName):
    try:
        conn,db = getDB()
        connection = db[connectionName]
        # 保存数据
        # connection.insert_many(list) # 批量保存
        for i in list:
            connection.save(i) # 有则更新，没有则插入
    except Exception as e:
        print("saveData Error")
        traceback.print_exc()
    finally:
        conn.close()

# 退出线程
def exitThread():
    print(threading.current_thread().name, 'exit')
    sys.exit()

# 结束程序
def exit():
    print('os exit')
    os._exit(0) # 0为正常退出，其他数值（1-127）为不正常，可抛异常事件供捕获

# 发送请求，获取响应的数据（json）
def getJsonResult(url, params):
    # time.sleep(random.uniform(2,5)) # 随机休眠2-5秒
    # 请求头
    headers = {
        'Content-Encrypt':'',
        'Accept-Encrypt':'',
        'noencrypt':'1',
        'X-Client-Proto':'https',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent':'okhttp/3.10.0'
    }
    result_json = ''
    # 错误的数据直接跳过
    try:
        # 对请求数据进行编码
        data = urllib.parse.urlencode(params).encode(encoding='UTF8')
        context = ssl._create_unverified_context()
        req = urllib.request.Request(url, headers=headers, data=data)

        # 发送请求，获取返回结果
        response_result = urllib.request.urlopen(req,context=context, timeout=120).read().decode('unicode_escape') # unionCode转中文
        # 转为json
        result_json = json.loads(response_result, strict=False)
    finally:
        return result_json

def main(startRoleId,startUserId,TOKEN,total,startDate):
    global_roleId = startRoleId
    global_userId = startUserId
    # 数据的开始时间
    startDateStr = datetime.datetime.strptime(startDate,"%Y-%m-%d")
    startDateSeconds = time.mktime(startDateStr.timetuple())
    # 保存爬取的数据
    list_master = []
    list_detail = []
    # 已爬取的用户
    list_beSpiderdRoleID = []
    list_beSpiderdRoleID.append(global_roleId)
    # 已爬取的比赛
    list_beSpiderGame = []

    # 主记录查询参数集合
    masterParamsList = []
    # 战绩主页面URL
    masterUrl = 'https://ssl.kohsocialapp.qq.com:10001/play/getmatchlist'
    masterParamsTemp = {
        'gameId':20001,
        'roleId': global_roleId,
        'lastTime':0, # 第一页默认值为0
        'userId': global_userId, #userId != null
        'token':TOKEN
    }
    masterParamsList.append(deepcopy(masterParamsTemp))

    # 战绩详情URL
    detailUrl = 'https://ssl.kohsocialapp.qq.com:10001/play/getplaydetail'
    detailParamsTemp = {
        'gameSeq': '',
        'roleId': '',
        'userId': '',
        'relaySvrId': '',
        'gameSvrId': '',
        'pvpType': '',
        'token': TOKEN
    }
    # 一直循环，直到 masterParamsList 值为空
    while(len(masterParamsList)>0):
        hasMore = True;
        try:
            # 分页爬取
            while(hasMore):# 先获取战绩列表
                masterJson = getJsonResult(masterUrl,masterParamsList[0])
                if(masterJson == ''):
                    print(datetime.datetime.now(),'masterJson is empty')
                    continue
                # 从主记录中解析
                returnCode = masterJson['returnCode'] # 状态码，0为正常
                returnMsg = masterJson['returnMsg'] # 错误信息，ok为正常

                # 获取数据异常，则休眠10秒，然后跳过
                # -10461：服务器繁忙
                # -30408：召唤师隐藏了个人战绩，无法查看
                # -30139：操作速度太快,请休息一下
                if(returnCode != 0):
                    print(datetime.datetime.now(),'❌❌❌ master',returnCode,returnMsg)
                    hasMore = False
                    if(returnCode == -10461 or returnCode == -30139):
                        time.sleep(10)
                    continue
                data = masterJson['data'] # 比赛信息
                hasMore = data['hasMore'] # 是否还有数据未加载
                lastTime = data['lastTime'] # 下一页的比赛时间
                battle_list = data['list'] # 战绩详情

                # 保存战绩主记录信息
                data['url'] = masterUrl
                data['_id']= masterParamsList[0]
                list_master.append(data)
                print(datetime.datetime.now(),'master',len(list_master))
                # 遍历战绩详情
                for item in battle_list:
                    try:
                        isGaming = item["isGaming"]
                        if(isGaming): # 如果是正在进行的比赛，不进行采集
                            continue
                    except KeyError as e:
                        pass
                    # 解析主记录中的比赛信息
                    dteventtime = item["dteventtime"]
                    # gametype = item["gametype"] # 4:排位，5:匹配
                    # wincamp = item["wincamp"]
                    # gametime = item["gametime"] # 比赛时间
                    # killcnt = item["killcnt"] # 杀人数
                    # deadcnt = item["deadcnt"] # 死亡数
                    # assistcnt = item["assistcnt"] # 助攻数
                    # gameresult = item["gameresult"]
                    # mvpcnt = item["mvpcnt"] # 胜方MVP
                    # losemvp = item["losemvp"] # 败方MVP
                    # heroId = item["heroId"] # 英雄ID
                    # AcntCamp = item["AcntCamp"]
                    # mapName = item["mapName"] # 地图名称
                    # detailUrl = item["detailUrl"]
                    # rampage = item["rampage"]
                    gameSvrId = item["gameSvrId"]
                    relaySvrId = item["relaySvrId"]
                    gameSeq = item["gameSeq"]
                    pvpType = item["pvpType"]
                    # multiCampRank = item["multiCampRank"]
                    # battleType = item["battleType"]
                    # branchEvaluate = item["branchEvaluate"]
                    # oldMasterMatchScore = item["oldMasterMatchScore"]
                    # newMasterMatchScore = item["newMasterMatchScore"]
                    # battleRoyaleEvaluate = item["battleRoyaleEvaluate"]
                    # desc = item["desc"]
                    # heroIcon = item["heroIcon"]

                    # 爬取的数据量是否已经足够 & 比赛时间是否在范围中
                    if(total>0):
                        if(long(dteventtime)>=startDateSeconds):# 获取明细的参数拼接
                            detailParams = deepcopy(detailParamsTemp)
                            detailParams['gameSeq'] = gameSeq
                            detailParams['userId'] = global_userId
                            detailParams['relaySvrId'] = relaySvrId
                            detailParams['gameSvrId'] = gameSvrId
                            detailParams['pvpType'] = pvpType
                            detailParams['token'] = TOKEN
                            detailParams['roleId'] = '' # 同一场比赛，不同人的roleId不同，所以先把roleId置为空，然后把detailParams保存起来

                            # 已经爬取过的比赛，不再爬取
                            if(detailParams in list_beSpiderGame):
                                continue
                            # 将detailParams存起来，用来过滤已经爬过的比赛
                            list_beSpiderGame.append(detailParams)

                            detailParams['roleId'] = global_roleId

                            detailJson = getJsonResult(detailUrl,detailParams)
                            if(detailJson == ''):
                                print(datetime.datetime.now(),'detailJson is empty')
                                continue
                            detailReturnCode = detailJson['returnCode'] # 状态码，0为正常
                            detailReturnMsg = detailJson['returnMsg'] # 错误信息，ok为正常

                            if(detailReturnCode != 0):
                                print(datetime.datetime.now(),'❌❌❌ detail',detailReturnCode,detailReturnMsg)
                                if(detailReturnCode == -10461 or detailReturnCode == -30139):
                                    time.sleep(10)
                                continue

                            # 解析明细
                            detailData = detailJson['data']
                            pvpTypename = detailData["pvpTypename"]
                            battleType = detailData["battleType"]
                            usedtime = detailData["usedtime"] # 用时：分钟
                            eventtime = detailData["eventtime"] # 游戏开始时间
                            mapName = detailData["mapName"]
                            acntcampBlue = detailData["acntcampBlue"] # 蓝色方
                            acntcampRed = detailData["acntcampRed"] # 红色方

                            # 保存战绩明细信息
                            detailData['url'] = detailUrl
                            del detailParams['roleId']
                            detailData['_id']= detailParams
                            list_detail.append(detailData)
                            print(datetime.datetime.now(),'detail',len(list_detail))

                            # 将玩家信息拼接到一个list
                            acntcampList = acntcampBlue + acntcampRed
                            for person in acntcampList:
                                # 解析
                                roleId = person["roleId"]
                                # roleName = person["roleName"]
                                # heroName = person["heroName"]
                                userId = person["userId"]
                                # vest = person["vest"]
                                # jumpType = person["jumpType"]
                                # heroId = person["heroId"] # 英雄ID
                                # killCnt = person["killCnt"] # 杀人数
                                # deadCnt = person["deadCnt"] # 死亡数
                                # assistCnt = person["assistCnt"] # 助攻数
                                # totalOutputPerMin = person["totalOutputPerMin"] # 分均输出
                                # totalHurtHeroCntPerMin = person["totalHurtHeroCntPerMin"]
                                # totalBeHurtedCntPerMin = person["totalBeHurtedCntPerMin"]
                                # hero1TripleKillCnt = person["hero1TripleKillCnt"]
                                # godLikeCnt = person["godLikeCnt"]
                                # winMvp = person["winMvp"] # 胜方MVP
                                # hero1UltraKillCnt = person["hero1UltraKillCnt"]
                                # hero1RampageCnt = person["hero1RampageCnt"]
                                # loseMvp = person["loseMvp"] # 败方MVP
                                # vopenid = person["vopenid"]
                                # hero1GhostLevel = person["hero1GhostLevel"] # 英雄等级
                                finalEquipmentInfoList = person["finalEquipmentInfo"] # 出装信息
                                finalEquipmentInfo = ','.join(str(x['equId']) for x in finalEquipmentInfoList) # 用逗号拼接装备ID
                                # disGradeLevelId = person["disGradeLevelId"]
                                # gradeLevelId = person["gradeLevelId"]
                                # gradeLevel = person["gradeLevel"]
                                # maxKill = person["maxKill"] # 杀人最多，1:true，0:false
                                # maxHurt = person["maxHurt"] # 伤害最多
                                # maxAssist = person["maxAssist"] # 助攻最多
                                # maxTower = person["maxTower"] # 推塔最多
                                # maxBeHurt = person["maxBeHurt"] # 死亡最多
                                # heroSkillID = person["heroSkillID"]
                                # heroSkillIcon = person["heroSkillIcon"]
                                isSelf = person["isSelf"]
                                # isFriend = person["isFriend"]
                                # heroIcon = person["heroIcon"]
                                # gradeGame = person["gradeGame"] #评分
                                # totalHurtPercent = person["totalHurtPercent"]
                                # totalHurtHeroCntPercent = person["totalHurtHeroCntPercent"] # 对英雄伤害占比
                                # totalBeHurtedCntPercent = person["totalBeHurtedCntPercent"] # 承受英雄伤害占比
                                # acntcamp = person["acntcamp"] # 1:蓝方，2:红方
                                # playerId = person["playerId"]
                                # gameScore = person["gameScore"]
                                # sixKill = person["sixKill"]
                                # sevenKill = person["sevenKill"]
                                # eightKill = person["eightKill"]
                                # branchEvaluate = person["branchEvaluate"]
                                # heroPosition = person["heroPosition"]
                                # usedtime = person["usedtime"]
                                # gametype = person["gametype"]
                                # newGrow = person["newGrow"]
                                # newBattle = person["newBattle"]
                                # newSurvive = person["newSurvive"]
                                # newHurtHero = person["newHurtHero"]
                                # newKDA = person["newKDA"]
                                # maxMvpScore = person["maxMvpScore"]
                                # totalWinNum = person["totalWinNum"]
                                # totalLostNum = person["totalLostNum"]
                                # avgMvpScore = person["avgMvpScore"] # （使用该英雄）历史平均得分
                                # isMI = person["isMI"]
                                # oldMasterMatchScore = person["oldMasterMatchScore"]
                                # newMasterMatchScore = person["newMasterMatchScore"]
                                # heroId2 = person["heroId2"]
                                # hero2GhostLevel = person["hero2GhostLevel"]
                                # defeatAcntRatio = person["defeatAcntRatio"]
                                # hero2SkillIcon = person["hero2SkillIcon"]
                                # hero2SkillID = person["hero2SkillID"]
                                # hero2Icon = person["hero2Icon"]
                                # joinGamePercent = person["joinGamePercent"] #参团率
                                # sabcgrow = person["sabcgrow"]
                                # sabcbattle = person["sabcbattle"]
                                # sabcsurvive = person["sabcsurvive"]
                                # sabchurtHero = person["sabchurtHero"]
                                # sabcKDA = person["sabcKDA"]
                                # battleRoyaleEvaluate = person["battleRoyaleEvaluate"]
                                # battleRoyaleTotalTeamNum = person["battleRoyaleTotalTeamNum"]
                                # battleRoyaleGrade = person["battleRoyaleGrade"]
                                # battleRoyaleTimeToLive = person["battleRoyaleTimeToLive"]
                                # battleRoyaleGrowValue = person["battleRoyaleGrowValue"]
                                # hornorPercent = person["hornorPercent"]

                                # 将value为list的数据进行处理（否则转Dataframe会报错）
                                person['finalEquipmentInfo'] = finalEquipmentInfo
                                person.pop('finalHero2EquipmentInfo')
                                person.pop('heroScoreGrade')

                                if(isSelf == 1 or roleId in list_beSpiderdRoleID): # 如果是自己，或者是已经爬取过的用户，则不再次获取比赛主记录
                                    continue

                                list_beSpiderdRoleID.append(roleId)
                                # 拼接获取玩家比赛主记录的请求参数
                                global_roleId = roleId
                                masterParams = deepcopy(masterParamsTemp)
                                masterParams['roleId'] = global_roleId
                                masterParams['lastTime'] = 0 # 第一页默认值为0
                                masterParams['userId'] = global_userId
                                masterParams['token'] = TOKEN
                                masterParamsList.append(masterParams)
                        else:
                            # 因为列表中的数据是按时间顺序倒序排列的，所以当时间不满足时，则之后的时间也不满足，所以直接爬取下一个openId
                            hasMore = False
                            break;
                    else:
                        # 数据已足够，则保存数据，结束程序
                        saveData(list_master,'masterInfo')
                        saveData(list_detail,'detailInfo')
                        exit()
                # 详情遍历完，获取下一页
                masterParamsList[0]['lastTime'] = lastTime
        except Exception as e:
            print("main Error") # repr()：给出较全的异常信息，包括异常信息的类型，如1/0的异常信息
            traceback.print_exc()
        finally:
            # 移除已经爬取的openId[0]
            masterParamsList.pop(0)
            # 保存数据
            # if(len(list_master) >= 100):
            saveData(list_master,'masterInfo')
            saveData(list_detail,'detailInfo')
            print(datetime.datetime.now(),'saveData success：','masterInfo',len(list_master),'detailInfo',len(list_detail))
            total -= len(list_detail)
            print('total:',total)
            list_master = []
            list_detail = []
    print('🐶🐶🐶🐶🐶🐶🐶🐶🐶🐶🐶🐶🐶🐶🐶🐶🐶🐶🐶🐶🐶🐶🐶🐶')

# 获取master的最后一条数据
def getLastMasterInfo():
    data =''
    try:
        conn,db = getDB()
        count = db['masterInfo'].find().count()
        if(count == 0):
            data = ''
        cursor = db['masterInfo'].find().limit(1).skip(count-1)
        data = cursor[0]
    except Exception as e:
        print("getLastMasterInfo Error")
        traceback.print_exc()
    finally:
        conn.close()
        return data

# 查询比赛记录详情的数量
def getDetailInfoCount():
    count = 0
    try:
        conn,db = getDB()
        count = db['detailInfo'].find().count()
    except Exception as e:
        print("getLastMasterInfo Error")
        traceback.print_exc()
    finally:
        conn.close()
        return count

if __name__ == '__main__':
    TOKEN = 'UGFbh8ed'
    # total = 10000 # 总共取1万条数据
    total = 100000
    startDate = '2018-11-01'
    startRoleId = '1225872175'
    startUserId = '360083271'
    # 获取master的最后一条数据
    lastMasterInfo = getLastMasterInfo()
    if(lastMasterInfo != ''):
        startRoleId = lastMasterInfo['_id']['roleId']
        startUserId = lastMasterInfo['_id']['userId']
    # 查询已爬取比赛记录详情的数量
    count = getDetailInfoCount()
    total -= count

    main(startRoleId,startUserId,TOKEN,total,startDate)
