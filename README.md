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

```
A declaration includes the name of the function, its arguments and the returning type 

  decl max (a:Int, b:Int):Int
  
A definition has the same contents, but also has a block, corresponding to the body of the function

  def max (a:Int, b:Int):Int {
    if a > b {
      return a;
    }
    return b;
  }
```

A block is always started and ended with curly parenthesis and features zero or more statements:(Return statements can have an expression or not (for Void functions),Expressions are statements, if statements have (at least) a condition and a (then) block. Optionally they can have an else block, separated by a else keyword, while blocks have a similar structure with a condition and a block, Variable declarations require a type and a starting value, Variable assignments do not require the type.
  
 Expressions represent values. They can be:(Binary operators, The not unary operator, Boolean literals, Integer literals where underscores can be present in any position, Float literals, String literals, Variables, which start with a letter or understore and are followed by any number of letters, underscores or numbers, index access, function invocation where arguments can be expressions

######  Syntactic Errors
Your compiler should detect errors in the input files. In the case of a unexpected character, it should be printed along with its line and column. The parser should resume after that character.
