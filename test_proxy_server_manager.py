from unittest import TestCase


class TestProxyServerManager(TestCase):
    def set_random_firefox_proxy(self):
        self.fail()

class TestInit(TestProxyServerManager):
    def test_initial_driver(self):
        self.assertIsNotNone(self.AFP.driver)