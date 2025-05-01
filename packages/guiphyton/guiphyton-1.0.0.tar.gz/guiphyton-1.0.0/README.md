# GuiPhyton

Simple and customizable console-based UI library — no Tkinter, no graphics, just Python!

## Install

```bash
pip install guiphyton
```

## Example

```python
from guiphyton import GuiPhyton

ui = GuiPhyton("Example")
ui.header("Welcome")
ui.label("This is a full console UI")

name = ui.input_box("Enter your name")

def hello():
    print(f"\nHello {name}!")
    exit()

btns = [ui.button("Say Hello", hello)]
ui.run(btns)
```
