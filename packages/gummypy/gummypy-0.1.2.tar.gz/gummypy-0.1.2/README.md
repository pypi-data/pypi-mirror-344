# Gummypy

A small library that contains wrapper functions around the [gum](https://github.com/charmbracelet/gum) CLI tool.

# Usage
Below is an example on how to use the `choose` function. There are many other public function (denoted by no underscore prefix) that use `choose`, `join`, `file`, etc.
Each public function has two arguments the input needed that `gum` command and the options of that command.

```python
import gummypy

def main():
    gummypy.choose(["foo", "bar", "baz"], limit=2)

if __name__ == "__main__":
    main()
```
