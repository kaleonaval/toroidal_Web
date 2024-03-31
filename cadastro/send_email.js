



document.getElementById("cadastroButton2").addEventListener("click", function() {
emailjs.init("pQ_4FrYYyWkHH1NjJ");
var to_send=document.getElementById("email_cadastro").value
var button = document.getElementById("cadastroButton2");
var code =  button.getAttribute("data-variable");
console.log(code,to_send)
if (to_send.includes("@")) {
    var params = {
        sendername: "tkpropeller@gmail.com",
        to: to_send,
        replyto: "kaleonaval.20221@poli.ufrj.br",
        message: " Seja bem vindo ao site Tk Propeller. Seu código de ativação é: \n" + code
    };

    var serviceID = "service_tv6myy8";
    var templateID = "template_od1jv6b";

    emailjs.send(serviceID, templateID, params)
        .then(function(response) {
            console.log("Email enviado")
            alert("Email enviado com sucesso!");
        }, function(error) {
            alert("Email inválido")
        });
    } else {
        console.log("Email não enviado")
        alert("Email inválido")

    }
    });