import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from schema_drift.core import SchemaValidator


class TestSchemaValidator(unittest.TestCase):
    def test_matching_contracts(self):
        py_src = """
class UserProfile:
    user_id: int
    username: str
    is_active: bool
"""
        ts_src = """
interface UserProfile {
    user_id: number;
    username: string;
    is_active: boolean;
}
"""
        issues = SchemaValidator.validate(py_src, ts_src)
        self.assertEqual(len(issues), 0)

    def test_missing_field_in_ts(self):
        py_src = """
class Order:
    order_id: str
    total_amount: float
"""
        ts_src = """
interface Order {
    order_id: string;
}
"""
        issues = SchemaValidator.validate(py_src, ts_src)
        self.assertEqual(len(issues), 1)
        self.assertIn("Missing field in TypeScript contract: 'total_amount'", issues[0])

    def test_type_mismatch(self):
        py_src = """
class SensorData:
    timestamp: int
"""
        ts_src = """
interface SensorData {
    timestamp: string;
}
"""
        issues = SchemaValidator.validate(py_src, ts_src)
        self.assertEqual(len(issues), 1)
        self.assertIn("Type mismatch on 'timestamp'", issues[0])


if __name__ == "__main__":
    unittest.main()
