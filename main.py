#eu sei que vc pegou meu código João. 
# Dessa vez vc vai ter que se esforçar um pouco mais
# n é vc é que o MAIORAL? 
# n é vc que sabe mais que todo mundo 

from pyscript import when,display,document 
from toroidal import toroidal

@when("click","#my_button2")
def run():

    button = document.getElementById("my_button1")
    npas = int(document.getElementById("num_pas").value)
    aeao=float(document.getElementById("relacao_ae_ao").value)
    pd=float(document.getElementById("relacao_p_d").value)
    rake=float(document.getElementById("relacao_rake").value)
    diametro_boço=float(document.getElementById("diametro_boço_value").value)
    y=float(document.getElementById("y").value)
    yy=float(document.getElementById("yy").value)

    meutoroide=toroidal()
    meutoroide.generation(pas=npas,AEAO=aeao,PD1=pd,rake=rake,tronco=diametro_boço,yy=y,xx=yy)
    arquivo=meutoroide.criarobj()
    button.setAttribute("data-variable", arquivo)# ta colocando o toroidal inteiro aqui no botão 
    button1 = document.getElementById("my_button1")
    button1.click()


