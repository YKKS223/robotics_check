import collections
import copy
import cv2

class meiro():
    def __init__(self,filename):
        self.filename = filename
        self.lsNM = self.con_img_to_ls(self.filename)
        if self.lsNM is None:
            print(f"エラー：画像ファイル '{self.filename}' を読み込めません。ファイルパス/整合性を確認してください。")
            return
        self.setst()
        self.setgl()
        self.solve()

    def con_img_to_ls(self,filename):
        img = cv2.imread(filename, 0) #グレースケールで読み込み
        if img is None:
            return None
        self.N = len(img)             #横のピクセル長
        self.M = len(img[0])          #縦のピクセル長
        lsNM = [['.']*(self.M) for i in range(self.N)]
        cnt = 0
        for i in range(self.N):
            for j in range(self.M):
                if img[i][j] <= 180: #道を通れないor壁を突き抜ける場合は値を変える
                    lsNM[i][j] = '#' #壁を作る
                    cnt += 1
        return lsNM

    def setst(self):
        def printCoor(event,x,y,flags,param):
            if event == cv2.EVENT_LBUTTONDOWN:
                print('start =',y, x)
                self.st = (y,x)
        img = cv2.imread(self.filename)
        cv2.namedWindow('setstart',cv2.WINDOW_NORMAL)
        cv2.setMouseCallback('setstart',printCoor)
        cv2.moveWindow('setstart', 100, 200)
        while(1):
            cv2.imshow('setstart',img)
            #ESCキーでブレーク
            if cv2.waitKey(20) & 0xFF == 27:
                break
        cv2.destroyAllWindows()
        self.lsNM[self.st[0]][self.st[1]] = 'S'
            
    def setgl(self):
        def printCoor(event,x,y,flags,param):
            if event == cv2.EVENT_LBUTTONDOWN:
                print('goal =',y, x)
                self.gl = (y,x)
        img = cv2.imread(self.filename)
        cv2.namedWindow('setgoal',cv2.WINDOW_NORMAL)
        cv2.setMouseCallback('setgoal',printCoor)
        cv2.moveWindow('setgoal', 100, 200)
        while(1):
            cv2.imshow('setgoal',img)
            #ESCキーでブレーク
            if cv2.waitKey(20) & 0xFF == 27:
                break
        cv2.destroyAllWindows()
        self.lsNM[self.gl[0]][self.gl[1]] = 'G'
                
    def solve(self):  #BFSをやるところ
        d = collections.deque([self.st])
        dxy = [(1,0),(0,1),(-1,0),(0,-1)]
        used = [[False]*self.M for i in range(self.N)]
        lscost = [[float('INF')]*self.M for i in range(self.N)]
        lscost[self.st[0]][self.st[1]] = 0
        comefrom = [[-1]*self.M for i in range(self.N)]
        while d:
            x,y = d.popleft()
            if used[x][y]:
                continue
            used[x][y] = True
            for dx,dy in dxy:
                if 0 <= x+dx < self.N and 0 <= y+dy < self.M:
                    if used[x+dx][y+dy]:
                        continue
                    if self.lsNM[x+dx][y+dy] == '#':
                        continue
                    if lscost[x+dx][y+dy] > lscost[x][y] +1:
                        lscost[x+dx][y+dy] = lscost[x][y] +1
                        comefrom[x+dx][y+dy] = (x,y)
                        d.append((x+dx,y+dy))
        print('cost =',lscost[self.gl[0]][self.gl[1]])
        #たどり着けない場合
        if lscost[self.gl[0]][self.gl[1]] == float('INF'):
            print('No ans')
            exit()
        #経路復元
        self.lsNM2 = copy.deepcopy(self.lsNM)
        x,y = self.gl
        while True:
            x,y = comefrom[x][y]
            if self.lsNM2[x][y] == 'S':
                break
            self.lsNM2[x][y] = 'o'

    def output(self,outputname,line_thickness=100): #画像の作成と出力
        lsimg = cv2.imread(self.filename)
        for i in range(self.N):
            for j in range(self.M):
                if self.lsNM2[i][j] == 'o':
                     lsimg[i][j] = [0, 0, 255]
        cv2.imwrite(outputname, lsimg)

if __name__ == "__main__":
    filename = input('filename = ')
    meiroA = meiro(filename)
    if meiroA.lsNM is not None:
        meiroA.output('ans2.jpg')
