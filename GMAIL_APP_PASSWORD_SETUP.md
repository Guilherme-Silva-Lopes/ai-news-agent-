# 📧 Configuração de Senha de Aplicativo Gmail (SIMPLES!)

Este guia mostra como configurar o envio de email usando **Senha de Aplicativo do Gmail** - muito mais simples que OAuth2!

## ✅ Passo 1: Ativar Verificação em Duas Etapas

1. Acesse: https://myaccount.google.com/security
2. Role até **"Como fazer login no Google"**
3. Clique em **"Verificação em duas etapas"**
4. Siga as instruções para ativar (se ainda não estiver ativo)

## ✅ Passo 2: Criar Senha de Aplicativo

1. Ainda na página de Segurança, procure por **"Senhas de app"** (ou acesse diretamente: https://myaccount.google.com/apppasswords)
2. Se não aparecer, certifique-se que a verificação em 2 etapas está ativa
3. Na seção "Senhas de app", clique em **"Criar"**
4. Digite um nome como: `Kestra AI News Agent`
5. Clique em **"Criar"**
6. O Google exibirá uma **senha de 16 caracteres** (ex: `abcd efgh ijkl mnop`)
7. **COPIE ESTA SENHA** - você só verá ela uma vez!

## ✅ Passo 3: Configurar no Kestra

No Kestra, vá em **Namespace Variables** (ou KV Store) e adicione/atualize:

### Criar Secret `GMAIL_APP_PASSWORD`:
```
abcdefghijklmnop
```
(Cole a senha de 16 caracteres **sem espaços**)

### Criar/Atualizar `GMAIL_EMAIL`:
```
seu-email@gmail.com
```

### Manter `RECEIVER_EMAIL`:
```
email-destinatario@example.com
```

## 🎯 Resumo das Variáveis Necessárias

Você precisa ter estas 3 variáveis no Kestra KV Store:

| Variável | Tipo | Exemplo |
|----------|------|---------|
| `GMAIL_EMAIL` | String | `seu-email@gmail.com` |
| `GMAIL_APP_PASSWORD` | Secret | `abcdefghijklmnop` (sem espaços) |
| `RECEIVER_EMAIL` | String | `destinatario@example.com` |

## ✅ Pronto!

Execute o workflow novamente. O email será enviado com sucesso! 🚀

## 🔧 Troubleshooting

**Erro "535 Authentication failed":**
- Verifique se a senha de aplicativo está correta (sem espaços)
- Confirme que a verificação em 2 etapas está ativa

**Erro "Username and Password not accepted":**
- Use seu email completo em `GMAIL_EMAIL` (ex: `user@gmail.com`)
- Gere uma nova senha de aplicativo se necessário

**Não encontro "Senhas de app":**
- Certifique-se que a verificação em 2 etapas está ativada
- Aguarde alguns minutos após ativar a verificação em 2 etapas
