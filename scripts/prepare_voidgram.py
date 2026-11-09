#!/usr/bin/env python3
"""Aplica identidade VoidGram em um checkout rastreável do Telegram Android.

Uso: python3 scripts/prepare_voidgram.py --source Telegram
Sem API_ID/API_HASH próprios, gera somente tech preview (login indisponível).
Nunca coloque credenciais no repositório. Use GitHub Actions Secrets.
"""
from __future__ import annotations

import argparse
import os
import re
from pathlib import Path

PACKAGE = "com.pedrovoid.voidgram"

ICON_XML = """<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp" android:height="108dp"
    android:viewportWidth="108" android:viewportHeight="108">
    <path android:fillColor="#111528"
        android:pathData="M54,4 a50,50 0,1 0,0 100 a50,50 0,1 0,0 -100"/>
    <path android:fillColor="#00000000" android:strokeColor="#5BDCF2"
        android:strokeWidth="3"
        android:pathData="M54,14 a40,40 0,1 0,0 80 a40,40 0,1 0,0 -80"/>
    <path android:fillColor="#A76CFF"
        android:pathData="M22,35 L34,35 L46,68 L58,35 L70,35 L51,79 L41,79 Z"/>
    <path android:fillColor="#5BDCF2"
        android:pathData="M62,35 L76,35 Q91,35 91,49 Q91,63 76,63 L73,63 L73,79 L62,79 Z M73,45 L73,54 L76,54 Q81,54 81,49 Q81,45 76,45 Z"/>
</vector>
"""

def replace_exact(text: str, pattern: str, replacement: str, context: str) -> str:
    changed, count = re.subn(pattern, lambda _match: replacement, text, count=1, flags=re.MULTILINE)
    if count != 1:
        raise ValueError(f"Falha ao localizar exatamente uma vez: {context}")
    return changed

def rewrite(path: Path, transform) -> None:
    if not path.is_file():
        raise FileNotFoundError(f"Arquivo da base ausente: {path}")
    before = path.read_text(encoding="utf-8")
    after = transform(before)
    if before != after:
        path.write_text(after, encoding="utf-8")

def prepare(root: Path, api_id: str = "", api_hash: str = "") -> str:
    if not (root / "TMessagesProj" / "src" / "main").is_dir():
        raise FileNotFoundError("Diretório não parece conter o Telegram Android original")
    if bool(api_id) != bool(api_hash):
        raise ValueError("Configure VOIDGRAM_API_ID e VOIDGRAM_API_HASH juntos")
    live = bool(api_id)
    if live and (not api_id.isdecimal() or int(api_id) <= 0 or not re.fullmatch(r"[0-9a-fA-F]{32}", api_hash)):
        raise ValueError("API_ID precisa ser positivo e API_HASH precisa ter 32 dígitos hexadecimais")
    api_id = api_id if live else "0"
    api_hash = api_hash.lower() if live else "0" * 32
    name = "VoidGram" if live else "VoidGram Preview"

    properties = root / "gradle.properties"
    rewrite(properties, lambda s: replace_exact(
        s, r"^APP_PACKAGE=[^\n]+$", "APP_PACKAGE=" + PACKAGE, "APP_PACKAGE"
    ))

    buildvars = root / "TMessagesProj/src/main/java/org/telegram/messenger/BuildVars.java"
    def patch_vars(s: str) -> str:
        s = replace_exact(s, r"public static int APP_ID\s*=\s*\d+;", f"public static int APP_ID = {api_id};", "APP_ID")
        s = replace_exact(s, r'public static String APP_HASH\s*=\s*"[^"]*";',
                          f'public static String APP_HASH = "{api_hash}";', "APP_HASH")
        s = replace_exact(s, r"public static boolean SUPPORTS_PASSKEYS\s*=\s*(true|false);",
                          "public static boolean SUPPORTS_PASSKEYS = false;", "passkeys oficiais")
        s = replace_exact(s, r"public static boolean SUPPORTS_FPNV\s*=\s*(true|false);",
                          "public static boolean SUPPORTS_FPNV = false;", "PNV oficial")
        s = replace_exact(s, r"public static boolean CHECK_UPDATES\s*=\s*(true|false);",
                          "public static boolean CHECK_UPDATES = false;", "updater oficial")
        return s
    rewrite(buildvars, patch_vars)

    strings = root / "TMessagesProj/src/main/res/values/strings.xml"
    def patch_strings(s: str) -> str:
        s = replace_exact(s, r'<string name="AppName">[^<]+</string>',
                          f'<string name="AppName">{name}</string>', "AppName")
        s = replace_exact(s, r'<string name="AppNameBeta">[^<]+</string>',
                          '<string name="AppNameBeta">VoidGram Beta</string>', "AppNameBeta")
        return s
    rewrite(strings, patch_strings)

    # Standalone evita configurar um Firebase de terceiros no protótipo.
    # Todas as variantes de ícone desse manifesto passam a usar a marca VoidGram.
    manifest = root / "TMessagesProj/config/release/AndroidManifest_standalone.xml"
    def patch_manifest(s: str) -> str:
        replaced, count = re.subn(r'android:(icon|roundIcon)="@mipmap/[^"]+"',
                                  lambda m: f'android:{m.group(1)}="@drawable/voidgram_icon"', s)
        if count < 2:
            raise ValueError("Não foi possível substituir ícones do manifesto standalone")
        return replaced
    rewrite(manifest, patch_manifest)

    app_gradle = root / "TMessagesProj_AppStandalone/build.gradle"
    rewrite(app_gradle, lambda s: replace_exact(
        s, r'applicationIdSuffix "\.web"', 'applicationIdSuffix ".beta"', "suffix da variante debug"
    ))

    icon = root / "TMessagesProj/src/main/res/drawable/voidgram_icon.xml"
    icon.parent.mkdir(parents=True, exist_ok=True)
    icon.write_text(ICON_XML, encoding="utf-8")

    return "LOGIN_HABILITADO" if live else "PREVIEW_SEM_LOGIN"

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    args = parser.parse_args()
    result = prepare(args.source, os.getenv("VOIDGRAM_API_ID", ""), os.getenv("VOIDGRAM_API_HASH", ""))
    print(f"VoidGram preparado: {result}")
    print("Pacote de depuração previsto: " + PACKAGE + ".beta")
    if result == "PREVIEW_SEM_LOGIN":
        print("Credenciais próprias ausentes: este APK é apenas uma prévia técnica; login NÃO funciona.")

if __name__ == "__main__":
    main()
