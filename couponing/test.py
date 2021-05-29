import unittest

from main import find_coupon


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.coupons = [
            {"Category Name": "Comforter Sets", "Coupon Name": "Comforters Sale", "Date Modified": "2020-01-01"},
            {"Category Name": "Comforter Sets", "Coupon Name": "Cozy Comforter Coupon", "Date Modified": "2020-01-01"},
            {"Category Name": "Bedding", "Coupon Name": "Best Bedding Bargains", "Date Modified": "2019-01-01"},
            {"Category Name": "Bedding", "Coupon Name": "Savings on Bedding", "Date Modified": "2019-01-01"},
            {"Category Name": "Bed & Bath", "Coupon Name": "Low price for Bed & Bath", "Date Modified": "2018-01-01"},
            {"Category Name": "Bed & Bath", "Coupon Name": "Bed & Bath extravaganza", "Date Modified": "2019-01-01"}
        ]

        categories = [
            {"Category Name": "Comforter Sets", "Category Parent Name": "Bedding"},
            {"Category Name": "Bedding", "Category Parent Name": "Bed & Bath"},
            {"Category Name": "Bed & Bath", "Category Parent Name": None},
            {"Category Name": "Soap Dispensers", "Category Parent Name": "Bathroom Accessories"},
            {"Category Name": "Bathroom Accessories", "Category Parent Name": "Bed & Bath"},
            {"Category Name": "Toy Organizers", "Category Parent Name": "Baby And Kids"},
            {"Category Name": "Baby And Kids", "Category Parent Name": None}
        ]
        self.categories_child_parent = {x['Category Name']: x['Category Parent Name'] for x in categories}
        self.inout = {
            "Bed & Bath": ['Bed & Bath extravaganza'],
            "Bedding": ['Best Bedding Bargains', 'Savings on Bedding'],
            "Bathroom Accessories": ['Bed & Bath extravaganza'],
            "Comforter Sets": ['Comforters Sale', 'Cozy Comforter Coupon'],
            "Toy Organizers": [],
        }

    def test_find_coupon(self):
        for k, v in self.inout.items():
            self.assertListEqual(find_coupon(k, coupons=self.coupons, categories=self.categories_child_parent), v)


if __name__ == '__main__':
    unittest.main()
