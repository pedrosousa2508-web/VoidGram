# VoidGram — Pesquisa técnica de base e forks (v0.1)
Data da auditoria: 2026-11-09. Plataforma-alvo: Android 16, POCO C75. Desenvolvimento e testes do usuário **somente pelo celular**, com compilação remota no GitHub Actions.

## Estado observado
- Repositório VoidGram criado, ramo `main`, com README inicial. **Ainda não contém os códigos dos clientes nem APK compilado.**
- A pesquisa abaixo inspecionou README, estrutura de código, arquivos de configuração, workflows e metadados de repositórios públicos; **não é auditoria integral linha a linha**, nem teste de build/execução.
- Todo recurso citado está **planejado/avaliado**, não implementado no VoidGram.

## Fontes e decisões de base

| Cliente | Fonte | Referência observada em 09/11/2026 | Papel / achados |
|---|---|---|---|
| Telegram Android (original) | https://github.com/DrKLO/Telegram | `7be672ead283d022812d75c729d3a04dd4c2a2c6` | **Base candidata prioritária**. Código Android oficial, GPL-2.0; bibliotecas nativas, MTProto, chats, mídia, chamadas e manutenção de protocolo. Requer SDK 36 e NDK 27.2.12479018 conforme README. |
| Nekogram | https://github.com/Nekogram/Nekogram | `199abde0f100d92cee8d925337561633e6e11186` | Referência de tradução, gestos, configurações locais, reprodução e personalização; `NekoConfig.java` expõe ações de duplo toque, câmera, transcrição e opções de interface. |
| NekoX (legado) | https://github.com/NekoX-Dev/NekoX | `3581a10f8ecaa0f6d42d7a77442742caf95c6a13` | Preservar boas ideias: múltiplas contas, proxies, packs de emoji, organização, download e QR. Último push observado em fevereiro de 2026; parte dos motores de proxy é declarada **não mantida**. Não usar como base única. |
| Nagram | https://github.com/NextAlone/Nagram | `8f2a8a03aa7aec599150b09d302bfd5023283344` | Continuação derivada do NekoX: combinar mensagens, estilização de texto, desfazer/refazer, prévia rolável, supressão de ruído, organização, Telegram local. GPL-3.0: requer verificação específica de compatibilidade de licença antes de transplantar código. Sua marca e ícone não são livres para reuso. |
| Mercurygram | https://github.com/Mercurygram/Mercurygram | `7a23db2f47eccc82ec21fd563709025b62a6472c` | Referência para engenharia de patches, atualizações via upstream, privacidade, notificações alternativas, pastas locais, builds reproduzíveis e atestação. |
| Forkgram | https://github.com/forkgram/TelegramAndroid | `405bfeb5732c54684b26c3b40e51dcd7a1ed03da` | Referência para fixar conversas *localmente* além do limite sincronizado, mídias, opções de interface e privacidade visual. |
| Telegram-FOSS | https://github.com/Telegram-FOSS-Team/Telegram-FOSS | README/estrutura inspecionados | Referência para builds sem componentes Google, substituição/compilação de binários nativos, push alternativo e dependências verificáveis. |
| exteraGram | https://github.com/exteraSquad/exteraGram | Arquivado em 2026 | Referência histórica para Material You, personalização, player e arquitetura experimental de plugins. Não usar diretamente como base desatualizada. |
| OwlGram | https://github.com/OwlGramDev/OwlGram | Arquivado em 2023 | Somente inspiração histórica; reavaliar segurança e licença de qualquer componente. |
| Telegram X | https://github.com/TGX-Android/Telegram-X | `bf82021249e358337b8e4d3f219e0d2c9561eb79` | Arquitetura **alternativa**, baseada em TDLib; não misturar diretamente projeto e módulos com o cliente MTProto original sem projeto de integração específico. GPL-3.0. |
| Cherrygram | https://github.com/Qing0721/Cherrygram | Código público antigo com lacunas; versões atuais relatadas como não totalmente abertas | Inspecionar ideias de UI, nunca copiar trechos sem licença, procedência e revisão de segurança. |
| AyuGram | https://docs.ayugram.one/android/ | Documentação histórica de funções com violação de ToS | **Não incorporar** ghost mode, preservação de autodestruição, ou outras alterações que burlam as garantias de privacidade dos participantes. |

Fontes oficiais de requisitos: https://core.telegram.org/api/terms, https://core.telegram.org/api/premium, https://www.telegram.org/faq_premium?setln=pt-br, https://core.telegram.org/api/obtaining_api_id.

## Classificação de funcionalidades

### A. Implementáveis localmente, sem conta Premium (sujeito a teste)
- Temas, ícones e animações **próprios** VoidGram; controles Material You; ajustes de densidade/interface e modo econômico no POCO C75.
- Player com fila, temporizador para dormir, equalização via capacidades locais, velocidade para áudios e organização de arquivos.
- Transcrição de áudio **local** por modelo opcional (ex.: Vosk, https://github.com/alphacep/vosk-api), com download de modelo autorizado e alerta de tamanho/uso de memória.
- Tradução local de texto via modelo obtido com consentimento (ex.: ML Kit on-device, https://developers.google.com/ml-kit/language/translation/android), observando termos, rede e espaço.
- Pastas, fixados e etiquetas adicionais **locais**, sem afirmar que sincronizam com Telegram nem excedem quotas do servidor.
- Múltiplas contas, QR, opções avançadas de encaminhamento, cópia, ordenação, gestos, nome de arquivos, controles de câmera e visualização de dados que a API realmente retorna.
- Fontes/emoji/estilos próprios **na interface local**; não garantir que outros usuários vejam ícones/emoji Premium ou de fonte personalizada.

### B. Dependem do servidor, licença/assinatura ou regras do Telegram
- Upload de 4 GB para conta comum, quota Premium de pastas/canais/stories, velocidade prioritária de transferência, badge oficial Premium, reações/emoji Premium como envio de conta não Premium, status Premium, usuários/nomes reservados, recursos pagos em Stars.
- Tentar trocar flag `premium` no app **não altera autorização do servidor**. A API expõe o status de assinatura para o próprio usuário.
- Conteúdo patrocinado oficial em canais não deve ser suprimido por fork: ToS da API exige suporte.
- Recursos disponibilizados a usuários gratuitos pela própria API continuam utilizáveis sem assinatura — ex.: receber/baixar arquivos grandes publicados por assinantes, conforme FAQ.

### C. Excluídos do projeto
- Falsificar recibos de leitura, digitação, online/visto por último, ou impedir autodestruição em chats secretos.
- Desabilitar verificação de assinatura/JNI sem análise e alternativa segura.
- Usar `api_id`/`api_hash` de outros clientes, incorporar ícone/logo do Telegram/Nagram, publicar chaves de assinatura no código.
- Copiar código GPLv3/fechado ou assets protegidos sem comprovar compatibilidade; adotar bibliotecas obsoletas de proxy ou suprimir mensagens patrocinadas oficiais.
- Coletar conversas para treinamento de IA: restrito pelos termos de conteúdo da plataforma.

## Proposta técnica: manutenção e segurança
1. **Base:** fork rastreável do original `DrKLO/Telegram`, atualizações frequentes do upstream e diffs pequenos. Guardar SHA e changelog de cada integração.
2. **Identidade:** nome VoidGram; package/applicationId proposto `com.pedrovoid.voidgram`, instalação separada do Telegram; arte e marcas inéditas. Base GPL-2.0: manter avisos de copyright e publicar fonte correspondente ao APK. Revisão jurídica específica para transplantes GPLv3.
3. **Módulos:** `voidgram/settings`, `voidgram/theme`, `voidgram/media`, `voidgram/translate`, `voidgram/offline_transcribe`, `voidgram/local_folders`, `voidgram/privacy`, `voidgram/update`; adaptar ao layout real do upstream antes de criar patches.
4. **Segurança:** uso do MTProto original; contas e sessões sob controle do usuário; não desativar garantias de privacidade; criptografar dados locais sensíveis; não imprimir hashes/chaves/telefones em logs; permissões mínimas; não enviar conteúdo a serviços de terceiros sem opt-in explícito.
5. **Build remoto:** GitHub Actions Ubuntu + JDK/Gradle + Android SDK 36, NDK 27.2.12479018 (reconferir com SHA adotado), submódulos recursivos. Primeiro validar depêndencias/identidade; depois build debug; depois APK assinado separadamente, sem expor keystore. Adotar cache com limites e releases verificáveis. Em geral exige espaço/tempo de CI expressivos.
6. **Credenciais:** obter `api_id` e `api_hash` próprios em https://my.telegram.org; armazenar em GitHub **Actions Secrets**. Nunca colar em issue/README/commit/chat público. Configurar Firebase próprio somente se arquitetura de push escolhida exigir; prever fallback sem Google.
7. **Testes:** login por conta própria; enviar/receber chats, mídia, áudios, chamadas, login múltiplo, notificações em segundo plano/HyperOS 3, bateria/RAM, acessibilidade, atualização sem perder dados, segurança de chats secretos; rodar unit/instrumentation e confirmar APK no POCO C75.
8. **Publicação:** documentação reproduzível e changelog, assinatura própria, verificação SHA256 e atualização do código-fonte junto a cada release.

## Entregas por marcos
- **M0 (pesquisa):** inventário, licenças, riscos e plano em repositório. ✅
- **M1 (fonte/build):** importar base oficial rastreável, renomear aplicação, configurar build debug via GitHub Actions e gerar APK instalável. ⬜
- **M2 (experiência):** tema VoidGram, preferências e acessibilidade no POCO C75. ⬜
- **M3 (utilitários):** organização local, ações de chat, player e downloads. ⬜
- **M4 (offline):** tradução/transcrição opcionais sem assinatura Premium. ⬜
- **M5 (hardening):** testes de privacidade, atualização, documentação, compatibilidade, performance e release assinado. ⬜

## Verificação dos fatos
Este documento é um inventário preliminar profissional com **inspeção seletiva do código e README**. Não há alegação de auditoria exaustiva de cada commit/arquivo, de integração dos forks ou de um APK funcional. O próximo passo técnico é criar a linha de build na infraestrutura remota sem comprometer credenciais e testar um primeiro APK real.
