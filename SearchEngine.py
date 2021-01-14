import json
import os
import timeit

from collections import OrderedDict
from konlpy.tag import Komoran

komoran = Komoran()
search_count = 0
index_count = 0
print_number = 0
print_dict = {}

class Search:
    def KMPSearch(pat, txt):
        M = len(pat)
        N = len(txt)
        if(N==1):
            return False

        lps = [0] * M

        # Preprocess the pattern
        Search.computeLPS(pat, lps)

        i = 0  # index for txt[]
        j = 0  # index for pat[]
        while i < N:
            # 문자열이 같은 경우 양쪽 인덱스를 모두 증가시킴
            if pat[j] == txt[i]:
                i += 1
                j += 1
            # Pattern을 찾지 못한 경우
            elif pat[j] != txt[i]:
                # j!=0인 경우는 짧은 lps에 대해 재검사
                if j != 0:
                    j = lps[j - 1]
                # j==0이면 일치하는 부분이 없으므로 인덱스 증가
                else:
                    i += 1

            # Pattern을 찾은 경우
            if j == M:
                return True
        return False

    def computeLPS(pat, lps):
        leng = 0  # length of the previous longest prefix suffix

        # 항상 lps[0]==0이므로 while문은 i==1부터 시작한다.
        i = 1
        while i < len(pat):
            # 이전 인덱스에서 같았다면 다음 인덱스만 비교하면 된다.
            if pat[i] == pat[leng]:
                leng += 1
                lps[i] = leng
                i += 1
            else:
                # 일치하지 않는 경우
                if leng != 0:
                    # 이전 인덱스에서는 같았으므로 leng을 줄여서 다시 검사
                    leng = lps[leng - 1]
                    # 다시 검사해야 하므로 i는 증가하지 않음
                else:
                    # 이전 인덱스에서도 같지 않았다면 lps[i]는 0 이고 i는 1 증가
                    lps[i] = 0
                    i += 1

class Array:
    def __init__(self, get_array):
        self.array = get_array

    def print_array(self):
        for i in self.array:
            print(i.print())

    def search_array(self, data):
        print_array = []
        data_array = []
        d_array = []
        data = komoran.nouns(data)
        #이진탐색
        for j in data:
            k = self.binarySearch(j, 0, len(self.array)-1)
            if(k != None):
                print_array.append(k)

        for i in range(0, len(self.array)):
            global search_count
            search_count += 1
            title = self.array[i].title_print()
            check1 = self.array[i].data_searchcheck()
            if(check1 == True):
                data_array = self.array[i].data_search()
                data_array = self.tf(data_array)
            for j in data:
                check = Search.KMPSearch(title, j)
                if(check == True):
                    print_array.append(i)
                elif(check1 == True) :
                    a = self.binarySearch2(data_array, j, 0, len(data_array) - 1)
                    if(a != None):
                        d_array.append((i, a))

        d_array = self.count_sort(d_array)
        print_array = self.print_append(print_array, d_array)

        global print_number
        print_number = len(print_array)
        for i in print_array:
            print("Title : ", self.array[i].title_print())
            id = self.array[i].id_print()
            print("ID : ", id)
            print("문서 내용 : ", print_dict[id])
            #print(self.array[i].print2())

    def array_dedup(self, array):
        array = list(OrderedDict.fromkeys(array))
        return array

    def print_append(self, print, darray):
        for i in darray:
            print.append(i[0])
            if(len(print) >= 10):
                print = self.array_dedup(print)
            if(len(print) >= 10):
                break
        if(len(print)<10):
            print = self.array_dedup(print)
        return print

    def count_sort(self, array):
        for i in range(len(array) - 1):
            for j in range(len(array) - i - 1):
                if (array[j][1] < array[j + 1][1]):
                    array[j], array[j + 1] = array[j + 1], array[j]
        return array

    def binarySearch(self, target, left, right):
        while (left <= right):
            global search_count
            search_count += 1
            mid = (left + right)//2
            if(self.array[mid].title_print() == target):
                return mid
            elif(self.array[mid].title_print()<target):
                left = mid+1
            else:
                right = mid-1
        return None

    def binarySearch2(self, array, target, left, right):
        while (left <= right):
            mid = (left + right)//2
            if(array[mid][0] == target):
                return array[mid][1]
            elif(array[mid][0]<target):
                left = mid+1
            else:
                right = mid-1
        return None

    def tf(self, array):
        sum = 0
        for i in range(0, len(array)):
            sum += array[i][1]
        for i in range(0, len(array)):
            array[i][1] /= sum
        return array

class Node:
    def __init__(self, data):
        self.data = data
        self.count = 0
        self.next = None

class LinkedList:
    def __init__(self, data):
        self.head = Node(data)

    def add(self, data):
        cur = self.head
        while(cur.next != None):
            cur = cur.next
        cur.next = Node(data)

    def delete_duplicate(self):
        cur = self.head
        dict = {}
        prev = None
        while(cur != None):
            if cur.data in dict:
                prev.next = cur.next
                if(cur.data == self.head.data):
                    self.head.count += 1
                else:
                    prev.count +=1
            else:
                dict[cur.data] = True
                prev = cur
            cur = cur.next


    def print(self):
        cur = self.head
        res = []
        while cur != None:
            res.append((cur.data, cur.count))
            cur = cur.next
        return str(res)

    def print2(self):
        cur = self.head
        res = []
        #res.append(cur.data)
        print("문서 제목 : ", cur.data)
        cur = cur.next
        print("문서 ID : ", cur.data)
        #res.append(cur.data)
        cur = cur.next.next
        while(cur != None):
            res.append(cur.data)
            cur = cur.next
            
        print("문서 내용 : ")
        return str(res)

    def id_print(self):
        cur = self.head
        cur = cur.next
        return cur.data

    def title_print(self):
        cur = self.head
        return cur.data

    def title_search(self, data):
        cur = self.head
        if(cur.data == data):
            return True
        return False

    def data_searchcheck(self):
        cur = self.head
        cur = cur.next.next.next
        if(cur == None):
            return False
        else :
            return True

    def data_search(self):
        data_array = []
        cur = self.head
        cur = cur.next.next.next
        while(cur!=None):
            data_array.append([cur.data, cur.count])
            cur = cur.next
        return data_array

    def delete_link(self):
        cur = self.head
        prev = cur.next.next
        cur = cur.next.next.next
        while(cur != None):
            if(cur.count<2):
                prev.next = cur.next
            else:
                prev = cur
            cur = cur.next

    def count_check(self):
        cur = self.head
        while(cur != None):
            if(cur.count>=4):
                print(cur.count)
                return True
            cur = cur.next
        return False

    def concat(self, head2):
        cur = self.head
        while(cur!=None):
            cur = cur.next
        cur.next = head2
        return self

class JsonProcess:
    def processjson(dirname):
        with open(dirname, 'r', encoding='UTF8') as f:
            data = json.loads(f)

        print(json.dumps(data))

    def search(dirname):
        count = 0
        file_data = OrderedDict()
        filename = os.listdir(dirname)
        for i in filename:
            filename1 = os.listdir(dirname + '\\' + i)
            for j in filename1:
                print(j)

                with open(dirname + "\\" + i + "\\" + j, 'r', encoding='UTF8') as f:
                    for line in f:
                        data = json.loads(line.strip())
                        for item in data:
                            file_data[item] = data[item]
                        with open("C:\\Users\\user\\Desktop\\project\\json\\json" + str(count), 'w',
                                  encoding="utf-8") as make_file:
                            json.dump(file_data, make_file, ensure_ascii=False, indent='\t')
                        count += 1

    def read_json(dirname, j):
        global count
        file_data = OrderedDict()
        with open(dirname, 'r', encoding='UTF8') as f:
            for line in f:
                data = json.loads(line.strip())

                for item in data:
                    file_data[item] = data[item]
                with open('words.json' + str(count), 'w', encoding="utf-8") as make_file:
                    json.dump(file_data, make_file, ensure_ascii=False, indent='\t')
                count += 1

class Indexing:
    def sort_insert(self, array, title):
        global index_count
        index_count += 1
        index = len(array)
        for i in range(len(array)):
            if(array[i].title_print()>title):
                index = i
                break
        return index

    def indexing_json(self, route):
        array = []

        file_list = os.listdir(route)
        for i in file_list:
            with open(route+'\\'+i, 'r', encoding='UTF8') as f:
                try:
                    print(i)
                    json_data = json.load(f)
                    title = json_data['title']
                    head = LinkedList(title)
                    id = int(json_data['id'])
                    head.add(id)
                    head.add(json_data['url'])
                    print_dict[id] = json_data['text'][0:200]
                    nouns = komoran.nouns(json_data['text'])
                    nouns = sorted(nouns)
                    for i in nouns:
                        head.add(i)
                    head.delete_duplicate()
                    head.delete_link()
                    if(len(array)!=0):
                        i = self.sort_insert(array, title)
                        array.insert(i, head)
                    else:
                        global index_count
                        index_count = 1
                        array.append(head)
                    #if(len(text_array)!=0):

                except UnicodeDecodeError:
                    print("Unicode error")
                    pass

                except Exception:
                    print("Exception error")
                    pass

        return array

loute2 = "C:\\Users\\user\\Desktop\\project\\json2"

#read_json(loute1)
#search(loute)
#print(komoran.morphs(u'우왕 코모란도 오픈소스가 되었어요'))
#f = JsonProcess()
#f.processjson(loute2)

#index = indexing()
#index.indexing_json(loute2)
a = Indexing()
b = Array(a.indexing_json(loute2))
print("===========================")

while(True):
    print("========================================")
    sea = input('검색할 문자를 입력하세요\n')
    start = timeit.default_timer()
    b.search_array(sea)
    protime = timeit.default_timer() - start
    print("검색된 문서의 수 : ", print_number)
    print("걸린시간 : ", protime)
    print("인덱싱된 문서 갯수 : ", index_count)
    print("전체 검색된 문서 : ", search_count)


