from plotter import Plotter
xmin = 10000000000
ymin = 10000000000
xmax = -10000000000
ymax = -10000000000
def isRayIntersectsSegment(poi,s_poi,e_poi):
    if s_poi[1]==e_poi[1]:  #Excluding parallel and coincident with the ray, the first and last endpoints of the line segment coincide
        # https://cloud.tencent.com/developer/article/1515808，29/09/2019，蛰虫始航
        return False
    if s_poi[1]>poi[1] and e_poi[1]>poi[1]:  #The line segment is above the ray
        # https://cloud.tencent.com/developer/article/1515808，29/09/2019，蛰虫始航
        return False
    if s_poi[1]<poi[1] and e_poi[1]<poi[1]:  #The line segment is below the ray
        # https://cloud.tencent.com/developer/article/1515808，29/09/2019，蛰虫始航
        return False
    if s_poi[1]==poi[1] and e_poi[1]>poi[1]:  #The intersection point is the upper endpoint, corresponding to the spoint
        # https://cloud.tencent.com/developer/article/1515808，29/09/2019，蛰虫始航
        return False
    if e_poi[1]==poi[1] and s_poi[1]>poi[1]:  #The intersection point is the lower endpoint, corresponding to the spoint
        # https://cloud.tencent.com/developer/article/1515808，29/09/2019，蛰虫始航
        return False
    if s_poi[0]<poi[0] and e_poi[1]<poi[1]:  #The line segment is to the left of the ray
        # https://cloud.tencent.com/developer/article/1515808，29/09/2019，蛰虫始航
        return False

    xseg=e_poi[0]-(e_poi[0]-s_poi[0])*(e_poi[1]-poi[1])/(e_poi[1]-s_poi[1])  #Find the intersection point
    # https://cloud.tencent.com/developer/article/1515808，29/09/2019，蛰虫始航
    if xseg<poi[0]:  #The intersection point is to the left of the starting point of the ray
        # https://cloud.tencent.com/developer/article/1515808，29/09/2019，蛰虫始航
        return False
    return True  #After ruling out the above
def isPoiWithinPoly(poi,poly):
    global xmin
    global xmax
    global ymin
    global ymax
    sinsc=0  #Number of intersections
    x0 = poi[0]
    y0 = poi[1]
    if x0<xmin and y0<ymin or x0>xmax and y0>ymax:  # Loop to judge whether the point is outside the smallest rectangle of the polygon create.
        return "outside"
    for epoly in poly:
        for i in range(len(epoly)-1): #[0,len-1]
            # https://cloud.tencent.com/developer/article/1515808，29/09/2019，蛰虫始航
            s_poi=epoly[i]
            e_poi=epoly[i+1]
            x1 = s_poi[0]
            y1 = s_poi[1]
            x2 = e_poi[0]
            y2 = e_poi[1]
            if x0>=min(x1,x2) and x0<=max(x1,x2) and y0>=min(y1,y2) and y0<=max(y1,y2) and (y2-y0)*(x1-x0)==(y1-y0)*(x2-x0):
                # Loop to judge if a point is on a polygon.
                return "boundary"

    for epoly in poly:  #Loop each edge-point curve->each polygon is a two-dimensional array of[[x1,y1],...[xn,yn]]
            # https://cloud.tencent.com/developer/article/1515808，29/09/2019，蛰虫始航
        for i in range(len(epoly)-1): #[0,len-1]
            s_poi=epoly[i]
            e_poi=epoly[i+1]
            if isRayIntersectsSegment(poi,s_poi,e_poi): # https://cloud.tencent.com/developer/article/1515808，29/09/2019，蛰虫始航
                sinsc+=1   #If an intersection exists, add 1
                    # https://cloud.tencent.com/developer/article/1515808，29/09/2019，蛰虫始航

    return "inside" if sinsc%2==1 else "outside" 
    #If the intersection is cardinal, it is on the inside. If the intersection point is even, it is outside.
    # https://cloud.tencent.com/developer/article/1515808，29/09/2019，蛰虫始航
def main():
    global xmin
    global xmax
    global ymin
    global ymax
    input_list = []
    poly_list = []
    p_list=[[]]
    c = []
    plotter = Plotter()
    print('read polygon.csv')
    with open("polygon.csv","r",encoding='utf-8') as f:   #Import polygon.csv
        for i in f.readlines():
            i=i.strip().split(",")
            if i[0]=="id":
                continue
            xmin = min(xmin,float(i[1]))
            xmax = max(xmax,float(i[1]))
            ymin = min(ymin, float(i[2]))
            ymax = min(ymax, float(i[2]))
            poly_list.append([float(i[1]),float(i[2])]) #Add the coordinates to the list
            p_list[0].append([float(i[1]),float(i[2])])
    print('read input.csv')
    with open("input.csv","r",encoding='utf-8') as f: #Import input.csv
        for i in f.readlines():
            i=i.strip().split(",")
            if i[0]=="id":
                continue
            input_list.append([float(i[1]),float(i[2])])  #Add the coordinates to the list
    print('categorize points')
    for i in input_list:
        c.append(isPoiWithinPoly(i, p_list))  #Classify
    print('write output.csv')
    with open("output.csv","w",encoding='utf-8')as f: #Output to csv file
        f.write("id"+","+"category"+"\n")
        for i in range(len(input_list)):
            f.write(str(i+1)+","+c[i]+"\n")
    print('plot polygon and points')
    x=[]
    y=[]
    for point in poly_list:
        x.append(point[0])
        y.append(point[1])
    plotter.add_polygon(x,y)  #Draw polygon
    a=[]
    b=[]
    for point in input_list:
        a.append(point[0])
        b.append(point[1])
    for i in range(len(input_list)):
        plotter.add_point(a[i],b[i],c[i])  #Draw text points
        import matplotlib.pyplot as plt  #https://matplotlib.org, John Hunter
        plt.hlines(b[i], a[i], 8, 'orange', '-', label='ray')  #Draw ray
        plt.legend(loc='lower right')

    plotter.show()


if __name__ == '__main__':
    main()
