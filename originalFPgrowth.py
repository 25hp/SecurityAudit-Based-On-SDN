# coding=utf-8
'''

@author:Breeze modified
'''


class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode  # needs to be updated
        self.children = {}

    def inc(self, numOccur):
        self.count += numOccur

    def disp(self, ind=1):
        print '  ' * ind, self.name, ' ', self.count
        for child in self.children.values():
            child.disp(ind + 1)


def createTree(recordNum,dataSet, minSup=0.5):  # create FP-tree from dataset but don't mine
    headerTable = {}
    # go over dataSet twice
    # ItemNums=len(dataSet)
    for trans in dataSet:  # first pass counts frequency of occurance
        for item in trans:
            # if item=="":
            #     pass
            # else:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    for k in headerTable.keys():  # remove items not meeting minSup
        if headerTable[k]*1.0/recordNum < minSup:
            del (headerTable[k])
    freqItemSet = set(headerTable.keys())  # L1
    # print 'freqItemSet: ', freqItemSet
    if len(freqItemSet) == 0: return None, None  # if no items meet min support -->get out
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]  # reformat headerTable to use Node link
    # print 'headerTable: ', headerTable
    retTree = treeNode('Null Set', 1, None)  # create tree
    for tranSet, count in dataSet.items():  # go through dataset 2nd time
        localD = {}
        for item in tranSet:  # put transaction items in order
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
            updateTree(orderedItems, retTree, headerTable, count)  # populate tree with ordered freq itemset
    return retTree, headerTable  # return tree and header table


def updateTree(items, inTree, headerTable, count):
    if items[0] in inTree.children:  # check if orderedItems[0] in retTree.children
        inTree.children[items[0]].inc(count)  # incrament count
    else:  # add items[0] to inTree.children
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        if headerTable[items[0]][1] == None:  # update header table
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    if len(items) > 1:  # call updateTree() with remaining ordered items
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)


def updateHeader(nodeToTest, targetNode):  # this version does not use recursion
    while (nodeToTest.nodeLink != None):  # Do not use recursion to traverse a linked list!
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


def ascendTree(leafNode, prefixPath):  # ascends from leaf node to root
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)


def findPrefixPath(basePat, treeNode):  # treeNode comes from header table
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats


def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1])]  # (sort header table)
    for basePat in bigL:  # start from bottom of header table
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        print 'finalFrequent Item: ', newFreqSet  # append to set
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        # print 'condPattBases :',basePat, condPattBases
        # 2. construct cond FP-tree from cond. pattern base
        myCondTree, myHead = createTree(condPattBases, minSup)
        # print 'head from conditional tree: ', myHead
        if myHead != None:  # 3. mine cond. FP-tree
            # print 'conditional tree for: ',newFreqSet
            # myCondTree.disp(1)
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)


def mineTreeII(inTree, headerTable, minSup, preFix, freqItemList, supportData, recordCount):
    if headerTable is None:
        print 'headerTable is None'
        return None
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1])]  # (sort header table)
    for basePat in bigL:  # start from bottom of header table
        # indexLayerC=indexLayer
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        print 'finalFrequent Item: ', newFreqSet  # append to set
        # freqItemList.append(newFreqSet)
        freqItemList.append(frozenset(newFreqSet))
        supportData[frozenset(newFreqSet)] = headerTable[basePat][0] * 1.0 / recordCount
        # supportData[basePat]
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        # print 'condPattBases :',basePat, condPattBases
        # 2. construct cond FP-tree from cond. pattern base
        myCondTree, myHead = createTree(recordCount,condPattBases, minSup)
        # print 'head from conditional tree: ', myHead
        if myHead != None:  # 3. mine cond. FP-tree
            # print 'conditional tree for: ',newFreqSet
            # myCondTree.disp(1)
            mineTreeII(myCondTree, myHead, minSup, newFreqSet, freqItemList, supportData, recordCount)


def loadDataSet():
    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]

def loadTestData():
    dataSet=[]
    f=open('testData.txt','r')
    re=f.readlines()
    for i in re:
        # print i
        # print type(i)
        i=i.strip('\n')
        # print i.split(" ")
        dataSet.append(i.split(" "))
    return dataSet
def loadSimpDat():
    simpDat = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return simpDat


def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = retDict.get(frozenset(trans), 0)+1
    return retDict


def aprioriGen(Lk, k, Lset):  # cut the Lk
    """the Lk's type is set structure,the retList's element type is also set structure,
    certainly is frozenset structure
     e.g:
     [[1],[2],[3]]-->[1,2],[1,3],[2,3]"""
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
            # 前k-2项相同时，将两个集合合并
            L1 = list(Lk[i])[:k - 2]
            L2 = list(Lk[j])[:k - 2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                if (Lk[i] | Lk[j]) in Lset:  # the new set must be in the Lset (Frequsent Set)
                    retList.append(Lk[i] | Lk[j])
    return retList


def calcConf(freqSet, H, supportData, brl, minConf=0.7):
    ''' 对候选规则集进行评估 '''
    prunedH = []
    for conseq in H:
        conf = supportData[freqSet]*1.0 / supportData[freqSet - conseq]  # calculate the conf other conduct to conseq
        if conf >= minConf:
            # print freqSet - conseq, '-->', conseq, 'conf:', conf
            brl.append((freqSet - conseq, conseq, conf))
            prunedH.append(conseq)
    return prunedH


def rulesFromConseq(Lset, freqSet, H, supportData, brl, minConf=0.7):
    ''' 生成候选规则集 '''
    m = len(H[0])  # m=1
    # print 'm'
    # print m
    if (len(freqSet) > (m + 1)):
        Hmpl = aprioriGen(H, m + 1, Lset)
        Hmpl = calcConf(freqSet, Hmpl, supportData, brl, minConf)
        if (len(Hmpl) > 1):
            rulesFromConseq(Lset, freqSet, Hmpl, supportData, brl, minConf)


def generateRules(L, supportData, minConf=0.7):
    """L :Frequent set type--list
        supportData:each frequent entry's support value type--dict"""
    bigRuleList = []
    for i in range(0, len(L)):
        eleLen = len(L[i])
        if eleLen > 1:
            H1 = [frozenset([item]) for item in L[i]]
            freqSet = L[i]
            if eleLen > 2:
                rulesFromConseq(L, freqSet, H1, supportData, bigRuleList, minConf)
            else:
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList

def fpgrowthMain(data,minSupport=0.5,minConf=0.5):
    initSet = createInitSet(data)
    record_num=len(data)
    myFPtree, myHeaderTab = createTree(record_num,initSet, minSupport)

    myFreqList = []
    supportData = {}
    mineTreeII(myFPtree, myHeaderTab, minSupport, set([]), myFreqList, supportData, record_num)

    rules = generateRules(myFreqList, supportData, minConf)
    return myFreqList,supportData,rules

if __name__=='__main__':
    minSup = 0.5
    simpDat = loadDataSet()
    freqlist,supportData,rules=fpgrowthMain(simpDat,0.5,0.5)

    print 'frequent list'
    print len(freqlist)
    for item in freqlist:
        print item

    print 'supportData'
    for item in supportData:
        print item,' :',supportData[item]

    print 'rules'
    for item in rules:
        print item

    # print len(simpDat)
    # initSet = createInitSet(simpDat)
    # print 'record num'
    # record_num=0
    # for key in initSet:
    #     record_num+=initSet[key]
    # print record_num
    # myFPtree, myHeaderTab = createTree(record_num,initSet, minSup)
    # # print myFPtree
    # # myFPtree.disp()
    # myFreqList = []
    # supportData = {}
    # FreqList2 = []
    # mineTreeII(myFPtree, myHeaderTab, minSup, set([]), FreqList2, supportData, record_num)
    # print 'FreqList2'
    # print FreqList2
    # print 'supportData'
    # for item in supportData:
    #     print item,' :',supportData[item]
    #
    # rules = generateRules(FreqList2, supportData, minConf=0.5)
    # print 'rules 0.5'
    # for item in rules:
    #     print item
