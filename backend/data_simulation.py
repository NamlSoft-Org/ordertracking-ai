import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

NUM_DELIVERY_BOYS = 5
ORDERS_PER_BOY = 10
DRUG_TYPES = ['Antibiotics', 'Painkillers', 'Vitamins', 'Insulin', 'Vaccines']
DELIVERY_BOYS = [f"DeliveryBoy_{i+1}" for i in range(NUM_DELIVERY_BOYS)]
STATUS_OPTIONS = ['Pending', 'In-Progress', 'Delivered']

def generate_orders():
    orders = []
    for i in range(NUM_DELIVERY_BOYS * ORDERS_PER_BOY):
        order = {
            'OrderID': f"PO-{i+1:04d}",
            'RetailerName': fake.company(),
            'Contact': fake.phone_number(),
            'Address': fake.address(),
            'DrugType': random.choice(DRUG_TYPES),
            'Quantity': random.randint(10, 100),
            'Price': round(random.uniform(50, 500), 2),
            'DeliveryDate': (datetime.now() + timedelta(days=random.randint(0, 3))).date(),
            'AssignedDeliveryBoy': random.choice(DELIVERY_BOYS),
            'ExpectedDeliveryTime': datetime.now() + timedelta(hours=random.randint(1, 24)),
            'Status': 'Pending',
            'Distance': random.uniform(5, 50),
            'DeliveryBoyLoad': random.randint(1, 10),
            'TrafficDelay': random.uniform(0, 2)
        }
        orders.append(order)
    return pd.DataFrame(orders)


orders_df = generate_orders()
notifications = []