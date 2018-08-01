#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PySudoku v0.2 by Adrien MALINGREY
Sudoku game assistant
Tested on Windows 10 with Python 3.6.3 and Linux Mint 18 with Python 3.5.1
"""
try:
    from tkinter import *
    from tkinter import ttk
    from tkinter.filedialog import askopenfilename, asksaveasfilename
    from tkinter.messagebox import showinfo, showerror, askokcancel, askyesnocancel
    from pickle import Pickler, Unpickler, UnpicklingError
    from itertools import combinations
    from os.path import basename, dirname, exists
    from random import sample, shuffle
    from webbrowser import open as open_web_browser
    from sys import argv, exit
    from string import digits
except ImportError as e:
    exit(e.msg)


# Labels
APP_TITLE = "PySudoku"

GRID_LABEL = "Grid"
GENERATE_LABEL = "Generate..."
CREATE_LABEL = "Create"
EDIT_LABEL = "Edit"
VALIDATE_LABEL = "Validate"
SOLVE_LABEL = "Solve"

GAME_LABEL = "Game"
LOAD_LABEL = "Load..."
SAVE_LABEL = "Save..."
RESTART_LABEL = "Restart..."

VIEW_LABEL = "View"
THEME_LABEL = "Theme"
SHOW_TIPS_LABEL = "Show tips"
SHOW_CONFLICTS_LABEL = "Show conflicts"

HELP_LABEL = "?"
WIKI_LABEL = "Wikipedia"
ABOUT_LABEL = "About..."

GENERATE_PROGRESS_BOX_TITLE = "Grid generation"
GENERATE_PROGRESS_BOX_TEXT = "Generating a new grid..."
CLUES_DELETING_PROGRESS_BOX_TEXT = "Deleting clues..."
CANCEL_AUTO_CREATE_BUTTON_TEXT = "Stop"

VALIDATION_PROGRESS_BOX_TITLE = "Grid validation"
VALIDATION_PROGRESS_BOX_TEXT = "Checking if grid has a unique solution..."

NO_SOLUTION_MESSAGE_BOX_TITLE = "Can't solve grid"
NO_SOLUTION_MESSAGE_BOX_TEXT = (
    "Some boxes have no solution. "
    "Please correct it."
)
NO_OTHER_SOLUTION_PROGESS_BOX_TEXT = "Checking if grid has other solutions..."

INCORRECT_GRID_MESSAGE_BOX_TITLE = "Incorrect grid"
SEVERAL_SOLUTIONS_MESSAGE_BOX_TEXT = "The grid has several solutions."
CONFLICTS_MESSAGE_BOX_TEXT = (
    "Some boxes from the same row, column or region "
    "have same digit. Please correct them."
)

SOLVING_PROGRESS_BOX_TITLE = "Solving grid"
CALCULATING_SURE_DIGITS_TEXT = "Calculating sure digits..."
TESTS_PROGRESS_BOX_TEXT = "Test: {} on {}"
NO_SOLUTION_EXCEPTION = (
    "There are some error. "
    "Please correct them to solve the grid."
)
CANCEL_EXCEPTION = "Cancelled"

SOLVED_GRID_MESSAGE_BOX_TITLE = "Congratulations!"
SOLVED_GRID_MESSAGE_BOX_TEXT = "The grid is solved."

NB_CLUES_MESSAGE_BOX_TITLE = "Generate a new grid"
NB_CLUES_INPUT_LABEL = "Please enter minimum number of clues:"
HARDER_LABEL = "← harder"
EASIER_LABEL = "easier →"
CANCEL_BUTTON_TEXT = "Cancel"
OK_BUTTON_TEXT = "OK"

CANCELLED_PROGRESS_BOX_TEXT = "Cancelling..."
STOPPING_PROGRESS_BOX_TEXT = "Stopping..."

CONFIRM_ERASE_MESSAGE_BOX_TITLE = "Erase the current game?"
CONFIRM_ERASE_MESSAGE_BOX_TEXT = "A game is in progress. Do you want to erase it?"

OPEN_FILE_MESSAGE_BOX_TITLE = "Open game"
FILE_TYPE_NAME = "PySudoku game"
FILE_ERROR_MESSAGE_BOX_TITLE = "File error"
CORRUPTED_FILE_MESSAGE_BOX_TEXT = "The file {} can't be read."
FILE_NOT_FOUND_MESSAGE_BOX_TEXT = "The file {} can't be found."

SAVE_FILE_MESSAGE_BOX_TITLE = "Save game"

WIKI_URL = "https://en.wikipedia.org/wiki/Sudoku"

ABOUT_MESSAGE_BOX_TITLE = "About PySudoku"
ABOUT_MESSAGE_BOX_TEXT = "Author: Adrien Malingrey\n" "Licence: MIT"

CLOSE_MESSAGE_BOX_TITLE = "Save game?"
CLOSE_MESSAGE_BOX_TITLE = "A game is in progress. Would you like to save it?"

# 16x16, 32x32, 48x48 gif images encoded in base64
ICON16 = """
         R0lGODlhEAAQAPcAAAAAAGlpaW1tbe0cJKCgoMDAgODggOPj4/Dw8P///wAAAAAAAAAAAAAAAAAA
         AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
         AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
         AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
         AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
         AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
         AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
         AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
         AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
         AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
         AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
         AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
         AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
         AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAAAEAAQAAAIfAADCBxI
         sOCBAAgSIiCgcKGBhwYOIhAgYOHEigQgRkRI0WLHjBAlKmQ4UuNBAihTqlR5MIHLBARewixAs0DL
         lzEBAJhJ0WYAmTl3EijQ86bLmDhr+lzJNOVBpUNrgnz4tOdQqwYGDNhIVECBq14zauUqFarJA2jT
         ql17ICAAOw=="""

ICON32 = """
         R0lGODlhIAAgAPcAAAAAAGlpaX9/f+0cJL23a6CgoPDmjOPj4/Dw8P///wAAAAAAAAAAAAAAAAAA
         AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
         AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
         AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
         AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
         AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
         AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
         AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
         AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
         AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
         AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
         AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
         AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
         AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAAAIAAgAAAI/wALCBxI
         sKDBgwMTFAjAsGHDAw4jQoz4UGEABBgzYoSoUSNEAyBDgjxgsWNGjiYRfBQZkuTCjAIEnLyIMeZM
         li1L1pS5kSYCmz1xjtT5k6dKn0CPCjXgEqlRlEVvCm2a8mjVlTippoTaEStLlwfCih1LtqzZsBYp
         Mpyoli3Fpgniyo0Lce5ciATy6s0L1y7dAH7/7t3b12/duAAAyMWbN6bewnYPJ0i8OIBex3wtBk4g
         mbLgxgIeaw7cWfFnApgJQL4LmLTlwZkXbpYc+TVssGdz60a7UG0AtxJ9/7YIm6/twV5FNi2u+jjh
         AEuXg35sOzXWAQNyLrwc2jh36iGxaymv3r35d+Phsw/dPt17++bpxzNnfBv6VOLF6SO3n1Xh7v9m
         bSbggH4FBAA7"""

ICON48 = """
         R0lGODlhMAAwAPcAAAIAAAAADgkKCgAAEgkXHh0LAAAAOQQVJQcMcAMVeAQdfiI/am0GA20/IV9F
         K19ebX97RWNjbWRqbGhhaGtjbm9lbW9pZ2hoa2hob29qbW1sbGdwbGp1bHFqbHppbnptbX1obHZp
         cXJpenJza3V+a31ybHt6bHFycXR0czl8uxJ4xV1yi2VzgWp7jHJ5kWx8p22Aan2NanyQa16Eg3WF
         l26ArXONunSev3WhyKFNDodobId3bJ1vcJR4dP4BAPwLB/8AHvoUBfkjCP4gLf4vJf4mNcd1I/VR
         G/ZEJfRxJf1BRftvVJR6kIuJV4qJW4yKWIWTa4uaapaCbJyJbJSXapWfap6aa5+oaqSdXaSJbKyG
         eqmKeaeVbKKUdLqOcrCSbLebbLeQfKGtaq6oa6Kwaa60abKiarGqa7usarS5abmzZ7qyarq0aLy2
         ari5ab25ab+5bMGBU9afVsCqa8+gYM2kdsCyasG5asC6bcG8asK8bvKdQveOb/iOcO7VXe/Yc//G
         eoCAg4GBhIaGhoWHiIeOjY2Oh4iIiIqKjJqQhpeXl5efn5+fl5iYmJ6enpmZq52jop2sq7CcmqKj
         naCgoKSkpKqqqq2trauyuLiypbGxsbW1tbm5uZ680Yy55abB1qjL36jM2KTW6bzc7L/c9sOqisuw
         kt2zh9W9mMq0pd/PktPBtfLLi+PPq+XVs+7fs+/lie/mje7rjeXlne/jlu/tku71lO73mO74lvDl
         i/DljPLoivLpjfbsjvDzkObmoOvrpfHwoPX0sfv7sPz6tvz8sP78t///vsnJycPM09PMxNLPz9LS
         1drW1cHf7cjX5Mb//9Hp89fs9dfv+d3q8d7u8tX28d/w/+XZyvTdxO7hw+Hh2ejn3eno3vTlxfLj
         0PT33+Xl5O7u7u7v8OD9+Ony8uv18u7w8O/w9PDu5fDv7vDw5vDw7vL07Pj37f/z7P/+5fDw8PHx
         9fL08PXy8PT09PH0+PX7+Pf///j08f369vr6+vr+////+f7+/gAAACwAAAAAMAAwAAAI/wAVHRpI
         sKDBQQYTEkSoMGGgcIMaVZpIsSJFSpcsapzoyB2WjyBDhhQm71CleChTqkwpjlK9lTDjievGS5fN
         mzhvEit5MubKli99sqSZs6jNnSZTspuX6tCjeONYumSpzVAhZ1FRzqxpNCfSnvHQmWrBqcsLc1KD
         xss2AVMmCtGGcu2qk2fKdpKmnbvnQVralKdw5LNXx5Ncuji/rlTXLMwNen9ReguRTJkIa4cRH7Wr
         Mh0hFDTKndM6VWuPEydcZJVJVLMuxSpHx9PSKTI7L6FQorIhe6vr15zjgWNC7py8LZ9s8wBFT16r
         Gr1ba4YdT14pFpQSraDWu3Q8VxgWMf+yMCrz9OBLVzmKdE5dZKjYJkF65l6rdMTUhcr0LtS36/z9
         8eeTf+cdQok4CCaooIKOyLTgg+JwswssFFZoYYU7DcLJJRx26GGHliDz4YgcWpKOEyimqKKKv5S0
         iT8wxiijjJfMaGOM2+iBx4489shjMC7eeGONQs64DRxtJKnkkkoCeciLRdI44zvLMMOPkUgy2cYY
         bCzpJJRRwkgkjPoUIIAABFyJY5ZLfhFBGV4GGaaYMuaQAox0qCDjkUyiwUEGcDYp55xj9sOAKDC+
         koCa/vCp5BodpNFBoEl+OSedMRqxAD79NIAAo462YUcJZbwxaZxPXurPmP704wAAA8z/oACobE5B
         ghVWdECFG4Kmeimr31wDoxx6rpnkG1OYoKwGI6TRK5hhsgqIAdWoEgA0e7KppKmUtmHprzPGAcAB
         pGCp5RsVdPstoaqGuuQbTK4bbbvaatmrJqpa0i4bavTr77/+AilIN9sUbPDBB6+D8MIGwwPMwxBH
         HPEw8iACARwYZ6xxxm00ocfGIMPBBjC98GLyySifvJPF9mrJxhN4tLykGsDMhV/FEDCZx855LPly
         zEnyzLOSNNvMiy22yJJLYjgviUYEUD9A6c9K6gB1BBJc0GUbRd8ECxI++EAEK0yzrKQZIwytJNVB
         73xHCWIQXfNNewxByy1HKCFLXWYn58mFDGdw6TPMTCIbw8xz65JLLXvn4kcRe2/W9xtSMNuBBLwm
         ybaSc2COuM02wSJEH7DwnfOjW+9QxdqELykFFEx2jZMsQSwRueSnB61kFrBr3vqxH5ARe+I2/eED
         H7Esbfq2IESRBxodXME60EnasQG8n9uUyx8/sIIL0soD13cbZ3yAdRR3TL8kGDCkn71NSYQdNhC+
         LP9uHu6rv23+cnO1ONIADN/KciezNmxOZrI7z/hkdsCWJfBmgphFMCZIwQpWUIIWzOAEi2EMYnjw
         gyD84DHkEQ55mPCEKEyhClfIwhbKYx8BAQA7"""


class CustomStyle(ttk.Style):
    """
    Manage widgets' style
    """

    def __init__(self, app):
        ttk.Style.__init__(self, app)
        self.app = app
        self.theme = StringVar()
        self.theme.trace_variable("w", self.change_theme)
        self.theme.set(self.theme_use())

    def change_theme(self, *args):
        """
        Called on "View > Theme > theme_name" menu pressed
        Change and customize theme of tkinter.ttk widgets
        """
        new_theme = self.theme.get()
        self.theme_use(new_theme)
        # Redefine Entry layout to permit fieldbackground color change
        if new_theme in ("vista", "xpnative"):
            try:
                self.element_create("clam.field", "from", "clam")
            except TclError:
                pass
            self.layout(
                "Box.TEntry",
                [
                    (
                        "Entry.clam.field",
                        {
                            "sticky": "nswe",
                            "border": "1",
                            "children": [
                                (
                                    "Entry.padding",
                                    {
                                        "sticky": "nswe",
                                        "children": [
                                            ("Entry.textarea", {"sticky": "nswe"})
                                        ],
                                    },
                                )
                            ],
                        },
                    )
                ],
            )
            self.configure(
                "Box.TEntry",
                bordercolor="grey",
                background="grey",
                foreground="black",
                fieldbackground="white",
            )
            if new_theme == "vista":
                self.map(
                    "Box.TEntry",
                    bordercolor=[
                        ("hover", "!focus", "!disabled", "black"),
                        ("focus", "dodger blue"),
                    ],
                    background=[
                        ("hover", "!focus", "!disabled", "black"),
                        ("focus", "dodger blue"),
                    ],
                )
        # Define style for boxes with highlighted digits or digits' conflicts
        self.configure("Box.TEntry", fieldbackground="white")
        self.map("Box.TEntry", fieldbackground=[("disabled", "light grey")])
        self.configure("HighlightArea.Box.TEntry", fieldbackground="light cyan")
        self.map(
            "HighlightArea.Box.TEntry",
            fieldbackground=[("disabled", "light steel blue")],
        )
        self.configure(
            "HighlightBox.HighlightArea.Box.TEntry", foreground="midnight blue"
        )
        self.map(
            "HighlightBox.HighlightArea.Box.TEntry", foreground=[("disabled", "blue")]
        )
        self.configure("ErrorArea.Box.TEntry", fieldbackground="khaki")
        self.map("ErrorArea.Box.TEntry", fieldbackground=[("disabled", "dark khaki")])
        self.configure("ErrorBox.ErrorArea.Box.TEntry", foreground="red")
        self.map("ErrorBox.ErrorArea.Box.TEntry", foreground=[("disabled", "red")])

    def redraw(self):
        """
        Called when a box's digit is changed
        Colorize boxes where highlighted digit can't be written
        and boxes with same digits in the same area
        """
        if self.app.gr1d.progress_box and self.app.gr1d.progress_box.title() in (
            VALIDATION_PROGRESS_BOX_TITLE,
            GENERATE_PROGRESS_BOX_TITLE,
        ):
            # Hide digits behind "?" when grid is validating
            for box in self.app.gr1d:
                if box.instate(("!disabled",)):
                    box.configure(style="Box.TEntry", show="?")
        else:  # Reset style
            for box in self.app.gr1d:
                box.configure(style="Box.TEntry", show="")
            # Disable highlight_button if all it's digit are solved
            for digit, highlight_button in enumerate(
                self.app.highlight_buttons.buttons, start=1
            ):
                if (
                    sum(
                        box.digit.get() == highlight_button.digit
                        for box in self.app.gr1d
                    )
                    == 9
                ):
                    highlight_button.disable()
                else:
                    highlight_button.enable()
            if HighlightButton.digit:  # Highlight selected digitures' area
                for box in self.app.gr1d:
                    if HighlightButton.digit not in box.possible_digits:
                        box.configure(style="HighlightArea.Box.TEntry")
                    if HighlightButton.digit == box.digit.get():
                        box.configure(style="HighlightBox.HighlightArea.Box.TEntry")


class MenuBar(Menu):
    """
    Window menu bar
    """

    def __init__(self, app):
        Menu.__init__(self, app)
        self.app = app
        # Grid menu
        self.grid = IndexedMenu(app)
        self.grid.add_command(
            label=GENERATE_LABEL,
            underline=0,
            command=self.app.gr1d.open_nb_clues_message_box,
        )
        self.grid.add_separator()
        self.grid.add_command(
            label=CREATE_LABEL, underline=0, command=self.app.gr1d.create
        )
        self.grid.add_command(
            label=EDIT_LABEL, underline=4, command=self.app.gr1d.edit, state=DISABLED
        )
        self.grid.add_command(
            label=VALIDATE_LABEL,
            underline=0,
            command=self.app.gr1d.validate,
            state=DISABLED,
        )
        self.grid.add_separator()
        self.grid.add_command(
            label=SOLVE_LABEL, underline=0, command=self.app.gr1d.solve, state=DISABLED
        )
        self.add_cascade(label=GRID_LABEL, underline=0, menu=self.grid)
        # Game menu
        self.game = IndexedMenu(app)
        self.game.add_command(label=LOAD_LABEL, underline=0, command=self.app.game.open)
        self.game.add_command(
            label=SAVE_LABEL, underline=0, command=self.app.game.save, state=DISABLED
        )
        self.game.add_separator()
        self.game.add_command(
            label=RESTART_LABEL,
            underline=0,
            command=self.app.game.restart,
            state=DISABLED,
        )
        self.add_cascade(label=GAME_LABEL, underline=0, menu=self.game)
        # View menu
        self.view = IndexedMenu(app)
        self.view.theme_menu = Menu(self.view, tearoff=0)
        self.view.add_cascade(label=THEME_LABEL, underline=0, menu=self.view.theme_menu)
        for label in self.app.style.theme_names():
            self.view.theme_menu.add_radiobutton(
                label=label, variable=self.app.style.theme
            )
        self.view.add_separator()
        self.view.add_checkbutton(
            label=SHOW_TIPS_LABEL, underline=13, variable=self.app.gr1d.tips_shown
        )
        self.view.add_checkbutton(
            label=SHOW_CONFLICTS_LABEL,
            underline=13,
            variable=self.app.gr1d.conflicts_shown,
        )
        self.add_cascade(label=VIEW_LABEL, underline=0, menu=self.view)
        # Help menu
        self.help = IndexedMenu(app)
        self.help.add_command(label=WIKI_LABEL, underline=0, command=self.app.open_wiki)
        self.help.add_separator()
        self.help.add_command(
            label=ABOUT_LABEL, underline=2, command=self.app.show_about
        )
        self.add_cascade(label=HELP_LABEL, underline=0, menu=self.help)


class IndexedMenu(Menu):
    """
    tkinter.Menu redefined to get menus indices
    """

    def __init__(self, parent):
        Menu.__init__(self, parent, tearoff=0)
        self.labels = []

    def add(self, itemType, cnf, **kw):
        super().add(itemType, cnf, **kw)
        if "label" in cnf:
            self.labels.append(cnf["label"])
        elif "label" in kw:
            self.labels.append(kw["label"])
        else:
            self.labels.append(None)

    def entryconfigure(self, label_or_index, label=None, **options):
        """
        Redefined Menu.entryconfigure
        label_or_index can be the entry index as usual or its label
        """
        if isinstance(label_or_index, int):
            index = label_or_index
        elif isinstance(label_or_index, str):
            index = self.labels.index(label_or_index)
        else:
            raise TypeError(
                "label_or_index must be the entry index as int or its label as str"
            )
        if label:
            super().entryconfigure(index, label=label, **options)
            self.labels[index] = label
        else:
            super().entryconfigure(index, **options)


class Gr1d(Frame):
    """
    The 9x9 boxes sudoku grid
    Leet speak for Grid not to confuse with tkinter.Grid class
    """

    def __init__(self, app):
        Frame.__init__(self, app)
        self.app = app
        self.correct = True
        self.solutions = self.solution_generator()
        self.progress_box = None
        self.tips_shown = IntVar(value=True)
        self.conflicts_shown = IntVar(value=True)
        self.conflicts_shown.trace_variable("w", self.check)
        self.regions = [
            [Region(self, reg_row, reg_col) for reg_col in range(3)]
            for reg_row in range(3)
        ]
        # Structures of boxes used by Gr1d.__iter__ and Box.neighbourhood
        self.rows = [
            [
                Box(
                    app,
                    self,
                    self.regions[row // 3][col // 3],
                    row,
                    col,
                    row // 3 * 3 + col // 3,
                )
                for col in range(9)
            ]
            for row in range(9)
        ]
        self.boxes_of = {
            "row": self.rows,
            "col": [[self.rows[row][col] for row in range(9)] for col in range(9)],
            "reg": [
                [
                    self.rows[row][col]
                    for row in range(reg_row, reg_row + 3)
                    for col in range(reg_col, reg_col + 3)
                ]
                for reg_row in range(0, 9, 3)
                for reg_col in range(0, 9, 3)
            ],
        }
        self.pack()

    def __getitem__(self, key):
        """ Returns a box """
        if isinstance(key, int):
            # grid[row][box] returns box of coordinates [row][col] with row, col its integer indices
            return self.rows[key]
        elif isinstance(key, str):
            # grid[area][m][n] returns the nth box of the mth area
            # with area in "row" (row), "col" (column) or "reg" (region)
            return self.boxes_of[key]
        else:
            raise TypeError("key must be the row index as int or a area as str")

    def __iter__(self):
        """ Browses every box of the grid """
        for boxes_of_row in self.rows:
            for box in boxes_of_row:
                yield box

    def open_nb_clues_message_box(self):
        """
        Opens a message box to get the minimum number of clues,
        then generate a grid with a near number of clues
        """
        if self.app.game.confirm_erase():
            self.create()
            NbCluesMessageBox(self.app)

    def auto_create(self, min_nb_clues):
        """ Automatic grid creation """
        self.progress_box = ProgressBox(
            self.app,
            GENERATE_PROGRESS_BOX_TITLE,
            GENERATE_PROGRESS_BOX_TEXT,
            maximum=81,
        )
        # Build a valid solution
        try:
            self.solve()
        except CancelInterrupt:
            # self.create(force=True)
            self.progress_box.destroy()
            self.progress_box = None
        else:
            remaining_boxes = [box for box in self]
            shuffle(remaining_boxes)
            nb_clues = len(remaining_boxes)
            self.progress_box.text.set(CLUES_DELETING_PROGRESS_BOX_TEXT)
            self.progress_box.progress_bar.configure(maximum=81)
            self.progress_box.cancel_button.configure(
                text=CANCEL_AUTO_CREATE_BUTTON_TEXT, command=self.progress_box.on_stop
            )
            self.progress_box.cancel_button.bind("<space>", self.progress_box.on_stop)
            self.progress_box.bind("<Escape>", self.progress_box.on_stop)
            # Remove clues while the grid is valid
            # until the number of clues is near the number requested by user
            while (
                remaining_boxes
                and nb_clues > min_nb_clues
                and not self.progress_box.cancel_pressed
            ):
                box = remaining_boxes.pop(0)
                tmp_digit = box.digit.get()
                box.state(("!disabled",))
                self.progress_box.variable.set(81 - len(remaining_boxes))
                box.digit.set("")
                if self.validate():
                    nb_clues -= 1
                else:
                    box.digit.set(tmp_digit)
                    box.state(("disabled",))
                    self.app.update()
                    self.progress_box.update()
            self.validate()
            self.app.game.restart(force=True)
            self.app.game.erase_enabled = False
            self.progress_box.destroy()
            self.progress_box = None
            self.check()

    def create(self, force=False):
        """ Make a blank grid to edit """
        if self.app.game.confirm_erase(force):
            app.title(APP_TITLE)
            for box in self:
                box.digit.set("")
            self.edit(force=True)
            self[0][0].focus_set()

    def edit(self, force=False):
        """ Allow user to write the grid """
        if self.app.game.confirm_erase(force):
            self.app.game.restart(force=True)
            for box in self:
                box.state(("!disabled",))
            self.app.menu.grid.entryconfigure(EDIT_LABEL, state=DISABLED)
            self.app.menu.grid.entryconfigure(VALIDATE_LABEL, state=NORMAL)
            self.app.menu.grid.entryconfigure(SOLVE_LABEL, state=DISABLED)
            self.app.menu.game.entryconfigure(LOAD_LABEL, state=NORMAL)
            self.app.menu.game.entryconfigure(SAVE_LABEL, state=NORMAL)
            self.app.menu.game.entryconfigure(RESTART_LABEL, state=DISABLED)

    def validate(self):
        """ Check if grid is valid: if it has a unique solution """
        if self.correct:
            if not self.progress_box:
                self.progress_box = ProgressBox(
                    self.app,
                    VALIDATION_PROGRESS_BOX_TITLE,
                    VALIDATION_PROGRESS_BOX_TEXT,
                    maximum=sum(
                        len(box.possible_digits) for box in self if not box.digit.get()
                    ),
                )
                self.progress_box.variable.set(0)
            hidden_solutions = self.solution_generator()
            try:
                next(hidden_solutions)
            except StopIteration:  # No solution
                self.app.game.restart(force=True)
                if self.progress_box.title() == VALIDATION_PROGRESS_BOX_TITLE:
                    self.progress_box.destroy()
                    self.progress_box = None
                    showerror(
                        NO_SOLUTION_MESSAGE_BOX_TITLE,
                        NO_SOLUTION_MESSAGE_BOX_TEXT,
                        icon="error",
                    )
                    self.edit()
                else:
                    return False
            except CancelInterrupt:
                self.app.game.restart(force=True)
                if self.progress_box.title() == VALIDATION_PROGRESS_BOX_TITLE:
                    self.progress_box.destroy()
                    self.progress_box = None
                    self.edit(force=True)
                else:
                    return False
            else:
                if self.progress_box.title() == VALIDATION_PROGRESS_BOX_TITLE:
                    self.progress_box.text.set(NO_OTHER_SOLUTION_PROGESS_BOX_TEXT)
            try:
                next(hidden_solutions)
            except StopIteration:  # Unique solution
                self.app.game.restart(force=True)
                if self.progress_box.title() == VALIDATION_PROGRESS_BOX_TITLE:
                    self.progress_box.destroy()
                    self.progress_box = None
                else:
                    return True
            except CancelInterrupt:
                self.app.game.restart(force=True)
                if self.progress_box.title() == VALIDATION_PROGRESS_BOX_TITLE:
                    self.progress_box.destroy()
                    self.progress_box = None
                    self.edit(force=True)
                else:
                    return False
            else:  # More than 1 solution
                self.app.game.restart(force=True)
                if self.progress_box.title() == VALIDATION_PROGRESS_BOX_TITLE:
                    self.progress_box.destroy()
                    showerror(
                        INCORRECT_GRID_MESSAGE_BOX_TITLE,
                        SEVERAL_SOLUTIONS_MESSAGE_BOX_TEXT,
                        icon="error",
                    )
                    self.edit(force=True)
                else:
                    return False
        else:  # Incorrect grid
            if not self.progress_box:
                showerror(
                    INCORRECT_GRID_MESSAGE_BOX_TITLE,
                    CONFLICTS_MESSAGE_BOX_TEXT,
                    icon="error",
                )
            return False

    def solve(self):
        """ Automatic grid solving: the first generated solution """
        if self.correct:
            if not self.progress_box:
                self.progress_box = ProgressBox(
                    self.app,
                    SOLVING_PROGRESS_BOX_TITLE,
                    CALCULATING_SURE_DIGITS_TEXT,
                    maximum=sum(
                        len(box.possible_digits) for box in self if not box.digit.get()
                    ),
                )
                self.progress_box.variable.set(0)
            try:
                next(self.solutions)
            except StopIteration as e:
                self.app.menu.grid.entryconfigure(SOLVE_LABEL, state=DISABLED)
                if self.progress_box.title() == SOLVING_PROGRESS_BOX_TITLE:
                    self.progress_box.destroy()
                    self.progress_box = None
                    showerror(
                        NO_SOLUTION_MESSAGE_BOX_TITLE,
                        e.args[0] if e.args else "Pas de solution trouvée.",
                        icon="error",
                    )
            except CancelInterrupt:
                if self.progress_box.title() == SOLVING_PROGRESS_BOX_TITLE:
                    self.progress_box.destroy()
                    self.progress_box = None
                else:
                    raise CancelInterrupt
            else:
                self.app.menu.grid.entryconfigure(SOLVE_LABEL, state=NORMAL)
                if self.progress_box.title() == SOLVING_PROGRESS_BOX_TITLE:
                    self.progress_box.destroy()
                    self.progress_box = None
        else:  # Incorrect grid
            if not self.progress_box:
                showerror(
                    INCORRECT_GRID_MESSAGE_BOX_TITLE,
                    CONFLICTS_MESSAGE_BOX_TEXT,
                    icon="error",
                )
            return False

    def check(self, *args):
        """
        Called when a box's digit is changed
        Check if there is no boxes with same digits in conflict in the same area
        """
        self.app.game.erase_enabled = False
        self.app.style.redraw()  #  Redraw GUI
        # Check and show digits' conflicts
        self.correct = True
        for area in "row", "col", "reg":
            for index in range(9):
                for box1, box2 in combinations(self.app.gr1d[area][index], 2):
                    if box1.digit.get() == box2.digit.get() != "":
                        self.correct = False
                        if self.conflicts_shown.get():
                            for box in self.app.gr1d[area][index]:
                                box.config(style="ErrorArea.Box.TEntry")
                            for box in box1, box2:
                                box.config(style="ErrorBox.ErrorArea.Box.TEntry")
                for box in self.app.gr1d[area][index]:
                    if (
                        self.conflicts_shown
                        and not box.digit.get()
                        and not box.possible_digits
                    ):
                        box.config(style="ErrorBox.ErrorArea.Box.TEntry")
        if not self.progress_box:
            # Check if grid is solved
            if self.correct:
                if sum(box.digit.get() == "" for box in self) == 0:
                    self.app.menu.grid.entryconfigure(SOLVE_LABEL, state=DISABLED)
                    self.app.game.erase_enabled = True
                    showinfo(
                        SOLVED_GRID_MESSAGE_BOX_TITLE, SOLVED_GRID_MESSAGE_BOX_TEXT
                    )
                else:  # Focus to the easiest box to solve
                    try:
                        next(
                            box
                            for box in self
                            if not box.digit.get()
                            and len(box.possible_digits) == 1
                            and HighlightButton.digit in {""} | box.possible_digits
                        ).focus_set()
                    except StopIteration:
                        pass
            self.solutions = self.solution_generator()
            self.app.menu.grid.entryconfigure(VALIDATE_LABEL, state=NORMAL)
            self.app.menu.grid.entryconfigure(EDIT_LABEL, state=NORMAL)
            self.app.menu.grid.entryconfigure(SOLVE_LABEL, state=NORMAL)
            self.app.menu.game.entryconfigure(LOAD_LABEL, state=NORMAL)
            self.app.menu.game.entryconfigure(SAVE_LABEL, state=NORMAL)
            self.app.menu.game.entryconfigure(RESTART_LABEL, state=NORMAL)

    def solution_generator(self, nb_recursion=1):
        """
        Yields each solution of the grid
        """
        empty_boxes = [box for box in self if box.digit.get() == ""]
        found_boxes = []
        shuffle(empty_boxes)
        another_digit_found = True
        # Find sure digits: when there is only 1 possible digit in the box
        while (
            self.correct
            and empty_boxes
            and another_digit_found
            and not self.progress_box.cancel_pressed
        ):
            another_digit_found = False
            for box in empty_boxes:
                if box.possible_digits:
                    if len(box.possible_digits) == 1:
                        box.digit.set(box.possible_digits.pop())
                        if (
                            self.progress_box.title() == SOLVING_PROGRESS_BOX_TITLE
                            or self.progress_box.text.get()
                            == GENERATE_PROGRESS_BOX_TEXT
                        ):
                            if (
                                self.progress_box.text.get()
                                == GENERATE_PROGRESS_BOX_TEXT
                            ):
                                box.state(("disabled",))
                                box.update()
                            self.progress_box.variable.set(
                                self.progress_box.variable.get() + 1 / nb_recursion
                            )
                        found_boxes.append(box)
                        empty_boxes.remove(box)
                        another_digit_found = True
        if self.progress_box.cancel_pressed:
            self.solutions = self.solution_generator()
            raise CancelInterrupt(CANCEL_EXCEPTION)
        # Try every possible digits
        elif self.correct:
            if empty_boxes:
                empty_boxes.sort(key=lambda box: len(box.possible_digits))
                tested_box = empty_boxes[0]
                digits_to_try = sample(
                    tested_box.possible_digits, len(tested_box.possible_digits)
                )
                for tested_digit in digits_to_try:
                    tested_box.digit.set(tested_digit)
                    if self.progress_box.title() == SOLVING_PROGRESS_BOX_TITLE:
                        self.progress_box.text.set(
                            TESTS_PROGRESS_BOX_TEXT.format(
                                tested_digit, str(tested_box)
                            )
                        )
                    elif self.progress_box.text.get() == GENERATE_PROGRESS_BOX_TEXT:
                        tested_box.state(("disabled",))
                        tested_box.update()
                    self.progress_box.variable.set(
                        self.progress_box.variable.get() + 1 / nb_recursion
                    )
                    yield from self.solution_generator(
                        1
                        if self.progress_box.text.get() == GENERATE_PROGRESS_BOX_TEXT
                        else nb_recursion + 1
                    )
                    for box in empty_boxes:
                        if box.digit.get():
                            if self.progress_box.title() == GENERATE_PROGRESS_BOX_TITLE:
                                box.state(("!disabled",))
                            box.digit.set("")
            else:
                yield None
        else:
            # Incorrect grid, maybe a wrong hypothesis
            self.app.menu.grid.entryconfigure(SOLVE_LABEL, state=DISABLED)
            raise StopIteration(NO_SOLUTION_EXCEPTION)
        for box in found_boxes:
            if self.progress_box.title() == GENERATE_PROGRESS_BOX_TITLE:
                box.state(("!disabled",))
            box.digit.set("")
        self.app.menu.grid.entryconfigure(SOLVE_LABEL, state=DISABLED)

    def set_box_focus(self, box, row_delta, col_delta):
        """ Select an enabled adjacent box """
        row, col = box.row, box.col
        keep_browse = True
        while keep_browse:
            col += col_delta
            row += row_delta
            if col > 8:
                col = 0
                row = (row + 1) % 9
            elif col < 0:
                col = 8
                row = (row - 1) % 9
            if row < 0:
                row = 8
                col = (col - 1) % 9
            elif row > 8:
                row = 0
                col = (col + 1) % 9
            keep_browse = self.rows[row][col].instate(("disabled",))
        self.rows[row][col].focus_set()


class Region(Frame):
    """
    3x3 boxes subgrid/region
    """

    def __init__(self, grid, reg_row, reg_col):
        Frame.__init__(self, grid, relief=SUNKEN, borderwidth=2)
        self.grid(row=reg_row, column=reg_col, sticky="nswe")


class Box(ttk.Entry):
    """
    Entry box of the grid
    """

    def __init__(self, app, gr1d, region, row, col, reg, *options):
        self.app = app
        self.digit = StringVar()
        self.digit.trace_variable("w", self.on_digit_change)
        ttk.Entry.__init__(
            self,
            region,
            textvariable=self.digit,
            style="Box.TEntry",
            font=("Arial", 16),
            width=2,
            justify=CENTER,
            validate="key",
            validatecommand=(app.register(self.check), "%P"),
            *options
        )
        self.state(("disabled",))
        self.row, self.col, self.reg = row, col, reg
        self.possible_digits = set(digits)
        self.grid(row=row % 3, column=col % 3)
        self.bind("<FocusIn>", self.on_focus)
        self.bind("<KeyPress-Up>", lambda event: gr1d.set_box_focus(self, -1, 0))
        self.bind("<KeyPress-Down>", lambda event: gr1d.set_box_focus(self, +1, 0))
        self.bind("<KeyPress-Left>", lambda event: gr1d.set_box_focus(self, 0, -1))
        self.bind("<KeyPress-Right>", lambda event: gr1d.set_box_focus(self, 0, +1))
        self.tip = Tooltip(self)
        gr1d.tips_shown.trace_variable("w", self.show_tips)

    def check(self, changed_digit):
        """
        Called on user input
        Input is allowed only if it's one digit
        """
        return len(changed_digit) <= 1 and changed_digit in digits

    def on_focus(self, event):
        """ Selects text """
        self.select_range(0, END)

    def neighbourhood(self, area):
        """
        neighbourhood(area) browses every boxes of the area of the box
        with area in "row" (row), "col" (column) or "reg" (region)
        """
        for box in self.app.gr1d[area][getattr(self, area)]:
            yield box

    def on_digit_change(self, *args):
        """
        Called when a box's digit is changed
        Find the digits wich aren't in the row, column or region of the box
        """
        for area in "row", "col", "reg":
            for box in self.neighbourhood(area):
                box.possible_digits = set(digits)
                for box_area in "row", "col", "reg":
                    box.possible_digits -= {
                        box.digit.get() for box in box.neighbourhood(box_area)
                    }
                if self.app.gr1d.tips_shown.get() and box.digit.get() == "":
                    if box.possible_digits:
                        box.tip.text = " ".join(sorted(box.possible_digits)) + " ?"
                    else:
                        box.tip.text = "???"
                    box.tip.shown = True
                else:
                    box.tip.shown = False
        if (
            not self.app.gr1d.progress_box
            and not HighlightButton.digit
            and self.digit.get()
        ):
            self.app.gr1d.set_box_focus(self, 0, +1)
        self.app.gr1d.check()
        if not self.app.gr1d.correct:
            self.focus_set()

    def show_tips(self, *args):
        """
        Called when "View > Show tips" menu is changed
        Show or hide a tooltip on the box with its possible digits
        """
        self.tip.shown = self.tips_shown.get()

    def __str__(self):
        return "case " + str((self.row + 1, self.col + 1))

    def __repr__(self):
        return (
            str((self.row, self.col))
            + str([self.digit.get()])
            + str(self.possible_digits)
        )


class Tooltip:
    """
    It creates a tooltip for a given widget as the mouse goes on it.

    see:

    http://stackoverflow.com/questions/3221956/
           what-is-the-simplest-way-to-make-tooltips-
           in-tkinter/36221216#36221216

    http://www.daniweb.com/programming/software-development/
           code/484591/a-tooltip-class-for-tkinter

    - Originally written by vegaseat on 2014.09.09.

    - Modified to include a delay time by Victor Zaccardo on 2016.03.25.

    - Modified
        - to correct extreme right and extreme bottom behavior,
        - to stay inside the screen whenever the tooltip might go out on
          the top but still the screen is higher than the tooltip,
        - to use the more flexible mouse positioning,
        - to add customizable background color, padding, waittime and
          wraplength on creation
      by Alberto Vassena on 2016.11.05.

      Tested on Ubuntu 16.04/16.10, running Python 3.5.2

    TODO: themes styles support
    """

    TIP_DELAY = 2000

    def __init__(
        self,
        widget,
        *,
        bg="white",
        fg="dim gray",
        pad=(3, 2, 3, 2),
        text="widget info",
        delay=TIP_DELAY,
        wraplength=250,
        shown=True
    ):

        self.shown = shown  #  Added by AM
        self.delay = delay  #  in milliseconds, originally 500
        self.wraplength = wraplength  #  in pixels, originally 180
        self.widget = widget
        self.text = text
        self.bg = bg
        self.fg = fg
        self.pad = pad
        self.id = None
        self.tw = None
        self.widget.bind("<Enter>", self.onEnter)
        self.widget.bind("<Leave>", self.onLeave)
        self.widget.bind("<ButtonPress>", self.onLeave)

    def onEnter(self, event=None):
        if self.shown:  #  Added by AM
            self.schedule()

    def onLeave(self, event=None):
        self.unschedule()
        self.hide()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.delay, self.show)

    def unschedule(self):
        id_ = self.id
        self.id = None
        if id_:
            self.widget.after_cancel(id_)

    def show(self):
        def tip_pos_calculator(widget, label, *, tip_delta=(10, 5), pad=(5, 3, 5, 3)):

            w = widget

            s_width, s_height = w.winfo_screenwidth(), w.winfo_screenheight()

            width, height = (
                pad[0] + label.winfo_reqwidth() + pad[2],
                pad[1] + label.winfo_reqheight() + pad[3],
            )

            mouse_x, mouse_y = w.winfo_pointerxy()

            x1, y1 = mouse_x + tip_delta[0], mouse_y + tip_delta[1]
            x2, y2 = x1 + width, y1 + height

            x_delta = x2 - s_width
            if x_delta < 0:
                x_delta = 0
            y_delta = y2 - s_height
            if y_delta < 0:
                y_delta = 0

            offscreen = (x_delta, y_delta) != (0, 0)

            if offscreen:

                if x_delta:
                    x1 = mouse_x - tip_delta[0] - width

                if y_delta:
                    y1 = mouse_y - tip_delta[1] - height

            offscreen_again = y1 < 0  # out on the top

            if offscreen_again:
                # No further checks will be done.

                # TIP:
                # A further mod might automagically augment the
                # wraplength when the tooltip is too high to be
                # kept inside the screen.
                y1 = 0

            return x1, y1

        bg = self.bg
        fg = self.fg
        pad = self.pad
        widget = self.widget

        # creates a toplevel window
        self.tw = Toplevel(widget)

        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)

        border = Frame(self.tw, background=fg)
        win = Frame(border, background=bg, borderwidth=1)
        label = Label(
            win,
            text=self.text,
            justify=LEFT,
            background=bg,
            foreground=fg,
            relief=SOLID,
            borderwidth=0,
            wraplength=self.wraplength,
        )

        label.grid(padx=(pad[0], pad[2]), pady=(pad[1], pad[3]), sticky=NSEW)
        win.grid(padx=1, pady=1)
        border.grid()

        x, y = tip_pos_calculator(widget, label)

        self.tw.wm_geometry("+%d+%d" % (x, y))

    def hide(self):
        tw = self.tw
        if tw:
            tw.destroy()
        self.tw = None


class NbCluesMessageBox(Toplevel):
    """
    A message box allowing user to choose a number of clues boxes
    """

    DEFAULT_NB_CLUES = 25
    MIN_NB_CLUES = 17
    MAX_NB_CLUES = 80

    def __init__(self, app):
        Toplevel.__init__(self, app)
        self.app = app
        self.title(NB_CLUES_MESSAGE_BOX_TITLE)
        self.resizable(width=False, height=False)
        self.grab_set()
        self.nb_clues = IntVar()
        self.nb_clues.set(NbCluesMessageBox.DEFAULT_NB_CLUES)
        self.nb_clues.trace_variable("w", self.round_nb_clues)
        message_box_frame = ttk.Frame(self)
        enter_nb_frame = ttk.Frame(message_box_frame)
        enter_nb_label = ttk.Label(enter_nb_frame, text=NB_CLUES_INPUT_LABEL)
        enter_nb_label.pack(side=LEFT)
        spinbox = Spinbox(
            enter_nb_frame,
            width=2,
            from_=NbCluesMessageBox.MIN_NB_CLUES,
            to=NbCluesMessageBox.MAX_NB_CLUES,
            increment=1,
            textvariable=self.nb_clues,
        )
        spinbox.pack(side=RIGHT)
        enter_nb_frame.pack(padx=5, pady=5, fill=X)
        scale_frame = ttk.Frame(message_box_frame)
        simpler_msg = ttk.Label(scale_frame, text=HARDER_LABEL, justify=RIGHT)
        simpler_msg.pack(side=LEFT)
        self.scale = ttk.Scale(
            scale_frame,
            command=self.round_nb_clues,
            length=162,
            from_=NbCluesMessageBox.MIN_NB_CLUES,
            to=NbCluesMessageBox.MAX_NB_CLUES,
            orient=HORIZONTAL,
            variable=self.nb_clues,
        )
        self.scale.pack(side=LEFT, padx=5, pady=5)
        more_difficult_msg = ttk.Label(scale_frame, text=EASIER_LABEL, justify=LEFT)
        more_difficult_msg.pack(side=LEFT, padx=5, pady=5)
        scale_frame.pack(padx=5, pady=5)
        buttons_frame = ttk.Frame(message_box_frame)
        cancel_button = ttk.Button(
            buttons_frame, text=CANCEL_BUTTON_TEXT, command=self.destroy
        )
        cancel_button.pack(side=RIGHT, padx=5, pady=5)
        cancel_button.bind("<space>", lambda event: self.destroy())
        ok_button = ttk.Button(buttons_frame, text=OK_BUTTON_TEXT, command=self.on_ok)
        ok_button.pack(side=RIGHT, padx=5, pady=5)
        ok_button.bind("<space>", self.on_ok)
        ok_button.focus_set()
        buttons_frame.pack()
        self.bind("<Return>", self.on_ok)
        self.bind("<Escape>", self.destroy)
        message_box_frame.pack()

    def round_nb_clues(self, *args):
        try:
            nb = int(self.nb_clues.get())
        except TclError:
            nb = NbCluesMessageBox.MIN_NB_CLUES
        finally:
            if nb < NbCluesMessageBox.MIN_NB_CLUES:
                nb = NbCluesMessageBox.MIN_NB_CLUES
            elif nb > NbCluesMessageBox.MAX_NB_CLUES:
                nb = NbCluesMessageBox.MAX_NB_CLUES
            self.nb_clues.set(nb)
            self.update()

    def on_ok(self, event=None):
        """ Generate a grid on [OK] button press """
        self.destroy()
        self.app.gr1d.auto_create(self.nb_clues.get())


class CancelInterrupt(KeyboardInterrupt):
    pass


class ProgressBox(Toplevel):
    """
    Message box showing progress used by Gr1d.validate and Gr1d.generate
    """

    def __init__(self, app, title="", text="", **options):
        Toplevel.__init__(self, app)
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.title(title)
        self.resizable(width=False, height=False)
        self.grab_set()
        frame = ttk.Frame(self)
        self.text = StringVar()
        self.text.set(text)
        label = ttk.Label(frame, textvariable=self.text)
        label.pack(anchor=W, padx=10, pady=5)
        self.variable = DoubleVar(0)
        self.variable.trace_variable("w", lambda *args: self.update())
        self.progress_bar = ttk.Progressbar(
            frame,
            length=250,
            orient="horizontal",
            mode="determinate",
            variable=self.variable,
            **options
        )
        self.progress_bar.pack(padx=10, pady=5)
        self.cancel_button = ttk.Button(
            frame, text=CANCEL_BUTTON_TEXT, command=self.on_cancel
        )
        self.cancel_button.bind("<space>", self.on_cancel)
        self.cancel_button.pack(side=RIGHT, padx=10, pady=5)
        self.cancel_pressed = False
        frame.pack(ipady=5)
        self.bind("<Escape>", self.on_cancel)
        self.update()

    def on_cancel(self, event=None):
        """
        Called on Cancel button or quit button press
        """
        self.cancel_button.state(("disabled",))
        self.text.set(CANCELLED_PROGRESS_BOX_TEXT)
        self.cancel_pressed = True
        self.update()

    def on_stop(self, event=None):
        """
        Called on Cancel button or quit button press
        """
        self.cancel_button.state(("disabled",))
        self.text.set(STOPPING_PROGRESS_BOX_TEXT)
        self.cancel_pressed = True
        self.update()


class HighlightButtonsFrame(Frame):
    """ Frame of HighlightButtons looking like a status bar """

    def __init__(self, app):
        Frame.__init__(self, app, border=1, relief=SUNKEN)
        self.buttons = [HighlightButton(app, self, digit) for digit in digits]
        self.pack(fill=X)


class HighlightButton(ttk.Button):
    """
    Buttons showing every digits
    Allowing user to see where not to write the selected digit
    """

    digit = ""

    def __init__(self, app, parent, digit):
        self.digit = digit
        self.pressed = False
        self.app = app
        ttk.Button.__init__(
            self, parent, text=digit, width=2, padding="0 0", command=self.on_click
        )
        self.app = app
        self.state(("disabled",))
        self.pack(side="left", expand=True, fill="x")

    def on_click(self, *args):
        """
        Select or unselect a digit and show where not to write the selected digit
        """
        if self.pressed:
            self.state(("!pressed",))
            self.pressed = False
            HighlightButton.digit = ""
        else:
            for highlight_button in self.app.highlight_buttons.buttons:
                highlight_button.state(("!pressed",))
                highlight_button.pressed = False
            self.state(("pressed",))
            self.pressed = True
            HighlightButton.digit = self.digit
        self.app.gr1d.check()

    def enable(self):
        """ Enable button when all the same digits aren't found """
        self.state(("!disabled",))

    def disable(self):
        """ Disable button when all the same digits are found """
        self.state(("disabled",))
        if HighlightButton.digit == self.digit:
            HighlightButton.digit = ""


class Game:
    """
    Game functions
    """

    def __init__(self, app):
        self.app = app
        self.erase_enabled = True
        self.file_path = ""

    def confirm_erase(self, force=False):
        """ If a game is started, pop a message box to confirm game erasement """
        self.erase_enabled = (
            self.erase_enabled
            or force
            or askokcancel(
                CONFIRM_ERASE_MESSAGE_BOX_TITLE,
                CONFIRM_ERASE_MESSAGE_BOX_TEXT,
                default="cancel",
                icon="warning",
            )
        )
        return self.erase_enabled

    def open(self, file_path=""):
        """ Open a game saved in a file """
        if self.confirm_erase():
            self.file_path = file_path or askopenfilename(
                parent=self.app,
                defaultextension=".pysudoku",
                initialdir=".",
                title=OPEN_FILE_MESSAGE_BOX_TITLE,
                filetypes=[(FILE_TYPE_NAME, "*.pysudoku")],
            )
        if self.file_path:
            if exists(self.file_path):
                self.app.gr1d.create()
                with open(self.file_path, "rb") as file:
                    loader = Unpickler(file)
                    try:
                        HighlightButton.digit = loader.load()
                        for box in self.app.gr1d:
                            box.state(("!disabled",))
                            box.state(loader.load())
                            box.digit.set(loader.load())
                    except UnpicklingError:
                        showerror(
                            FILE_ERROR_MESSAGE_BOX_TITLE,
                            CORRUPTED_FILE_MESSAGE_BOX_TEXT.format(basename(file_path)),
                            icon="error",
                        )
                    else:
                        print(
                            basename(self.file_path),
                            basename(self.file_path).rstrip(APP_TITLE),
                        )
                        self.app.title(
                            basename(self.file_path).rstrip(".pysudoku") + " - PySudoku"
                        )
                        self.erase_enabled = True
                        self.app.menu.grid.entryconfigure(VALIDATE_LABEL, state=NORMAL)
                        self.app.self.app.menu.grid.entryconfigure(
                            EDIT_LABEL, state=NORMAL
                        )
                        self.app.menu.grid.entryconfigure(SOLVE_LABEL, state=NORMAL)
                        self.app.menu.game.entryconfigure(LOAD_LABEL, state=NORMAL)
                        self.app.menu.game.entryconfigure(SAVE_LABEL, state=DISABLED)
                        self.app.menu.game.entryconfigure(RESTART_LABEL, state=NORMAL)
            else:
                showerror(
                    FILE_ERROR_MESSAGE_BOX_TITLE,
                    FILE_NOT_FOUND_MESSAGE_BOX_TEXT.format(basename(file_path)),
                    icon="error",
                )

    def save(self):
        """ Save a game in a file """
        save_path = asksaveasfilename(
            parent=self.app,
            defaultextension=".pysudoku",
            initialdir=dirname(self.file_path),
            initialfile=basename(self.file_path),
            title=SAVE_FILE_MESSAGE_BOX_TITLE,
            filetypes=[(FILE_TYPE_NAME, "*.pysudoku")],
        )
        if save_path:
            self.file_path = save_path
            with open(save_path, "wb") as file:
                saver = Pickler(file)
                saver.dump(HighlightButton.digit)
                for box in self.app.gr1d:
                    saver.dump(box.state())
                    saver.dump(box.digit.get())
            self.erase_enabled = True
            self.app.title(basename(self.file_path).rstrip(".pysudoku") + " - PySudoku")
        return save_path

    def restart(self, force=False):
        """ Restart game: blank enabled boxes and keep clues boxes """
        if force or self.confirm_erase():
            for box in self.app.gr1d:
                if box.instate(("!disabled",)):
                    box.digit.set("")
            self.erase_enabled = True
            self.app.menu.grid.entryconfigure(EDIT_LABEL, state=NORMAL)
            self.app.menu.grid.entryconfigure(VALIDATE_LABEL, state=DISABLED)
            self.app.menu.grid.entryconfigure(SOLVE_LABEL, state=NORMAL)
            self.app.menu.game.entryconfigure(LOAD_LABEL, state=NORMAL)
            self.app.menu.game.entryconfigure(SAVE_LABEL, state=NORMAL)
            self.app.menu.game.entryconfigure(RESTART_LABEL, state=NORMAL)


class App(Tk):
    def __init__(self, argv):
        Tk.__init__(self)
        self.title(APP_TITLE)
        self.iconphoto(
            True,
            PhotoImage(name="icon16", data=ICON16),
            PhotoImage(name="icon32", data=ICON32),
            PhotoImage(name="icon48", data=ICON48),
        )  # Titlebar
        try:  # Windows taskbar icon
            from ctypes import windll

            windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                "MALINGREY.Adrien.PySudoku.0.2"
            )
        except ImportError:  # Linux
            pass
        self.resizable(width=False, height=False)
        self.style = CustomStyle(self)
        self.gr1d = Gr1d(
            self
        )  #  leet speak for grid not to confuse with tkinter.Grid.grid method
        self.highlight_buttons = HighlightButtonsFrame(self)
        self.game = Game(self)
        self["menu"] = self.menu = MenuBar(self)  # Window menu bar
        self.protocol("WM_DELETE_WINDOW", self.on_close)  # Action on close button press
        if len(argv) > 1:
            self.game.open(argv[1])

    def open_wiki(self):
        """ Open Sudoku article on wikipedia to learn sudoku rules (and more) """
        open_web_browser(WIKI_URL)

    def show_about(self):
        """ About message box """
        showinfo(ABOUT_MESSAGE_BOX_TITLE, ABOUT_MESSAGE_BOX_TEXT)

    def on_close(self):
        """
        Called on close button press
        Allow user to save started game and quit
        """
        save_before_close = not self.game.erase_enabled and askyesnocancel(
            CLOSE_MESSAGE_BOX_TITLE,
            CLOSE_MESSAGE_BOX_TITLE,
            icon="warning",
            default="cancel",
        )

        if save_before_close != None:  # [Yes] or [No] button pressed (not [Cancel])
            if save_before_close == True:  # [Yes] button pressed
                if self.game.save() == "":  # Save dialog box cancelled
                    self.on_close()  # Ask again
            self.quit()
        else:  # [Cancel] button pressed : do nothing
            pass


if __name__ == "__main__":
    app = App(argv)
    exit(app.mainloop())
