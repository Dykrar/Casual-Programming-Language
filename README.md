# Casual-Programming-Language
Casual is a programming language designed to be as simple as possible, while being user-friendly.

In this project, you will design an interpreter and a compiler for the Casual programming language.

## Project #1

## Phase 1

In the first phase, you will design a tokenizer and a parser for the Casual programming language. Your program should detect syntactic errors, but not semantic ones

######  Language Description
Comments in Casual are started with the pound (#) character and finish at the end of the line.

Casual is whitespace insensitive

A program is made of several declarations or definitions: 


- A declaration includes the name of the function, its arguments and the returning type 
```python
  decl max (a:Int, b:Int):Int
 ```
  
  
- A definition has the same contents, but also has a block, corresponding to the body of the function
```python
  def max (a:Int, b:Int):Int {
    if a > b {
      return a;
    }
    return b;
  }
```

- A block is always started and ended with curly parenthesis and features zero or more statements:
```python 
  - Return statements can have an expression or not (for Void functions): return; or return 1 + 1;
  - Expressions are statements: 1; or f(3);
  - if statements have (at least) a condition and a (then) block. Optionally they can have an else block, 
 separated by a else keyword.
  - while blocks have a similar structure with a condition and a block.
  - Variable declarations require a type and a starting value a:Int = 0;
  - Variable assignments do not require the type a = 1.
  - 
```


 - Expressions represent values. They can be:
  ```python
  - Binary operators, with a C-like precedence and parenthesis to force other precedences: &&, ||, ==, !=, 
 >=, >, <=, <, +, -, *, /, % em que a divisão tem sempre a semântica da divisão decimal.
  - The not unary operator (!true)
  - Boolean literals (true, false)
  - Integer literals (1, 01, 12312341341, 1_000_000) where underscores can be present in any position.
  - Float literals (1.1, .5, 123.3123131231321)
  - String literals ("", "a", "aa", "qwertyuiop", "qwerty\tuiop")
  - Variables, which start with a letter or understore and are followed by any number of letters, underscores or numbers.
  - index access, (a[0] or get_array()[i+1])
  - function invocation (function(arg1, arg2)) where arguments can be expressions
 
 ```
 

######  Syntactic Errors
Your compiler should detect errors in the input files. In the case of a unexpected character, it should be printed along with its line and column. The parser should resume after that character.

## Phase 2

During this phase, you will improve your compiler to detect and reject program which are semantically invalid. These are the programs that are successfully parsed, but contain errors that can be statically detected.

 In particular, you should cover the following cases:


- The arguments of functions should have the exact type. Example:
```python
  decl f2(a:Bool):Bool
def f():Void {
  f2(1); # <— 1:Int is not of type Bool. 
  return; 
}

 ```
  
- A definition has the same contents, but also has a block, corresponding to the body of the function
```python
  def max (a:Int, b:Int):Int {
    if a > b {
      return a;
    }
    return b;
  }
```

- Variable declarations and assignments should have the correct type. Invalid statements include: .
```python 
  a:Int = true;, a=1.0;.
```


 - return expressions should be of the same type of return type of the function. Three examples below:
  ```python
  def f():Int {
  return; <-- return requires an Int expression.
}
def f():Void {
  return "hello"; <-- return should not have an expression.
}
def f():Int {
 return "hello"; <-- return expression expects Int, found "hello":String.
} 
 
 ```

- if and while conditions expect booleans.
- Boolean operators expect booleans (&&, ||, !)
- Comparison and arithmetic operators expect either Int or Float (+,-,*,/,<,>,<=,>=), as long as they are of the same type. 
- The % operator requires integers.
- Equality operators (==, !=) support Bool, Int or Float, as long as they are of the same type.
- Index operator (a[i]) requires a to be of type array (“[something]”), i to be of type Int and a[i] is of type something.

######  Syntactic Errors

Your zip file should include two files: setup.sh, which will install all dependencies on a ubuntu-based linux; and run.sh which will run your compiler over the file passed as the first argument.

Additionally, you should also have several examples of valid and invalid programs, apart from the ones provided.

