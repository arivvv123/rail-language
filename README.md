# rail-language
**Rail** is a programming language designed for fast computing. It's a blend of Rust and Go.

Status: *In development*

Version: **V0.2**

## Features (planned)
- Static typing with type inference
- Memory safety without GC
- C-like performance
- Simple concurrency model
- Compiles to C (currently)

## Building & Running
1. Clone repo: `git clone https://github.com/arivvv123/rail-language`
2. Got to the project's folder: `cd rail-language`
3.  **Note**: The project uses only standard Python libraries. No external packages are required (see empty `requirements.txt`).
4. Run compiler: `python rail_compiler/compiler.py input.rail`
5. Output: `output.c` → compile with GCC: `gcc output.c -o program`

## License
    Rail - programming language for fast computing
    Copyright (C) 2026  arivvv

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

### Contact:
E-Mail: populus123123123@gmail.com