# overlay/

Arquivos **novos** do VoidGram, organizados na mesma árvore do Telegram Android.
O `scripts/prepare_voidgram.py` copia cada arquivo para o checkout do upstream antes de compilar.

Regras:
- Só arquivos novos. Se um arquivo já existir no upstream, o script falha em vez de sobrescrever.
  Mudanças em arquivos do Telegram são feitas como patch no script, com `replace_exact` e teste.
- Nomes com prefixo `VoidGram`/`voidgram_` para não colidir com o upstream.
- Este `README.md` não é copiado.
