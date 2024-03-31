import { OBJLoader } from '../three.js-master/examples/jsm/loaders/OBJLoader.js';
import * as THREE from '../three.js-master/build/three.module.js';
import { OrbitControls } from '/three.js-master/examples/jsm/controls/OrbitControls.js';
var urlAtual = window.location.href;

var time = 100000000000000000000000000
var minhaClasse = null;
var downloads = 0;
var variableName="None"
const fileUrl = 'toroide_inicial.obj'; // Substitua 'arquivo.txt' pelo caminho do seu arquivo de texto  
verificarTokenServidor()

fetch(fileUrl)
    .then(response => response.text())
    .then(text => {
        variableName= text
        minhaClasse = init(variableName)
        ;})

var objLoader = null

// Seleciona todos os controles deslizantes
const sliders = document.querySelectorAll('input[type="range"]');

// Para cada controle deslizante, adicione um evento de input
sliders.forEach(slider => {
    // Adiciona um evento de input ao controle deslizante
    slider.addEventListener('input', function() {
        // Atualiza o valor exibido ao lado do controle deslizante
        const output = document.querySelector(`#${this.id}_value`);
        output.textContent = this.value;
    });
});



const canvas= document.querySelector("#root")
const largura = canvas.clientWidth;
const altura = canvas.clientHeight;

document.getElementById("my_button1").addEventListener("click", function() {
    var button = document.getElementById("my_button1");
    variableName = button.getAttribute("data-variable");
    button.setAttribute("data-variable", 'None')
    var botao = document.getElementById("my_button2");

    botao.innerText = "Aguarde...";

    // Adiciona uma pequena pausa antes de continuar
    setTimeout(function() {
        if (!minhaClasse) {
            minhaClasse = init(variableName);
        } else {
            minhaClasse.update(variableName);
        }

        // Atualiza o texto do botão de volta para "Atualizar"
        botao.innerText = "Atualizar";
    }, 1000); // Tempo de pausa em milissegundos

});

document.getElementById("download").addEventListener("click", async function() {
    if (!verificarTokenServidor()) {
        return;
    }

    var texto = variableName;
    var name = texto.split('\n')[6].replace("#", "");
    var blob = new Blob([texto], { type: "text/plain" });
    var link = document.createElement("a");
    await menos_download_();

    console.log(downloads)
    if (downloads>0){
    link.download = name + ".obj"; // Nome do arquivo
    link.href = window.URL.createObjectURL(blob);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
    
});

function verificarTokenServidor() {
    time = localStorage.getItem('token'); // Certifique-se de declarar a variável com 'const' ou 'let'
    const dif = (Date.now() / 1000) - time; // Calcula a diferença em segundos
    const button = document.getElementById("login_button");

    if (dif > 600) {
        alert("Para baixar o modelo, primeiro faça o login.");
        button.style.display = "block";
        localStorage.setItem('token', 0); // Armazena o token no localStorage
        localStorage.setItem('client', 0);
        return false;
    } else {
        
        button.style.display = "none";
        return true;
    }
}

document.getElementById("login_button").addEventListener("click", function() {
    var time = 100000000000000000000000000
    var minhaClasse = null;
    var downloads = 0;
    var variableName="None"
    const fileUrl = 'toroide_inicial.obj'; // Substitua 'arquivo.txt' pelo caminho do seu arquivo de texto  
    window.location.href = urlAtual.substring(0, urlAtual.lastIndexOf('/'));

});



async function menos_download_() {

        const email = localStorage.getItem('client');
        const response = await fetch('http://localhost:3000/menos_download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email })
        })
        await get_download()
    }
    
        
async function get_download() {

        const email = localStorage.getItem('client');
        const response = await fetch('http://localhost:3000/get_downloads', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email })
        }
        )
        const data = await response.json()
        downloads = data.novoDownload
        if (downloads>0){
            alert(`Você tem apenas mais ${downloads} downloads disponíveis.`)
        }
        else{alert("Você não tem mais downloads disponíveis")}

        downloads = data.novoDownload
    }






function init(variableName) {
    if (!objLoader) {
        objLoader = new OBJLoader();
    }
    

    const renderer = new THREE.WebGLRenderer({
        antialias:true,

    })

    renderer.setSize(largura,altura);
    canvas.appendChild(renderer.domElement);
    
    
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xeeeeee);
    
    const camera = new THREE.PerspectiveCamera(
        45,
        largura /altura,
        1,
        2000
    );
    camera.position.set(500, 100, 1000);
    
    var object = objLoader.parse(variableName); // Parse do texto diretamente
    // Calcular e normalizar os vetores normais
    object.traverse((child) => {
        if (child.isMesh) {
            child.geometry.computeVertexNormals();
            child.material.side = THREE.DoubleSide;
        }
    });
    object.scale.set(50, 50, 50);
    scene.add(object);
    
    // Funções de callback de carga não são necessárias ao carregar diretamente o texto
    
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xfffffd, 0.5);
    directionalLight.position.set(0, 1, 0); // from top
    const light_front = new THREE.DirectionalLight(0xffffff, 0.3);
    directionalLight.position.set(1, 0, 0); // from top
    const back_front = new THREE.DirectionalLight(0xffffff, 0.1);
    directionalLight.position.set(1, 1, 1); // from top
    
    scene.add(directionalLight);
    scene.add(light_front);
    scene.add(back_front);
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true; // smooth camera movement
    controls.dampingFactor = 0.25;
    controls.screenSpacePanning = false;
    
    const animate = function () {
        requestAnimationFrame(animate);
        controls.update();
        renderer.render(scene, camera);
    };
    
    animate();

    // Retorna a instância da classe para que possa ser reutilizada
    return {
        update: function(newVariableName) {
            scene.remove(object);

            // Atualize o objeto com o novo valor
            const newObject = objLoader.parse(newVariableName);
            // Remova o objeto anterior da cena
            
            // Adicione o novo objeto à cena
            newObject.traverse((child) => {
                if (child.isMesh) {
                    child.geometry.computeVertexNormals();
                    child.material.side = THREE.DoubleSide;
                }
            });
            newObject.scale.set(50, 50, 50);
            scene.add(newObject);
            // Atualize a referência para o novo objeto
            object = newObject;
        }



    };   


    
    
}
