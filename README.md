📈 Bank Invest - API de Investimentos

🎯 Objetivo
Desenvolver uma API de investimentos com autenticação segura, regras de negócio específicas e interface web funcional para demonstração das funcionalidades.

🚀 Tecnologias Utilizadas
Backend: Python + Flask
Banco de Dados: SQLite
Autenticação: Hash
Frontend: HTML, CSS, JavaScript
Testes: Postman

📋 Funcionalidades Implementadas
✅ Autenticação

Cadastro de usuários com perfil (conservador, moderado, arrojado)
Login seguro com senhas armazenadas como hash
Gerenciamento de sessão

✅ Gestão de Investimentos

Listagem de investimentos disponíveis
Filtro por tipo (Renda Fixa, Renda Variável, Fundos)
Investimento em Renda Fixa (POST)
Investimento em Fundos Imobiliários (POST)
Consulta de investimentos do usuário

✅ Regras de Negócio

Tempo mínimo de resgate: 30 dias para todos os investimentos
Verificação de perfil: Usuário só pode investir em títulos adequados ao seu perfil
Cálculo de IR no resgate:
12 meses: 10% de IR
6 meses: 20% de IR
≤ 6 meses: 5% de IR

🏗️ Arquitetura do Projeto
text
bank-investimentos/
├── app.py # Aplicação Flask principal
├── database.py # Configuração do banco SQLite
├── requirements.txt # Dependências Python
├── index.html # Interface web completa
├── style.css # Estilos CSS
├── script.js # Lógica frontend
├── investimentos.db # Banco de dados (gerado automaticamente)
└── README.md # Esta documentação

bash
python app.py
http://localhost:5000

📡 Endpoints da API
Autenticação
POST /api/register - Cadastrar novo usuário
POST /api/login - Autenticar usuário

Investimentos
GET /api/investimentos - Listar todos os investimentos
GET /api/investimentos?tipo=renda_fixa - Filtrar por tipo
POST /api/investir - Realizar investimento
GET /api/meus_investimentos?usuario_id=X - Investimentos do usuário
POST /api/simular - Simular resgate com regras de negócio

🎮 Como Usar

1. Cadastro de Usuário
   json
   POST /api/register
   {
   "nome": "User 1",
   "email": "user@email.com",
   "senha": "senha123",
   "perfil": "moderado"
   }
2. Login
   json
   POST /api/login
   {
   "email": "user@email.com",
   "senha": "senha123"
   }
3. Listar Investimentos Disponíveis
   bash
   GET /api/investimentos
4. Investir em Renda Fixa
   json
   POST /api/investir
   {
   "usuario_id": 1,
   "investimento_id": 1,
   "valor": 1000.00
   }
5. Testar Regras de Resgate
   json
   POST /api/simular
   {
   "valor": 1000,
   "rentabilidade": 12.5,
   "dias": 60,
   "vencimento": 180
   }
   🗄️ Banco de Dados
   Tabelas
   usuarios

id, nome, email, senha_hash, perfil, data_criacao

investimentos

id, nome, tipo, perfil_minimo, rentabilidade_anual, vencimento_dias

user_investimentos

id, usuario_id, investimento_id, valor_investido, data_investimento, status

Investimentos Pré-cadastrados
CDB Banco X (Renda Fixa, Conservador, 12.5%)

Tesouro Selic (Renda Fixa, Conservador, 11.8%)

Ações Petrobras (Renda Variável, Moderado, 15.0%)

Fundo Imobiliário XP (Fundo, Moderado, 10.5%)

Tesouro IPCA+ (Renda Fixa, Moderado, 13.2%)

🔐 Segurança
Senhas: Armazenadas como hash SHA-256 (nunca em texto puro)

Autenticação: Verificação por comparação de hash

Perfis: Hierarquia conservador < moderado < arrojado

Validação: Todos os inputs são validados no backend

🧪 Testando com Postman
Importe a collection do Postman disponível no repositório ou use os exemplos acima.

📱 Interface Web
A aplicação inclui uma interface web completa com:

Cadastro e Login interativos

Listagem de investimentos com filtros

Formulário de investimento com validação

Simulador de resgate para testar as regras

Dashboard com investimentos do usuário

⚙️ Regras de Negócio Detalhadas

1. Verificação de Perfil
   perfis = ['conservador', 'moderado', 'arrojado']

# Usuário conservador NÃO pode investir em moderado/arrojado

# Usuário moderado pode investir em conservador/moderado

# Usuário arrojado pode investir em qualquer perfil

Execute python app.py

👨‍💻 Autor
Carlos Corrêa
LinkedIn: https://www.linkedin.com/in/carlosedop
Este projeto foi desenvolvido para fins educacionais.

Nota: Este projeto demonstra habilidades em desenvolvimento backend com Python, criação de APIs REST, implementação de regras de negócio e desenvolvimento frontend básico. Todas as funcionalidades solicitadas foram implementadas conforme os requisitos do desafio técnico.

Última atualização: Janeiro 2026
