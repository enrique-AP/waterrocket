#Programa de optimización
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import math


tol=2.3/10**14
#Constantes
###############################
#Masa payload
mf=3.525
#Presión inicial (en atm)
p0=15
#Coeficiente de drag
cd=0.5
#Radio da botella (en cm)
rb=3.75
#Radio da boquilla da botella (en cm)
r=3.75
#Densidade da auga
rhow=1000
#Coeficiente de Drag inicial
cd=0.5
#Velocidade inicial
vi=0 #En caso de querer simular etapas



# create a time array
nstep = 30
Lmin = 0.5
Lmax = 20.
maxmaxh=np.zeros(nstep+1)

Lvec = np.linspace(Lmin,Lmax,nstep+1) 

for j in range(0,len(Lvec)):
    nstep = 20
    mwmin = 0.
    mf=0.1156+1.705*Lvec[j]
    vtubo=Lvec[j]*3.1969
    maxh=np.zeros(nstep+1)
    mwvec = np.linspace(0,vtubo/1.3,nstep+1)     
    for i in range(0,len(mwvec)):
        mw=mwvec[i]     
        def F(t, Y):
            FF = np.zeros_like(Y)
            v0=vtubo-mw
            if Y[0]>0:
                pin=p0*((v0+(mw-Y[0]))/v0)**-1.4
                ve=(2*(pin-1)*101325/rhow)**0.5
                FF[0] = -math.pi*(r/100)*(r/100)*rhow*ve #Derivada da masa de auga
                FF[1] = -9.81 + 2*math.pi*(r/100)*(r/100)*(pin-1)*101325/(Y[0]+mf)     -    0.5*1.225*Y[1]*Y[1]*math.pi*(rb/100)*(rb/100)*cd/(Y[0]+mf)   #Derivada da velocidade
                FF[2] = Y[1]   #Derivada posición
            else:
                if Y[1]>0:
                    FF[0] = 0
                    FF[1] = -9.81 -0.5*1.225*Y[1]*Y[1]*math.pi*(rb/100)*(rb/100)*cd/(mf)   #Derivada da velocidade
                    FF[2] = Y[1]   #Derivada posición
                else:
                    if Y[2]>0:
                        FF[0] = 0
                        FF[1] = -9.81 +0.5*1.225*Y[1]*Y[1]*math.pi*(rb/100)*(rb/100)*cd/(mf)   #Derivada da velocidade
                        FF[2] = Y[1]   #Derivada posición
                    else:
                        FF[0] = 0
                        FF[1] = 0   #Derivada da velocidade
                        FF[2] = 0   #Derivada posición
    
            return FF
                
        # create a time array
        nstep = 100000
        t0 = 0.
        tf = 10.    
        t = np.linspace(t0,tf,nstep+1) 
        # Vector de valores iniciais
        Yin = ([mw,vi,0])      
        sol = solve_ivp(F, (t0,tf), Yin, t_eval=t, method='RK45', atol=tol, rtol=tol)          
        Y = sol.y
        maxh[i]=max(Y[2])
                    
    maxmaxh[j]=max(maxh)
    
print(max(maxmaxh))

result = np.where(maxmaxh == np.amax(maxmaxh))
print(result)
    
plt.figure()
plt.rc('font', family='serif')
plt.plot(Lvec,maxmaxh,color='blue', label=r"Variación de z")
plt.xlabel(r'Lonxitude (L)')
plt.title(r"Evolución da altura máxima en función da lonxitude do foguete ", fontsize=16, color='gray')
plt.legend()
#plt.savefig('2.pdf')                   
plt.show()         
        
                    
                
        
            
    
    
    
    
    
        