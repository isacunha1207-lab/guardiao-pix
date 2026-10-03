# 🛡️ Guardião Pix: Prevenção a Golpes por Engenharia Social

Sistema inteligente de avaliação de risco pré-transacional e intervenção comportamental focado em mitigar fraudes por engenharia social no ecossistema Pix.

---

### 📌 Sobre o Projeto

As fraudes financeiras baseadas em manipulação psicológica (ex.: golpe do falso parente, falsa central telefônica) passam frequentemente pelos sistemas perimetrais de cibersegurança tradicionais por serem executadas voluntariamente pelas próprias vítimas.

O **Guardião Pix** combina **Ciência de Dados** e a **Teoria do Nudge (Arquitetura da Escolha)** para criar um índice dinâmico de risco (*Risk Score*) e acionar uma rede de apoio ("Guardião") antes da conclusão de transações suspeitas.

---

### 🔒 Conformidade Regulatória (LGPD)

Para estar em total conformidade com a Lei Geral de Proteção de Dados (Lei nº 13.709/2018):
- Nenhuma chave Pix é armazenada ou processada em texto puro.
- As chaves são convertidas em **Hashes Criptográficos SHA-256** unidirecionais antes de qualquer consulta ou gravação na base de dados.