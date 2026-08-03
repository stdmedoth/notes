# 📝 Obsidian Assets & Note Scans

Este repositório privado é dedicado ao armazenamento e hospedagem de imagens, diagramas e escaneamentos de anotações manuscritas utilizados no meu cofre do **Obsidian**.

---

## 📁 Estrutura de Pastas

```text
.
├── assets/
│   ├── 2026/             # Organização por ano (opcional)
│   └── ...
├── README.md
└── .gitignore
```

---

## ⚙️ Como Funciona a Integração

1. **Captura:** Anotações em papel são digitalizadas/fotografadas (ex: via app vFlat ou Adobe Scan).
2. **Upload Automático:** Utiliza-se o plugin **Image Auto Upload Plugin** (ou PicGo) integrado ao Obsidian.
3. **Link na Nota:** O Obsidian insere automaticamente o link cru (*raw*) da imagem hospedada aqui:
   `![Anotação](https://raw.githubusercontent.com/<SEU_USUARIO>/<SEU_REPOSITORIO>/main/assets/imagem.png)`

---

## 🔑 Configuração Rápida do Token (PAT)

Para permitir que o Obsidian faça upload automático para este repositório:
1. Vá em **GitHub > Settings > Developer Settings > Personal Access Tokens > Tokens (classic)**.
2. Gere um novo token com a permissão **`repo`** (ou `contents: write`).
3. Copie o token gerado e insira nas configurações do plugin no Obsidian.

---

## 🔒 Privacidade e Boas Práticas

* **Repositório Privado:** Mantenha este repositório marcado como **Privado** caso contenha anotações pessoais ou acadêmicas.
* **Tamanho do Repositório:** Mantenha o repositório abaixo de 1 GB a 5 GB para garantir bom desempenho no Git.
* **Formato de Imagem Recomendado:** Dê preferência a formatos compactados (como `.webp` ou `.jpg` otimizado) para economizar espaço e acelerar o carregamento.

---

*Mantido automaticamente via Obsidian.*
