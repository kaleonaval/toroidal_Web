//https://6608c2fe66b2335d65c1d25a--hilarious-llama-e5e1f4.netlify.app/

var host = window.location.hostname
var hostAtual = window.location.hostname;
var urlAtual = window.location.href


alert(urlAtual)

// Determine se estamos em localhost
var novoUrl="http://"+host.replace("/","")+":3000"
console.log(novoUrl)


// Função para fazer uma requisição protegida ao servidor
async function fetchProtectedResource(url) {
    try {
        const token = localStorage.getItem('token'); // Obtém o token do localStorage

        if (!token) {
            throw new Error('Token não encontrado');
        }

        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}` // Define o token no cabeçalho Authorization
            }
        });

        if (!response.ok) {
            throw new Error('Erro ao acessar o recurso protegido');
        }

        return await response.json(); // Retorna os dados da resposta
    } catch (error) {
        console.error('Erro ao fazer a requisição protegida:', error.message);
        throw error; // Rejeita a promise com o erro
    }
}

// Função para autenticar o usuário e obter um token JWT
async function fazerLogin(email, senha) {
    try {url=novoUrl+'/verificar_login'
        console.log(url)
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, senha })
        });

        if (!response) {
            throw new Error('Erro ao verificar login');
        }

        const data = await response.json();
        console.log(data)

        if (data.success) {
            console.log(data.token)
            time=Date.now()/1000;
            localStorage.setItem('token', time); // Armazena o token no localStorage
            localStorage.setItem('client', email);
            alert('Login bem-sucedido!');
            window.location.href = urlAtual+"/toroidal_home";
            

        } else {
            throw new Error('Credenciais inválidas');
        }
    } catch (error) {
        console.error('Erro ao fazer login:', error.message);
        alert('Credenciais inválidas.');
    }
}


// Event listener para o botão de login
document.getElementById('login_button').addEventListener('click', async function() {
    const email = document.getElementById('loginUsername').value;
    const senha = document.getElementById('loginPassword').value;
    await fazerLogin(email, senha);
});

