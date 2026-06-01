import os
import secrets
import unittest
from unittest import mock

os.environ.setdefault("SECRET_KEY", "test-secret-key")

import app as finfinder_app


class FinFinderSmokeTests(unittest.TestCase):
    def setUp(self):
        finfinder_app.app.config.update(TESTING=True, SECRET_KEY="test-secret-key")
        self.client = finfinder_app.app.test_client()

    def test_core_pages_render(self):
        for path in [
            "/",
            "/recommender",
            "/all-about-surfboard-fins",
            "/fin-setups",
            "/fin-systems",
            "/longboard-fins",
            "/fin-sizing-guide",
            "/about",
            "/finsights",
        ]:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)

    def test_legacy_urls_redirect_to_canonicals(self):
        expected_redirects = {
            "/all-about-fins": "/all-about-surfboard-fins",
            "/fin-box-systems": "/fin-systems",
            "/how-surfboard-fins-work-lift-physics": "/finsights/how-surfboard-fins-work-lift-physics",
            "/pivot-vs-flex-longboard-fins-single-fin-guide": "/finsights/pivot-vs-flex-longboard-fins-single-fin-guide",
            "/finsights/surfboard-fin-prices-skyrocketed-200-300": "/finsights/why-are-fins-so-expensive-real-costs",
        }
        for path, target in expected_redirects.items():
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 301)
                self.assertTrue(response.headers["Location"].endswith(target))

    def test_blog_lookup_and_post_route(self):
        posts = finfinder_app.load_blog_posts()
        self.assertGreater(len(posts), 0)
        first_post = posts[0]
        self.assertIs(finfinder_app.get_post_by_slug(first_post["slug"]), first_post)

        response = self.client.get(f"/finsights/{first_post['slug']}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(first_post["title"].encode("utf-8"), response.data)

    def test_sitemap_contains_core_routes_and_blog_posts(self):
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        body = response.get_data(as_text=True)
        self.assertIn("https://finfinder.ai/recommender", body)
        self.assertIn("https://finfinder.ai/finsights", body)
        self.assertIn("https://finfinder.ai/finsights/", body)

    def test_discovery_files_have_short_cache_lifetime(self):
        for path in ["/robots.txt", "/sitemap.xml", "/llms.txt"]:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertIn("max-age=3600", response.headers.get("Cache-Control", ""))

    def test_health_endpoint_and_common_security_headers(self):
        response = self.client.get("/healthz")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})
        self.assertEqual(response.headers.get("Cache-Control"), "no-store")

        response = self.client.get("/")
        self.assertIn("max-age=600", response.headers.get("Cache-Control", ""))
        self.assertEqual(response.headers.get("X-Content-Type-Options"), "nosniff")
        self.assertEqual(response.headers.get("X-Frame-Options"), "SAMEORIGIN")
        self.assertEqual(response.headers.get("Referrer-Policy"), "strict-origin-when-cross-origin")

    def test_ask_falls_back_when_model_is_unavailable(self):
        with mock.patch.object(finfinder_app, "model", None):
            response = self.client.post("/ask", json={"question": "I am 175 lbs on a shortboard in small waves"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get("Cache-Control"), "no-store")
        payload = response.get_json()
        self.assertTrue(payload["fallback"])
        self.assertIn("amzn.to", payload["answer"])
        self.assertIn("(Amazon)", payload["answer"])

    def test_ask_rejects_missing_question(self):
        response = self.client.post("/ask", json={})
        self.assertEqual(response.status_code, 400)

    def test_ask_keeps_session_cookie_below_browser_limit(self):
        class FakeModel:
            def generate_content(self, prompt):
                randomish_text = secrets.token_urlsafe(3500)

                class FakeResponse:
                    text = (
                        f"THE RESEARCH:\n{randomish_text}\n\n"
                        "HERE'S WHAT I RECOMMEND:\n"
                        "**FCS 2 Performer PC Tri-Fin Set** - https://amzn.to/4bgFEht\n"
                        "**Futures Fins JJF Alpha Medium** - https://amzn.to/3YyRBYd"
                    )
                    parts = []

                return FakeResponse()

        with mock.patch.object(finfinder_app, "model", FakeModel()):
            for index in range(4):
                response = self.client.post(
                    "/ask",
                    json={"question": f"I am 175 lbs on a shortboard in small waves. Follow-up {index}?"},
                )
                self.assertEqual(response.status_code, 200)
                self.assertLess(len(response.headers.get("Set-Cookie", "")), 4093)


if __name__ == "__main__":
    unittest.main()
