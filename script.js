// Variáveis globais
let currentUser = null;
let investimentoSelecionado = null;

// Função para mostrar mensagens
function showMessage(text, type = "success") {
  const messageDiv = document.getElementById("message");
  messageDiv.textContent = text;
  messageDiv.className = `message ${type}`;
  messageDiv.style.display = "block";

  setTimeout(() => {
    messageDiv.style.display = "none";
  }, 5000);
}

// Trocar abas
function showTab(tabId) {
  // Esconder todas as abas
  document.querySelectorAll(".tab-content").forEach((tab) => {
    tab.classList.remove("active");
  });

  // Remover active dos botões
  document.querySelectorAll(".tab-btn").forEach((btn) => {
    btn.classList.remove("active");
  });

  // Mostrar aba selecionada
  document.getElementById(tabId).classList.add("active");

  // Ativar botão correspondente
  document.querySelectorAll(".tab-btn").forEach((btn) => {
    if (
      btn.textContent.includes(tabId.charAt(0).toUpperCase() + tabId.slice(1))
    ) {
      btn.classList.add("active");
    }
  });

  // Carregar dados se necessário
  if (tabId === "investimentos") {
    carregarInvestimentos();
  }
}

// Testar API
async function testarAPI() {
  try {
    const response = await fetch("/api/health");
    const data = await response.json();
    showMessage(`✅ API Online - ${data.projeto}`, "success");
  } catch (error) {
    showMessage("❌ API Offline", "error");
  }
}

// Cadastrar usuário
document
  .getElementById("registerForm")
  ?.addEventListener("submit", async function (e) {
    e.preventDefault();

    const userData = {
      nome: document.getElementById("nome").value,
      email: document.getElementById("email").value,
      senha: document.getElementById("senha").value,
      perfil: document.getElementById("perfil").value,
    };

    try {
      const response = await fetch("/api/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(userData),
      });

      const result = await response.json();

      if (result.success) {
        showMessage("✅ Cadastro realizado! Faça login.", "success");
        this.reset();
        showTab("login");
      } else {
        showMessage(`❌ ${result.message}`, "error");
      }
    } catch (error) {
      showMessage("❌ Erro de conexão", "error");
    }
  });

// Login
document
  .getElementById("loginForm")
  ?.addEventListener("submit", async function (e) {
    e.preventDefault();

    const loginData = {
      email: document.getElementById("loginEmail").value,
      senha: document.getElementById("loginSenha").value,
    };

    try {
      const response = await fetch("/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(loginData),
      });

      const result = await response.json();

      if (result.success) {
        currentUser = result.user;
        showMessage(`✅ Bem-vindo, ${currentUser.nome}!`, "success");

        // Mostrar informações do usuário
        document.getElementById("userInfo").style.display = "block";
        document.getElementById("userName").textContent = currentUser.nome;
        document.getElementById("userPerfil").textContent = currentUser.perfil;
        document.getElementById("userId").textContent = currentUser.id;

        this.reset();
        showTab("investimentos");
      } else {
        showMessage(`❌ ${result.message}`, "error");
      }
    } catch (error) {
      showMessage("❌ Erro de conexão", "error");
    }
  });

// Carregar investimentos
async function carregarInvestimentos(tipo = null) {
  const url = tipo ? `/api/investimentos?tipo=${tipo}` : "/api/investimentos";

  try {
    const response = await fetch(url);
    const investimentos = await response.json();

    const container = document.getElementById("investimentosList");
    container.innerHTML = "";

    investimentos.forEach((inv) => {
      const div = document.createElement("div");
      div.className = "investimento";
      div.innerHTML = `
                <h3>${inv.nome}</h3>
                <span class="tipo ${inv.tipo}">
                    ${
                      inv.tipo === "renda_fixa"
                        ? "🏦 Renda Fixa"
                        : inv.tipo === "renda_variavel"
                        ? "📊 Renda Variável"
                        : "🏢 Fundo"
                    }
                </span>
                <span><strong>Perfil:</strong> ${inv.perfil_minimo}</span>
                <p><strong>Rentabilidade:</strong> ${
                  inv.rentabilidade
                }% ao ano</p>
                ${
                  inv.vencimento_dias
                    ? `<p><strong>Vencimento:</strong> ${inv.vencimento_dias} dias</p>`
                    : ""
                }
                
                ${
                  ["renda_fixa", "fundo"].includes(inv.tipo)
                    ? `<button onclick="abrirModalInvestir(${inv.id}, '${inv.nome}', '${inv.tipo}')" class="btn">
                        Investir
                    </button>`
                    : ""
                }
            `;
      container.appendChild(div);
    });
  } catch (error) {
    showMessage("❌ Erro ao carregar investimentos", "error");
  }
}

// Carregar meus investimentos
async function carregarMeusInvestimentos() {
  if (!currentUser) {
    showMessage("❌ Faça login primeiro", "error");
    return;
  }

  try {
    const response = await fetch(
      `/api/meus_investimentos?usuario_id=${currentUser.id}`
    );
    const investimentos = await response.json();

    const container = document.getElementById("meusInvestimentosList");

    if (investimentos.length === 0) {
      container.innerHTML = "<p>Você ainda não tem investimentos.</p>";
      return;
    }

    let html = "";
    investimentos.forEach((inv) => {
      html += `
                <div class="investimento">
                    <h4>${inv.nome}</h4>
                    <span class="tipo ${inv.tipo}">${inv.tipo}</span>
                    <p><strong>Valor:</strong> R$ ${parseFloat(
                      inv.valor
                    ).toFixed(2)}</p>
                    <p><strong>Data:</strong> ${inv.data}</p>
                </div>
            `;
    });

    container.innerHTML = html;
  } catch (error) {
    showMessage("❌ Erro ao carregar investimentos", "error");
  }
}

// Modal de investimento
function abrirModalInvestir(id, nome, tipo) {
  if (!currentUser) {
    showMessage("❌ Faça login para investir", "error");
    showTab("login");
    return;
  }

  investimentoSelecionado = { id, nome, tipo };

  document.getElementById("modalInfo").innerHTML = `
        <p><strong>Investimento:</strong> ${nome}</p>
        <p><strong>Tipo:</strong> ${
          tipo === "renda_fixa" ? "Renda Fixa" : "Fundo"
        }</p>
        <p><strong>Seu perfil:</strong> ${currentUser.perfil}</p>
    `;

  document.getElementById("valorInvestimento").value = "";
  document.getElementById("investModal").style.display = "flex";
}

function fecharModal() {
  document.getElementById("investModal").style.display = "none";
}

async function confirmarInvestimento() {
  const valor = document.getElementById("valorInvestimento").value;

  if (!valor || parseFloat(valor) < 100) {
    showMessage("❌ Valor mínimo: R$ 100", "error");
    return;
  }

  const data = {
    usuario_id: currentUser.id,
    investimento_id: investimentoSelecionado.id,
    valor: parseFloat(valor),
  };

  try {
    const response = await fetch("/api/investir", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    const result = await response.json();

    if (result.success) {
      showMessage("✅ " + result.message, "success");
      fecharModal();
      carregarMeusInvestimentos();
    } else {
      showMessage("❌ " + result.message, "error");
    }
  } catch (error) {
    showMessage("❌ Erro de conexão", "error");
  }
}

// Simular resgate
document
  .getElementById("simularForm")
  ?.addEventListener("submit", async function (e) {
    e.preventDefault();

    const simData = {
      valor: parseFloat(document.getElementById("simValor").value),
      rentabilidade: parseFloat(
        document.getElementById("simRentabilidade").value
      ),
      dias: parseInt(document.getElementById("simDias").value),
      vencimento: parseInt(document.getElementById("simVencimento").value),
    };

    try {
      const response = await fetch("/api/simular", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(simData),
      });

      const resultado = await response.json();

      const container = document.getElementById("resultadoSimulacao");

      if (resultado.erro) {
        container.innerHTML = `
                <div class="message error">
                    <h4>❌ ${resultado.erro}</h4>
                </div>
            `;
      } else {
        container.innerHTML = `
                <div class="message success">
                    <h4>📊 Resultado da Simulação</h4>
                    <p><strong>Valor investido:</strong> R$ ${resultado.valor_investido}</p>
                    <p><strong>Rendimento bruto:</strong> R$ ${resultado.rendimento_bruto}</p>
                    <p><strong>IR descontado:</strong> R$ ${resultado.ir_descontado}</p>
                    <p><strong>Valor final:</strong> R$ ${resultado.valor_final}</p>
                    <p><strong>Dias investidos:</strong> ${resultado.dias_investido}</p>
                </div>
            `;
      }
    } catch (error) {
      showMessage("❌ Erro na simulação", "error");
    }
  });

// Fechar modal ao clicar fora
window.onclick = function (event) {
  const modal = document.getElementById("investModal");
  if (event.target === modal) {
    fecharModal();
  }
};

// Inicialização
window.onload = function () {
  showTab("home");
};
