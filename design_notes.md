# Rail Design Notes 
## Control Structures (v0.3) 
### if/elif/else 
- Syntax: `if condition { ... } elif condition { ... } else { ... }` 
- `elif` is a single token, unlimited number of them. 
- `else` is required for if-EXPRESSIONS, optional for statements. 
### Empty statement `empty` 
- The `empty;` keyword 
- Only in statement contexts (function bodies, if/else blocks, loops). 
- Disallowed in expressions (arguments, conditions, right-hand sides of =).
## Error Handling (v0.2.1) 
- Add line numbers to compile errors. 
- Later: add column numbers.