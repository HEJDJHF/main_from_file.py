import sys
sys.path.append("./")
from plotter import Plotter

xmin = 1000000000
ymin = 1000000000
xmax = 1000000000
ymax = 1000000000
def isRayIntersectsSegment(poi,s_poi,e_poi):
    if s_poi[1]==e_poi[1]:  #排除与射线平行、重合，线段首尾端点重合的情况
        return False
    if s_poi[1]>poi[1] and e_poi[1]>poi[1]:  #线段在射线上方
        return False
    if s_poi[1]<poi[1] and e_poi[1]<poi[1]:  #线段在射线下方
        return False
    if s_poi[1]==poi[1] and e_poi[1]>poi[1]:  #交点为上端点，对应spoint
        return False
    if e_poi[1]==poi[1] and s_poi[1]>poi[1]:  #交点为下端点，对应spoint
        return False
    if s_poi[0]<poi[0] and e_poi[1]<poi[1]:  #线段在射线左边
        return False

    xseg=e_poi[0]-(e_poi[0]-s_poi[0])*(e_poi[1]-poi[1])/(e_poi[1]-s_poi[1]) #求交
    if xseg<poi[0]:  #交点在射线起点的左侧
        return False
    return True  #排除上述情况后
def isPoiWithinPoly(poi,poly):
    global xmin
    global xmax
    global ymin
    global ymax
    sinsc = 0  #交点数量
    x0 = poi[0]
    y0 = poi[1]
    if x0<xmin and y0<ymin or x0>xmax and y0>ymax: return "outside"
    for epoly in poly:
        for i in range(len(epoly)-1):  #[0,len-1]
            s_poi = epoly[i]
            e_poi = epoly[i+1]
            x1 = s_poi[0]
            y1 = s_poi[1]
            x2 = e_poi[0]
            y2 = e_poi[1]
            if x0>=min(x1,x2) and x0<=max(x1,x2) and y0>=min(y1,y2) and y0<=max(y1,y2) and (y2-y0)*(x1-x0)==(y1-y0)*(x2-x0):
                # 循环判断点是否在多边形上
                return "boundary"
        for epoly in poly:  #循环每条边点曲线->each polygon 是二维数组[[x1,y1],...[xn,yn]]
            for i in range(len(epoly)-1):  #[0,len-1]
                s_poi = epoly[i]
                e_poi = epoly[i+1]
                if isRayIntersectsSegment(poi, s_poi, e_poi):
                    sinsc+=1  #如果存在交点，则加1

        return "inside" if sinsc%2==1 else "outside"  #交点为基数，则在内部。交点为偶数，则在外部。
def main():
    global xmin
    global xmax
    global ymin
    global ymax
    input_list = []
    poly_list = []
    p_list = [[]]
    c = []
    plotter = Plotter()
    print('read polygon.csv')
    with open("polygon.csv","r",encoding='utf-8') as f:  #读取polygon.csv
        for i in f.readlines():
            i=i.strip().split(",")
            if i[0]=="id":
                continue
            xmin = min(xmin, float(i[1]))
            xmax = max(xmax, float(i[1]))
            ymin = min(xmin, float(i[2]))
            ymax = max(ymax, float(i[2]))
            poly_list.append([float(i[1]), float(i[2])])  #将坐标添加到列表里
            p_list[0].append([float(i[1]), float(i[2])])
    n = int(input("请输入点的数量："))
    for i in range(n):
        x = float(input("x:"))
        y = float(input("y:"))
        input_list.append([x,y])  #将坐标添加到列表当中
    print('categorize points')
    for i in input_list:
        c.append(isPoiWithinPoly(i,p_list))  #分类
        print('write output.csv')
    with open("output.csv","w",encoding='utf-8') as f:  #输出到csv
            f.write("id"+","+"category"+"\n")
            for i in range(len(input_list)):
                f.write(str(i+1)+"," +c[i]+ "\n")
    print('plot polygon and points')
    x = []
    y = []
    for point in poly_list:
        x.append(point[0])
        y.append(point[1])
    plotter.add_polygon(x,y)  #画出多边形
    a = []
    b = []
    for point in input_list:
        a.append(point[0])
        b.append(point[1])
    for i in range(len(input_list)):
        plotter.add_point(a[i],b[i],c[i])  #画出检测点
    plotter.show()

if __name__== '__main__':
    main()
