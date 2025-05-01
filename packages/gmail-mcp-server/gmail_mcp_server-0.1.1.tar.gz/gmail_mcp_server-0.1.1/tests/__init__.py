import unittest

class TestGmailMCPServer(unittest.TestCase):
    def test_import(self):
        from gmail_mcp_server import server
        self.assertTrue(hasattr(server, 'main'))

if __name__ == '__main__':
    unittest.main()