# 📝 Changelog

## [1.0.1] - 2025-10-23

### 🔒 Security
- **CRÍTICO:** Removidos arquivos com API keys hardcoded
- Adicionada validação de entrada em todas as mensagens
- Implementado rate limiting (10 req/min por usuário)
- Proteção contra prompt injection
- Sanitização de caracteres de controle

### ✨ Features
- **WhatsApp Integration** - Agentes podem responder no WhatsApp Web 📱
  - `whatsapp_bot.py` - Bot principal para WhatsApp
  - `integrations/whatsapp/whatsapp_service.py` - Serviço WhatsApp
  - `docs/WHATSAPP_SETUP.md` - Guia completo de setup
- Validador de entrada (`core/validators.py`)
- Rate limiter (`core/rate_limiter.py`)
- Documentação de segurança (`SECURITY.md`)

### 🛠️ Improvements
- Melhor tratamento de erros
- Mensagens de erro mais claras
- Logging aprimorado
- README atualizado com integração WhatsApp

### 🗑️ Removed
- Arquivos de teste com credenciais expostas
- API keys hardcoded

## [1.0.0] - 2025-10-23

### 🎉 Initial Release
- Framework de agentes AI
- Templates: Restaurant & Consulting
- CLI interativo
- Suporte OpenAI e Anthropic
- Integração com NVIDIA API
