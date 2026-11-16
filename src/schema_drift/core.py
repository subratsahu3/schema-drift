"""SchemaDrift: Polyglot AST Interface & Wire-Protocol Consistency Validator."""

import ast
import re
from typing import Dict, List


class PythonModelVisitor(ast.NodeVisitor):
    """Extracts typed attribute fields from Python class declarations."""

    def __init__(self):
        self.fields: Dict[str, str] = {}

    def visit_AnnAssign(self, node: ast.AnnAssign):
        if isinstance(node.target, ast.Name):
            field_name = node.target.id
            field_type = ast.unparse(node.annotation) if hasattr(ast, "unparse") else "Any"
            self.fields[field_name] = field_type


class SchemaValidator:
    """
    Statically analyzes cross-language contract divergence between Python and TypeScript
    definitions without requiring live services or build pipelines.
    """

    TYPE_MAPPING = {
        "str": "string",
        "int": "number",
        "float": "number",
        "bool": "boolean",
        "list": "any[]",
        "dict": "Record<string, any>",
        "None": "null",
    }

    @classmethod
    def parse_python_fields(cls, python_src: str) -> Dict[str, str]:
        tree = ast.parse(python_src)
        visitor = PythonModelVisitor()
        visitor.visit(tree)
        return visitor.fields

    @classmethod
    def parse_typescript_fields(cls, ts_src: str) -> Dict[str, str]:
        fields: Dict[str, str] = {}
        # Match lines like: foo: string; or bar?: number;
        pattern = r"(\w+)\s*\??\s*:\s*([^;,\n]+)"
        for match in re.finditer(pattern, ts_src):
            field_name = match.group(1).strip()
            field_type = match.group(2).strip()
            fields[field_name] = field_type
        return fields

    @classmethod
    def validate(cls, python_src: str, typescript_src: str) -> List[str]:
        """
        Detects drift discrepancies between Python and TypeScript schemas.
        Returns a list of violation descriptions.
        """
        py_fields = cls.parse_python_fields(python_src)
        ts_fields = cls.parse_typescript_fields(typescript_src)
        discrepancies: List[str] = []

        # Check Python -> TypeScript coverage
        for py_name, py_type in py_fields.items():
            if py_name not in ts_fields:
                discrepancies.append(f"Missing field in TypeScript contract: '{py_name}'")
            else:
                expected_ts = cls.TYPE_MAPPING.get(py_type, py_type)
                actual_ts = ts_fields[py_name]
                if expected_ts.lower() != actual_ts.lower():
                    discrepancies.append(
                        f"Type mismatch on '{py_name}': Python expects '{py_type}', but TypeScript declares '{actual_ts}'"
                    )

        # Check TypeScript -> Python unexpected extra fields
        for ts_name in ts_fields:
            if ts_name not in py_fields:
                discrepancies.append(f"Unexpected extra field in TypeScript contract: '{ts_name}'")

        return discrepancies
