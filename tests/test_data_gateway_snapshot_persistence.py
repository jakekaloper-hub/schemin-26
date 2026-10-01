import json
import os
import pathlib
import subprocess
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "data-gateway" / "persist_snapshot_to_data_live.sh"


def run(cmd, cwd, check=True, env=None):
    return subprocess.run(
        cmd,
        cwd=cwd,
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
    )


class SnapshotPersistenceIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = pathlib.Path(self.tmp.name)
        self.remote = base / "remote.git"
        self.work = base / "work"
        run(["git", "init", "--bare", str(self.remote)], cwd=base)
        run(["git", "clone", str(self.remote), str(self.work)], cwd=base)
        run(["git", "checkout", "-b", "main"], cwd=self.work)
        run(["git", "config", "user.name", "test"], cwd=self.work)
        run(["git", "config", "user.email", "test@example.com"], cwd=self.work)
        (self.work / "README.md").write_text("fixture\n")
        run(["git", "add", "README.md"], cwd=self.work)
        run(["git", "commit", "-m", "fixture"], cwd=self.work)
        run(["git", "push", "-u", "origin", "main"], cwd=self.work)
        self.snapshot = self.work / "data" / "snapshots" / "1417621"
        self.snapshot.mkdir(parents=True)
        self.write_snapshot("2026-10-01T00:00:00+00:00")

    def tearDown(self):
        self.tmp.cleanup()

    def write_snapshot(self, fetched_at):
        meta = {
            "league_id": 1417621,
            "season": 2026,
            "fetched_at": fetched_at,
            "snapshot_age_seconds": 0,
            "stale": False,
            "failure_reason": None,
        }
        (self.snapshot / "latest.json").write_text(
            json.dumps({"meta": meta, "data": {"id": 1417621}}, separators=(",", ":"))
        )
        (self.snapshot / "manifest.json").write_text(json.dumps(meta, indent=2))

    def invoke(self, check=True):
        env = os.environ.copy()
        env.update({
            "LEAGUE_ID": "1417621",
            "SCHEMIN_DATA_BRANCH": "data/live",
            "SCHEMIN_DATA_REMOTE": "origin",
        })
        return run(["bash", str(SCRIPT)], cwd=self.work, check=check, env=env)

    def remote_sha(self):
        return run(
            ["git", "--git-dir", str(self.remote), "rev-parse", "refs/heads/data/live"],
            cwd=self.work,
        ).stdout.strip()

    def remote_file(self, path):
        return run(
            ["git", "--git-dir", str(self.remote), "show", f"data/live:{path}"],
            cwd=self.work,
        ).stdout

    def test_first_untracked_snapshot_is_committed_and_verified_remotely(self):
        self.invoke()
        remote = self.remote_file("data/snapshots/1417621/latest.json")
        self.assertEqual(remote, (self.snapshot / "latest.json").read_text())
        self.assertIn("Durable remote snapshot verified", self.invoke().stdout)

    def test_unchanged_snapshot_does_not_create_new_commit(self):
        self.invoke()
        before = self.remote_sha()
        result = self.invoke()
        after = self.remote_sha()
        self.assertEqual(before, after)
        self.assertIn("Snapshot state unchanged", result.stdout)

    def test_changed_snapshot_creates_new_durable_commit(self):
        self.invoke()
        before = self.remote_sha()
        self.write_snapshot("2026-10-01T00:30:00+00:00")
        self.invoke()
        after = self.remote_sha()
        self.assertNotEqual(before, after)
        remote = json.loads(self.remote_file("data/snapshots/1417621/latest.json"))
        self.assertEqual(remote["meta"]["fetched_at"], "2026-10-01T00:30:00+00:00")

    def test_push_failure_is_red_and_preserves_previous_remote_snapshot(self):
        self.invoke()
        before = self.remote_file("data/snapshots/1417621/latest.json")
        hooks = self.remote / "hooks"
        hook = hooks / "pre-receive"
        hook.write_text(
            "#!/usr/bin/env bash\n"
            "while read old new ref; do\n"
            "  if [[ \"$ref\" == \"refs/heads/data/live\" ]]; then exit 1; fi\n"
            "done\n"
            "exit 0\n"
        )
        hook.chmod(0o755)
        self.write_snapshot("2026-10-01T01:00:00+00:00")
        result = self.invoke(check=False)
        self.assertNotEqual(result.returncode, 0)
        after = self.remote_file("data/snapshots/1417621/latest.json")
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
