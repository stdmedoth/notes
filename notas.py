import argparse
import json
import os
import shutil
import subprocess
from datetime import datetime

CONFIG_FILE = 'disciplinas.json'
BASE_DIR = 'Aulas'

def carregar_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"Erro: Arquivo '{CONFIG_FILE}' não encontrado.")
        exit(1)
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def obter_pasta_dia(id_disciplina):
    hoje = datetime.now().strftime('%Y-%m-%d')
    return os.path.join(BASE_DIR, f"{hoje}_{id_disciplina}")

def cmd_list(args):
    """Lista as disciplinas cadastradas e sinaliza as de hoje."""
    config = carregar_config()
    dias_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
    dia_atual = datetime.now().weekday()
    
    print("="*40)
    print(" DISCIPLINAS CADASTRADAS")
    print("="*40)
    
    for id_disc, dados in config.items():
        dias_numeros = dados.get('dias_aula', [])
        dias_nomes = [dias_semana[d] for d in dias_numeros]
        
        marcacao_hoje = " \033[92m[* AULA HOJE *]\033[0m" if dia_atual in dias_numeros else ""
        
        print(f"ID: {id_disc}{marcacao_hoje}")
        print(f"  Nome:      {dados.get('nome')}")
        print(f"  Professor: {dados.get('professor')}")
        print(f"  Dias:      {', '.join(dias_nomes)}")
        print("-" * 40)

def cmd_init(args):
    """Cria as pastas para as disciplinas do dia atual."""
    config = carregar_config()
    dia_semana = datetime.now().weekday()
    
    disciplinas_hoje = [
        id_disc for id_disc, dados in config.items() 
        if dia_semana in dados.get('dias_aula', [])
    ]
    
    if not disciplinas_hoje:
        print("Nenhuma disciplina cadastrada para hoje.")
        return

    for id_disc in disciplinas_hoje:
        pasta = obter_pasta_dia(id_disc)
        pasta_img = os.path.join(pasta, 'imagens')
        os.makedirs(pasta_img, exist_ok=True)
        print(f"[OK] Diretório criado/verificado: {pasta}")

def cmd_add(args):
    """Adiciona uma imagem à pasta da disciplina."""
    pasta = obter_pasta_dia(args.disciplina)
    pasta_img = os.path.join(pasta, 'imagens')
    
    if not os.path.exists(pasta_img):
        print(f"Erro: Pasta para {args.disciplina} não foi inicializada. Rode 'python notas.py init'.")
        return
        
    if not os.path.exists(args.arquivo):
        print(f"Erro: Arquivo '{args.arquivo}' não encontrado.")
        return

    nome_arquivo = os.path.basename(args.arquivo)
    destino = os.path.join(pasta_img, nome_arquivo)
    shutil.copy(args.arquivo, destino)
    print(f"[OK] Imagem '{nome_arquivo}' adicionada à disciplina {args.disciplina}.")

def realizar_compilacao(id_disc, dados_disc, assunto):
    """Função base para compilar o PDF de uma disciplina específica."""
    pasta = obter_pasta_dia(id_disc)
    pasta_img = os.path.join(pasta, 'imagens')
    
    if not os.path.exists(pasta_img):
        print(f"Erro: Pasta de imagens não encontrada para {id_disc}.")
        return False

    imagens = sorted([img for img in os.listdir(pasta_img) if img.lower().endswith(('.png', '.jpg', '.jpeg'))])
    
    if not imagens:
        print(f"Erro: Nenhuma imagem encontrada na pasta de {id_disc} para compilar.")
        return False

    hoje_formatado = datetime.now().strftime('%d/%m/%Y')
    
    latex_content = f"""\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc}}
\\usepackage[brazilian]{{babel}}
\\usepackage{{graphicx}}
\\usepackage{{geometry}}
\\geometry{{a4paper, margin=1in}}

\\title{{Anotações de Aula - {dados_disc['nome']}}}
\\author{{Professor: {dados_disc['professor']}}}
\\date{{{hoje_formatado} \\\\ Assunto: {assunto}}}

\\begin{{document}}
\\maketitle
"""
    for img in imagens:
        latex_content += f"""
\\begin{{figure}}[h!]
    \\centering
    \\includegraphics[width=\\textwidth]{{imagens/{img}}}
\\end{{figure}}
\\clearpage
"""
    latex_content += "\\end{document}\n"

    caminho_tex = os.path.join(pasta, 'anotacoes.tex')
    with open(caminho_tex, 'w', encoding='utf-8') as f:
        f.write(latex_content)

    print(f"[INFO] Compilando PDF para '{dados_disc['nome']}'...")
    processo = subprocess.run(
        ['pdflatex', '-interaction=nonstopmode', 'anotacoes.tex'],
        cwd=pasta,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    if processo.returncode == 0:
        print(f"[SUCESSO] PDF gerado em: {os.path.join(pasta, 'anotacoes.pdf')}")
        return True
    else:
        print(f"[ERRO] Falha ao compilar o LaTeX para {id_disc}.")
        return False

def cmd_compile(args):
    """Compila as imagens de uma única disciplina especificada."""
    config = carregar_config()
    if args.disciplina not in config:
        print("Erro: Disciplina não encontrada no JSON.")
        return
    realizar_compilacao(args.disciplina, config[args.disciplina], args.assunto)

def cmd_compile_all(args):
    """Compila todas as disciplinas do dia que tiverem imagens."""
    config = carregar_config()
    dia_semana = datetime.now().weekday()
    
    disciplinas_hoje = [
        id_disc for id_disc, dados in config.items() 
        if dia_semana in dados.get('dias_aula', [])
    ]
    
    if not disciplinas_hoje:
        print("Nenhuma disciplina cadastrada para hoje.")
        return

    compilacoes_feitas = 0
    for id_disc in disciplinas_hoje:
        pasta_img = os.path.join(obter_pasta_dia(id_disc), 'imagens')
        
        # Só tenta compilar se a pasta de imagens existir e não estiver vazia
        if os.path.exists(pasta_img) and any(f.lower().endswith(('.png', '.jpg', '.jpeg')) for f in os.listdir(pasta_img)):
            print("-" * 40)
            assunto = input(f"Digite o assunto da aula de '{config[id_disc]['nome']}': ")
            if not assunto.strip():
                assunto = "Anotações Gerais"
            
            realizar_compilacao(id_disc, config[id_disc], assunto)
            compilacoes_feitas += 1
            
    if compilacoes_feitas == 0:
        print("Nenhuma foto foi adicionada nas pastas das disciplinas de hoje. Nada para compilar.")
    else:
        print("-" * 40)
        print("Todas as disciplinas do dia foram compiladas!")

# Configuração do CLI
parser = argparse.ArgumentParser(description="Console de Notas em LaTeX")
subparsers = parser.add_subparsers(dest="comando")

# Comando LIST
parser_list = subparsers.add_parser('list', help='Lista as disciplinas cadastradas')

# Comando INIT
parser_init = subparsers.add_parser('init', help='Cria as pastas das disciplinas do dia atual')

# Comando ADD
parser_add = subparsers.add_parser('add', help='Adiciona uma foto à disciplina')
parser_add.add_argument('arquivo', help='Caminho para o arquivo da foto')
parser_add.add_argument('--disciplina', required=True, help='ID da disciplina')

# Comando COMPILE (Individual)
parser_compile = subparsers.add_parser('compile', help='Gera o PDF de uma disciplina específica')
parser_compile.add_argument('--disciplina', required=True, help='ID da disciplina')
parser_compile.add_argument('--assunto', required=True, help='Assunto da aula')

# Comando COMPILE-ALL (Tudo de hoje)
parser_compile_all = subparsers.add_parser('compile-all', help='Gera PDFs de todas as disciplinas do dia')

if __name__ == '__main__':
    args = parser.parse_args()
    if args.comando == 'list':
        cmd_list(args)
    elif args.comando == 'init':
        cmd_init(args)
    elif args.comando == 'add':
        cmd_add(args)
    elif args.comando == 'compile':
        cmd_compile(args)
    elif args.comando == 'compile-all':
        cmd_compile_all(args)
    else:
        parser.print_help()
