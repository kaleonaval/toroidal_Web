

import  {serviceID,templateID} from '/cadastro/ambient.js';


var host = window.location.hostname
var hostAtual = window.location.hostname;
var urlAtual = window.location.href


alert(urlAtual)

// Determine se estamos em localhost
var novoUrl="https://"+host.replace("/","")+":3000"
console.log(novoUrl)

// Determine se estamos em localhost
var novoUrl;
if (hostAtual === 'localhost' || hostAtual === '127.0.0.1') {
    novoUrl = 'http://localhost:3000'; // Use o localhost como base
} else {
    novoUrl = 'https://' + hostAtual; // Use o domínio atual como base
}

console.log(novoUrl)


async function verifica_email() {
    const query_email1 = `SELECT COUNT(*) AS count FROM TABLETK2 WHERE email = '${email_}'`;
    console.log(query_email1);
    
    try {
        const response = await fetch(novoUrl + '/verificar_email', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query_email: query_email1
            })
        });

        if (response.ok) {
            const data = await response.json();
            const { result } = data;
            const rowCount = result.recordset[0].count;

            if (rowCount > 0) {
                return false

            } else {
                await preenche_dados()
                return true
            }
        } else {
            throw new Error('Erro ao verificar o email:', response.statusText);
            
        }
    } catch (error) {
        console.error('Erro ao enviar solicitação fetch:', error);
    }
}







async function preenche_dados() {
    email_ = document.getElementById("email_cadastro").value;

    const query = `
    INSERT INTO TABLETK2(cliente, cpf, email, senha, code, donwload)
    VALUES ('${cliente_}', '${cpf_}', '${email_}', '${senha_}', '${code_}', '${download}')
    `;

    try {
        const response = await fetch(novoUrl +'/inserir_dados', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: query
            })  
        });
        if (response.ok) {
            console.log('Valores inseridos com sucesso na tabela.');
            var caminho_html=urlAtual+"/cadastro/codigo"
            document.location.href = caminho_html
        } else {
            throw new Error('Erro ao inserir valores na tabela:', response.statusText);
        }
    } catch (error) {
        console.error('Erro ao enviar solicitação fetch:', error);
    }
};


async function atualiza_cadastros() {
    var email = document.getElementById("email_cadastro").value;

    try {
        const response = await fetch(novoUrl+'/atualiza_cadastros', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email
            })
        });

        if (!response.ok) {
            throw new Error('Erro ao atualizar cadastros');
        }
        alert('Cadastros atualizados com sucesso!');
    } catch (error) {
        console.error('Erro:', error.message);
        alert('Ocorreu um erro ao atualizar cadastros.');
    }
}


document.getElementById("cadastroButton2").addEventListener("click", function() {
    emailjs.init("pQ_4FrYYyWkHH1NjJ");
    email_ = document.getElementById("email_cadastro").value;
    senha_=document.getElementById("cadastroSenha").value;
    cpf_ =document.getElementById("cadastroCPF").value;
    cliente_=email_;
    atualiza_cadastros()
    setTimeout(function() {

    var length = cpf_.length;
    if (length !== 11) {
        alert("CPF INVÁLIDO");
        return; // Isso fará com que a função retorne imediatamente
    } else {
        // Continue com o restante do código se o comprimento for 11
    }

    if (senha_.length<6){
        alert("Senha deve ter no mínimo 6 digitos");
        return;
    }else{
    }


    var email = email_;
    code_ = Math.floor(Math.random() * 900000) + 100000;
    
    console.log(code_, email_);
    if (email_.includes("@")) {
        var params = {
            sendername: "tkpropeller@gmail.com",
            to: email_,
            message:`Seja bem vindo ao site Tk Propeller.\n A sua SENHA: ${senha_} \n\n\n O seu CÓDIGO: ${code_} \n\n\n Senha e código sujeitos a alteração caso código não seja válidado. \n\n Att Equipe TK `
        };
    } else { 
        alert("Email inválido");
        return;
    }

    verifica_email().then(email_valido => {
        if (email_valido) {
            console.log(params);
            var ooi=emailjs.send(serviceID, templateID, params)
            console.log("Email enviado");
            console.log(ooi)
            alert("Email enviado com sucesso!");

        } else {
            alert("Este email já existe nos cadastros");
            location.reload();
        }
    });
}, 2000);
}











    
);