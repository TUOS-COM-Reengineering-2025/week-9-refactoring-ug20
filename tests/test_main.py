import unittest
import io
import contextlib
import pytest

from main import CustomerManager, calculate_shipping_fee_for_fragile_items, calculate_shipping_fee_for_heavy_items

class TestCustomerManager(unittest.TestCase):

    def test_add_customer(self):
        cm = CustomerManager()
        name = "Alice"
        purchases = [{'price': 50, 'item': 'banana'}, {'price': 80, 'item': 'apple'}]
        cm.add_customer(name, purchases)

        self.assertEqual(
            {name: purchases},
            cm.customers
        )

    def test_add_purchase(self):
        cm = CustomerManager()
        name = "Alice"
        purchase = {'price': 50, 'item': 'banana'}
        cm.add_purchase(name, purchase)

        self.assertEqual(
            {name: [purchase]},
            cm.customers
        )

    def test_add_purchase_multiple(self):
        cm = CustomerManager()
        name = "Alice"
        purchase = {'price': 50, 'item': 'banana'}
        cm.add_purchase(name, purchase)
        cm.add_purchase(name, purchase)

        self.assertEqual(
            {name: [purchase, purchase]},
            cm.customers
        )

    def test_discount_eligibility(self):
        cm = CustomerManager()
        cm.add_customer("Bob", [{'price': 600}])

        # Capture printed output
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            cm.generate_report()

        output = captured.getvalue()

        self.assertIn("Bob", output)
        self.assertIn("Eligible for discount", output)

    def test_heavy_item_shipping_fee(self):
        cm = CustomerManager()
        purchases = [{'price': 100, 'weight': 25}]

        fee = cm.calculate_shipping_fee(purchases)
        self.assertEqual(fee, 50)

    def test_fragile_item_shipping_fee(self):
        purchases = [{'price': 70, 'fragile': True}]

        fee = calculate_shipping_fee_for_fragile_items(purchases)
        self.assertEqual(fee, 60)

    def test_no_special_items_shipping_fee(self):
        cm = CustomerManager()
        purchases = [{'price': 40, 'weight': 5, 'fragile': False}]

        fee = cm.calculate_shipping_fee(purchases)
        self.assertEqual(fee, 20)

        fee_fragile = calculate_shipping_fee_for_fragile_items(purchases)
        self.assertEqual(fee_fragile, 25)
        
    def test_calculate_shipping_fee_for_heavy_items(self):
        """Test shipping fee calculation for heavy items"""
        # Test with no heavy items
        light_items = [
            {'weight': 10},
            {'weight': 15},
            {'weight': 5}
        ]
        assert calculate_shipping_fee_for_heavy_items(light_items) == 20

        # Test with one heavy item
        heavy_items = [
            {'weight': 10},
            {'weight': 25},  # Heavy item
            {'weight': 5}
        ]
        assert calculate_shipping_fee_for_heavy_items(heavy_items) == 50

        # Test with multiple heavy items
        multiple_heavy_items = [
            {'weight': 21},
            {'weight': 25},
            {'weight': 30}
        ]
        assert calculate_shipping_fee_for_heavy_items(multiple_heavy_items) == 50

        # Test with empty purchase list
        assert calculate_shipping_fee_for_heavy_items([]) == 20

        # Test with missing weight
        no_weight_items = [
            {'price': 10},
            {'name': 'item'}
        ]
        assert calculate_shipping_fee_for_heavy_items(no_weight_items) == 20
        
    def test_add_purchases(self):
        cm = CustomerManager()
        name = "Alice"
        purchases = [{'price': 50, 'item': 'banana'}, {'price': 80, 'item': 'apple'}]
        cm.add_purchases(name, purchases)

        self.assertEqual(
            {name: purchases},
            cm.customers
        )

if __name__ == "__main__":
    unittest.main()
