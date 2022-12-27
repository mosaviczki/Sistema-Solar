"""
Trabalho de Computação Gráfica
Sistema solar em pyOpenGL
Monique Saviczki
"""

#imports
import math
from re import I
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
import sys
from PIL import Image as Image
import numpy

#Global variables
global angle, fAspect,ResX,ResY
global rotx,roty,rotz,trans ,obsX, obsY, obsZ, obsX_ini, obsY_ini, obsZ_ini , x_ini,y_ini
global rotX, rotY, rotX_ini, rotY_ini
global SENS_ROT	
global  SENS_OBS	
global SENS_TRANSL,tetaMerc,tetaVen,tetater,tetamar,tetajuo,tetasat,tetaur,tetanet,teta
global texmercurio,texvenus,texterra,texsol,texmarte,texjup,texlua,texceu,texsat,texurano,texnetuno
global speed,pause,qobj,axis,day,orbit,last
global Nx,Ny,Nz,Rnx,Rny,Rnz,view

#variables
Nx=Ny=Nz=400
Rnx=Rny=Rnz=0
view = 1
orbit = axis = False
pause = rotx = roty = rotz = transz = transy= tranx = 0
obsX = obsY = rotX = rotY =0
obsZ = 500

tetaMerc = tetaVen = tetater = tetamar = tetajuo = tetasat = tetaur = tetanet = teta = 0
last = -1
day = 1
SENS_ROT = 5.0
SENS_OBS = 10.0
SENS_TRANSL = 10.0
speed = 1
ResX=800
ResY=600


#textures read
def readTexture(filename):
    img = Image.open(filename)
    img_data = numpy.array(list(img.getdata()), numpy.int8)
    textID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textID)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    return textID

#textures creation
def creationTexture():
    global texterra,texsol,texlua,texceu,qobj,texmarte,texjup,texmercurio,texvenus,texsat,texurano,texnetuno
    texceu = readTexture('ceu.jpg')
    texsol = readTexture('sol.jpg')
    texlua = readTexture('/img/lua.jpg')
    texterra = readTexture('/img/terra.jpg')
    texmarte = readTexture('/img/marte.jpg')
    texjup = readTexture('/img/jupiter.jpg')
    texmercurio = readTexture('/img/mercurio.jpg')
    texvenus = readTexture('/img/venus.jpg')
    texsat = readTexture('/img/saturno.jpg')
    texurano = readTexture('/img/urano.jpg')
    texnetuno = readTexture('/img/netuno.jpg')
    
#Position of view
def positionView():
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    Ilumina()
    
    if view == 1:
        glTranslatef(-obsX,-obsY,-obsZ)
        glRotatef(rotX,1,0,0)
        glRotatef(rotY,0,1,0)

    if view == 3:
        glTranslatef(-1000,-1000,-3000)
        glRotatef(rotX,1,0,0)
        glRotatef(rotY,0,1,0)

        
def whel(button,direction,x,y):
    global Ny,Rny,last

    if(direction>0):
       # Ny+=1
        Rny+= 5
        if(Rny>45):
         Rny = 45
        positionView()
    else:
        #Ny-=1
        Rny-=5
        if(Rny<-45):
         Rny =-45
        positionView() 
    glutPostRedisplay()

def motion(x,y):
    global Nz,bot,rotX,rotY,obsZ,SENS_ROT,SENS_OBS,rotY_ini,rotX_ini,y_ini,obsZ_ini

    if(bot==GLUT_LEFT_BUTTON):
        deltax = x_ini - x;
        deltay = y_ini - y;
       

        rotY = rotY_ini - deltax/SENS_ROT
        rotX = rotX_ini - deltay/SENS_ROT

    elif(bot==GLUT_RIGHT_BUTTON):
        
        deltaz = y_ini - y;
        
        obsZ = obsZ_ini + deltaz/SENS_OBS;
        

    positionView()
    glutPostRedisplay()

def keyboard(key,x,y):
    global speed,pause,Nx,Ny,Nz,Rnx,Rny,Rnz,last
    
    ascii = ord(key.upper())

    if(key==GLUT_KEY_UP):
        
         if(speed-1<0):
            speed = 0
         else:
            speed -=1				
        
    if(key==GLUT_KEY_DOWN):
        speed+=1
        
    if(key==chr(32)):
        pause+=1
        if(pause>1):
            pause=0
        if(pause==0):
         speed = 25   
         glutTimerFunc(25, Anima, 999999)
        else:
          speed = 999999  

    if(key==chr(119)):
        rad = math.radians(Rnx)
        rady = math.radians(Rny)
        Nx-= math.sin(rad)*5
        Ny-= math.sin(rady)*5
        Nz-= math.cos(rad)*5
        positionView()
    if(key==chr(115)):
        rad = math.radians(Rnx)
        rady = math.radians(Rny)
        Nx+= math.sin(rad)*5
        Ny+= math.sin(rady)*5
        Nz+= math.cos(rad)*5
        positionView()
    if(key==chr(97)):
        Rnx+=15
        last = 0
        positionView()

        
    if ascii == 100: #Letter D
        Rnx-=15
        last = 0
        positionView()

    if ascii == 49:
        glutTimerFunc(speed, Anima, 5)

    if ascii == 50:
        view = 2
        positionView( )

    glutPostRedisplay()
    
def keyboardGLUT(key,x,y):
    global speed,pause,axis,orbit,view
    

    if(key==GLUT_KEY_UP):
         
         if(speed-1<0):
            speed = 0
         else:
            speed -=1				
        
    if(key==GLUT_KEY_DOWN):
        speed+=1

    if(key==GLUT_KEY_INSERT):
           if(axis==False):
               axis=True
           else:
               axis=False
               
    if(key==GLUT_KEY_HOME):
               if(orbit==False):
                   orbit=True
               else:
                   orbit=False

    if(key==GLUT_KEY_F1):
        view = 1
        positionView()

    if(key==GLUT_KEY_F2):
        view = 3
        positionView()             
        
    glutPostRedisplay()
    
def mouse(button,state,  x,  y):
    global x_ini,y_ini,obsX_ini,obsY_ini,obsZ_ini,bot,rotX_ini,rotY_ini

    if (state==GLUT_DOWN):
        x_ini = x
        y_ini = y
        obsX_ini = obsX
        obsY_ini = obsY
        obsZ_ini = obsZ
        rotX_ini = rotX
        rotY_ini = rotY
        bot = button
        
    else:
      bot = -1
     
def Ilumina ():

    luzAmbiente=[0.2,0.2,0.2,1]
    luzDifusa=[0.7,0.7,0.7,1]
    luzEspecular=[1,1,1,1]
    posicaoLuz=[0, 0, 0,1]
    
    especularidade=[1.0,1.0,1.0,1.0]
    especMaterial = 60
   

    glShadeModel(GL_SMOOTH)
    glMaterialfv(GL_FRONT,GL_SPECULAR, especularidade)
    glMateriali(GL_FRONT,GL_SHININESS,especMaterial)
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, luzAmbiente)

    glLightfv(GL_LIGHT0, GL_AMBIENT, luzAmbiente)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, luzDifusa )
    glLightfv(GL_LIGHT0, GL_SPECULAR, luzEspecular )
    glLightfv(GL_LIGHT0, GL_POSITION, posicaoLuz )
    
    luzAmbiente=[1,1,1,1]
    luzDifusa=[0.7,0.7,0.7,1]
    luzEspecular=[1,1,1,1]
    posicaoLuz=[Nx,Ny,Nz,1]
    glLightfv(GL_LIGHT3, GL_AMBIENT, luzAmbiente);
    glLightfv(GL_LIGHT3, GL_DIFFUSE, luzDifusa );
    glLightfv(GL_LIGHT3, GL_SPECULAR, luzEspecular );
    glLightfv(GL_LIGHT3, GL_POSITION, posicaoLuz );

    rx = (math.sin(math.radians(Rnx)))
    ry = (math.sin(math.radians(Rny)))
    rz = (math.cos(math.radians(Rnx)))
    glLightfv(GL_LIGHT3, GL_POSITION, posicaoLuz )
    glLightfv(GL_LIGHT3, GL_SPOT_DIRECTION, [-rx,-ry,-rz,1])
    glLightfv(GL_LIGHT3, GL_SPOT_CUTOFF, 30.0)


    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT3)

    glEnable(GL_DEPTH_TEST)
    
def Anima(value):
    global teta,day, tetaMerc, tetaVen,tetater,tetamar,tetajuo,tetasat,tetaur,tetanet
    glutPostRedisplay()
    
    glutTimerFunc(speed,Anima, 10)
    teta += 1
    tetaMerc+=3
    tetaVen+=2.5
    tetater+=1.7
    tetamar+=1.1
    tetajuo+=0.8
    tetasat+=0.6
    tetaur+=0.3
    tetanet+=0.1

    day+=1
    if(day>366):
        day = 1
    #print speed

def init2D(r,g,b):

    glClearColor(r,g,b,1)    
    glMatrixMode (GL_PROJECTION)
    glLoadIdentity()
    
    gluPerspective (90, ResX/ResY, 1, 100000)
    #glTranslatef(0,0,-30)
    
    glMatrixMode (GL_MODELVIEW)
    positionView()
    
def Axis():
    if(axis==True):
        glPushMatrix()
        glLineWidth(5)
        glBegin(GL_LINES)
        glColor3f(1,0,0)
        glVertex3f(0,0,0)
        glVertex3f(50,0,0)
        glColor3f(0.5,0,0)
        glVertex3f(0,0,0)
        glVertex3f(-50,0,0)
        glColor3f(0,1,0)
        glVertex3f(0,0,0)
        glVertex3f(0,50,0)
        glColor3f(0,0.5,0)
        glVertex3f(0,0,0)
        glVertex3f(0,-50,0)
        glColor3f(0,0,1)
        glVertex3f(0,0,0)
        glVertex3f(0,0,50)
        glColor3f(0,0,0.5)
        glColor3f(1,0,0)
        glVertex3f(0,0,0)
        glColor3f(1,0,0)
        glVertex3f(0,0,0)
        glColor3f(1,0,0)
        glVertex3f(0,0,0)
        glVertex3f(0,0,0)
        glVertex3f(0,0,-50)
        glEnd()
        glBegin(GL_TRIANGLES)
        glColor3f(1,0,0)
        glVertex3f(50,0,4)
        glVertex3f(50,0,-4)
        glVertex3f(54,0,0)
        glVertex3f(50,4,0)
        glColor3f(1,0,0)
        glVertex3f(50,0,4)
        glVertex3f(50,-4,0)
        glVertex3f(54,0,0)
        glColor3f(0,1,0)
        glVertex3f(0,50,4)
        glVertex3f(0,50,-4)
        glVertex3f(0,54,0)
        glVertex3f(4,50,0)
        glVertex3f(-4,50,0)
        glVertex3f(0,54,0)
        glColor3f(0,0,1)
        glVertex3f(0,4,50)
        glVertex3f(0,-4,50)
        glVertex3f(0,0,54)
        glVertex3f(4,0,50)
        glVertex3f(-4,-0,50)
        glVertex3f(0,0,54)
        glEnd()
        glPopMatrix()


def TranslacaoMercurio():
    x = math.sin(math.radians(tetaMerc))*200*3
    z = math.cos(math.radians(tetaMerc))*200*3
    return x,0,z

def TranslacaoVenus():
    x = math.sin(math.radians(tetaVen))*250*3
    z = math.cos(math.radians(tetaVen))*250*3
    return x,0,z

def TranslacaoTerra():
    x = math.sin(math.radians(tetater))*300*3
    z = math.cos(math.radians(tetater))*300*3
    return x,0,z

def TranslacaoLua(ox,oy,oz):
    rad = math.radians(teta*10)
    x = math.sin(rad)*15 + ox
    z = math.cos(rad)*15 + oz
    y = oy
    return x,0,z

def TranslacaoMarte():
    x = math.sin(math.radians(tetamar))*350*3
    z = math.cos(math.radians(tetamar))*350*3
    return x,0,z

def TranslacaoJupiter():
    x = math.sin(math.radians(tetajuo))*400*3
    z = math.cos(math.radians(tetajuo))*400*3
    return x,0,z

def TranslacaoSaturno():
    x = math.sin(math.radians(tetasat))*480*3
    z = math.cos(math.radians(tetasat))*480*3
    return x,0,z

def TranslacaoUrano():
    x = math.sin(math.radians(tetaur))*550*3
    z = math.cos(math.radians(tetaur))*550*3
    return x,0,z

def TranslacaoNetuno():
    x = math.sin(math.radians(tetanet))*600*3
    z = math.cos(math.radians(tetanet))*600*3
    return x,1,z

def OrbitaMercurio(o):
    x = math.sin(math.radians(o))*200*3
    z = math.cos(math.radians(o))*200*3/2.6
    return x,0,z

def OrbitaVenus(o):
    x = math.sin(math.radians(o))*250*3
    z = math.cos(math.radians(o))*250*3/2.6
    return x,0,z

def OrbitaTerra(o):
    x = math.sin(math.radians(o))*300*3
    z = math.cos(math.radians(o))*300*3/2.6
    return x,0,z

def OrbitaMarte(o):
    x = math.sin(math.radians(o))*350*3
    z = math.cos(math.radians(o))*350*3/2.6
    return x,0,z

def OrbitaJupiter(o):
    x = math.sin(math.radians(o))*400*3
    z = math.cos(math.radians(o))*400*3/2.6
    return x,0,z

def OrbitaSaturno(o):
    x = math.sin(math.radians(o))*450*3
    z = math.cos(math.radians(o))*450*3/2.6
    return x,0,z

def OrbitaUrano(o):
    x = math.sin(math.radians(o))*500*3
    z = math.cos(math.radians(o))*500*3/2.6
    return x,0,z

def OrbitaNetuno(o):
    x = math.sin(math.radians(o))*550*3
    z = math.cos(math.radians(o))*550*3/2.6
    return x,0,z

def OrbitaLua(o,ox,oy,oz):
    rad = math.radians(o)
    x = math.sin(rad)*15 + ox
    z = math.cos(rad)*15 + oz
    y = oy
    return x,0,z

def Nave():
    glPushMatrix()
    glTranslatef(Nx,Ny,Nz)
    glRotatef(0,1,0,0)
    glRotatef(1,0,1,0)
    glRotatef(Rnx,0,1,0)
    glRotatef(-Rny,1,0,0)
    glRotatef(180,0,1,0)
    glRotatef(0,0,1,0)
    glRotatef(1,1,0,0)
    glRotatef(180,0,1,0)
    glColor3f(1,0,0)
    glutSolidCone(1,3,10,10)
    glTranslate(0,0,-1)
    glutSolidCube(2)
    glBegin(GL_TRIANGLES)
    
    glColor3f(0,0,1)
    
    glVertex3f(1,0,1)
    glVertex3f(5,4,-1)
    glVertex3f(1,0,-1)

    glVertex3f(-1,0,1)
    glVertex3f(-5,4,-1)
    glVertex3f(-1,0,-1)

    glVertex3f(1,0,1)
    glVertex3f(5,4,-1)
    glVertex3f(1,0,-1)

    glVertex3f(-1,0,1)
    glVertex3f(-5,4,-1)
    glVertex3f(-1,0,-1)

    glVertex3f(1,0,1)
    glVertex3f(5,-4,-1)
    glVertex3f(1,0,-1)

    glVertex3f(1,0,1)
    glVertex3f(5,-4,-1)
    glVertex3f(1,0,-1)

    glVertex3f(1,0,1)
    glVertex3f(5,-4,-1)
    glVertex3f(1,0,-1)

    glVertex3f(1,0,1)
    glVertex3f(5,-4,-1)
    glVertex3f(1,0,-1)

    glVertex3f(-1,0,1)
    glVertex3f(-5,-4,-1)
    glVertex3f(-1,0,-1)
    
    glEnd()

    glPopMatrix()
    
def Orbita(xt,yt,zt):
    if(orbit==True):

        #ORBITA MERCURIO
        glPushMatrix()
        glLineWidth(1)
        glColor3f(1,1,1)
        glTranslatef(20,0,5)
        glBegin(GL_LINES)
        for i in range(360):
            ox,oy,oz=OrbitaMercurio(i)
            ox1,oy1,oz1=OrbitaMercurio(i+1)
            glVertex3f(ox,oy,oz)
            glVertex3f(ox1,oy1,oz1)
        glEnd()    
        glPopMatrix()
        
        #ORBITA VENUS
        glPushMatrix()
        glLineWidth(1)
        glColor3f(1,1,1)
        glTranslatef(50,0,5)
        glBegin(GL_LINES)
        speedVenus = 4
        for i in range(360):
            ox,oy,oz=OrbitaVenus(i)
            ox1,oy1,oz1=OrbitaVenus(i+1)
            glVertex3f(631,0,240)
            glVertex3f(681,0,250)
        glEnd()    
        glPopMatrix()

        #ORBITA TERA
        glPushMatrix()
        glLineWidth(1)
        glColor3f(1,1,1)
        glTranslatef(20,0,5)
        glBegin(GL_LINES)
        for i in range(360):
            ox,oy,oz=OrbitaTerra(i)
            ox1,oy1,oz1=OrbitaTerra(i+1)
            glVertex3f(ox,oy,oz)
            glVertex3f(ox1,oy1,oz1)
        glEnd()    
        glPopMatrix()
        
        #ORBITA LUA
        glPushMatrix()
        glLineWidth(1)
        glColor3f(1,1,1)
        glTranslatef(20,0,5)
        glBegin(GL_LINES)
        for i in range(360):
            ox,oy,oz=OrbitaLua(i,xt,yt,zt)
            ox1,oy1,oz1=OrbitaLua(i+1,xt,yt,zt)
            glVertex3f(ox,oy,oz)
            glVertex3f(ox1,oy1,oz1)
        glEnd()
        glPopMatrix()

        #ORBITA MARTE
        glPushMatrix()
        glLineWidth(1)
        glColor3f(1,1,1)
        glTranslatef(20,0,5)
        glBegin(GL_LINES)
        for i in range(360):
            ox,oy,oz=OrbitaMarte(i)
            ox1,oy1,oz1=OrbitaMarte(i+1)
            glVertex3f(ox,oy,oz)
            glVertex3f(ox1,oy1,oz1)
        glEnd()    
        glPopMatrix()

        #ORBITA Jupiter
        glPushMatrix()
        glLineWidth(1)
        glColor3f(1,1,1)
        glTranslatef(20,0,5)
        glBegin(GL_LINES)
        for i in range(360):
            ox,oy,oz=OrbitaJupiter(i)
            ox1,oy1,oz1=OrbitaJupiter(i+1)
            glVertex3f(ox,oy,oz)
            glVertex3f(ox1,oy1,oz1)
        glEnd()    
        glPopMatrix()

        #ORBITA SATURNO
        glPushMatrix()
        glLineWidth(1)
        glColor3f(1,1,1)
        glTranslatef(20,0,5)
        glBegin(GL_LINES)
        for i in range(360):
            ox,oy,oz=OrbitaSaturno(i)
            ox1,oy1,oz1=OrbitaSaturno(i+1)
            glVertex3f(ox,oy,oz)
            glVertex3f(ox1,oy1,oz1)
        glEnd()    
        glPopMatrix()
        
        #ORBITA URANO
        glPushMatrix()
        glLineWidth(1)
        glColor3f(1,1,1)
        glTranslatef(20,0,5)
        glBegin(GL_LINES)
        for i in range(360):
            ox,oy,oz=OrbitaUrano(i)
            ox1,oy1,oz1=OrbitaUrano(i+1)
            glVertex3f(ox,oy,oz)
            glVertex3f(ox1,oy1,oz1)
        glEnd()    
        glPopMatrix()

        #ORBITA NETUNO
        glPushMatrix()
        glLineWidth(1)
        glColor3f(1,1,1)
        glTranslatef(20,0,5)
        glBegin(GL_LINES)
        for i in range(360):
            ox,oy,oz=OrbitaNetuno(i)
            ox1,oy1,oz1=OrbitaNetuno(i+1)
            glVertex3f(ox,oy,oz)
            glVertex3f(ox1,oy1,oz1)
        glEnd()    
        glPopMatrix()



def display():
    glClear ( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    #glTranslatef(0,0,30)
    
    Ilumina()
    
    
    qobj = gluNewQuadric()
    gluQuadricTexture(qobj, GL_TRUE)
    glEnable(GL_TEXTURE_2D)
    

    #CEU   
    glPushMatrix()
    glRotatef(teta/5,1,1,1)
    glBindTexture(GL_TEXTURE_2D,texceu)
    gluSphere(qobj,10000, 999, 999)
    glPopMatrix()

    #SOL   
    glPushMatrix()
    glRotatef(teta*3,1,1,0)
    glBindTexture(GL_TEXTURE_2D,texsol)
    gluSphere(qobj,300, 999, 999)
    glPopMatrix()
    
    #MERCURIO
    glPushMatrix()
    xm,ym,zm = TranslacaoMercurio()
    glTranslatef(20,0,5)
    glTranslatef(xm,ym,zm)
    glRotatef(teta*366,0,1,0)
    glRotatef(97, 1, 0, 0)
    glBindTexture(GL_TEXTURE_2D, texmercurio)
    gluSphere(qobj,15, 300, 300)
    glPopMatrix()

    #VENUS
    glPushMatrix()
    xm,ym,zm = TranslacaoVenus()
    glTranslatef(20,0,5)
    glTranslatef(xm,ym,zm)
    glRotatef(teta*366,0,1,0)
    glRotatef(-267, 1, 0, 0)
    glBindTexture(GL_TEXTURE_2D, texvenus)
    gluSphere(qobj,35, 200, 200)
    glPopMatrix()
  
    #TERRA
    glPushMatrix()
    xt,yt,zt = TranslacaoTerra()
    glTranslatef(20,0,5)
    glTranslatef(xt,yt,zt)
    glRotatef(teta*366,0,1,0)
    glRotatef(90,1,0,0)
    glBindTexture(GL_TEXTURE_2D, texterra)
    gluSphere(qobj,40, 10000, 10000)
    glPopMatrix()


    #LUA
    glPushMatrix()
    glTranslatef(20,0,5)
    xl,yl,zl = TranslacaoLua(xt,yt,zt)
    glTranslatef(xl,yl,zl)
    glRotatef(teta*2*366,0,1,0)
    glBindTexture(GL_TEXTURE_2D, texlua)
    gluSphere(qobj,15, 999, 999)
    glPopMatrix()
    
    
    #MARTE
    glPushMatrix()
    xm,ym,zm = TranslacaoMarte()
    glTranslatef(20,0,5)
    glTranslatef(xm,ym,zm)
    glRotatef(teta*366,0,1,0)
    glRotatef(90,1,0,0)
    glBindTexture(GL_TEXTURE_2D, texmarte)
    gluSphere(qobj,20, 10, 10)
    glPopMatrix()
    
    
    #JUPITER
    glPushMatrix()
    xm,ym,zm = TranslacaoJupiter()
    glTranslatef(20,0,5)
    glTranslatef(xm,ym,zm)
    glRotatef(teta*366,0,1,0)
    glRotatef(90,1,0,0)
    glBindTexture(GL_TEXTURE_2D, texjup)
    gluSphere(qobj,100, 10, 10)
    glPopMatrix()

    #SATURNO
    glPushMatrix()
    xm,ym,zm = TranslacaoSaturno()
    glTranslatef(20,0,5)
    glTranslatef(xm,ym,zm)
    glRotatef(teta*366,0,1,0)
    glRotatef(90,1,0,0)
    glBindTexture(GL_TEXTURE_2D, texsat)
    gluSphere(qobj,85, 10, 10)
    glPopMatrix()

    #URANO
    glPushMatrix()
    xm,ym,zm = TranslacaoUrano()
    glTranslatef(20,0,5)
    glTranslatef(xm,ym,zm)
    glRotatef(teta*366,0,2,0)
    glRotatef(90,1,0,0)
    glBindTexture(GL_TEXTURE_2D, texurano)
    gluSphere(qobj,35, 10, 10)
    glPopMatrix()

    #Netuno
    glPushMatrix()
    xm,ym,zm = TranslacaoNetuno()
    glTranslatef(20,0,5)
    glTranslatef(xm,ym,zm)
    glRotatef(teta*366,0,1,0)
    glRotatef(90,1,0,0)
    glBindTexture(GL_TEXTURE_2D, texnetuno)
    gluSphere(qobj,35, 10, 10)
    glPopMatrix()
    
    glDisable(GL_TEXTURE_2D)
    gluDeleteQuadric(qobj)


    #EIXOS
    Axis()
    #ORBITAS
    Orbita(xt,yt,zt)
    Orbita(xm,ym,zm)
    #NAVE
 
    Nave()

    
    glutSwapBuffers()



def main():
    glutInit("")
    glutInitDisplayMode (GLUT_RGB| GLUT_DOUBLE |GLUT_DEPTH)
    glutInitWindowSize (ResX, ResY)
    glutInitWindowPosition (0, 0)
    glutCreateWindow ('Sistema Solar')
    creationTexture()
    glutDisplayFunc(display)
    init2D(0.0,0.0,0.0)
    glEnable(GL_DEPTH_TEST)
    #glutTimerFunc(speed, Anima, 999999)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(keyboardGLUT)
    glutMouseFunc(mouse)
    glutMouseWheelFunc(whel)
    glutMotionFunc(motion)
    glutMainLoop() 
 
main()