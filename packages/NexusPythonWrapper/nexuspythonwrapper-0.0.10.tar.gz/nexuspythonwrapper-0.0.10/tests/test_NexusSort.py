import unittest
from NexusPythonWrapper import NexusSort


class TestNexusSort(unittest.TestCase):

    def test_ascending_true(self):
        f = NexusSort().sort("LL_ID")
        self.assertEqual(f.build(raw=True), [{"field": "LL_ID", "ascending": True}])

    def test_ascending_false(self):
        f = NexusSort().sort("LL_ID", ascending=False)
        self.assertEqual(f.build(raw=True), [{"field": "LL_ID", "ascending": False}])

    def test_multiple_sorts(self):
        f = NexusSort().sort("LL_ID").sort("Component_ID", ascending=False)
        self.assertEqual(f.build(raw=True), [{"field": "LL_ID", "ascending": True}, {"field": "Component_ID", "ascending": False}])


if __name__ == '__main__':
    unittest.main()