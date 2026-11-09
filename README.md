# VoidGram 🪐
**Cliente Android não oficial do ecossistema Telegram — projeto PedroVoid.**

Um mensageiro personalizado, extensível e transparente: preservar toda a experiência básica de mensagens e agregar recursos **locais e gratuitos** de personalização, tradução/transcrição, organização e mídia. Projeto pensado para desenvolvimento **100% pelo celular**, com compilações remotas no GitHub Actions e testes no POCO C75 (Android 16 / HyperOS 3).

> **Status em 09/11/2026:** fase de pesquisa e arquitetura. **Ainda não há APK compilado, cliente funcional ou implementação de recursos dos forks.**

## Documentação
- [Pesquisa técnica v0.1: código oficial, Nekogram, NekoX, Nagram, Mercurygram, Forkgram e outros](docs/PESQUISA_TECNICA_V0_1.md)
- [Regras oficiais da API do Telegram](https://core.telegram.org/api/terms)
- [Código-fonte Android oficial](https://github.com/DrKLO/Telegram)

## Diretrizes do projeto
- **Primeira escolha de base:** Telegram Android original GPL-2.0, com commits rastreáveis. Os outros clientes são referências; integrações precisam ser revisadas por segurança, manutenção e licença.
- **Diferenciação:** marca, ícone e `applicationId` próprios; não se passar pelo aplicativo oficial. Manter avisos/copyleft e publicar fonte correspondente.
- **Privacidade:** sem falsificação de status de leitura/presença, sem quebrar chats secretos, sem coleta de conteúdo para treino de IA.
- **Premium:** oferecer alternativas locais quando possíveis; **não prometer** burlar limites, quotas, funcionalidades de servidor ou compras em Stars. Respeitar mensagens patrocinadas oficiais.
- **Build:** GitHub Actions com chaves próprias em Secrets, builds verificáveis e testes no Android; nunca publicar credenciais em arquivos versionados.

## Roadmap
1. [ ] **M1** — importar base, configurar API própria, identidade VoidGram e produzir APK debug via Actions.
2. [ ] **M2** — configurar visual, tema, acessibilidade e desempenho.
3. [ ] **M3** — organização local, player e utilitários.
4. [ ] **M4** — transcrição/tradução offline opcionais.
5. [ ] **M5** — qualidade, privacidade, performance e versão assinada.

**VoidGram não é afiliado, patrocinado ou endossado pelo Telegram.**
