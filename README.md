# VoidGram 🪐
**Cliente Android não oficial do ecossistema Telegram — projeto PedroVoid.**

Um mensageiro personalizado, extensível e transparente: preservar toda a experiência básica de mensagens e agregar recursos **locais e gratuitos** de personalização, tradução/transcrição, organização e mídia. Projeto pensado para desenvolvimento **100% pelo celular**, com compilações remotas no GitHub Actions e testes no POCO C75 (Android 16 / HyperOS 3).

> **Status em 14/11/2026 — v0.2.1:** o APK experimental compila no GitHub Actions a partir do Telegram Android 13.2.1 (commit fixado), com pacote, nome, ícone e API próprios. Login e carregamento de conversas foram confirmados no POCO C75. Chamadas e notificações ainda não foram testadas. **Nenhum recurso extra dos forks foi implementado.**

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
1. [x] **M1** — importar base, configurar API própria, identidade VoidGram e produzir APK debug via Actions.
2. [ ] **M2** — configurar visual, tema, acessibilidade e desempenho.
3. [ ] **M3** — organização local, player e utilitários.
4. [ ] **M4** — transcrição/tradução offline opcionais.
5. [ ] **M5** — qualidade, privacidade, performance e versão assinada.

**VoidGram não é afiliado, patrocinado ou endossado pelo Telegram.**


## Compilação (GitHub Actions)
- [Workflow](.github/workflows/voidgram-android.yml): roda os testes, baixa o Telegram Android no commit fixado, aplica o patch e compila.
- [Script de personalização](scripts/prepare_voidgram.py): pacote `com.pedrovoid.voidgram.beta`, nome, ícone, API própria, versão do VoidGram (arquivo [`VERSION`](VERSION)) e arquiteturas do APK. Desliga passkeys, o atualizador oficial e o Firebase do Telegram.
- [Testes do script](tests/test_prepare_voidgram.py).

O código do Telegram é obtido a cada execução e **não** fica neste repositório.

### Secrets (Settings → Secrets and variables → Actions)
| Secret | Para quê |
|---|---|
| `VOIDGRAM_API_ID`, `VOIDGRAM_API_HASH` | Credenciais próprias de https://my.telegram.org. Obrigatórios. |
| `VOIDGRAM_ARTIFACT_PASSWORD` | Senha (12+ caracteres) do zip do APK. Sem ela o APK **não é publicado**, porque o repositório é público. |
| `VOIDGRAM_KEYSTORE_PASSWORD` | Senha (12+ caracteres) da assinatura fixa. |
| `VOIDGRAM_KEYSTORE_BASE64` | A assinatura fixa, gerada uma única vez (abaixo). |

Nunca cole esses valores em commits, Issues, README ou mensagens.

### Assinatura fixa (uma única vez)
1. Crie `VOIDGRAM_ARTIFACT_PASSWORD` e `VOIDGRAM_KEYSTORE_PASSWORD`.
2. Em **Actions → VoidGram Android → Run workflow**, escolha o modo `gerar-keystore`.
3. Baixe o artefato `VoidGram-Keystore-protegido` (expira em 1 dia) e abra o zip com a senha do artefato (AES-256; se o gerenciador de arquivos não abrir, use o ZArchiver).
4. Copie todo o conteúdo de `VOIDGRAM_KEYSTORE_BASE64.txt` para o Secret `VOIDGRAM_KEYSTORE_BASE64`.
5. Guarde o zip em local seguro. Perder a chave ou a senha obriga a reinstalar o app.

Com a assinatura fixa, cada novo APK instala por cima do anterior e preserva login e dados. Sem ela, o build usa uma assinatura temporária e avisa.

### Baixar o APK
O artefato `VoidGram-APK-protegido` contém um zip com senha, com o APK e um `BUILD_INFO.txt` (versão, commits, tipo de assinatura, impressão digital do certificado e SHA-256). O APK padrão é só `arm64-v8a`; outras arquiteturas podem ser pedidas no campo `abis` ao executar o workflow.

## Licença
O VoidGram deriva do Telegram para Android e é distribuído sob a [GNU GPL versão 2 ou posterior](LICENSE). O código-fonte correspondente a cada APK é este repositório no commit indicado em `BUILD_INFO.txt`, aplicado sobre o commit do upstream ali registrado.

**Atenção:** a API e a infraestrutura do Telegram permanecem sujeitas aos termos da plataforma. Recursos Premium validados no servidor não são desbloqueáveis no APK.
