import pathlib
import unittest

from canon.characters.cccp_resolver import resolve_character
from canon.characters.runtime.generation_eligibility import issue_eligibility, validate_eligibility
from canon.characters.runtime.reference_mount import CharacterReferenceMount
from canon.characters.runtime.renderer_capabilities import negotiate


ROOT=pathlib.Path(__file__).resolve().parents[3]
HASH="a"*64
BLOB="b"*40
CAP_RECEIPT="cap-redteam-1"
ALL_IDS=[
    "CHAR-JAKE-KALOPER","CHAR-KEVIN-ZEEK","CHAR-JORDAN-HOLLINGSHEAD",
    "CHAR-DAVID-BABB","CHAR-WILSON-LOOK","CHAR-PHILLIP-PITTS",
    "CHAR-BRANDON-PRYOR","CHAR-MANNING-WELTY","CHAR-AUSTIN-BYARS",
    "CHAR-BOBBY-MITCHELL","CHAR-ZACH-WILSON","CHAR-BEN-WHIPPLE",
]
CAP={"redteam":{
    "evidence_state":"PROVEN",
    "capability_receipt_id":CAP_RECEIPT,
    "supports_image_references":True,
    "returns_attachment_receipt":True,
    "returns_mounted_byte_hash_receipt":True,
    "supports_subject_binding":True,
    "returns_subject_binding_receipt":True,
    "max_references":12,
    "reference_mechanism":"synthetic-test-only",
    "subject_binding_mechanism":"slot-map",
}}


def authority_receipt(ids):
    return {
        "state": "REFERENCE_AUTHORITY_RESOLVED",
        "results": [
            {
                "state": "REFERENCE_AUTHORITY_RESOLVED",
                "character_id": cid,
                "expected_sha256": HASH,
                "source_filename": f"{cid}.jpeg",
            }
            for cid in ids
        ],
    }


def make_mount(cid,index,*,slot=None,binding=None,mount_receipt=None,expected=HASH,mounted=HASH):
    return CharacterReferenceMount(
        cid,f"OWNER-{index}",f"ASSET-{index}",f"repo://canon/{cid}.jpeg",
        HASH,"image/jpeg",(100,100),"1","APPROVED",
        True,True,True,True,"redteam",
        f"ref-{index}",
        slot or f"subject-{index}",
        True,
        binding or f"bind-{index}",
        "now",
        expected,
        mounted,
        f"canon/characters/assets/{cid}/primary/source.jpeg",
        BLOB,
        100,
        mount_receipt or f"mount-{index}",
        CAP_RECEIPT,
    )


class CharacterPortabilityRedTeam(unittest.TestCase):
    def test_obiwan_no_belt_lock_survives(self):
        text=(ROOT/"canon/characters/CHAR-JAKE-KALOPER/T04_CHARACTER_SPEC.md").read_text()
        self.assertIn("championship belt",text.lower())
        self.assertIn("NEGATIVE LOCKS",text)

    def test_wilson_aliases_forward_resolve_to_current_gorilla_centaur(self):
        for query in ("Arsenal Centaur","Baker Moore Purdy"):
            r=resolve_character(query)
            self.assertEqual(r["status"],"CURRENT_CANON_RESOLVED")
            self.assertEqual(r["character_id"],"CHAR-WILSON-LOOK")
            self.assertEqual(r["identity"],"Arsenal Gorilla Centaur Warrior")
        retired=resolve_character("Arsenal Centaur")
        self.assertNotEqual(retired.get("input_state"),"SUPERSEDED_ALIAS")

    def test_tds_one_body_three_heads_and_negative_locks_survive(self):
        text=(ROOT/"canon/characters/CHAR-PHILLIP-PITTS/T04_CHARACTER_SPEC.md").read_text()
        self.assertIn("ONE reptilian humanoid BODY with EXACTLY THREE serpent HEADS",text)
        for forbidden in ("three separate snakes","single-headed reptile","Medusa","human substitute"):
            self.assertIn(forbidden,text)

    def test_belt_keeper_team_aliases_do_not_redesign_identity(self):
        for query in ("The Immortal","That's Fantasy","His Majesty's Blood"):
            r=resolve_character(query)
            self.assertEqual(r["character_id"],"CHAR-AUSTIN-BYARS")
            self.assertEqual(r["identity"],"The Belt Keeper")
        text=(ROOT/"canon/characters/CHAR-AUSTIN-BYARS/T04_CHARACTER_SPEC.md").read_text()
        for forbidden in ("king","vampire","blood creature","rename-driven anatomy or mascot redesign"):
            self.assertIn(forbidden,text)

    def _roundtrip(self,count):
        ids=ALL_IDS[:count]
        mounts=[make_mount(cid,i+1) for i,cid in enumerate(ids)]
        capability=negotiate("redteam",CAP,count)
        eligibility=issue_eligibility(
            f"r-{count}",ids,mounts,"redteam",capability,
            authority_receipt=authority_receipt(ids),
            signing_key="test-key",now=1,
        )
        self.assertEqual(eligibility["state"],"GENERATION_ELIGIBLE")
        self.assertEqual(
            validate_eligibility(
                eligibility,f"r-{count}",list(reversed(ids)),list(reversed(mounts)),
                "redteam",authority_receipt=authority_receipt(ids),signing_key="test-key",now=2,
            ),
            "GENERATION_ELIGIBLE",
        )

    def test_two_subject_binding_is_order_independent(self):
        self._roundtrip(2)

    def test_six_subject_binding_is_order_independent(self):
        self._roundtrip(6)

    def test_twelve_subject_binding_is_order_independent(self):
        self._roundtrip(12)

    def test_twelve_subject_collision_blocks(self):
        ids=ALL_IDS
        mounts=[make_mount(cid,i+1) for i,cid in enumerate(ids)]
        mounts[-1]=make_mount(ids[-1],12,slot="subject-1")
        capability=negotiate("redteam",CAP,12)
        eligibility=issue_eligibility(
            "r-collision",ids,mounts,"redteam",capability,
            authority_receipt=authority_receipt(ids),
            signing_key="test-key",now=1,
        )
        self.assertEqual(eligibility["state"],"GENERATION_BLOCKED")

    def test_correct_character_with_wrong_mounted_hash_blocks(self):
        mounts=[make_mount(ALL_IDS[0],1,mounted="c"*64)]
        capability=negotiate("redteam",CAP,1)
        eligibility=issue_eligibility(
            "r-hash",[ALL_IDS[0]],mounts,"redteam",capability,
            authority_receipt=authority_receipt([ALL_IDS[0]]),
            signing_key="test-key",now=1,
        )
        self.assertEqual(eligibility["state"],"GENERATION_BLOCKED")


if __name__=="__main__":
    unittest.main()
