# Método CAVERNA no VoidGram — integração operacional

**Registrado em:** 23/11/2026  
**Escopo:** documentação e disciplina de desenvolvimento do cliente Android VoidGram (não é alteração de funcionalidade).  
**Fonte principal:** [Biblioteca Mestre — Caverna da IA (Notion)](https://app.notion.com/p/4216139f13ed81e5872acadc7618d83c?pvs=204).  
**Protocolo adaptado:** [JARVIS × CAVERNA v2.0](https://app.notion.com/p/4216139f13ed81a0b10df88c989c06ef).  
**Prioridade em conflitos:** estado real do repositório e do CI, decisões expressas do responsável e as regras existentes do [AGENTS.md](../AGENTS.md) prevalecem sobre exemplos didáticos. Os cinco agentes são referências de especialidade; a leitura de seus manuais não significa execução de plugins.

## Estado de continuidade verificado em 23/11/2026

- O desenvolvimento usa `pedrosousa2508-web/VoidGram`, GitHub Actions e dispositivo Android POCO C75 (Android 16 / HyperOS 3), sem exigir computador.
- `main` tem `VERSION=0.2.1`; [PR #3](https://github.com/pedrosousa2508-web/VoidGram/pull/3) está aberto, com `VERSION=0.3.0` na branch `ccr-376dd754-itsyed`.
- [Build de 19/11/2026 da branch de desenvolvimento](https://github.com/pedrosousa2508-web/VoidGram/actions/runs/44492421297): GitHub Actions passou e publicou o artefato `VoidGram-APK-protegido`, usando assinatura fixa e `arm64-v8a`. Isso comprova compilação, **não** teste do novo menu ou atualização no aparelho.
- Relatos anteriores do responsável confirmaram login e conversas no POCO; novas funções da 0.3.0 (tela VoidGram, navegação e atualização por cima) **ainda não foram verificadas no aparelho nesta integração**.
- A fase seguinte definida na conversa é avaliar ideias de forks (Nekogram, NekoX, Nagram, Forkgram, Mercurygram), sem copiar código incompatível nem prometer Premium do servidor.

## Método CAVERNA — aplicação sem burocracia

| Letra | Significado da fonte | Critério operacional no VoidGram |
| --- | --- | --- |
| **C** | **Contexto** | Identificar versão, branch, upstream fixado, ambiente Android, decisão aprovada e bug/recurso concreto. |
| **A** | **Ação** | Especificar se a tarefa é diagnosticar, alterar um arquivo, compilar, testar ou publicar; evitar verbos vagos. |
| **V** | **Variáveis** | Reutilizar `VERSION`, `UPSTREAM_SHA`, `BUILD_INFO.txt`, logs, scripts, APK e diferenças da branch; jamais revelar Secrets. |
| **E** | **Entrega** | Produzir patch/comits, PR, evidência do Actions, artefato ou roteiro de teste correspondente ao pedido. |
| **R** | **Regras** | Preservar assinatura, `applicationId`, login, conversas, GPL, chaves, modificações anteriores e possibilidade de rollback. |
| **N** | **Nível de qualidade** | Teste automatizado, patch válido contra upstream real, build verificável e testes no POCO para alegações de funcionamento. |
| **A** | **Ajuste** | Depois de evidência concreta, manter o válido, corrigir só a falha, testar novamente e registrar o resultado. |

As seis primeiras letras estruturam a tarefa. **Ajuste** é avaliação e correção posterior; não significa que uma revisão já ocorreu.

## Especialidades — o que realmente é aplicável

- **Gandalf 3.0 (arquitetura de prompts):** traduzir solicitação em especificação curta, critérios de aceite, limites de escopo, dependências e instruções de continuidade. Usar `DIAGNOSTICAR`, `LAPIDAR`, `TESTAR` ou `RETOMAR` apenas quando compatíveis com a tarefa real. O entregável padrão do agente é um prompt; este repositório precisa de código e builds quando solicitado.
- **Prisma (direção de imagens):** identidade VoidGram, ícones e telas. Separar invariantes da interface aprovada de paleta, escala, tipografia ou ilustração que possam mudar. Uma arte gerada não é componente Android implementado; validar legibilidade e layout no celular.
- **Forja (desenvolvimento de jogos):** reutilizar somente técnicas **transversais** de protótipo mínimo, DEPURAR, checkpoint, patch localizado, teste regressivo e versão rastreável. Não é um agente Android nativo nem justifica criar jogos.
- **Atlas (mundos e construções):** usar princípios de escala, circulação, hierarquia e acesso somente como referência para arquitetura de navegação visual, se aplicável. Não executar exemplos de Blender/Minecraft nem alegar que Atlas é especialista em UI Android.
- **Diretor (vídeo/desafios):** quando o responsável pedir apresentação, documentar roteiro de captura da função real, testes e changelog; não inventar métricas, cenas, vídeos, timestamps nem publicações.

Referências integrais: [Gandalf](https://app.notion.com/p/4216139f13ed81b7a7a5cd5f83416bd8), [Prisma](https://app.notion.com/p/4216139f13ed8167a702e04483bd3ad4), [Forja](https://app.notion.com/p/4216139f13ed81f2aee8f08cf298dacf), [Atlas](https://app.notion.com/p/4216139f13ed81b4a36fefcf0e00ea61), [Diretor](https://app.notion.com/p/4216139f13ed81e8a176c6059d4eafe1). Não duplicar integralmente as configurações no repositório público.

## Pipeline de implementação e evidência

1. Consultar `AGENTS.md`, `README.md`, `VERSION`, `docs/CHECKLIST_REGRESSAO.md`, o último commit e as branches/PRs abertos. **Não reiniciar.**
2. Definir o menor recorte da tarefa e os arquivos realmente afetados. Para alterações de comportamento, prever teste reproduzível e reversão.
3. Implementar em branch; se necessário, usar `replace_exact` no patch e adicionar fixture/teste. Não alterar `main` com recurso não validado.
4. Separar resultados: **proposto**, **produzido** (arquivo/commit), **executado** (testes/CI), **verificado** (evidência), **pendente** (no POCO).
5. Ao finalizar: links para commit, PR, workflow e APK quando existirem; versão; SHA/certificado; testes realizados e ainda pendentes. Não confundir sucesso do CI com login, notificações ou tela funcionando.
6. Só abrir caminho para forks após a validação da v0.3.0. Pesquisar licença, compatibilidade de versão e consequências sobre privacidade; implementar um recurso por vez, com rollback.

### Critérios de aceite específicos da v0.3.0

- Build da branch de desenvolvimento concluído e pacote verificável: **evidência de CI existente**.
- Instalar por cima da v0.2.1 **com mesma assinatura fixa**, sem perda de login e conversas: **pendente de teste real**.
- Entrada `VoidGram` nas Configurações visível, tela abre/fecha, informações de versão e links coerentes: **pendente de teste real**.
- PR #3 revisado e integrado após avaliação, não como consequência automática desta integração: **pendente**.

## O que este registro fez e não fez

- **Fez:** vinculou o curso e o protocolo aos procedimentos do VoidGram, preservando as regras atuais de `AGENTS.md`, as versões e o PR aberto.
- **Não fez:** compilar APK, executar plugins separados, iniciar os exercícios do curso, ativar automação, adicionar recurso de fork, alterar assinatura ou validar a 0.3.0 no POCO.
- **Segurança:** não armazenar `VOIDGRAM_API_HASH`, senhas, conteúdo do keystore ou base64 em documentação pública. O conteúdo do curso fica no Notion; arquivos binários originais não são necessários para implementar estas regras textuais.
