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
import shutil
import subprocess
from pathlib import Path

PACKAGE = "com.pedrovoid.voidgram"
VERSION_FILE = Path(__file__).resolve().parents[1] / "VERSION"
OVERLAY_DIR = Path(__file__).resolve().parents[1] / "overlay"
PROFILE = "TMessagesProj/src/main/java/org/telegram/ui/ProfileActivity.java"
ALLOWED_ABIS = ("arm64-v8a", "armeabi-v7a", "x86", "x86_64")
DEFAULT_ABIS = "arm64-v8a"

def read_version(path: Path = VERSION_FILE) -> str:
    version = path.read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError("VERSION precisa ter o formato N.N.N")
    return version

def parse_abis(value: str) -> list[str]:
    abis = [item for item in re.split(r"[,\s]+", value.strip()) if item]
    if not abis or len(set(abis)) != len(abis) or any(a not in ALLOWED_ABIS for a in abis):
        raise ValueError("ABIs válidas (sem repetir): " + ", ".join(ALLOWED_ABIS))
    return abis

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

def replace_count(text: str, old: str, new: str, expected: int, context: str) -> str:
    """Troca literal que precisa ocorrer exatamente `expected` vezes."""
    if text.count(old) != expected:
        raise ValueError(f"Esperado {expected} ocorrência(s), achei {text.count(old)}: {context}")
    return text.replace(old, new)

def apply_overlay(root: Path, overlay: Path) -> list[str]:
    """Copia arquivos novos do VoidGram; nunca sobrescreve arquivo do upstream."""
    copied = []
    for src in sorted(overlay.rglob("*")):
        if not src.is_file() or src.relative_to(overlay) == Path("README.md"):
            continue
        rel = src.relative_to(overlay)
        dest = root / rel
        if dest.exists():
            raise FileExistsError(f"overlay sobrescreveria arquivo do upstream: {rel}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
        copied.append(rel.as_posix())
    return copied

def upstream_commit(root: Path) -> str:
    if not (root / ".git").exists():
        return "desconhecido"
    try:
        out = subprocess.run(["git", "-C", str(root), "rev-parse", "--short=12", "HEAD"],
                             capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "desconhecido"
    return out if re.fullmatch(r"[0-9a-f]{7,40}", out) else "desconhecido"

def patch_profile(s: str) -> str:
    """Item "VoidGram" no topo das Configurações, abrindo VoidGramSettingsActivity."""
    s = replace_exact(s, r"^    private int languageRow;$",
                      "    private int languageRow;\n    private int voidgramRow;", "campo da linha")
    s = replace_exact(s, r"^        languageRow = -1;$",
                      "        languageRow = -1;\n        voidgramRow = -1;", "reset da linha")
    s = replace_exact(s, r"^                settingsSectionRow2 = rowCount\+\+;\n                chatRow = rowCount\+\+;$",
                      "                settingsSectionRow2 = rowCount++;\n"
                      "                voidgramRow = rowCount++;\n"
                      "                chatRow = rowCount++;", "posição no topo das Configurações")
    s = replace_exact(s, r"^            \} else if \(position == liteModeRow\) \{\n"
                         r"                presentFragment\(new LiteModeSettingsActivity\(\)\);$",
                      "            } else if (position == voidgramRow) {\n"
                      "                presentFragment(new VoidGramSettingsActivity());\n"
                      "            } else if (position == liteModeRow) {\n"
                      "                presentFragment(new LiteModeSettingsActivity());", "toque na linha")
    s = replace_exact(s, r"^                    \} else if \(position == devicesRow\) \{\n"
                         r"                        textCell\.setTextAndIcon\(LocaleController\.getString\(R\.string\.Devices\)",
                      "                    } else if (position == voidgramRow) {\n"
                      "                        textCell.setTextAndIcon(LocaleController.getString(R.string.VoidGramSettings), "
                      "R.drawable.voidgram_settings_icon, true);\n"
                      "                    } else if (position == devicesRow) {\n"
                      "                        textCell.setTextAndIcon(LocaleController.getString(R.string.Devices)",
                      "desenho da linha")
    # isEnabled e getItemViewType: cada método possui âncora independente.
    # O upstream fixado inclui stickersRow; os recuos são distintos.
    s = replace_exact(s, r"^                        position == questionRow \|\| position == devicesRow \|\| position == filtersRow \|\| position == stickersRow \|\|$",
                      "                        position == questionRow || position == devicesRow || position == filtersRow || position == stickersRow || position == voidgramRow ||",
                      "isEnabled da linha")
    s = replace_exact(s, r"^                    position == questionRow \|\| position == devicesRow \|\| position == filtersRow \|\| position == stickersRow \|\|$",
                      "                    position == questionRow || position == devicesRow || position == filtersRow || position == stickersRow || position == voidgramRow ||",
                      "getItemViewType da linha")
    s = replace_exact(s, r"^            put\(\+\+pointer, devicesRow, sparseIntArray\);$",
                      "            put(++pointer, devicesRow, sparseIntArray);\n"
                      "            put(++pointer, voidgramRow, sparseIntArray);", "animação da lista")
    return s

def rewrite(path: Path, transform) -> None:
    if not path.is_file():
        raise FileNotFoundError(f"Arquivo da base ausente: {path}")
    before = path.read_text(encoding="utf-8")
    after = transform(before)
    if before != after:
        path.write_text(after, encoding="utf-8")

def prepare(root: Path, api_id: str = "", api_hash: str = "",
            version: str | None = None, abis: str = DEFAULT_ABIS,
            overlay: Path = OVERLAY_DIR) -> str:
    version = read_version() if version is None else version
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError("Versão do VoidGram precisa ter o formato N.N.N")
    abi_list = parse_abis(abis)
    abi_gradle = ", ".join(f'"{a}"' for a in abi_list)
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

    # O google-services.json do upstream pertence ao Telegram e nao possui
    # cliente com o applicationId do VoidGram. Um build de preview nao deve
    # reutilizar esse Firebase, nem fingir uma configuracao valida.
    # Quando houver um projeto Firebase proprio, rever este patch e fornecer
    # google-services.json exclusivo pelo Actions Secrets.
    rewrite(app_gradle, lambda s: replace_exact(
        s, r"^apply plugin: 'com\.google\.gms\.google-services'$",
        "// Firebase desativado no VoidGram Preview; push FCM nao configurado.",
        "Google Services plugin do app standalone"
    ))

    # Versão própria: só o versionName do app muda. APP_VERSION_NAME e
    # versionCode do upstream ficam intactos (o código interno os utiliza).
    rewrite(app_gradle, lambda s: replace_exact(
        s, r"^(\s*)versionName APP_VERSION_NAME$",
        f'        versionName APP_VERSION_NAME + "-voidgram{version}"', "versionName do app"
    ))

    # Somente as arquiteturas pedidas: no empacotamento do app e na
    # compilação nativa da biblioteca (que, sem filtro, compila as quatro).
    rewrite(app_gradle, lambda s: replace_exact(
        s, r'abiFilters "armeabi-v7a", "arm64-v8a", "x86", "x86_64"',
        "abiFilters " + abi_gradle, "ABIs do app standalone"
    ))
    lib_gradle = root / "TMessagesProj/build.gradle"
    rewrite(lib_gradle, lambda s: replace_exact(
        s, r"^(\s*)vectorDrawables\.generatedDensities = [^\n]+$",
        "        vectorDrawables.generatedDensities = ['mdpi', 'hdpi', 'xhdpi', 'xxhdpi']\n"
        "        ndk { abiFilters " + abi_gradle + " }", "ABIs da biblioteca nativa"
    ))

    # Tela do VoidGram: arquivos novos do overlay + entrada nas Configurações.
    apply_overlay(root, overlay)
    build_res = root / "TMessagesProj/src/main/res/values/voidgram_build.xml"
    if build_res.exists():
        raise FileExistsError("voidgram_build.xml já existe no upstream")
    build_res.write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'
        f'    <string name="VoidGramVersion" translatable="false">{version}</string>\n'
        f'    <string name="VoidGramUpstreamCommit" translatable="false">{upstream_commit(root)}</string>\n'
        '</resources>\n', encoding="utf-8")
    rewrite(root / PROFILE, patch_profile)

    icon = root / "TMessagesProj/src/main/res/drawable/voidgram_icon.xml"
    icon.parent.mkdir(parents=True, exist_ok=True)
    icon.write_text(ICON_XML, encoding="utf-8")

    return "LOGIN_HABILITADO" if live else "PREVIEW_SEM_LOGIN"

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    args = parser.parse_args()
    abis = os.getenv("VOIDGRAM_ABIS", "") or DEFAULT_ABIS
    result = prepare(args.source, os.getenv("VOIDGRAM_API_ID", ""), os.getenv("VOIDGRAM_API_HASH", ""), abis=abis)
    print(f"VoidGram {read_version()} preparado: {result}")
    print("Arquiteturas: " + ", ".join(parse_abis(abis)))
    print("Pacote de depuração previsto: " + PACKAGE + ".beta")
    if result == "PREVIEW_SEM_LOGIN":
        print("Credenciais próprias ausentes: este APK é apenas uma prévia técnica; login NÃO funciona.")

if __name__ == "__main__":
    main()
