const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors'); // Importe o pacote cors
const sql = require('mssql');
const app = express();
const port = 3000;
var timestamp = 0

// Use o middleware cors
app.use(cors());

// Configuração do banco de dados
const config = {
    driver: 'SQL Server',
    user: 'kaleologin',
    password: 'Gislaine470@',
    server: '192.168.0.102\\KALEOSERVER2',
    database: 'tempdb',
    options: {
        encrypt: false // Desabilitar a verificação de certificado
    }
};



app.use(bodyParser.json());

app.post('/inserir_dados', async (req, res) => {
    try {
        // Desestruturando os dados do corpo da requisição
        const { query } = req.body;
        
        // Conectando ao banco de dados
        await sql.connect(config);

        // Definindo a consulta SQL de inserção

        console.log(query)

        // Executando a consulta de inserção
        await sql.query(query);

        console.log('Valores inseridos com sucesso na tabela.');
        res.sendStatus(200);
    } catch (error) {
        console.error('Erro ao inserir valores na tabela:', error);
        res.sendStatus(500);
    } finally {
        // Fechando a conexão com o banco de dados
        await sql.close();
    }

})



app.post('/verificar_email', async (req, res) => {
    try {
        await sql.connect(config);
        const { query_email } = req.body;
        const result = await sql.query(query_email);
        // Enviar a resposta de volta ao cliente
        res.json({ result: result });
    } catch (error) {
        console.error('Erro ao verificar o email:', error);
        res.status(500).json({ error: 'Erro interno do servidor' });
    }
    finally {
        await sql.close();
    }
});


app.post("/atualiza_cadastros", async (req, res) => {
    try {
        await sql.connect(config);
        const { email } = req.body;
        
        // Construir a consulta SQL com parâmetros de consulta
        const query = ` DELETE FROM TABLETK2 WHERE email = '${email}' AND code <> 1`;

        // Executar a consulta
        const result=await sql.query(query);
        console.log(`Email ${email} retirado da lista`)
        
        res.status(200).send('Cadastros atualizados com sucesso.');
    } catch (error) {
        // Em caso de erro, envie uma resposta com o erro
        console.error('Erro ao atualizar cadastros:', error.message);
        res.status(500).send('Ocorreu um erro ao atualizar cadastros.');
    } finally {
        // Fechar a conexão com o banco de dados
        await sql.close();
    }
});

app.post('/verificar_codigo', async (req, res) => {
    try {

        const { codigo } = req.body;
        const query_code = `SELECT COUNT(*) AS count FROM TABLETK2 WHERE code = '${codigo}'`;
        console.log(query_code)
        await sql.connect(config);
        const result = await sql.query(query_code);
        const rowCount = result.recordset[0].count;
        res.json({ result: result });
        if (rowCount > 0) {
            const query_subs = `UPDATE TABLETK2 SET code = '1' WHERE code = '${codigo}'`;
            await sql.query(query_subs);
        } 
    } finally {
        await sql.close();
    }
});





app.post('/verificar_login', async (req, res) => {
    try {
        const { email, senha } = req.body;
        const query_code = `SELECT * FROM TABLETK2 WHERE email = '${email}' AND senha = '${senha}'`;
    
        await sql.connect(config);
        const result = await sql.query(query_code);
        const rowCount = result.recordset.length;
        
        if (rowCount > 0) {
            timestamp = Date.now();
            res.json({ success: true, timestamp });
        } else {
            // Login falhou
            res.json({ success: false });
        }
    } catch (error) {
        console.error('Erro ao verificar o login:', error);
        res.status(500).json({ error: 'Erro interno do servidor' });
    }
});


app.post('/menos_download', async (req, res) => {
    try {
        const { email } = req.body;

        // Atualiza a coluna 'donwload' decrementando 1
        const queryUpdate = `UPDATE TABLETK2 SET donwload = donwload - 1 WHERE email = '${email}'`;
        await sql.connect(config);
        await sql.query(queryUpdate);

        // Consulta o novo valor da coluna 'donwload'
        const querySelect = `SELECT donwload FROM TABLETK2 WHERE email = '${email}'`;
        const result = await sql.query(querySelect);
        const novoDownload = result.recordset[0].donwload; // novo valor da coluna 'donwload'

        res.json({ success: true, novoDownload });
    } catch (error) {
        console.error('Erro ao decrementar o donwload:', error);
        res.status(500).json({ success: false, error: 'Erro interno do servidor' });
    }
});


app.post('/get_downloads', async (req, res) => {
    try {
        const { email } = req.body;

        const querySelect = `SELECT donwload FROM TABLETK2 WHERE email = '${email}'`;
        const result = await sql.query(querySelect);
        const novoDownload = result.recordset[0].donwload; // novo valor da coluna 'donwload'

        res.json({ success: true, novoDownload });
    } catch (error) {
        console.error('Erro ao decrementar o donwload:', error);
        res.status(500).json({ success: false, error: 'Erro interno do servidor' });
    }
    
});


























app.listen(port, () => {
    console.log(`Servidor iniciado em http://localhost:${port}`);
});
