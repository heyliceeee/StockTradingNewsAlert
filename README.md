# 📈 Stock Alert Bot

Um sistema automatizado que monitoriza diariamente a variação percentual de uma ação e identifica movimentos relevantes no mercado. Quando a oscilação ultrapassa um limite definido, o bot recolhe as notícias mais recentes relacionadas com a empresa e envia alertas formatados para um canal de Telegram.

---

## 🔍 Funcionalidade

- Observa a evolução diária do preço de uma ação.
- Calcula a variação percentual entre os dois dias mais recentes.
- Compara essa variação com um limite configurado.
- Quando o limite é ultrapassado, recolhe as três notícias mais recentes sobre a empresa.
- Envia cada notícia como uma mensagem independente, incluindo:
  - símbolo da ação  
  - direção e percentagem da variação  
  - título da notícia  
  - breve descrição  

---

## 📰 Formato das mensagens

Cada alerta segue esta estrutura:

```
TSLA: 🔺5.12%
Headline: Example headline here
Brief: Short summary of the article here
```

---

## ⚡ Automação diária

O projeto integra-se com GitHub Actions, que executa o processo automaticamente **uma vez por dia**, garantindo que os alertas são enviados de forma consistente e sem necessidade de intervenção manual.

---

## ⚙️ Configuração

O comportamento do bot é controlado por variáveis de ambiente que definem:

- chaves de acesso às APIs externas  
- token e destino do canal de Telegram  
- ação monitorizada  
- limite mínimo de variação para gerar alertas  
