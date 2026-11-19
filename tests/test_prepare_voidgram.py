"""Testes rápidos dos patches sem baixar o repositório gigante do Telegram."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "prepare_voidgram.py"
spec = importlib.util.spec_from_file_location("prepare_voidgram", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# Trechos reais do ProfileActivity.java do upstream fixado, com a mesma indentação.
PROFILE_FIXTURE = (
    "    private int languageRow;\n"
    "    void reset() {\n"
    "        languageRow = -1;\n"
    "    }\n"
    "                settingsSectionRow2 = rowCount++;\n"
    "                chatRow = rowCount++;\n"
    "            } else if (position == liteModeRow) {\n"
    "                presentFragment(new LiteModeSettingsActivity());\n"
    "                    } else if (position == liteModeRow) {\n"
    "                    } else if (position == devicesRow) {\n"
    "                        textCell.setTextAndIcon(LocaleController.getString(R.string.Devices), R.drawable.msg2_devices, true);\n"
    "                        position == questionRow || position == devicesRow || position == filtersRow ||\n"
    "                    position == questionRow || position == devicesRow || position == filtersRow ||\n"
    "            put(++pointer, devicesRow, sparseIntArray);\n"
)

class PrepareTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        fixtures = {
            "gradle.properties": "APP_PACKAGE=org.telegram.messenger\nAPP_VERSION_NAME=13.2.1\n",
            "TMessagesProj/src/main/java/org/telegram/messenger/BuildVars.java": (
                'public static int APP_ID = 4;\n'
                'public static String APP_HASH = "old";\n'
                'public static boolean SUPPORTS_PASSKEYS = true;\n'
                'public static boolean SUPPORTS_FPNV = true;\n'
                'public static boolean CHECK_UPDATES = true;\n'
            ),
            "TMessagesProj/src/main/res/values/strings.xml": (
                '<resources><string name="AppName">Telegram</string>\n'
                '<string name="AppNameBeta">Telegram Beta</string></resources>\n'
            ),
            "TMessagesProj/config/release/AndroidManifest_standalone.xml": (
                '<manifest><application android:icon="@mipmap/ic_launcher_sa" '
                'android:roundIcon="@mipmap/ic_launcher_sa" /></manifest>'
            ),
            "TMessagesProj_AppStandalone/build.gradle": (
                'debug { applicationIdSuffix ".web" }\n'
                'standalone { applicationIdSuffix ".web" }\n'
                'afat { ndk { abiFilters "armeabi-v7a", "arm64-v8a", "x86", "x86_64" } }\n'
                '        versionName APP_VERSION_NAME\n'
                "apply plugin: 'com.google.gms.google-services'\n"
            ),
            mod.PROFILE: PROFILE_FIXTURE,
            "TMessagesProj/build.gradle": (
                "    defaultConfig {\n"
                "        vectorDrawables.generatedDensities = ['mdpi', 'hdpi', 'xhdpi', 'xxhdpi']\n"
                "    }\n"
            ),
        }
        for name, data in fixtures.items():
            p = self.root / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(data, encoding="utf-8")

    def read(self, path):
        return (self.root / path).read_text(encoding="utf-8")

    def test_offline_preview_never_uses_official_api(self):
        self.assertEqual(mod.prepare(self.root), "PREVIEW_SEM_LOGIN")
        self.assertIn("APP_PACKAGE=com.pedrovoid.voidgram", self.read("gradle.properties"))
        vars = self.read("TMessagesProj/src/main/java/org/telegram/messenger/BuildVars.java")
        self.assertIn("APP_ID = 0;", vars)
        self.assertIn('APP_HASH = "00000000000000000000000000000000";', vars)
        self.assertIn("CHECK_UPDATES = false;", vars)
        self.assertIn("SUPPORTS_PASSKEYS = false;", vars)
        self.assertIn("VoidGram Preview", self.read("TMessagesProj/src/main/res/values/strings.xml"))
        self.assertIn('@drawable/voidgram_icon', self.read("TMessagesProj/config/release/AndroidManifest_standalone.xml"))
        self.assertIn('applicationIdSuffix ".beta"', self.read("TMessagesProj_AppStandalone/build.gradle"))
        self.assertNotIn("apply plugin: 'com.google.gms.google-services'",
                         self.read("TMessagesProj_AppStandalone/build.gradle"))
        self.assertTrue((self.root / "TMessagesProj/src/main/res/drawable/voidgram_icon.xml").is_file())

    def test_with_credentials(self):
        self.assertEqual(mod.prepare(self.root, "12345", "a" * 32), "LOGIN_HABILITADO")
        self.assertIn("APP_ID = 12345;", self.read("TMessagesProj/src/main/java/org/telegram/messenger/BuildVars.java"))
        self.assertIn('<string name="AppName">VoidGram</string>', self.read("TMessagesProj/src/main/res/values/strings.xml"))

    def test_version_and_default_abi(self):
        mod.prepare(self.root, version="0.2.1")
        app = self.read("TMessagesProj_AppStandalone/build.gradle")
        self.assertIn('versionName APP_VERSION_NAME + "-voidgram0.2.1"', app)
        self.assertIn('abiFilters "arm64-v8a" }', app)
        self.assertNotIn("x86", app)
        self.assertIn('ndk { abiFilters "arm64-v8a" }', self.read("TMessagesProj/build.gradle"))
        # A versão do upstream não pode ser alterada.
        self.assertIn("APP_VERSION_NAME=13.2.1", self.read("gradle.properties"))

    def test_custom_abis(self):
        mod.prepare(self.root, version="0.2.1", abis="arm64-v8a, armeabi-v7a")
        self.assertIn('ndk { abiFilters "arm64-v8a", "armeabi-v7a" }', self.read("TMessagesProj/build.gradle"))

    def test_refuses_bad_version_or_abi(self):
        for kwargs in ({"version": "v0.2"}, {"version": "0.2.1", "abis": "mips"},
                       {"version": "0.2.1", "abis": ""}, {"version": "0.2.1", "abis": "x86,x86"}):
            with self.assertRaises(ValueError):
                mod.prepare(self.root, **kwargs)

    def test_version_file_is_valid(self):
        self.assertRegex(mod.read_version(), r"^\d+\.\d+\.\d+$")

    def test_settings_entry_and_overlay(self):
        mod.prepare(self.root, version="0.3.0")
        p = self.read(mod.PROFILE)
        self.assertIn("    private int voidgramRow;", p)
        self.assertIn("        voidgramRow = -1;", p)
        # "Otimização na entrada": o item fica no topo da seção de Configurações.
        self.assertIn("settingsSectionRow2 = rowCount++;\n                voidgramRow = rowCount++;\n"
                      "                chatRow = rowCount++;", p)
        self.assertIn("presentFragment(new VoidGramSettingsActivity());", p)
        self.assertIn("R.drawable.voidgram_settings_icon", p)
        self.assertEqual(p.count("position == voidgramRow ||"), 2)
        self.assertIn("put(++pointer, voidgramRow, sparseIntArray);", p)
        self.assertTrue((self.root / "TMessagesProj/src/main/java/org/telegram/ui/VoidGramSettingsActivity.java").is_file())
        self.assertTrue((self.root / "TMessagesProj/src/main/res/values/voidgram_strings.xml").is_file())
        self.assertFalse((self.root / "README.md").exists())
        build = self.read("TMessagesProj/src/main/res/values/voidgram_build.xml")
        self.assertIn('name="VoidGramVersion" translatable="false">0.3.0<', build)
        self.assertIn(">desconhecido<", build)

    def test_overlay_never_overwrites_upstream(self):
        existing = self.root / "TMessagesProj/src/main/res/values/voidgram_strings.xml"
        existing.write_text("<resources/>", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            mod.prepare(self.root, version="0.3.0")
        self.assertEqual(existing.read_text(encoding="utf-8"), "<resources/>")

    def test_settings_patch_fails_loudly_if_upstream_changes(self):
        (self.root / mod.PROFILE).write_text(PROFILE_FIXTURE.replace("chatRow = rowCount++;", "chat = 1;"),
                                             encoding="utf-8")
        with self.assertRaises(ValueError):
            mod.prepare(self.root, version="0.3.0")

    def test_overlay_strings_are_valid_xml(self):
        import xml.etree.ElementTree as ET
        for xml in mod.OVERLAY_DIR.rglob("*.xml"):
            ET.parse(xml)

    def test_refuses_incomplete_or_invalid_credentials(self):
        with self.assertRaises(ValueError):
            mod.prepare(self.root, "123", "")
        with self.assertRaises(ValueError):
            mod.prepare(self.root, "abc", "a" * 32)
        with self.assertRaises(ValueError):
            mod.prepare(self.root, "1", "NOT_A_HASH")

    def test_missing_upstream_is_error(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(FileNotFoundError):
                mod.prepare(Path(d))

if __name__ == "__main__":
    unittest.main()
