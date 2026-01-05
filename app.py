from flask import Flask, request, jsonify, send_file
from database import Database
import json

app = Flask(__name__, static_folder='.', static_url_path='')
db = Database()

# Função para cálculo de resgate (REGRAS DE NEGÓCIO)
def calcular_resgate(valor, rentabilidade, dias_investido, dias_vencimento):
    if dias_investido < 30:
        return {"erro": "Não pode resgatar antes de 30 dias"}
    
    rendimento_diario = rentabilidade / 365 / 100
    rendimento_bruto = valor * rendimento_diario * dias_investido
    
    if dias_vencimento > 365:
        ir = rendimento_bruto * 0.10
    elif dias_vencimento > 180:
        ir = rendimento_bruto * 0.20
    else:
        ir = rendimento_bruto * 0.05
    
    valor_final = valor + rendimento_bruto - ir
    
    return {
        "valor_investido": valor,
        "rendimento_bruto": round(rendimento_bruto, 2),
        "ir_descontado": round(ir, 2),
        "valor_final": round(valor_final, 2),
        "dias_investido": dias_investido
    }

# ===== PÁGINAS HTML =====
@app.route('/')
def home():
    return send_file('index.html')

# ===== API ENDPOINTS =====
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    perfil = data.get('perfil', 'conservador')
    
    if not all([nome, email, senha]):
        return jsonify({"success": False, "message": "Dados incompletos"}), 400
    
    if db.criar_usuario(nome, email, senha, perfil):
        return jsonify({"success": True, "message": "Usuário criado!"})
    return jsonify({"success": False, "message": "Email já existe"}), 400

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    senha = data.get('senha')
    
    usuario = db.verificar_login(email, senha)
    if usuario:
        return jsonify({
            "success": True,
            "user": {"id": usuario[0], "nome": usuario[1], "perfil": usuario[2]}
        })
    return jsonify({"success": False, "message": "Credenciais inválidas"}), 401

@app.route('/api/investimentos', methods=['GET'])
def listar_investimentos():
    tipo = request.args.get('tipo')
    investimentos = db.listar_investimentos(tipo)
    
    resultado = []
    for inv in investimentos:
        resultado.append({
            "id": inv[0], "nome": inv[1], "tipo": inv[2],
            "perfil_minimo": inv[3], "rentabilidade": inv[4],
            "vencimento_dias": inv[5]
        })
    return jsonify(resultado)

@app.route('/api/investir', methods=['POST'])
def investir():
    data = request.json
    usuario_id = data.get('usuario_id')
    investimento_id = data.get('investimento_id')
    valor = data.get('valor')
    
    if not all([usuario_id, investimento_id, valor]):
        return jsonify({"success": False, "message": "Dados incompletos"}), 400
    
    # Verificar perfil
    db.cursor.execute('SELECT perfil FROM usuarios WHERE id = ?', (usuario_id,))
    usuario = db.cursor.fetchone()
    
    db.cursor.execute('SELECT perfil_minimo FROM investimentos WHERE id = ?', (investimento_id,))
    investimento = db.cursor.fetchone()
    
    if not usuario or not investimento:
        return jsonify({"success": False, "message": "Não encontrado"}), 404
    
    perfis = ['conservador', 'moderado', 'arrojado']
    if perfis.index(usuario[0]) < perfis.index(investimento[0]):
        return jsonify({
            "success": False, 
            "message": f"Perfil {usuario[0]} inadequado para {investimento[0]}"
        }), 403
    
    if db.investir(usuario_id, investimento_id, valor):
        return jsonify({"success": True, "message": "Investido com sucesso!"})
    return jsonify({"success": False, "message": "Erro ao investir"}), 500

@app.route('/api/meus_investimentos', methods=['GET'])
def meus_investimentos():
    usuario_id = request.args.get('usuario_id')
    if not usuario_id:
        return jsonify({"success": False, "message": "Informe usuario_id"}), 400
    
    investimentos = db.meus_investimentos(usuario_id)
    resultado = []
    for inv in investimentos:
        resultado.append({
            "id": inv[0], "nome": inv[5], "tipo": inv[6],
            "valor": inv[3], "data": inv[4], "rentabilidade": inv[7]
        })
    return jsonify(resultado)

@app.route('/api/simular', methods=['POST'])
def simular():
    data = request.json
    valor = data.get('valor', 1000)
    rentabilidade = data.get('rentabilidade', 12.5)
    dias = data.get('dias', 60)
    vencimento = data.get('vencimento', 180)
    
    resultado = calcular_resgate(valor, rentabilidade, dias, vencimento)
    return jsonify(resultado)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "online",
        "projeto": "Sensedia Invest - Estágio",
        "tecnologias": ["Python", "Flask", "SQLite", "SHA-256"]
    })

if __name__ == '__main__':
    print("=" * 50)
    print("📈 SENSEDIA INVEST - API DE ESTÁGIO")
    print("=" * 50)
    print("✅ Banco de dados: investimentos.db")
    print("🔐 Autenticação: SHA-256")
    print("📊 Endpoints:")
    print("   • http://localhost:5000/ (Frontend)")
    print("   • /api/register  - Cadastrar")
    print("   • /api/login     - Login")
    print("   • /api/investimentos - Listar")
    print("   • /api/investir  - Investir")
    print("   • /api/simular   - Testar regras")
    print("=" * 50)
    print("\n🚀 Servidor: http://localhost:5000")
    print("   Ctrl+C para parar\n")
    
    app.run(debug=True, port=5000)