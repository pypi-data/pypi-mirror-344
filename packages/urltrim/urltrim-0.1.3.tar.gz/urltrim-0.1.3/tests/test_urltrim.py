import unittest
from urltrim import URLTrim

class TestURLTrim(unittest.TestCase):
    def setUp(self):
        self.url = "https://www.example.com/some/very/long/path?query=123"
        
    def test_default_mode(self):
        # Test default mode (domain + first path segment)
        link = URLTrim(self.url)
        self.assertEqual(str(link), "example.com/some")
        self.assertEqual(link.get_full_url(), self.url)
        
        # Test URL without path
        link_no_path = URLTrim("https://www.example.com")
        self.assertEqual(str(link_no_path), "example.com")
        
        # Test URL with query params in first segment
        link_with_query = URLTrim("https://www.example.com/path?query=123")
        self.assertEqual(str(link_with_query), "example.com/path")

    def test_domain_mode(self):
        # Test domain mode
        link = URLTrim(self.url, mode="domain")
        self.assertEqual(str(link), "example.com")
        
        # Test with IP address
        link_ip = URLTrim("http://192.168.1.1/path", mode="domain")
        self.assertEqual(str(link_ip), "192.168.1.1")
        
        # Test with port number
        link_port = URLTrim("http://example.com:8080/path", mode="domain")
        self.assertEqual(str(link_port), "example.com:8080")

    def test_full_path_mode(self):
        # Test full path mode
        link = URLTrim(self.url, mode="full_path")
        self.assertEqual(str(link), "example.com/some/very/long/path")
        
        # Test with trailing slash
        link_trailing = URLTrim("https://example.com/path/", mode="full_path")
        self.assertEqual(str(link_trailing), "example.com/path")
        
        # Test with no path
        link_no_path = URLTrim("https://example.com", mode="full_path")
        self.assertEqual(str(link_no_path), "example.com")

    def test_validation(self):
        # Test invalid URLs
        invalid_urls = [
            "invalid-url",
            "http://",
            "https://invalid",
            "ftp://example.com",  # non-http(s) protocol
            "http://.com",
            "http://example.",
        ]
        for url in invalid_urls:
            with self.assertRaises(ValueError):
                URLTrim(url, validate=True)
        
        # Test valid URLs
        valid_urls = [
            "http://example.com",
            "https://sub.example.com",
            "http://localhost",
            "http://192.168.1.1",
            "https://example.com:8080",
        ]
        for url in valid_urls:
            try:
                URLTrim(url, validate=True)
            except ValueError:
                self.fail(f"URLTrim raised ValueError for valid URL: {url}")

    def test_caching(self):
        # Test cache functionality
        link1 = URLTrim(self.url, mode="domain")
        link2 = URLTrim(self.url, mode="domain")
        self.assertIs(link1.parsed_url, link2.parsed_url)
        
        # Test different modes use different cache entries
        link3 = URLTrim(self.url, mode="full_path")
        self.assertNotEqual(link1.short_url, link3.short_url)
        
        # Test cache with different URLs
        other_url = "https://example.org/path"
        link4 = URLTrim(other_url, mode="domain")
        self.assertNotEqual(link1.short_url, link4.short_url)

    def test_www_removal(self):
        # Test www removal in different scenarios
        urls = [
            ("https://www.example.com", "example.com"),
            ("https://www2.example.com", "www2.example.com"),
            ("https://wwww.example.com", "wwww.example.com"),
            ("https://www.www.example.com", "www.example.com"),
        ]
        for input_url, expected in urls:
            link = URLTrim(input_url, mode="domain")
            self.assertEqual(str(link), expected)

if __name__ == "__main__":
    unittest.main()
