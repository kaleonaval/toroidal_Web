
from pyscript import when,display,document,window
import time



def open_link(link):
    current_url = document.location.href
    diretorio_atual = os.path.dirname(current_url)
    print("Diretório atual:", diretorio_atual)
    caminho_html = os.path.join(diretorio_atual, link)
    document.location.href = caminho_html


def check_exist_email(email):
    data=pd.read_csv("clientes.csv",sep=";")
    lista=data["Email"].to_list()
    if email in lista:
        window.alert("Email já esta cadastrado")

    else:
        code=random.randint(100000, 999999)
        temp_df = pd.DataFrame({'Email': [email], 'Senha':['11'], 'CPF':['11'], 'Code': [code]})
        data = pd.concat([data, temp_df], ignore_index=True)
        print(data)
        data.to_csv("clientes.csv")
        data=pd.read_csv("clientes.csv",sep=";")
        print(data)
        button=document.getElementById("send_email")
        button.setAttribute("data-variable", code)
        print(f"Código é {code}")
        button.click()
        for i in range(0,2):
            print(i)
            time.sleep(1)
        open_link("codigo.html")
    

@when("click","#cc")
def olacavalo():
    code=document.getElementById("code_email").value
    driver = 'SQL Server'
    server = 'DESKTOP-EJIT1M1\SQLEXPRESS'
    db1 = 'KALEOSQL'
    tcon = 'yes'
    uname = 'kaleologin'
    pword = 'Gislaine470@'



@when("click","#cadastroButton2")
def enviar_email():
    email=document.getElementById("email_cadastro").value
    print(email)
    approved_to_in=check_exist_email(email)
