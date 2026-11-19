const API = 'http://127.0.0.1:5000';

async function api(metodo, caminho, corpo = null) {
  const opcoes = {
    method: metodo,
    headers: { 'Content-Type': 'application/json' },
  };
  if (corpo !== null) opcoes.body = JSON.stringify(corpo); 

  const resposta = await fetch(API + caminho, opcoes);
  const dados = await resposta.json().catch(() => ({}));

  if (!resposta.ok) {
    throw new Error(dados.erro || `Erro ${resposta.status}`);
  }
  return dados;
}

// ---------- helpers de apresentação ----------

function formatarMoeda(valor) {
  return Number(valor || 0).toLocaleString('pt-BR', {
    style: 'currency', currency: 'BRL',
  });
}