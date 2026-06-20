# 🏋️ AI Gym Planner

> Aplicativo web de academia com **Inteligência Artificial** que gera planos de treino personalizados com base no perfil e objetivos do aluno.

![Badge](https://img.shields.io/badge/Python-Flask-blue?logo=python)
![Badge](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-61DAFB?logo=react)
![Badge](https://img.shields.io/badge/IA-Google%20Gemini-orange?logo=google)
![Badge](https://img.shields.io/badge/Banco%20de%20Dados-Firebase-FFCA28?logo=firebase)

---

## 📋 Sobre o Projeto

O **AI Gym Planner** é uma aplicação web fullstack que permite ao aluno informar seus dados (nome, objetivos, restrições físicas, nível de experiência e dias disponíveis por semana) e receber um **plano de treino semanal personalizado** gerado automaticamente pela Inteligência Artificial do Google (Gemini).

Os treinos gerados são salvos automaticamente no **Firebase Firestore**, permitindo que o aluno consulte seu histórico de treinos futuramente.

---

## 🚀 Funcionalidades

- 📝 **Formulário de perfil** — O aluno informa nome, objetivos, restrições, nível e disponibilidade de dias.
- 🤖 **IA Generativa** — A API do Google Gemini cria um plano de treino personalizado em formato JSON.
- 💾 **Banco de dados** — Os treinos são salvos no Firebase Firestore vinculados ao nome do aluno.
- ⚠️ **Modo offline** — O sistema funciona mesmo sem o banco de dados configurado, exibindo um aviso informativo.
- 🎨 **Interface moderna** — Design dark com efeito glassmorphism, animações e responsivo.

---

## 🛠️ Tecnologias Utilizadas

| Camada      | Tecnologia                        |
|-------------|-----------------------------------|
| Frontend    | React + Vite + CSS (Glassmorphism)|
| Backend     | Python + Flask                    |
| IA          | Google Gemini API (gemini-2.5-flash)|
| Banco de dados | Firebase Firestore             |
| Versionamento | Git + GitHub                   |

---

## 📁 Estrutura do Projeto

```
projetofinal/
├── backend/
│   ├── app.py                      # API Flask (rotas e lógica da IA)
│   ├── firebase-credentials.json   # ⚠️ NÃO está no GitHub (arquivo privado)
│   └── venv/                       # Ambiente virtual Python
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx                 # Componente principal React
│   │   └── index.css               # Estilos (Dark Mode + Glassmorphism)
│   └── index.html
│
├── .env                            # ⚠️ NÃO está no GitHub (chaves privadas)
├── .gitignore
└── README.md
```

---

## ⚙️ Como Executar Localmente

### Pré-requisitos
- Python 3.10+
- Node.js 18+
- Git

### 1. Clone o repositório
```bash
git clone https://github.com/marcelosenaiprojetoo/gym-ai-app.git
cd gym-ai-app
```

### 2. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:
```env
GEMINI_API_KEY=sua_chave_aqui
```
> 🔑 Obtenha sua chave gratuitamente em [Google AI Studio](https://aistudio.google.com/).

### 3. Configure o Backend (Python)
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux/Mac
pip install flask flask-cors google-generativeai python-dotenv firebase-admin
python app.py
```
O servidor backend estará rodando em `http://localhost:5000`.

### 4. Configure o Frontend (React)
```bash
cd frontend
npm install
npm run dev
```
A interface estará disponível em `http://localhost:5173`.

---

## 🔥 Configuração do Firebase (opcional)

Para ativar o salvamento de treinos no banco de dados:

1. Acesse o [Firebase Console](https://console.firebase.google.com/) e crie um projeto.
2. Vá em **Criação > Firestore Database** e crie um banco de dados (modo de teste).
3. Vá em **Configurações do Projeto > Contas de Serviço** e gere uma nova chave privada.
4. Salve o arquivo `.json` baixado dentro da pasta `backend/` com o nome exato: **`firebase-credentials.json`**.
5. Reinicie o backend. A mensagem `Firebase inicializado com sucesso!` aparecerá no terminal.

> ⚠️ O arquivo `firebase-credentials.json` **não deve ser enviado ao GitHub**. Ele já está no `.gitignore`.

---

## 📸 Como Usar

1. Abra o app em `http://localhost:5173`.
2. Preencha seu **nome**, **objetivos**, **restrições**, **nível** e **dias disponíveis**.
3. Clique em **"Gerar Meu Treino"**.
4. Aguarde a IA gerar seu plano personalizado.
5. O treino aparecerá na tela com exercícios, séries, repetições e dicas extras.

---

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais no **SENAI**.
