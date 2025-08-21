# 🎙️ Monday Bot

O **Monday Bot** é um bot desenvolvido em **Python** que cria clipes automaticamente na Twitch através de **comandos de voz**.

## 🚀 Tecnologias utilizadas
- **Python** → Lógica principal
- **Vosk** → Reconhecimento de fala offline
- **Twitch API** → Criação de clipes e envio de mensagens no chat
- **Websockets** → Comunicação em tempo real com o chat da Twitch
- **Requests / HTTP client** (requisições à API)

## ⚙️ Funcionalidades
- 🎤 Captura e transcrição de áudio em tempo real via **Vosk**
- 🎬 Criação de **clipes** no canal da Twitch
- 💬 **Feedback** automático no chat (mensagens confirmando o comando)
- 🔐 Credenciais lidas de **arquivo local de configuração JSON** (sem variáveis de ambiente)

## 🎯 Próximos passos
- Adicionar suporte a múltiplos comandos de voz
- Melhorar precisão do reconhecimento de voz com modelos customizados
- Mudança no armazenamento das credenciais