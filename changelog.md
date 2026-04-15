# Changelog
## v0.2.1: Add type annotations and improved error reporting with line numbers

### New:
- Add explicit type syntax (var x: int = 10)
- Type checker now validates explicit vs inferred types
- Error messages include line numbers (and column numbers in lexer)
- Fix print codegen for strings (add missing %s)
- Add bool literal parsing (true/false)
- Update parser to track token positions

## v0.2.0.1: Add explicit type annotations

### New:
- Add TYPE token (int/bool/string) to lexer
- Add COLON token for type declarations
- Update parser to handle optional explicit types
- Update typechecker to verify type consistency
- Update grammar.rail with new syntax

## v0.2
### Fixed:
- some bugs in codegen.py
### Added:
- typechecker
- some examples for test typechecker(see examples/typecheck/)