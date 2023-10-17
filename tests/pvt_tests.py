import os
from context import pvt
import matplotlib.pyplot as plt  

path = os.path.abspath(os.path.dirname(__file__))
def save_plot(plt, name):
    plt.savefig(path+'/plots/'+name+'.png')
    # plt.show()

def rs_test():
    pvt1 = pvt.PVT()
    pvt1.set_api(25.)
    pvt1.set_dg(0.8)
    pvt1.set_t(80.)

    p_init = 1
    p_end = 500
    steps = 200
    p = [p_init + i/(steps-1)*(p_end - p_init) for i in range(steps)]
    rs = {40:[], 80:[], 120:[]}

    _ = plt.figure() 
    for rsi in rs.keys():
        pvt1.set_gor(rsi)
        for pi in p:
            pvt1.set_p(pi)
            pvt1.calculate_rs_Standing()
            rs[rsi].append(pvt1.get_rs())
        plt.plot(p, rs[rsi])  

    ax = plt.gca() 
    ax.legend(['GOR = '+str(i) for i in rs.keys()]) 
    plt.grid()
    plt.xlabel('p [bar]')  
    plt.ylabel('rs [m3/m3]')  
    plt.title('Rs Using Standing Correlation')  
    save_plot(plt,'rs')

def pb_test():
    pvt1 = pvt.PVT()
    pvt1.set_api(25.)
    pvt1.set_dg(0.8)
    pvt1.set_t(80.)

    gor_init = 1
    gor_end = 200
    steps = 200
    gor = [gor_init + i/(steps-1)*(gor_end - gor_init) for i in range(steps)]
    pb = {'Original':[], 'Modified':[]}
    for gori in gor:
        pvt1.set_gor(gori)
        pvt1.calculate_p_bubble_Standing_Original()
        pb['Original'].append(pvt1.get_p_bubble())
        pvt1.calculate_p_bubble_Standing()
        pb['Modified'].append(pvt1.get_p_bubble())
    _ = plt.figure() 
    plt.plot(gor, pb['Original'])  
    plt.plot(gor, pb['Modified'])  

    ax = plt.gca() 
    ax.legend(pb.keys()) 
    plt.grid()
    plt.xlabel('GOR [m3/m3]')  
    plt.ylabel('P bubble [bar]')  
    plt.title('P Bubble Using Standing Correlation')  
    save_plot(plt,'p_bubble')

def pb_test2():
    pvt1 = pvt.PVT()
    pvt1.set_api(30.)
    pvt1.set_gor(200.)
    pvt1.set_dg(0.7)

    pvt2 = pvt.PVT()
    pvt2.set_api(15.)
    pvt2.set_gor(20.)
    pvt2.set_dg(0.8)

    t_init = 1
    t_end = 120
    steps = 200
    t = [t_init + i/(steps-1)*(t_end - t_init) for i in range(steps)]
    pb = {'light':[], 'heavy':[]}
    for ti in t:
        pvt1.set_t(ti)
        pvt1.calculate_p_bubble_Standing()
        pb['light'].append(pvt1.get_p_bubble())
        
        pvt2.set_t(ti)
        pvt2.calculate_p_bubble_Standing()
        pb['heavy'].append(pvt2.get_p_bubble())
    _ = plt.figure() 
    plt.plot(t, pb['light'])  
    plt.plot(t, pb['heavy'])  

    ax = plt.gca() 
    ax.legend(pb.keys()) 
    plt.grid()
    plt.xlabel('GOR [m3/m3]')  
    plt.ylabel('P bubble [bar]')  
    plt.title('P Bubble Using Standing Correlation')  
    save_plot(plt,'p_bubble2')

def bo_test():
    pvt1 = pvt.PVT()
    pvt1.set_api(30.)
    pvt1.set_gor(200.)
    pvt1.set_dg(0.7)
    pvt1.set_t(80.)

    pvt2 = pvt.PVT()
    pvt2.set_api(15.)
    pvt2.set_gor(20.)
    pvt2.set_dg(0.8)
    pvt2.set_t(80.)

    p_init = 100
    p_end = 400
    steps = 500
    p = [p_init + i/(steps-1)*(p_end - p_init) for i in range(steps)]
    bo = {'light':[], 'heavy':[]}
    for pi in p:
        pvt1.set_p(pi)
        pvt1.calculate_rs_Standing()
        pvt1.calculate_bo_Standing(auto=True)
        bo['light'].append(pvt1.get_bo())
        
        pvt2.set_p(pi)
        pvt2.calculate_rs_Standing()
        pvt2.calculate_bo_Standing(auto=True)
        bo['heavy'].append(pvt2.get_bo())
    _ = plt.figure() 
    plt.plot(p, bo['light'])  
    plt.plot(p, bo['heavy'])  

    ax = plt.gca() 
    ax.legend(bo.keys()) 
    plt.grid()
    plt.xlabel('p [bar]')  
    plt.ylabel('Bo [m3/m3]')  
    plt.title('Bo Using Standing Correlation')  
    save_plot(plt,'bo')    

def z_test():
    pvt1 = pvt.PVT()
    pvt1.set_dg(0.6)
    pvt1.set_t(80.)

    pvt2 = pvt.PVT()
    pvt2.set_dg(0.9)
    pvt2.set_t(80.)

    p_init = 1
    p_end = 500
    steps = 500
    p = [p_init + i/(steps-1)*(p_end - p_init) for i in range(steps)]
    dg = {'dg=0.6':[], 'dg=0.9':[]}
    for pi in p:
        pvt1.set_p(pi)
        pvt1.calculate_p_pr(auto=True)
        pvt1.calculate_z_Standing(auto=True)
        dg['dg=0.6'].append(pvt1.get_z())
        
        pvt2.set_p(pi)
        pvt2.calculate_p_pr(auto=True)
        pvt2.calculate_z_Standing(auto=True)
        dg['dg=0.9'].append(pvt2.get_z())
    _ = plt.figure() 
    plt.plot(p, dg['dg=0.6'])  
    plt.plot(p, dg['dg=0.9'])  

    ax = plt.gca() 
    ax.legend(dg.keys()) 
    plt.grid()
    plt.xlabel('p [bar]')  
    plt.ylabel('z')  
    plt.title('Z Using Standing Correlation')  
    save_plot(plt,'z')    

def bg_test():
    pvt1 = pvt.PVT()
    pvt1.set_dg(0.6)
    pvt1.set_t(80.)

    pvt2 = pvt.PVT()
    pvt2.set_dg(0.9)
    pvt2.set_t(80.)

    p_init = 50
    p_end = 500
    steps = 500
    p = [p_init + i/(steps-1)*(p_end - p_init) for i in range(steps)]
    dg = {'dg=0.6':[], 'dg=0.9':[]}
    for pi in p:
        pvt1.set_p(pi)
        pvt1.calculate_p_pr(auto=True)
        pvt1.calculate_z_Standing(auto=True)
        pvt1.calculate_bg(auto=True)
        dg['dg=0.6'].append(pvt1.get_bg())
        
        pvt2.set_p(pi)
        pvt2.calculate_p_pr(auto=True)
        pvt2.calculate_z_Standing(auto=True)
        pvt2.calculate_bg(auto=True)
        dg['dg=0.9'].append(pvt2.get_bg())
    _ = plt.figure() 
    plt.plot(p, dg['dg=0.6'])  
    plt.plot(p, dg['dg=0.9'])  

    ax = plt.gca() 
    ax.legend(dg.keys()) 
    plt.grid()
    plt.xlabel('p [bar]')  
    plt.ylabel('Bg')  
    plt.title('Bg Using Standing Correlation')  
    save_plot(plt,'bg')    

def uo_test():
    pvt1 = pvt.PVT()
    pvt1.set_api(15.)
    pvt1.set_dg(0.8)

    p_init = 1
    p_end = 300
    steps = 200
    p = [p_init + i/(steps-1)*(p_end - p_init) for i in range(steps)]
    uo = {(20,50):[], (60,50):[], (20,60):[]}

    _ = plt.figure() 
    for (gor, t) in uo.keys():
        pvt1.set_t(t)
        pvt1.set_gor(gor)
        for pi in p:
            pvt1.set_p(pi)
            pvt1.calculate_rs_Standing()
            pvt1.calculate_uo_do_Standing()
            pvt1.calculate_uo_Standing(auto=True)
            uo[(gor,t)].append(pvt1.get_uo())
        plt.plot(p, uo[(gor,t)])  

    ax = plt.gca() 
    ax.legend(['GOR='+str(gor)+' T='+str(t) for (gor,t) in uo.keys()]) 
    plt.grid()
    plt.xlabel('p [bar]')  
    plt.ylabel('Uo [cP]')  
    plt.title('Uo Using Standing Correlation')  
    save_plot(plt,'uo')

if __name__ == "__main__":
    rs_test()
    # pb_test()
    # pb_test2()
    # bo_test()
    # z_test()
    # bg_test()
    uo_test()