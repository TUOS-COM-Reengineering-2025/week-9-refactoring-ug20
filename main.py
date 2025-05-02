class CustomerManager:
    def __init__(self):
        self.customers = {}
        self.tax_rate = 0.2
        self.tax_threshold = 100
        self.discount_threshold = 500
        self.potential_discount_threshold = 300
        self.vip_threshold = 1000
        self.priority_threshold = 800

    def add_customer(self, name, purchases):
        if name in self.customers.keys():
            self.customers[name].extend(purchases)
        else:
            self.customers[name] = purchases

    def add_purchase(self, name, purchase):
        self.add_customer(name, [purchase])

    def add_purchases(self, name, purchases):
        self.add_customer(name, purchases)

    def calculate_total_with_tax(self, purchases):
        total = 0
        for purchase in purchases:
            if purchase['price'] > self.tax_threshold:
                taxed_price = purchase['price'] * (1 + self.tax_rate)
                total += taxed_price
            else:
                total += purchase['price']
        return total

    def get_discount_status(self, total_amount):
        if total_amount > self.discount_threshold:
            return "Eligible for discount"
        elif total_amount > self.potential_discount_threshold:
            return "Potential future discount customer"
        else:
            return "No discount"

    def get_customer_tier(self, total_amount):
        if total_amount > self.vip_threshold:
            return "VIP Customer!"
        elif total_amount > self.priority_threshold:
            return "Priority Customer"
        return ""

    def generate_report(self):
        for customer_name, purchases in self.customers.items():
            total_amount = self.calculate_total_with_tax(purchases)
            
            print(customer_name)
            print(self.get_discount_status(total_amount))
            
            customer_tier = self.get_customer_tier(total_amount)
            if customer_tier:
                print(customer_tier)


class ShippingCalculator:
    def __init__(self):
        self.heavy_item_threshold = 20
        self.heavy_item_fee = 50
        self.standard_fee = 20
        self.fragile_item_fee = 60
        self.fragile_standard_fee = 25

    def calculate_shipping_fee(self, purchases):
        if self._has_heavy_item(purchases):
            return self.heavy_item_fee
        return self.standard_fee
    
    def _has_heavy_item(self, purchases):
        for purchase in purchases:
            if purchase.get('weight', 0) > self.heavy_item_threshold:
                return True
        return False

    def calculate_shipping_fee_for_fragile_items(self, purchases):
        if self._has_fragile_item(purchases):
            return self.fragile_item_fee
        return self.fragile_standard_fee
    
    def _has_fragile_item(self, purchases):
        for purchase in purchases:
            if purchase.get('fragile', False):
                return True
        return False