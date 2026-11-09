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


## Primeira compilação Android (CI)
O repositório agora contém:
- [Workflow GitHub Actions](.github/workflows/voidgram-android.yml): executa testes, baixa a base oficial no commit rastreado e tenta compilar uma variante Android standalone.
- [Script de personalização](scripts/prepare_voidgram.py): troca identificador do pacote, nome visível, ícone PV experimental, configuração de API e desliga funções exclusivas da assinatura oficial.
- [Testes do script](tests/test_prepare_voidgram.py): verificações automáticas de mudanças e da configuração de credenciais.
- [Execuções e APKs de teste](../../actions/workflows/voidgram-android.yml).

O código-fonte original é obtido na própria execução, e **não** está integralmente presente neste repositório. O processo ainda não está validado como APK funcional.

### Login real (quando a primeira compilação passar)
1. Pelo **navegador do celular**, vá a https://my.telegram.org e crie um app de desenvolvedor para obter credenciais **próprias**.
2. Na versão web do GitHub, abra `VoidGram → Settings → Secrets and variables → Actions` e configure `VOIDGRAM_API_ID` e `VOIDGRAM_API_HASH` como **Repository secrets**.
3. Execute novamente o workflow (aba `Actions`). Não cole o hash em comentários, README, Issues ou mensagens públicas.

Sem esses Secrets, o build, caso passe, entrega **VoidGram Preview**, que não pode autenticar conta. A assinatura da build atual é temporária, por isso **não** guarda caminho de atualização estável; não use como app principal nem guarde conversas importantes nele.

**Atenção:** o código da API e a infraestrutura Telegram permanecem sujeitos aos termos da plataforma. Recursos Premium validados no servidor não são desbloqueáveis no APK.
