import math
import numpy as np

class toroidal:
    def __init__(self):
         pass

    def generation(self,PD1=1,PD2=1,AEAO=0.4,pas=4,xx=0.15,yy=0.05,pontos=50,espx=0.15,naca2=0.6,naca3=0.12,interface=None,rake=0,tronco=0.2,coringa=3):
        self.coringa=coringa
        self.troncod=tronco
        self.rake=rake
        self.interface=interface
        self.AE=AEAO
        AEAO=AEAO*2

        diametro=1
        self.xx=xx
        self.yy=yy
        self.pas=pas
        self.diametro=diametro
        self.raio=diametro/2
        self.comppa=self.raio*(diametro - 2*self.troncod)
        self.comptoroide=self.raio*(diametro - self.troncod)
        self.espx=espx
        self.m = 0.002 # Máxima espessura em relação à corda 
        self.p = naca2  # Posição da máxima espessura em relação à corda 
        self.t = naca3 # Espessura máxima em relação à corda 
        self.pontos=pontos
        self.partes=int(self.pontos/5)
        self.malhasup1=[]
        self.malhasup2=[]
        self.malhainf1=[]
        self.malhainf2=[]
        self.asaponta=[]
        self.troncob=[]
        self.allx=[]
        self.ally=[]
        self.allz=[]
        self.curvapa1=[]
        self.curvapa2=[]
        self.pontosz = np.linspace(0, self.comppa, self.partes)
        # Crie o gráfico dos pontos
        self.malha=[]
        self.pa1=[]
        self.pa2=[]
        self.time=0
        self.plotado=False

        self.pd1=PD1
        self.pd2=PD2
        passo1=diametro*PD1
        passo2=diametro*PD2
        self.passo1 = np.degrees(math.atan(passo1/(math.pi*(diametro/2))))
        self.passo2 = np.degrees(math.atan(passo2/(math.pi*(diametro/2))))

        self.pontoslista=[]
        self.faces=[]
        self.update3d=None

        AO=math.pi*self.raio*self.raio #fixosempre
        AE=AEAO*AO
        self.c=(AE-((self.diametro*self.troncod)**2)*math.pi)/(self.comptoroide*self.pas*1.6)
        self.main()

    def triangulate_faces(self,faces):
        # Lista para armazenar as faces trianguladas
        triangulated_faces_list = []
        # Iterar sobre as faces originais
        for face in faces:
            # Triangulando a face retangular
            # Dividindo em dois triângulos: ABC e ACD
            A, B, C, D = face
            triangulated_faces_list.append((A, B, C))
            triangulated_faces_list.append((A, C, D))
        return triangulated_faces_list

    def criararco(self,pontos_x, pontos_y, raio,angle):


        diffs_x = np.diff(pontos_x)
        diffs_y = np.diff(pontos_y)
        comprimento_total = np.max(pontos_x)-np.min(pontos_x)
        
        # Calcular o ângulo total do arco correspondente
        angulo_total = (comprimento_total / raio) 

        # Criar o arco
        num_pontos = len(pontos_x)
        t_arco = np.linspace(-angulo_total / 2, angulo_total / 2, num_pontos)
        arco_x = raio * np.sin(t_arco+angle)
        arco_y = raio * np.cos(t_arco+angle)


        t_arco2 = np.linspace(angulo_total / 2, 2*np.pi-angulo_total / 2, num_pontos)

        arco_x2 = raio * np.sin(t_arco2+angle)
        arco_y2 = raio * np.cos(t_arco2+angle)
        arcotx=np.concatenate((arco_x,arco_x2))
        arcoty=np.concatenate((arco_y,arco_y2))
    
        return arco_x, arco_y,arcotx,arcoty

    def criararco2(self,points, angle_degrees):
        # Converte o ângulo de graus para radianos
        angle_radians = np.radians(angle_degrees)
        xt=np.array(points[0])
        yt=np.array(points[1])
        zt=np.array(points[2])

        xtr = xt * np.cos(angle_radians) - zt * np.sin(angle_radians)
        ztr = xt * np.sin(angle_radians) + zt * np.cos(angle_radians)

        return xtr,yt,ztr



    def criarobj(self):
            malha=self.malhanova
            dic={}
            p=1
            for superficies in malha:
                i=0
                for pontos in superficies[0]:
                    t=0
                    face=[]
                    for x in superficies[0][0]:
                        ponto=[round(superficies[0][i][t]*10,4),round(superficies[1][i][t]*10,4),round(superficies[2][i][t]*10,4)]
                        self.pontoslista.append(ponto)

                        face.append(p)
                        t+=1
                        p+=1
                    self.faces.append(face)
                    i+=1



            self.faces=self.triangulate_faces(self.faces)
            name=f"SERIE-TK-BLADES.{self.pas}-PD1.{self.pd1*1}-PD2.{self.pd2}--D.{self.diametro}-MESH.{self.pontos}-YY.{self.xx}-Y(c).{self.yy}--NACA.{self.m,self.p,self.t}--CORINGA.{self.coringa}--AE{self.AE}.obj"
           
            arquivo=f'''
# TK PROPELLER 2.0
# www.tkpropeller.com
# by Kaléo Elias Gonçalves da Silva
# Phone +55 14-99636-6900
# Toroidal Propeller
# Model: {name}
'''
            
            for ponto in self.pontoslista:
                arquivo+=f'v {ponto[0]} {ponto[1]} {ponto[2]}\n'

            for face in self.faces:
                arquivo+=(f'f {face[0]} {face[1]} {face[2]}\n')



            
            return arquivo


    # Função para calcular os pontos do perfil NACA
    def calcular_pontos_naca(self, m, p, t, c, invertida=1):
        # Gere os pontos x (coordenada horizontal) igualmente espaçados

        x = np.linspace(0, c, self.pontos)
        yt = 5 * t * c * (0.2969 * np.sqrt(x / c) - 0.1260 * (x / c) - 0.3516 * (x / c)**2 + 0.2843 * (x / c)**3 - 0.1015 * (x / c)**4)
        yc = np.zeros_like(x)

        for i in range(len(x)):
            if x[i] <= p * c:
                yc[i] = (m / p**2) * (2 * p * (x[i] / c) - (x[i] / c)**2)
            else:
                yc[i] = (m / (1 - p)**2) * ((1 - 2 * p) + 2 * p * (x[i] / c) - (x[i] / c)**2)

        # coordenadas (x, y) dos pontos
    
        if invertida==1:
            xu = x - yt * np.sin(np.arctan2(yc, x)) +c/2
            xl = x + yt * np.sin(np.arctan2(yc, x)) +c/2
            yu = yc + yt * np.cos(np.arctan2(yc, x))
            yl = yc - yt * np.cos(np.arctan2(yc, x))
        elif invertida==2:
            xu = x - yt * np.sin(np.arctan2(yc, x)) -c/2
            xl = x + yt * np.sin(np.arctan2(yc, x)) -c/2
            yu = -yc - yt * np.cos(np.arctan2(yc, x))
            yl = -yc + yt * np.cos(np.arctan2(yc, x))

        
        if invertida==1:
             return xu, yu[::-1], xl, yl[::-1]
         
        else:
            return xu, yu, xl, yl
    

    def montar_naca(self,pa):
        if pa==1:
            bb=-self.yy
            x=-self.xx
            xx=-self.espx
            a=+0.9
            b=-0.2
        else:

            bb=self.yy
            x=self.xx
            xx=self.espx
            a=-0.9
            b=+0.2

        i=1
        t=0
        for parte in self.pontosz:
            parte=parte+self.troncod/2

            self.cf=self.c*(1-parte/(4*self.comppa))
            if pa==1:
                xu, yu, xl, yl = self.calcular_pontos_naca(self.m , self.p, self.t , self.cf,2)
                #if parte<=0.3:
                 #       yu[0:int(self.pontos/5)]*=(0.3-parte)+1
            else:
                xu, yu, xl, yl = self.calcular_pontos_naca(self.m , self.p, self.t , self.cf,invertida=1)
                #if parte<=0.3:
                 #       yu[0:int(self.pontos/5)]*=(0.3-parte)+1
            t+=1


            min=np.min(xu)
            max=np.max(xu)
            if pa==2:
                xu=xu-min
                xl=xl-min
            else:
                xu=xu-max
                xl=xl-max

      #      self.ax.plot(xu, yu,parte)
      #      self.ax.plot(xl, yl,parte)

            

            angle1=self.passo1*(1-(parte-self.troncod/2)/(self.coringa*self.comppa))
            angle2=self.passo2*(1-(parte-self.troncod/2)/(self.coringa*self.comppa))
      
            if pa==1:
                   self.angle_rad = np.radians(angle1)
            if pa==2:
                   self.angle_rad = np.radians(angle2)
        
  
                    
            xt=np.hstack((xu,xl))
            yt=np.hstack((yu,yl))
            xtr = (xt ) * np.cos(self.angle_rad) - (yt ) * np.sin(self.angle_rad) 
            ytr = (xt ) * np.sin(self.angle_rad) + (yt ) * np.cos(self.angle_rad) 


            lim=int(len(xt)/2)
            xu_rotated =xtr[0:lim]
            yu_rotated = ytr[0:lim]
            xl_rotated = xtr[lim:]
            yl_rotated = ytr[lim:]

            #ADICIONA O ESP Y 
            y=x*parte**2+bb
            yu_moved = yu_rotated + y
            yl_moved = yl_rotated + y



   
            if pa==1:
                angle= math.atan((a*parte**2+b*parte+xx)/parte)


            else:
                angle= math.atan((a*parte**2+b*parte+xx)/parte)
                

            #TRANSFORMA CIRCULAR AS ASAS E ADICIONA O EXP X
            xu_moved,z,arcototalx,arcototaly=self.criararco(xu_rotated,np.full_like(yl_moved, parte),parte,angle)
            xl_moved,z,arcototalx,arcototaly=self.criararco(xl_rotated,np.full_like(yl_moved, parte),parte,angle)
            if parte==self.troncod/2:
                if pa==1:
                        self.arcototalsup=arcototalx,arcototaly
                        self.arcofragsup= xu_moved,z
                else:
                        self.arcototalinf=arcototalx,arcototaly
                        self.arcofraginf= xu_moved,z



            xu_moved[-1]=xl_moved[-1]
            xu_moved[0]=xl_moved[0]
            yl_moved[-1]=yu_moved[-1]
            yl_moved[0]=yu_moved[0]


            
                 


            #RAKE AQUI 
            yl_moved= yl_moved-(parte-0.1)*math.sin(math.radians(self.rake))
            yu_moved= yu_moved-(parte-0.1)*math.sin(math.radians(self.rake))

            asa=xu_moved,yu_moved,z,xl_moved,yl_moved,z
        #    self.ax.plot(xu_moved,yu_moved,z)
        #    self.ax.plot(xl_moved,yl_moved,z)
            asasup=[xu_moved,yu_moved,z]
            asainf=[xl_moved,yl_moved,z]
            for yyy in yl_moved:
                self.ally.append(yyy)
            for yyy in yu_moved:
                self.ally.append(yyy)

            if pa==1:
                self.pa1.append(asa)
                self.malhasup1.append(asasup)
                self.malhainf1.append(asainf)
            else:
                self.pa2.append(asa)
                self.malhasup2.append(asasup)
                self.malhainf2.append(asainf)
            self.malha.append(asa)
            i+=1
   


    def pontaproper(self):

        xu, zu, xl, zl = self.calcular_pontos_naca(0 , 0.5, self.t/2 , self.cf/1.3,1)
        yu=np.full_like(xu,(self.malhainf1[-1][1][-1]+self.malhasup2[-1][1][0])/2)
        yl=yu
        xu=xu-self.cf/1.3
        zu=zu+self.comptoroide-self.t/8+self.troncod/2
        xl=xl-self.cf/1.3
        zl=zl+self.comptoroide-self.t/8+self.troncod/2

        if self.rake>20:
                self.angle_rad= 0
        elif self.rake <-20:
                self.angle_rad=0
        else:
                self.angle_rad= self.angle_rad/2 - math.radians(self.rake)/2

   

        xur = (xu ) * np.cos(self.angle_rad) - (yu ) * np.sin(self.angle_rad) 
        yur = (xu ) * np.sin(self.angle_rad) + (yu ) * np.cos(self.angle_rad) 
        xlr = (xl ) * np.cos(self.angle_rad) - (yl ) * np.sin(self.angle_rad) 
        ylr = (xl ) * np.sin(self.angle_rad) + (yl ) * np.cos(self.angle_rad) 
       # self.ax.plot(xur,yur,zu)
       # self.ax.plot(xlr,ylr,zl)
        self.asaponta.append([xlr,ylr,zl,xur,yur,zu])

        linhax=[]
        linhay=[]
        linhaz=[]

        i=0
        for xp in self.asaponta[-1][0]:

            linhax.append(self.pa1[-2][0][i])
            linhax.append(self.pa1[-1][0][i])
            linhax.append(self.asaponta[-1][3][i])
            linhax.append(self.pa2[-1][0][i])
            linhax.append(self.pa2[-2][0][i])
            
            linhay.append(self.pa1[-2][1][i])
            linhay.append(self.pa1[-1][1][i])
            linhay.append(self.asaponta[-1][4][i])
            linhay.append(self.pa2[-1][1][i])
            linhay.append(self.pa2[-2][1][i])
            
            linhaz.append(self.pa1[-2][2][i])
            linhaz.append(self.pa1[-1][2][i])
            linhaz.append(self.asaponta[-1][5][i])
            linhaz.append(self.pa2[-1][2][i])
            linhaz.append(self.pa2[-2][2][i])
            i+=1

        i=0
        for xp in self.asaponta[-1][3]:

            linhax.append(self.pa1[-2][3][i])
            linhax.append(self.pa1[-1][3][i])
            linhax.append(self.asaponta[-1][0][i])
            linhax.append(self.pa2[-1][3][i])
            linhax.append(self.pa2[-2][3][i])
            
            linhay.append(self.pa1[-2][4][i])
            linhay.append(self.pa1[-1][4][i])
            linhay.append(self.asaponta[-1][1][i])
            linhay.append(self.pa2[-1][4][i])
            linhay.append(self.pa2[-2][4][i])
            
            linhaz.append(self.pa1[-2][5][i])
            linhaz.append(self.pa1[-1][5][i])
            linhaz.append(self.asaponta[-1][2][i])
            linhaz.append(self.pa2[-1][5][i])
            linhaz.append(self.pa2[-2][5][i])
            i+=1

        self.ponta=[linhax,linhay,linhaz]


        return xlr,ylr,zl,xur,yur,zu

    def interpolar_entre_pontos(self,x, y, z, num_pontos):
        poly_x = np.polyfit(x, y, deg=len(x) - 1)
        poly_y = np.polyfit(x, y, deg=len(x) - 1)
        poly_z = np.polyfit(x, z, deg=len(x) - 1)

        #  polinômios nos novos pontos
        novos_x = np.linspace(min(x), max(x), int(num_pontos))
        novos_y = np.polyval(poly_x, novos_x)
        novos_z = np.polyval(poly_z, novos_x)

        return novos_x, novos_y, novos_z


    def criasuperficie(self,malha,ax=0):
        x=[]
        y=[]
        z=[]
        i=0
        j=0
        while j<len(malha[0][0][0:-1]):
            i=0
            while i<len(malha[0:-1]):  
                xx=malha[i][0][j],malha[i+1][0][j],malha[i+1][0][j+1],malha[i][0][j+1]
                yy=malha[i][1][j],malha[i+1][1][j],malha[i+1][1][j+1],malha[i][1][j+1]
                zz=malha[i][2][j],malha[i+1][2][j],malha[i+1][2][j+1],malha[i][2][j+1]
                x.append(xx)
                y.append(yy)
                z.append(zz)


 
                i+=1
            j+=1
        
        
        return(x,y,z)
    
    def criasuperficiesecao(self,malha):
        x=[]
        y=[]
        z=[]

        j=0
        raio= (np.max(malha[0])-np.min(malha[0]))/2
        while j<len(malha[0])-1:  
                xx=malha[0][0]-raio,malha[0][j],malha[0][j+1],malha[0][0]-raio
                yy=malha[1][0],malha[1][j],malha[1][j+1],malha[1][0]
                zz=malha[2][0],malha[2][j],malha[2][j+1],malha[2][0]
        
                x.append(xx)
                y.append(yy)
                z.append(zz)
                j+=1

        return(x,y,z)




    def tronco(self):
        theta = np.linspace(0, 2 * np.pi, int(self.pontos*2 * np.pi*0.5))  #  0 a 2*pi
        r = (self.troncod/2)
        X = r * np.cos(theta)  
        Y = r * np.sin(theta)  
        circ1=X,np.full_like(X,min(self.ally)),Y
        circ2=X,np.full_like(X,max(self.ally)),Y
        self.troncob.append(circ1)
        self.troncob.append(circ2)
        

       # ax.plot(circ1[0],circ1[1],circ1[2], color='b')
       # ax.plot(circ2[0],circ2[1],circ2[2], color='b')




    def main(self):
             
        self.montar_naca(1)
        self.montar_naca(2)


        for asa in self.malha:
            xu, yu,zu, xl, yl,zl = asa
           # plt.plot(xu, yu, zu)
          #  plt.plot(xl, yl, zu)


        xup,yup,zup,xlp,ylp,zlp=self.pontaproper()
      #=  plt.plot(xup, yup, zup)
      #  plt.plot(xlp, ylp, zlp)

        curva=[]
        t=5
        tt=t
        for i in range(0,len(self.ponta[0]),t):
              x,y,z=self.interpolar_entre_pontos(self.ponta[0][i:i+tt],self.ponta[1][i:i+tt],self.ponta[2][i:i+tt],self.pontos/3)
              curva.append([x,y,z])


        limc=int(len(curva)/2)
        curva1=[]
        curva2=[]
        curva1.append(curva[0])
        curva2.append(curva[0])
        i=1
        for curvas in curva[1:limc]:
            curva1.append(curva[i])
            i+=1
        for curvas in curva[1:limc]:
            curva2.append(curva[i])
            i+=1
        curva1.append(curva[-1])
        curva2.append(curva[-1])
        i=0

        curvasup=curva1
        curvainf=curva2
        self.pontaproper()
        self.tronco()
        xtt,ytt,ztt=self.criasuperficie(self.troncob)
        xsc1,ysc1,zsc1=self.criasuperficiesecao(self.troncob[0])
        xsc2,ysc2,zsc2=self.criasuperficiesecao(self.troncob[1])
        xsc3,ysc3,zsc3=self.criasuperficie([self.malhainf1[0],self.malhasup1[0]])
        xsc4,ysc4,zsc4=self.criasuperficie([self.malhainf2[0],self.malhasup2[0]])
        xs1,ys1,zs1=self.criasuperficie(self.malhasup1[0:-1])
        xs2,ys2,zs2=self.criasuperficie(self.malhasup2[0:-1])
        xf1,yf1,zf1=self.criasuperficie(self.malhainf1[0:-1]) 
        xf2,yf2,zf2=self.criasuperficie(self.malhainf2[0:-1])

        xp,yp,zp=self.criasuperficie(curvasup)
        xpi,ypi,zpi=self.criasuperficie(curvainf)



        malhatotal=[xs1,ys1,zs1],[xs2,ys2,zs2],[xf1,yf1,zf1],[xf2,yf2,zf2],[xp,yp,zp],[xpi,ypi,zpi],[xsc3,ysc3,zsc3],[xsc4,ysc4,zsc4]
    
      
        self.malhanova=[]
        j=0
        for s in range(0,self.pas):
            for sup in malhatotal:
                i=0
                xx=[]
                yy=[]
                zz=[]
                for arroba in sup[0]:
                    pontos=sup[0][i],sup[1][i],sup[2][i]
                    x,y,z=self.criararco2(pontos,j*(360/self.pas))
                    xx.append(x)
                    yy.append(y)
                    zz.append(z)
                    
    
        
                    i+=1
                sup=[xx,yy,zz]
                self.malhanova.append(sup)
            j+=1

        self.malhanova.append([xsc1,ysc1,zsc1])
        self.malhanova.append([xsc2,ysc2,zsc2])
        self.malhanova.append([xtt,ytt,ztt])

