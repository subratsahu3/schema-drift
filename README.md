# SchemaDrift: Polyglot AST Wire-Contract Validator

A static cross-language contract validator that inspects Python dataclass/Pydantic schemas and TypeScript interfaces to eliminate silent API wire mismatches in CI/CD.

## Features
- **Offline AST Inspection:** Zero database, microservice, or build server requirements.
- **Bi-Directional Drift Reporting:** Detects missing fields, unwanted extra fields, and incompatible type declarations.
- **Instant CI Verification:** Executes in milliseconds before deployment.

## Run Tests
```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Author
Subrat Sahu (@subratsahu3) — subratsahu195@gmail.com
