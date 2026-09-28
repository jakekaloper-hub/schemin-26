import json
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

APPROVED = {
    "Jake Kaloper": "The Trade Jedi",
    "Kevin Zeek": "The Predator Board",
    "Jordan Hollingshead": "Win Ugly",
    "David Babb": "Hostile Takeover",
    "Wilson Look": "The Philosopher-Warrior",
    "Phillip Pitts": "The Podium Shadow",
    "Brandon Pryor": "The Chili Outlaw",
    "Manning Welty": "The Weather System",
    "Austin Byars": "The Belt Keeper",
    "Bobby Mitchell": "Swamp-Born Menace",
    "Zach Wilson": "King of the Impossible Lie",
    "Ben Whipple": "The People's Champ",
}

SOURCE_SHA256 = "ddaf366e1075e9b895081f2c98737cbb2d789ccdb043ce2883ed21dbfe5f0bab"

class CharacterCanonLockTests(unittest.TestCase):
    def test_visual_lock_receipt_is_present(self):
        text = (ROOT / "canon" / "SCHEMIN_26_MASTER_VISUAL_CANON_REFERENCE_LOCK_V1.md").read_text()
        self.assertIn(SOURCE_SHA256, text)
        for owner, title in APPROVED.items():
            self.assertIn(owner, text)
            self.assertIn(title, text)

    def test_flaim_identity_registries_match_approved_titles(self):
        paths = [
            ROOT / "living-novel" / "os" / "adapters" / "flaim" / "PRO_SCHEMIN_IDENTITY_RESOLUTION_V1.json",
            ROOT / "living-novel" / "os" / "adapters" / "flaim" / "registries" / "PRO_SCHEMIN_IDENTITY_RESOLUTION_V1.json",
        ]
        for path in paths:
            data = json.loads(path.read_text())
            by_owner = {record["owner"]: record for record in data["records"]}
            self.assertEqual(set(by_owner), set(APPROVED))
            for owner, expected in APPROVED.items():
                actual = by_owner[owner].get("canonical_character", by_owner[owner].get("character"))
                self.assertEqual(actual, expected, f"{path}: {owner}")

    def test_master_canon_primary_titles_are_exact(self):
        text = (ROOT / "canon" / "SCHEMIN_26_MASTER_CHARACTER_CANON.md").read_text()
        sections = re.split(r"(?=### )", text)
        owner_sections = {}
        for section in sections:
            for owner in APPROVED:
                if section.startswith(f"### {owner} /"):
                    owner_sections[owner] = section
        self.assertEqual(set(owner_sections), set(APPROVED))
        for owner, expected in APPROVED.items():
            match = re.search(r"\*\*Character:\*\*\s*([^\\\n]+)", owner_sections[owner])
            self.assertIsNotNone(match, owner)
            self.assertEqual(match.group(1).strip().rstrip("."), expected)

    def test_high_risk_active_files_do_not_use_retired_titles_as_primary_identity(self):
        checks = {
            "living-novel/characters/03_JORDAN_HOLLINGSHEAD.md": "# Jordan Hollingshead — Win Ugly",
            "living-novel/characters/12_BEN_WHIPPLE.md": "# Ben Whipple — The People's Champ",
            "chronicles/production/reference-packets/characters/CHAR-SLOB/PACKET.md": "**Canonical character:** Win Ugly",
            "chronicles/production/reference-packets/characters/CHAR-CHINS/PACKET.md": "**Canonical character:** The People's Champ",
            "memo-os/week-3/WEEK_3_CHARACTER_PACKET_REGISTER_V1.md": "|03|Jordan Hollingshead / Slob on my Dobb|Win Ugly|",
        }
        for rel, required in checks.items():
            text = (ROOT / rel).read_text()
            self.assertIn(required, text, rel)

    def test_wilson_title_and_body_form_are_both_preserved(self):
        text = (ROOT / "canon" / "SCHEMIN_26_MASTER_CHARACTER_CANON.md").read_text()
        self.assertIn("**Character:** The Philosopher-Warrior.", text)
        self.assertIn("**Body-form lock:** Arsenal Centaur", text)
        self.assertIn("**Never:** gorilla, ape", text)


    def test_all_character_packets_match_approved_titles(self):
        packets = {
            "CHAR-JAKE": ("Jake Kaloper", "The Trade Jedi"),
            "CHAR-RED": ("Kevin Zeek", "The Predator Board"),
            "CHAR-SLOB": ("Jordan Hollingshead", "Win Ugly"),
            "CHAR-LLC": ("David Babb", "Hostile Takeover"),
            "CHAR-CENTAUR": ("Wilson Look", "The Philosopher-Warrior"),
            "CHAR-TDS": ("Phillip Pitts", "The Podium Shadow"),
            "CHAR-CHILI": ("Brandon Pryor", "The Chili Outlaw"),
            "CHAR-ELNINO": ("Manning Welty", "The Weather System"),
            "CHAR-BYARS": ("Austin Byars", "The Belt Keeper"),
            "CHAR-MUD": ("Bobby Mitchell", "Swamp-Born Menace"),
            "CHAR-DUCKHOOK": ("Zach Wilson", "King of the Impossible Lie"),
            "CHAR-CHINS": ("Ben Whipple", "The People's Champ"),
        }
        root = ROOT / "chronicles" / "production" / "reference-packets" / "characters"
        for packet, (owner, title) in packets.items():
            text = (root / packet / "PACKET.md").read_text()
            self.assertIn(f"**Owner:** {owner}", text, packet)
            self.assertIn(f"**Canonical character:** {title}", text, packet)
            self.assertIn("SCHEMIN_26_MASTER_VISUAL_CANON_REFERENCE_LOCK_V1.md", text, packet)

    def test_jake_no_belt_hard_lock_survives(self):
        text = (ROOT / "canon" / "SCHEMIN_26_MASTER_CHARACTER_CANON.md").read_text()
        section = text.split("### Jake Kaloper / ObiWan Jacoby", 1)[1].split("### ", 1)[0]
        self.assertIn("NO CHAMPIONSHIP BELT", section)

if __name__ == "__main__":
    unittest.main()
