import pygame,sys
import numpy as np
from time import sleep
pygame.init()

size = width, height = 900,600

black = 0, 0, 0
white=(255,)*3
screen = pygame.display.set_mode(size)
ln=300
l=np.linspace(10,width-10,10)+300j

#l=np.full([150],200+200j,np.complex128)

def bez(l,t):
    while l.shape[0]>1:
        l=l[:-1,:]*t+l[1:,:]*(1-t)
    return l.ravel()
def draw_bez(l,c=white):
    p=[(int(x.real),int(x.imag)) for x in bez(l[:,None],np.linspace(0,1,150))]
    if len(p)==1:
        pygame.draw.circle(screen, c, p[0], 2)
    else:
        pygame.draw.lines(screen,c,False,p)
def hbez(l,t,k,c=white):
    
    while l.shape[0]>k:
        l=l[:-1,:]*t+l[1:,:]*(1-t)
    for i in range(l.shape[1]):

        draw_bez(l[:,i],c)
attached=None
radius=7
from math import factorial
def c(x,y):
    z=np.zeros_like(x)
    zr=z.ravel()
    for i,(j,k) in enumerate(zip(x.ravel(),y.ravel())):
        zr[i]=factorial(j)/(factorial(k)*factorial(j-k))
    return z
while 1:
    e=pygame.mouse.get_pos()
    e=e[0]+1j*e[1]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if attached is not None:
                attached=None
            else:
                for ii,i in enumerate(l):
                    if abs(e-i)<radius:
                        attached=ii
        
    
    
    if attached is not None:
        l[attached]=e
    
    li=l.size
    
    ii=np.linspace(0,1,li)[:,None]
    p=np.arange(li)[None,:]
    q=p[:,::-1]
    k=ii**p*(1-ii)**q*c(np.full_like(p,li-1),p)
    ll=np.linalg.solve(k,l)
    #ll=l
    #assert 0
    screen.fill(black)
    #hbez(ll[:,None],np.linspace(0,1,4),3)
    #hbez(ll[:,None],np.linspace(0,1,4),2,(0,255,0))
    #hbez(ll[:,None],np.linspace(0,1,4),4,(0,0,255))
    draw_bez(ll)
    #pygame.draw.lines(screen,white,False,[(x.real,x.imag) for x in bez(l[:,None],np.linspace(0,1,10))])
    for i,x in enumerate(l):
        pygame.draw.circle(screen,(255,0,0),(int(x.real),int(x.imag)),radius)
    pygame.display.flip()
    sleep(0.02)
