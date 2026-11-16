# Checklist de regressão — teste no POCO C75

Preencha a cada APK novo antes de considerar a versão aprovada. Marque ✅ funcionou, ❌ falhou (descreva) ou ➖ não testado.

**Versão:** ______ **Build nº:** ______ **Data:** ______
**Assinatura (ver BUILD_INFO.txt):** fixa / temporária

## 1. Instalação
- [ ] O APK instalou **por cima** do anterior, sem desinstalar (só vale com assinatura fixa)
- [ ] O nome e o ícone são do VoidGram
- [ ] A versão em Configurações do Android → Apps mostra `…-voidgramN.N.N`

## 2. Login e dados
- [ ] Continuou logado após atualizar (ou o login por código funcionou, se foi instalação limpa)
- [ ] A lista de conversas carregou
- [ ] O histórico de uma conversa antiga carregou

## 3. Mensagens
- [ ] Enviar e receber texto
- [ ] Enviar e receber foto
- [ ] Gravar e ouvir mensagem de voz
- [ ] Baixar e abrir um arquivo
- [ ] Figurinhas e emojis aparecem

## 4. Notificações (sem Firebase: dependem da conexão em segundo plano)
Antes: em Configurações do HyperOS, ative **Início automático** e ponha a bateria em **Sem restrições** para o VoidGram.
- [ ] Notificação chega com o app aberto em outra conversa
- [ ] Notificação chega com o app em segundo plano
- [ ] Notificação chega com a tela bloqueada há 10 minutos
- [ ] Notificação chega depois de fechar o app pelos recentes
- [ ] Atraso observado: ______

## 5. Chamadas
- [ ] Fazer chamada de voz
- [ ] Receber chamada de voz (com o app em segundo plano)
- [ ] Chamada de vídeo

## 6. Outros
- [ ] Câmera dentro do app
- [ ] Envio de localização / mapa aparece
- [ ] Adicionar segunda conta (opcional)
- [ ] Nenhum travamento ou fechamento inesperado em 10 minutos de uso

## Observações
