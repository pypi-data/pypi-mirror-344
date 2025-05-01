import os

class EonConsoleUI:
    def __init__(self, title="EonConsoleUI"):
        self.title = title
        self.elements = []

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def header(self, text):
        self.elements.append(f"\n=== {text.upper()} ===")

    def label(self, text):
        self.elements.append(text)

    def input_box(self, prompt):
        self.elements.append(f"[INPUT] {prompt}")
        return input(f"{prompt}: ")

    def button(self, text, func):
        self.elements.append(f"[{len(self.elements)+1}] {text}")
        return (len(self.elements), func)

    def run(self, buttons=[]):
        while True:
            self.clear()
            print(f"{self.title}\n" + "-" * len(self.title))
            for item in self.elements:
                print(item)
            if buttons:
                try:
                    choice = int(input("\nSelect option: "))
                    for num, func in buttons:
                        if choice == num:
                            return func()
                except:
                    input("Invalid input. Press Enter to continue...")
