# AGENTS.md — regras do VoidGram para qualquer assistente de IA

Leia este arquivo antes de alterar o repositório. O README descreve o uso; aqui ficam as regras.

## Projeto
- Cliente Android não oficial do Telegram, projeto PedroVoid. Não é afiliado ao Telegram.
- Base: `DrKLO/Telegram` (GPL-2.0-ou-posterior), baixado a cada build no commit fixado em `UPSTREAM_SHA` do workflow. O código do Telegram **não** fica neste repositório.
- Este repositório contém só: workflow, `scripts/prepare_voidgram.py` (patch), testes, `VERSION` e documentação.
- Pacote: `com.pedrovoid.voidgram.beta`. Aparelho de teste: POCO C75, Android 16 / HyperOS 3.
- O dono trabalha 100% pelo celular: GitHub web e GitHub Actions. Não há computador nem Android Studio.

## Nunca
- Recomeçar o projeto, trocar a base ou reescrever o que já funciona.
- Escrever `api_id`, `api_hash`, senhas ou keystore em arquivos, commits, logs, Issues ou mensagens. Tudo fica em Actions Secrets.
- Imprimir Secrets nos logs (o repositório é público) ou publicar APK sem o zip com senha.
- Gerar outro keystore quando `VOIDGRAM_KEYSTORE_BASE64` já existe: isso impede atualizar o app instalado.
- Mudar o `applicationId` ou a assinatura: o usuário perderia login e dados.
- Usar credenciais de API, marca, ícone ou assets de outros clientes.
- Implementar modo fantasma, falsificação de leitura/presença, bloqueio de autodestruição ou remoção de mensagens patrocinadas.
- Prometer recursos Premium: o que o servidor valida não é desbloqueável no APK.
- Copiar código de forks GPL-3.0 (NekoX, Nagram) sem decisão explícita do dono; prefira reimplementar a ideia.
- Contratar serviços ou gastar créditos sem autorização.

## Como trabalhar
1. **Planejar → implementar → testar → aprovar** são etapas separadas. Mudanças de maior impacto esperam aprovação do dono.
2. Uma mudança por commit, pequena e reversível. Mudanças de interface ficam separadas de mudanças de rede/protocolo.
3. Todo patch novo no script usa `replace_exact` (falha se o alvo não existir exatamente uma vez) e ganha teste em `tests/`.
4. Antes de enviar: `python -m unittest discover -s tests -v`.
5. Valide patches contra os arquivos reais do upstream no commit fixado, não só contra os fixtures.
6. Trabalhe em branch; o `main` só recebe o que compilou no Actions.
7. Ao atualizar o `UPSTREAM_SHA`, faça isso em commit próprio e rode o checklist de regressão completo.

## O que conta como evidência
- "Compilou" ≠ "funciona". Build verde prova apenas que o APK foi gerado.
- Uma função só é declarada funcionando depois de testada pelo dono no POCO C75, seguindo `docs/CHECKLIST_REGRESSAO.md`.
- Em relatórios, separe: testado no aparelho, verificado no CI, verificado só localmente, e suposição.
- Registre em cada entrega: versão, commit, número do build e o `BUILD_INFO.txt` do APK.

## Versão e rollback
- A versão do VoidGram fica em `VERSION` (formato N.N.N) e entra no nome de versão do app.
- Cada marco testado recebe uma tag `vN.N.N`. Para voltar atrás, recompila-se a tag anterior; com a assinatura fixa, o APK instala por cima se o código de versão não for menor.
- O backup do keystore fica com o dono, fora do repositório.
