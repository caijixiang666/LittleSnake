from bug import Bug
#蛇的类，创建贪食蛇
class Snake:
    def __init__(self):
        self.__list=[(2,2)]
        #方向
        self.__toward=(1,0)

        #加操作锁
        self.__lock=False

        #让蛇控制时间
        @property
        def sleep_time(self):
            x=10-len(self.__list)*0.5
            if x<1:
                x=1
            return x/10

    #让蛇来计分
    @property
    def score(self):
        return len(self.__list)*100-100

    #蛇转向 new_toward可能的值是up down left right
    def set_toward(self,new_toward):
        if self.__lock: #加了锁就无法改方向了
            return
        dectionary={
            'UP':(-1,0),
            'DOWN':(1,0),
            'LEFT':(0,-1),
            'RIGHT':(0,1)
        }
        target__toward=dectionary[new_toward]
        #防止180度转头
        if (target__toward[0]+self.__toward[0]==0) and (target__toward[1]+self.__toward[1]==0):
            return
        self.__toward=target__toward
        self.__lock=True #锁定方向，不然短时间内连续换方向

    #返回蛇的坐标
    @property
    def points(self):
        return self.__list

    #编写蛇某一帧的行为，帧指屏幕的一次刷新
    def action(self,bug:Bug,wall_points):
        self.__move()
        self.__eat(bug)
        return self.__dead(wall_points)

    #走
    def __move(self):
        for i in range(len(self.__list)-1,0,-1):
            self.__list[i]=self.__list[i-1]
        #蛇头坐标是蛇头原坐标+方向
        self.__list[0]=(self.__list[0][0]+self.__toward[0],
                        self.__list[0][1]+self.__toward[1])
        self.__lock=False #走了一步即可解锁

    #吃的判定
    def __eat(self,bug:Bug):
        #头和虫子坐标一致就发送吃
        if self.__list[0]==bug.point[0]:
            #虫子瞬移
            bug.quicly_move(self.__list)
            #蛇会加长
            self.__list.append(self.__list[-1])

    #死的判定  参数是墙的坐标
    def __dead(self,points):
        #判断撞墙
        if self.__list[0] in points:
            return True

        #判断撞身体
        if self.__list[0] in self.__list[1:]:
            return True
        return False