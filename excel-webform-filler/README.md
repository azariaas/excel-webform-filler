# Excel Web Form Filler

Automação em Python que lê linhas pendentes de uma planilha Excel e preenche formulários de orçamento no navegador.

Este é um projeto independente de portfólio. O fluxo original preenchia formulários web a partir de uma planilha; esta versão usa um **site de demonstração local** e dados fictícios, para que qualquer pessoa possa clonar e executar sem depender de site de empresa, lista de clientes ou dados pessoais.

## Sobre

Cada aba da planilha representa uma loja. Cada linha é um pedido de orçamento (nome, telefone, e-mail, produto, versão, observações). O script:

1. associa a aba à URL da loja
2. mapeia o nome do produto para o slug da página
3. abre o formulário no Chrome com Selenium
4. preenche os campos e envia
5. pinta a linha de amarelo para não enviar de novo

## Problema

Copiar linhas da planilha para formulários web na mão é lento e sujeito a erro. Linhas já enviadas se misturam com as novas se não forem marcadas.

## Solução

```text
Planilha Excel (uma aba por loja)
        ↓
Lê o cabeçalho e ignora linhas vazias ou amarelas
        ↓
Mapeia loja + produto → URL do formulário
        ↓
Selenium preenche e envia o formulário local
        ↓
Marca a linha como processada (preenchimento amarelo)
```

A automação do navegador continua no mesmo espírito de um preenchimento de formulário. Só o **site de destino** é um demo servido em `localhost`.

## Tecnologias

- Python 3
- openpyxl
- Selenium
- webdriver-manager
- PyYAML
- pytest

## Estrutura

```text
excel-webform-filler/
├── main.py
├── config.yaml
├── form_filler/          # config, leitura do Excel, mapeamento de URL, Selenium
├── demo_site/           # formulários HTML gerados localmente
├── data/                # planilha de exemplo
├── scripts/
│   ├── generate_sample_data.py
│   └── serve_demo.py
└── tests/
```

## Como executar

1. Clone o repositório e entre na pasta.

2. Crie um ambiente virtual e instale as dependências:

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
source .venv/bin/activate # macOS / Linux
pip install -r requirements.txt
```

3. Gere o site de demonstração e a planilha de exemplo:

```bash
python scripts/generate_sample_data.py
```

4. Em **um terminal**, sirva o site local:

```bash
python scripts/serve_demo.py
```

5. Em **outro terminal**, valide a planilha sem abrir o navegador:

```bash
python main.py --validate-only
```

ou rode a automação completa (é preciso ter o Chrome instalado):

```bash
python main.py
```

6. Confira:

- o site demo mostra a página “Request received” depois de cada envio
- as linhas processadas em `data/leads.xlsx` ficam amarelas
- a primeira linha da aba Northside continua pulada (já vem amarela no exemplo)

```bash
python -m pytest
```

Não aponte `base_url` para um site de terceiros. A configuração de exemplo usa `http://127.0.0.1:8000` de propósito.

## Exemplo

**Aba `NORTH`**

| NAME | PHONE | EMAIL | PRODUCT | VERSION | NOTES |
| --- | --- | --- | --- | --- | --- |
| Casey Quinn (amarela) | 555-0101 | casey.quinn@example.com | Desk Lamp | Plus | já enviado |
| Sam Ortega | 555-0102 | sam.ortega@example.com | Office Chair | Standard | |

**Resultado**

- Casey é ignorado
- Sam é enviado para `http://127.0.0.1:8000/stores/north/new/office-chair.html`
- a linha é marcada de amarelo

Produtos desconhecidos (a linha de exemplo “Unknown Item”) aparecem como erro e não são marcados.

## Aprendizados

- Controle do Chrome com Selenium (waits, Select, send_keys, clique via JavaScript)
- Leitura de cabeçalhos e preenchimento de células com openpyxl
- Processamento idempotente (pular linhas já tratadas)
- URLs e catálogo de produtos via configuração
- Testes de mapeamento e regras da planilha sem abrir o navegador

## Melhorias futuras

- Flag de modo headless para execução sem janela
- Uma nova tentativa quando a página demorar a carregar
- Um log simples de enviados vs. pulados
- Suporte a CSV como entrada alternativa
