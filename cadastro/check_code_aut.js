




document.getElementById("code_id_button").addEventListener("click", async function verifica_codigo() {
    var code_client= document.getElementById("code_email").value
    console.log(code_client)
    
    
    try {
        const response = await fetch('http://localhost:3000/verificar_codigo', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                codigo: code_client
            })
        });
        console.log(response.ok)
        if (response.ok) {
            const data = await response.json();
            const { result } = data;
            const rowCount = result.recordset[0].count;
            

            if (rowCount > 0) {
                alert("Este código foi aprovado");
                caminho_html="http://localhost:8080/"
                document.location.href = caminho_html

            } else {
                alert("Código incorreto");
                caminho_html="http://localhost:8080/"
                document.location.href = caminho_html
            }
        } else {
            throw new Error('Erro ao verificar o codigo:', response.statusText);
        }
    } catch (error) {
        console.error('Erro ao enviar solicitação fetch:', error);
    }
}
)