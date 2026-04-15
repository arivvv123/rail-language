# Changelog
## v0.2
### Fixed:
- some bugs in codegen.py
### Added:
- typechecker
- some examples for test typechecker(see examples/typecheck/)
## v0.2.0.1: Add explicit type annotations

- Add TYPE token (int/bool/string) to lexer
- Add COLON token for type declarations
- Update parser to handle optional explicit types
- Update typechecker to verify type consistency
- Update grammar.rail with new syntax