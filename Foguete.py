import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import time
import math


tol=2.3/10**14


#Simulador Foguete de auga


#Constantes
###############################

#Masa final do foguete
mf=0.387
#Masa de auga
mw=1.5
#Presión inicial (en atm)
p0=4.5
#Radio da botella (en cm)
rb=3.3
#Radio da boquilla da botella (en cm)
r=1.25
#Densidade da auga
rhow=1000
#Volume do foguete
v0=3.3
#Coeficiente de Drag inicial
cd=0.4
#Velocidade inicial
vi=0 #En caso de querer simular etapas


##################################################
##################################################
#Fluxo compresible

#Parámetro adimensional beta
beta=1.03+0.021*1.4

#Temperatura ambiente
T0=285
#Presión ao final da descarga da auga
pb=p0*((v0+mw)/v0)**-1.4
#Temperatura ao final da descarga
T1=T0*(pb/p0)**(1-1/1.4)
print(pb)
print(T1)
#Nozzle time constant
tau=((2/0.4)*v0 *(1.2)**(2.4/0.8) )/(math.pi*r*r*math.sqrt(1.4*T1*286.9))
#tgas
tgas= tau*(((pb/(beta*1))**(0.4/2.8)-1))
print(tgas)
#Impulso
vi=pb*v0*math.sqrt(8/2.4)*(1-(beta/pb)**(2.4/2.8)+(1.2)**(1.4/0.4)*(1-(pb/(beta))**(0.4/2.4))/(pb*0.4))/(mf*math.sqrt(1.4*286.9*T1))
print(vi)
print(vi)

v0=v0-mw
def F(t, Y):
    FF = np.zeros_like(Y)
    if Y[0]>0:
        pin=p0*((v0+(mw-Y[0]))/v0)**-1.4
        ve=((pin-1)*101325/rhow)**0.5
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
nstep = 5000
t0 = 0.
tf = 15  

dt = (tf-t0)/nstep


t = np.linspace(t0,tf,nstep+1) 

# Vector de valores iniciais
Yin = ([mw,vi,0])


t1 = time.time()        

sol = solve_ivp(F, (t0,tf), Yin, t_eval=t, method='RK45', atol=tol, rtol=tol)          

Y = sol.y
pin=p0*((v0+(mw-Y[0]))/v0)**-1.4
ve=(2*(pin-1)*101325/rhow)**0.5
Isp=ve/9.8
#PLOT ALTURA
plt.figure()
plt.rc('font', family='serif')
plt.plot(t,Y[2],color='blue', label=r"Variación de h")
plt.xlabel(r'Tempo (s)')
plt.title(r"Evolución da altura en función do tempo ", fontsize=16, color='gray')
plt.legend()
#plt.savefig('2.pdf')                   

#PLOT ALTURA
plt.figure()
plt.rc('font', family='serif')
plt.plot(t[0:200],Y[0,0:200],color='blue', label=r"Variación de mw")
plt.xlabel(r'Tempo (s)')
plt.title(r"Evolución da masa de auga en función do tempo ", fontsize=16, color='gray')
plt.legend()
#plt.savefig('2.pdf')                   
plt.show() 

#PLOT ALTURA
plt.figure()
plt.rc('font', family='serif')
plt.plot(t,Y[1],color='blue', label=r"Variación de v")
plt.xlabel(r'Tempo (s)')
plt.title(r"Evolución da velocidade en función do tempo ", fontsize=16, color='gray')
plt.legend()
#plt.savefig('2.pdf')                   
plt.show() 
print(sum(Isp/len(Isp)))
print("A altura máxima é:",max(Y[2]))
