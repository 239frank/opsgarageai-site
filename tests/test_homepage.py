from __future__ import annotations

import json
import re
import struct
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = (ROOT / "index.html").read_text(encoding="utf-8")
SNAPSHOT = (ROOT / "ops-snapshot" / "index.html").read_text(encoding="utf-8")
INTAKE = (ROOT / "intake" / "index.html").read_text(encoding="utf-8")
CSS = (ROOT / "styles.css").read_text(encoding="utf-8")


def json_ld_graph() -> list[dict]:
    match = re.search(
        r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>',
        HOME,
        flags=re.DOTALL,
    )
    if not match:
        raise AssertionError("Homepage JSON-LD block is missing")
    payload = json.loads(match.group(1))
    return payload.get("@graph", [])


class HomepageConversionTests(unittest.TestCase):
    def test_primary_hero_action_starts_low_friction_fit_call(self) -> None:
        actions = re.search(r'<div class="hero-actions">(.*?)</div>', HOME, re.S)
        self.assertIsNotNone(actions)
        first_link = re.search(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', actions.group(1), re.S)
        self.assertIsNotNone(first_link)
        self.assertTrue(first_link.group(1).startswith("/ops-snapshot/"))
        self.assertIn("free workflow-fit call", re.sub(r"<.*?>", "", first_link.group(2)).lower())

    def test_homepage_answers_common_buyer_objections(self) -> None:
        self.assertIn('id="faq"', HOME)
        self.assertGreaterEqual(HOME.count("<details"), 4)
        faq_nodes = [node for node in json_ld_graph() if node.get("@type") == "FAQPage"]
        self.assertEqual(len(faq_nodes), 1)
        self.assertGreaterEqual(len(faq_nodes[0].get("mainEntity", [])), 4)

    def test_homepage_contains_truthful_assurance_signals(self) -> None:
        self.assertRegex(HOME, r'class="[^"]*\bassurance-grid\b[^"]*"')
        for phrase in (
            "Fixed scope before paid work",
            "Human-reviewed automation",
            "Works with your current tools",
        ):
            self.assertIn(phrase, HOME)

    def test_social_preview_uses_shareable_png(self) -> None:
        self.assertIn('property="og:image" content="https://opsgarageai.com/assets/og-image.png"', HOME)
        self.assertIn('property="og:image:width" content="1200"', HOME)
        self.assertIn('property="og:image:height" content="630"', HOME)
        image = ROOT / "assets" / "og-image.png"
        self.assertTrue(image.exists())
        with image.open("rb") as handle:
            self.assertEqual(handle.read(8), b"\x89PNG\r\n\x1a\n")
            length = struct.unpack(">I", handle.read(4))[0]
            self.assertEqual(handle.read(4), b"IHDR")
            width, height = struct.unpack(">II", handle.read(8))
        self.assertGreater(length, 0)
        self.assertEqual((width, height), (1200, 630))

    def test_mobile_sticky_cta_reserves_space_above_footer_links(self) -> None:
        self.assertIn('<body class="home-page">', HOME)
        self.assertRegex(
            CSS,
            r"\.home-page\s+\.site-footer\s*\{[^}]*padding-bottom:\s*110px",
        )

    def test_conversion_promise_is_consistent_across_primary_journey(self) -> None:
        self.assertGreaterEqual(HOME.lower().count("free workflow-fit call"), 3)
        self.assertIn("free workflow-fit call", SNAPSHOT.lower())
        self.assertIn("callback is free", INTAKE.lower())
        self.assertNotIn("free workflow review", HOME.lower())

    def test_skip_link_stays_above_sticky_header(self) -> None:
        self.assertRegex(CSS, r"\.skip-link\s*\{[^}]*z-index:\s*100")
        self.assertRegex(CSS, r"\.site-header\s*\{[^}]*z-index:\s*50")

    def test_interface_polish_and_accessibility_guards_exist(self) -> None:
        self.assertIn(":focus-visible", CSS)
        self.assertIn("prefers-reduced-motion", CSS)
        self.assertIn("text-wrap: balance", CSS)
        self.assertNotIn("transition: all", CSS)


if __name__ == "__main__":
    unittest.main()
