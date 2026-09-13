import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VERIFIER = ROOT / ".claude/scripts/verify_keymap.py"
KEYMAP = ROOT / "config/corne.keymap"


def verify(content):
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        target = root / "config/corne.keymap"
        target.parent.mkdir()
        target.write_text(content)
        return subprocess.run(
            [sys.executable, str(VERIFIER)],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )


class VerifyKeymapTests(unittest.TestCase):
    def test_rejects_nontransparent_alternate_layout_thumb(self):
        content = re.sub(
            r"&trans\s+&trans\s+&trans\s+&trans\s+&trans\s+&trans",
            "&kp ESC &trans &trans &trans &trans &trans",
            KEYMAP.read_text(),
            count=1,
        )

        result = verify(content)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Dvorak: thumb bindings must be transparent", result.stdout)

    def test_rejects_adjust_layer_that_is_not_highest(self):
        content = KEYMAP.read_text()
        start = content.index("                adjust_layer {")
        end = content.index("                };", start) + len("                };")
        adjust_layer = content[start:end]
        content = content[:start] + content[end:]
        insert_at = content.index("                colemak_layer {")
        content = content[:insert_at] + adjust_layer + "\n\n" + content[insert_at:]

        result = verify(content)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Adjust: must be the highest-numbered layer", result.stdout)

    def test_rejects_mismatched_adjust_layer_number(self):
        content = KEYMAP.read_text().replace("#define ADJUST    6", "#define ADJUST    5")

        result = verify(content)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Adjust: define must equal highest layer number", result.stdout)


if __name__ == "__main__":
    unittest.main()
