# 🛡️ Guardião Pix: Prevenção a Golpes por Engenharia Social

Sistema inteligente de avaliação de risco pré-transacional e intervenção comportamental focado em mitigar fraudes por engenharia social no ecossistema Pix.

---

## 📌 Sobre o Projeto

As fraudes financeiras baseadas em manipulação psicológica (ex.: golpe do falso parente, falsa central telefónica e engenharia social) frequentemente passam pelos sistemas tradicionais de cibersegurança por serem executadas diretamente pelos próprios utilizadores legítimos.

O **Guardião Pix** atua na camada de prevenção pré-transacional, analisando padrões de comportamento e dados do recebedor antes que o Pix seja concluído, acionando alertas dinâmicos e etapas de verificação graduais para proteger os utilizadores.

---

## 🎯 Origem e Motivação

O projeto nasceu de uma motivação real: a experiência de ver um familiar próximo ser vítima de um golpe por engenharia social no Pix. A necessidade de criar barreiras preventivas para proteger utilizadores em momentos de vulnerabilidade inspirou o desenvolvimento desta solução.

---

## 💡 Principais Funcionalidades

- **🔍 Verificação Pré-Transacional:** Análise de risco da chave Pix combinada a um questionário comportamental focado em engenharia social.
- **🚨 Canal de Denúncia Colaborativa:** Permitir o reporte em tempo real de chaves e abordagens suspeitas para alertar a comunidade.
- **🤝 Rede de Apoio (Mecanismo do Guardião):** Notificação preventiva para familiares/guardiões cadastrados em caso de transações de alto risco.
- **🔒 Privacidade & LGPD:** Aplicação do algoritmo de hash **SHA-256** para mascaramento e proteção de dados sensíveis.

---

## 🛠️ Tecnologias e Metodologia

- **Linguagem:** Python 3.x
- **Interface Web:** Streamlit
- **Segurança:** SHA-256 para anonimização de dados
- **Metodologia de Desenvolvimento:** Desenvolvimento assistido por Inteligência Artificial e **Engenharia de Prompt**, otimizando a prototipagem, a estruturação do código e a construção da interface de utilizador.

---

## 🚀 Como Executar o Projeto Localmente

1. Clone o repositório:
   ```bash
   git clone [https://github.com/isacunha1207-lab/guardiao-pix.git](https://github.com/isacunha1207-lab/guardiao-pix.git)
   cd guardiao-pix