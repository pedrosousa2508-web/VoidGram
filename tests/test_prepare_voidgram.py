"""Testes rápidos dos patches sem baixar o repositório gigante do Telegram."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "prepare_voidgram.py"
spec = importlib.util.spec_from_file_location("prepare_voidgram", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

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
