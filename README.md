# rail-language
**Rail** is a programming language designed for fast computing. It's a blend of Rust and Go.

Status: *In development*

Version: **V0.1**

## Features (planned)
- Static typing with type inference
- Memory safety without GC
- C-like performance
- Simple concurrency model
- Compiles to C (currently)

## Building & Running
1. Clone repo: `git clone https://github.com/arivvv123/rail-language`
2. Run compiler: `python rail_compiler/compiler.py input.rail`
3. Output: `output.c` → compile with GCC: `gcc output.c -o program`
