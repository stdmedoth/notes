# 📝 Arquivo de Anotações e Manuscritos (Automatizado com LaTeX)

Este repositório privado é dedicado ao armazenamento, backup e organização das fotos e digitalizações das minhas anotações feitas no papel [cite: 1]. 

Para otimizar o fluxo de estudo e economizar tempo, o repositório agora conta com uma automação em Python (`notas.py`) que organiza os arquivos automaticamente por data e disciplina, além de compilar tudo em PDFs profissionais utilizando LaTeX. A antiga sugestão de organização manual em pastas como `materias/` ou `por-data/` [cite: 1] foi totalmente substituída pelo novo console.

---

## ⚙️ Pré-requisitos

- **Python 3** (nativo do sistema)
- **LaTeX** (`pdflatex` instalado e adicionado ao PATH do sistema)

## 🛠️ Configuração

As disciplinas devem ser cadastradas no arquivo `disciplinas.json` na raiz do projeto. Defina os dias de aula usando uma escala de `0` (Segunda) a `6` (Domingo).

```json
{
    "fisica_computacional": {
        "nome": "Física Computacional",
        "professor": "Prof. Dr. Geraldo Sartori",
        "dias_aula": [0, 2]
    },
    "calculo_numerico": {
        "nome": "Cálculo Numérico",
        "professor": "Prof. Dr. João Silva",
        "dias_aula": [1, 3]
    }
}
```

## 🚀 Guia de Uso do Console (`notas.py`)

O gerenciamento das anotações agora é feito via linha de comando.

### 1. Ver a agenda
Lista todas as disciplinas cadastradas no JSON e destaca visualmente quais aulas estão programadas para o dia atual.
```bash
python notas.py list
```

### 2. Inicializar o dia
Cria as estruturas de pastas necessárias (`Aulas/DATA_Materia/imagens`) para todas as disciplinas do dia.
```bash
python notas.py init
```

### 3. Adicionar fotos do caderno
Copia uma imagem para a pasta da disciplina informada. *(Dica: para garantir a ordem correta no PDF, nomeie as fotos de forma sequencial, ex: `1.jpg`, `2.jpg`)*.
```bash
python notas.py add "caminho/para/1.jpg" --disciplina fisica_computacional
```

### 4. Compilar os PDFs

**Para compilar todas as aulas do dia (Recomendado):**
O console detecta quais matérias receberam fotos naquele dia, pede o assunto de cada uma em tempo real e compila os PDFs em sequência.
```bash
python notas.py compile-all
```

**Para compilar uma disciplina específica individualmente:**
```bash
python notas.py compile --disciplina fisica_computacional --assunto "Introdução à Dinâmica Molecular"
```

---

## 📁 Nova Estrutura de Diretórios Automática

Com o uso do script, o repositório assume dinamicamente o seguinte formato:

```text
.
├── notas.py                 # Console de automação
├── disciplinas.json         # Cadastro de disciplinas e dias
├── README.md                # Este documento
└── Aulas/                   # Gerado automaticamente pelo comando init
    └── 2026-08-03_fisica_computacional/
        ├── imagens/
        │   ├── 1.jpg
        │   └── 2.jpg
        ├── anotacoes.tex    # LaTeX estruturado gerado pelo script
        └── anotacoes.pdf    # Resultado final compilado pronto para revisão
```
