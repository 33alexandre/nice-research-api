# Nice Research API

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-05998b.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg)](https://www.postgresql.org/)

O **Nice Research** é uma API desenvolvida para digitalizar a coleta e análise de dados em pesquisas eleitorais. O sistema substitui o preenchimento manual por uma solução estruturada, garantindo organização, validação e acesso centralizado às informações coletadas.

## Diferenciais Técnicos 

- **Arquitetura Assíncrona:** Construída com FastAPI para suportar alta concorrência durante picos de coleta de dados.
- **Integridade Referencial:** Modelagem de dados rigorosa com PostgreSQL, garantindo que cada voto esteja vinculado corretamente a bairros e candidatos existentes.
- **Validação de Dados:** Uso extensivo de Pydantic para garantir que nenhum dado inconsistente entre no banco de dados.
- **Garantia de Qualidade:** Inclui scripts de **Stress Test** que validam a estabilidade do sistema sob carga (simulação de inserções simultâneas).

## Tecnologias Utilizadas

- **Back-end:** Python, FastAPI.
- **Banco de Dados:** PostgreSQL (Relacional).
- **ORM:** SQLAlchemy (Mapeamento Objeto-Relacional).
- **Documentação:** Swagger UI (OpenAPI) gerado automaticamente.
- **Ambiente:** Linux (Fedora Workstation).

## Funcionalidades Principais

- **Gestão de Bairros:** Cadastro e normalização de localidades.
- **Gestão de Candidatos:** Controle de partidos, números e cargos.
- **Registro de Entrevistas:** Coleta de votos com rastreabilidade (pesquisador, votante e timestamp).
- **Módulo de Inteligência:**
    - **Ranking Geral:** Cálculo automático de porcentagens e total de votos.
    - **Análise Qualitativa:** Feed de observações coletadas em campo.
    - **Mapa de Cobertura:** Relatório de volume de entrevistas por bairro.

## Como Executar o Projeto

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/33alexandre/nice-research-api.git](https://github.com/33alexandre/nice-research-api.git)
   cd nice-research-api
