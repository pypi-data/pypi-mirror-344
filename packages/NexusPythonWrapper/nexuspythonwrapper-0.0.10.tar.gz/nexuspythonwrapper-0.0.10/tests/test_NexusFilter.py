import unittest
from NexusPythonWrapper import NexusFilter

class TestNexusFilter(unittest.TestCase):

    def test_valid_operator(self):
        f = NexusFilter(operator='and')
        self.assertEqual(f.operator, 'and')

        f = NexusFilter(operator='AND')
        self.assertEqual(f.operator, 'and')

        f = NexusFilter(operator='or')
        self.assertEqual(f.operator, 'or')

        f = NexusFilter(operator='OR')
        self.assertEqual(f.operator, 'or')

    def test_invalid_operator(self):
        with self.assertRaises(ValueError):
            f = NexusFilter(operator='TEST')

    def test_where(self):
        f = NexusFilter().where('LL_ID', 4)
        self.assertEqual(f.build(raw=True), {"operator": "and", "where": [{"field": "LL_ID", "value": 4}]})

    def test_valid_method(self):
        f = NexusFilter().where('LL_ID', 4, 'eq')
        self.assertEqual(f.build(raw=True), {"operator": "and", "where": [{"field": "LL_ID", "value": 4, "method": "eq"}]})

        f = NexusFilter().where('LL_ID', 4, 'EQ')
        self.assertEqual(f.build(raw=True),{"operator": "and", "where": [{"field": "LL_ID", "value": 4, "method": "eq"}]})

        f = NexusFilter().where('LL_ID', 4, 'lt')
        self.assertEqual(f.build(raw=True),{"operator": "and", "where": [{"field": "LL_ID", "value": 4, "method": "lt"}]})

        f = NexusFilter().where('LL_ID', 4, 'gt')
        self.assertEqual(f.build(raw=True),{"operator": "and", "where": [{"field": "LL_ID", "value": 4, "method": "gt"}]})

        f = NexusFilter().where('LL_ID', 4, 'le')
        self.assertEqual(f.build(raw=True),{"operator": "and", "where": [{"field": "LL_ID", "value": 4, "method": "le"}]})

        f = NexusFilter().where('LL_ID', 4, 'ge')
        self.assertEqual(f.build(raw=True),{"operator": "and", "where": [{"field": "LL_ID", "value": 4, "method": "ge"}]})

    def test_invalid_method(self):
        with self.assertRaises(ValueError):
            f = NexusFilter().where('LL_ID', 4, 'TEST')

    def test_nested(self):
        f = NexusFilter().where('LL_ID', 4).nested(
            NexusFilter().or_().where("Item_Order", 5, 'lt').where("Item_Order", 10, 'gt')
        )
        self.assertEqual(f.build(raw=True),{
            "operator": "and",
            "where": [
                {
                    "field": "LL_ID",
                    "value": 4,
                }
            ],
            "nested": [
                {
                    "operator": "or",
                    "where": [
                        {
                            "field": "Item_Order",
                            "value": 5,
                            "method": "lt"
                        },
                        {
                            "field": "Item_Order",
                            "value": 10,
                            "method": "gt"
                        }
                    ]
                }
            ]
        })


if __name__ == '__main__':
    unittest.main()