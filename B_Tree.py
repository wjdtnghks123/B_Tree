import copy
class Node : 
    def __init__(self, m) :
        self.K = [0 for _ in range(m)]
        self.n = 0
        self.P = [0 for _ in range(m+1)]
    
class B_Tree : 
    def __init__(self) : 
        self.root = None 
        return None 
    
    def insertBT(self, T, m, newKey) : 
        if self.root == None : 
            T = self.getNode(m) 
            T.K[0] = newKey 
            T.n = 1
            self.root = T 
            return self.root
        
        T = self.root 
        found, stack = self.serachPath(T, m, newKey, None)
        
        if found == True : 
            print(f"i {newKey} : The key already exists")
            return self.root
        
        finished = False 
        self.x = stack.pop(-1)
        self.y = None 
        
        while True : 
            if self.x.n < m-1 : 
                self.insertKey(T, m, self.x, self.y, newKey) 
                finished = True 
            else : 
                newKey, self.y = self.splitNode(T, m, self.x, self.y, newKey)
                if len(stack) != 0 :
                    self.x = stack.pop(-1)
                else : 
                    T = self.getNode(m)
                    T.n = 1 
                    T.K[0] = newKey 
                    T.P[0] = self.x 
                    T.P[1] = self.y 
                    self.root = T 
                    finished = True 
            if finished == True : 
                break 
        return self.root 
    
    def serachPath(self, T, m, key, stack) : 
        if (stack == None) or (len(stack) == 0) : 
            stack = []
        self.x = T 
        
        while True : 
            i = 0
            
            while ((i < self.x.n) and (key > self.x.K[i])) : 
                i += 1
            if (i <= self.x.n) and (key == self.x.K[i]) : 
                stack.append(self.x) 
                return True, stack
            stack.append(self.x) 
            self.x = self.x.P[i]
            if self.x != 0 and self.x != None : 
                continue
            break 
        
        return False, stack 
    
    def insertKey(self, T, m, x, y, newKey) -> None : 
        i = self.x.n - 1 
        while ((i >= 0) and (newKey < self.x.K[i])) : 
            self.x.K[i+1] = self.x.K[i]
            self.x.P[i+2] = self.x.P[i+1]
            i = i-1
        self.x.K[i+1] = newKey 
        
        if y != None : 
            self.x.P[i+1] = self.relinkNode 
        self.x.P[i+2] = y 
        self.x.n = self.x.n+1
        return 
    
    def splitNode(self, T, m, x, y, newKey) : 
        self.insertKey(T, m, x , y, newKey)
        self.tempNode = copy.deepcopy(self.x)
        self.centerKey = self.tempNode.K[self.tempNode.n // 2 ]

        self.x = self.getNode(m)
        self.x.n = 0 
        i = 0
        
        while(self.tempNode.K[i] < self.centerKey) : 
            self.x.K[i] = self.tempNode.K[i]
            self.x.P[i] = self.tempNode.P[i]
            i += 1
            self.x.n += 1
        self.x.P[i] = self.tempNode.P[i]
        self.newNode = self.getNode(m)
        q = 0 
        i += 1
        while(i < self.tempNode.n) : 
            self.newNode.K[q] = self.tempNode.K[i]
            self.newNode.P[q] = self.tempNode.P[i]
            i += 1
            q += 1
            self.newNode.n += 1
            
        self.newNode.P[q] = self.tempNode.P[i]
        self.relinkNode = copy.deepcopy(self.x)
        return self.centerKey , self.newNode 
    
    def getNode(self, m) : 
        return Node(m) 
        
# ----------------------------------------------------------------
    def deleteBT(self, T, m, oldKey) : 
        T = self.root 
        found, stack = self.serachPath(T, m, oldKey, None)
        if found == False : 
            print(f"d {oldKey} : The key does not exist")
            return 
        self.internal_Node = stack[-1]
        self.x = stack.pop(-1)
        self.oldKey_index = -1
        is_internal_Node = False 
        
        # 내부노드에서 발견한 경우
        for i in range(0,len(self.x.P)) : 
            if (self.x.P[i] != 0) and (self.x.P[i] != None) : 
                is_internal_Node = True
        
        if is_internal_Node : 
            
            for i in range(0,len(self.internal_Node.K)) : 
                if self.internal_Node.K[i] == oldKey : 
                    self.oldKey_index = i
            
            found2, stack = self.serachPath(self.x.P[self.oldKey_index], m, self.x.K[self.oldKey_index], stack )
            
            self.x = stack.pop(-1)
            self.temp = self.internal_Node.K[self.oldKey_index]
            for i in range(0,len(self.x.K)) : 
                if self.x.K[i] != 0 : 
                    self.newKey_index = i 
            self.internal_Node.K[self.oldKey_index] = self.x.K[self.newKey_index]
            self.x.K[self.newKey_index] = self.temp
            
        finished = False 
        self.deleteKey(self.internal_Node, m, self.x, oldKey)
        
        if len(stack) != 0 : 
            self.y = stack.pop(-1)
            
        # 여기까지는 디버그 끝, 내부노드 or 말단노드에서 key 찾고 후행키와 교체하고 삭제하기 
        # 스플릿이나 머지 안했음 
        # 스켈레톤 코드 그대로 쓰기 
        ### ----------------------------------
        
        while True : 
            if (self.root == self.x) or (self.x.n >= m//2 ) :
                #if self.x.K[0] == 0 : 
                #    for i in range(0,len(self.internal_Node.P)) : 
                #        if self.internal_Node.P[i] == self.x : 
                #            self.internal_Node.P[i] = None
                #            break
                finished = True 
                # ok
            else :
                ##############11/26# internal Node를 넣을게아닌거같은데? 하 십ㄹ
                if self.x in self.y.P : 
                    self.bestSibling_result = self.bestSibling(T, m, self.x, self.y)
                    if self.y.P[self.bestSibling_result].n > m//2 :
                        self.redistributeKeys(T, m, self.x, self.y, self.bestSibling_result)
                        finished = True 
                    else :
                        self.mergeNode(T, m, self.x, self.y, self.bestSibling_result)
                        self.x = self.y
                        if len(stack) != 0 : 
                            self.y = stack.pop(-1)
                        else : 
                            finished = True  
                else : 
                    self.bestSibling_result = self.bestSibling(T, m, self.x, self.internal_Node)
                
                    if self.internal_Node.P[self.bestSibling_result].n > m//2 :
                        self.redistributeKeys(T, m, self.x, self.internal_Node, self.bestSibling_result)
                        finished = True 
                    else :
                        self.mergeNode(T, m, self.x, self.internal_Node, self.bestSibling_result)
                        self.x = self.internal_Node 
                        
                        if len(stack) != 0 : 
                            self.y = stack.pop(-1)
                        else : 
                            if self.internal_Node.K[0] == 0 : 
                                continue
                            finished = True 
            
            if finished == True : 
                break 
        
        #if self.y.n == 0 :
        #    T = self.y.P[0]
            ### discard y node 이걸 구현해야함..귀차늠...ㅇㅇ 
        
        ## stop 
        
        pass 

    def deleteKey(self, T, m, x, oldKey) : 
        i = 0
        q = 1
        while(oldKey > x.K[i]) : 
            i += 1 
            q += 1
            
        
        while(i < x.n) :
            x.K[i] = x.K[i+1]
            x.P[q] = x.P[q+1]
            i += 1
            q += 1
        
        ### 여기 P 마지막꺼만 삭제? 옮기느 작업을 추가해야하지않나싶긴하네
        x.n -= 1 
        
                    
        return 
        
    
    def bestSibling(self, T, m, x, y) : 
        i = 0
        bestSibling_ = 0
        while (y.P[i] != self.x) : 
            i += 1
        if i == 0 :
            bestSibling_ = i+1
        elif i == y.n : 
            bestSibling_ = i-1
        elif y.P[i-1].n >= y.P[i+1].n :
            bestSibling_ = i-1 
        else : 
            bestSibling_ = i+1 
        return bestSibling_    
    
    def redistributeKeys(self, T, m, x, y, bestSibling) : 
        i = 0
        while(y.P[i] != self.x) : 
            i += 1
        bestNode = y.P[bestSibling]
        if bestSibling < i : 
            lastKey = bestNode.K[bestNode.n-1]
            self.insertKey(T, m, self.x, None, y.K[i-1])
            self.deleteKey(T, m, bestNode, lastKey)
            y.K[i-1] = lastKey
        else : 
            firstKey = bestNode.K[0]
            self.insertKey(T, m, self.x, None ,y.K[i])
            self.x.P[i+1] = bestNode.P[0]
            bestNode.P[0] = bestNode.P[1] 
            self.deleteKey(T, m, bestNode, firstKey)
            y.K[i] = firstKey
            
            
            
        pass 
    
    def mergeNode(self, T, m, x, y, bestSibling) : 
        i = 0 
        while(y.P[i] != self.x) : 
            i += 1
        bestNode = y.P[bestSibling]
        if bestSibling > i : 
            #newNode_ = copy.deepcopy(self.x)
            self.x =  y.P[bestSibling]
            bestNode = y.P[i]
            pass
            # swap(bestSibling, i)
            #swap(bestNode, x)
        else :
        #17번에서 자꾸 지랄남...ㅅㅂ 
            i -= 1 
        bestNode.K[bestNode.n] = y.K[i]
        bestNode.n += 1
        j = 0
        while(j < self.x.n) : 
            bestNode.K[bestNode.n] = self.x.K[j]
            bestNode.P[bestNode.n] = self.x.P[j]
            bestNode.n = bestNode.n+1
            j += 1
        bestNode.P[bestNode.n] = self.x.P[self.x.n] ## 여기 다시 테케 만들어서 디버그 
        self.deleteKey(T, m, y, y.K[i])
        if (y.K[0] == 0) and (y == self.root) : 
            self.root = bestNode 
        
        pass 
    
    
# ----------------------------------------------------------------
    def inorderBT(self, T, m) :
        i = 0 
        while True : 
            if len(T.P) == i+1 : 
                break
            if T.P[i] == None or T.P[i] == 0 : 
                i += 1
                continue
            self.inorderBT(T.P[i],m)
            if T.K[i] != 0 : 
                print(f"{T.K[i]}", end = " ")
            i += 1 

        for k in T.P : 
            if k != None and k != 0 : 
                return 
        for k in T.K : 
            if k == 0 or k == None : 
                continue
            print(f"{k}", end = " ")
        
        return 
            
Test = B_Tree()
f = open("File_processing/B_Tree_File/BT-input.txt","r")
arr = [] 
#for i in f : 
#    data = i.split(' ')
#    data[1] = data[1][:-2]
#    arr.append(data)

for i in f : 
    data = i.split(' ')
    data[1] = data[1][:-1]
    #arr.append(data)
    if data[0] == 'i' : 
        Test.insertBT(Test,4,int(data[1]))
    else : 
        Test.deleteBT(Test,4,int(data[1]))
        ###########
        # 삭제가 되게 꼬인다. 다 출력해보면 꼬이는 부분이 어디인지 알수있는데 
        # 거기서부터 디버그하면 될 듯.
        # P의 경로가 꼬이는 거 같은데 힘들다...하..
        pass
    print(f"{int(data[1])} >")
    Test.inorderBT(Test.root,3)
    print("")
    
print(arr)
# Test.deleteBT(Test,5,28)
pass 
