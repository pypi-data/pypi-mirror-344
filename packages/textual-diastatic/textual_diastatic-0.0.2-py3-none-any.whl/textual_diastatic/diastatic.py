from textual.app import App, ComposeResult
from textual.validation import Integer, Regex
from textual.reactive import reactive, var
from textual import on
from textual.containers import (
    Vertical,
    VerticalScroll,
    Container,
    Horizontal,
)
from textual.widget import Widget
from textual.widgets import (
    Header,
    Footer,
    Input,
    Label,
    Markdown,
    DataTable,
    Button,
    Static,
)

import os
import sys


ROWS = [
    ("Id", "Fermentable", "DP", "unit"),
    (1, "Pale Ale", 85, "L"),
    (2, "Pilsner", 120, "L"),
    (3, "2-row pale", 140, "L"),
    (4, "6-row", 160, "L"),
    (5, "Vienna", 50, "L"),
    (6, "Munich 10L", 40, "L"),
    (7, "Wheat malt", "60-170", "L"),
    (8, "Rye", 105, "L"),
    (9, "Mild Malt", 50, "L"),
    (10, "Honey Malt", 50, "L"),
    (11, "Carafoam", 30, "L"),
    (12, "Aromatic Malt", 20, "L"),
    (13, "Caramel 20-120", 0, "L"),
    (14, "Black Malt", 0, "L"),
    (15, "Roasted Barley", 0, "L"),
    (16, "Carapils", 0, "L"),

]

dp_text = """ Malts with enough DP to convert
     themselves are at least 30 degrees
     Lintner; a grain bill that converts
     well in a 60 minute single infusion
     mash should have at least 60-70 degrees
     Lintner overall """


# ---------------- define widgets ------------------------

class InputWt(Vertical, can_focus=True):
    """Widget to gather basic fermentable data (weight) """

    def compose(self) -> ComposeResult:
        """Create child widgets of brew data."""

        with Container(id="wt_inputs"):
            with Horizontal(classes="inputs"):
                yield Label(classes="wt_label")
                yield Input(validators=[
                    Integer(),
                    Regex("[0123456789]*"),
                ],
                    placeholder="wt. #", classes="wt_input",
                    tooltip="Enter grain wt. as a positive Integer Only"
                )


class InputDp(Vertical, can_focus=True):
    """Widget to gather basic fermentable data (diastatic power) """

    def compose(self) -> ComposeResult:
        """Create child widgets of brew data."""

        with Container(id="dp_inputs"):
            with Horizontal(classes="inputs"):
                yield Label(classes="wt_label")
                yield Input(validators=[
                    Integer(),
                    Regex("[0123456789]*"),
                ],
                    placeholder="DP", classes="dp_input",
                    tooltip="Enter grain DP as a positive Integer Only"
                )


class SumData(Widget):
    """Widget to gather basic fermentable data (weight and diastatic power) """

    def compose(self) -> ComposeResult:
        """Create child widgets of brew data."""

        with Container(id="wt_dp_data"):
            with Horizontal(classes="sums"):
                yield Static("Total Wt.", classes="wt", id="res_wt")
                yield Label("Total DP", classes="dp", id="res_dp")


class DiastaticInfo(VerticalScroll):
    """Widget to display information in markdown about malt diastatic power"""

    def compose(self) -> ComposeResult:
        with VerticalScroll(classes="box"):
            yield Label("Typical Diastatic Pwr of Common Grains")
            yield DataTable()


# ********* begin App ***********
# *******************************
class DiastaticApp(App):
    # key binding (key, action name, description)
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit the app"),
        ("r", "reset_app", "Reset app"),
    ]

    # code to restart the program
    def action_reset_app(self) -> None:
        """Restart the application."""
        self.exit()  # Exits the current running instance of the app
        os.execl(sys.executable, 'python', "diastatic_calc_v01.py", *sys.argv[1:])

    # CSS file to use for styling
    CSS_PATH = "dp_v1.css"

    AUTO_FOCUS = ".wt_input"

    # reactives and variables
    wt1 = var(0)
    wt_list = var([])
    wt_total = reactive(0)
    wt_list_str = var([])
    dp1 = var(0)
    dp_list = var([])
    dp_total = var(0)
    dp_list_str = var([])
    gdp_list_str = var([])
    total_grist_dp = var(0)

    # ------------ App content begins here ----------------
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()

        with VerticalScroll(id="left_scroll"):
            yield InputWt(id="item1_wt")
            yield InputWt(id="item2_wt")
            yield InputWt(id="item3_wt")
            yield InputWt(id="item4_wt")
            yield InputWt(id="item5_wt")
            yield InputWt(id="item6_wt")
            yield InputWt(id="item7_wt")

        with VerticalScroll(id="mid_scroll"):
            yield InputDp(id="item1_dp")
            yield InputDp(id="item2_dp")
            yield InputDp(id="item3_dp")
            yield InputDp(id="item4_dp")
            yield InputDp(id="item5_dp")
            yield InputDp(id="item6_dp")
            yield InputDp(id="item7_dp")

        with Container(id="right_scroll"):
            yield DiastaticInfo()
            yield Label()
            yield Markdown(dp_text)

        with Container(id="bleft_scroll"):
            yield Label("Raw Weight & D-Power data:")
            yield Label()
            yield Static(id="wt_data")
            yield Static(id="wt_total")
            yield Label()
            yield Static(id="dp_data")
            yield Static(id="dp_total")

        with Container(id="bright_scroll"):
            yield Label("Grist Total DP Results:", classes="invisible", id="grist_results")
            yield Label()
            yield Button("Calculate Grist DP", tooltip="Press to calculate the grist DP", classes="grist_button",
                         id="calc_dp", disabled=True)
            yield Static(id="grist_dp")
            yield Label()
            yield Markdown(id="total_grist_dp")

    # ----------------- collect inputs -----------------------------------
    # --------------- collect weights and calc running total -------------
    # looks for input submission and updates output widget
    @on(Input.Submitted, ".wt_input")
    def update_wt1(self, event: Input.Submitted) -> None:
        # collect input (stored as a textual var)
        self.wt1 = event.value
        # add input value to a list
        self.wt_list.append(self.wt1)
        # Converting list to string using map() function
        self.wt_list_str = ' '.join(map(str, self.wt_list))
        # display list
        self.query_one("#wt_data").update(f"Grist wts: {self.wt_list_str}")
        # convert list and then sum
        wt_sum = self.wt_list_str
        self.wt_total = sum(map(int, wt_sum.split()))
        # display total weight as running total
        self.query_one("#wt_total").update(f"Total Grist Wt. = {self.wt_total}")
        # focus based on how many entries have been made
        to_focus = len(self.wt_list)
        dp_to_focus = f"#item{to_focus}_dp"
        self.query_one(dp_to_focus).focus()

    # --------------- collect diastatic power ----------------------------
    # looks for input submission and updates output widget
    @on(Input.Submitted, ".dp_input")
    def update_dp1(self, event: Input.Submitted) -> None:
        # collect input (stored as a textual var)
        self.dp1 = event.value
        # add input value to a list
        self.dp_list.append(self.dp1)
        # Converting list to string using map() function
        self.dp_list_str = ' '.join(map(str, self.dp_list))
        # display list
        self.query_one("#dp_data").update(f"Grist Dp {self.dp_list_str}")
        # convert list and then sum
        dp_sum = self.dp_list_str
        self.dp_total = sum(map(int, dp_sum.split()))
        # display total weight as running total
        self.query_one("#dp_total").update(f"Total DP = {self.dp_total}")
        # focus based on how many entries have been made
        to_focus = len(self.dp_list) + 1
        wt_to_focus = f"#item{to_focus}_wt"
        self.query_one(wt_to_focus).focus()
        self.query_one("#calc_dp").disabled = False

    # --------------- Calculate Grist DP _________________________________
    @on(Button.Pressed, "#calc_dp")
    def calc_grist_dp(self, event: Button.Pressed) -> None:
        wt_list_str = self.wt_list_str.split()
        dp_list_str = self.dp_list_str.split()
        wt_list_int = []
        dp_list_int = []
        for i in wt_list_str:
            wt_list_int.append(int(i))

        for i in dp_list_str:
            dp_list_int.append(int(i))

        grist_dp_list = []
        for i in range(len(self.wt_list)):
            grist_dp_list.append(wt_list_int[i] * dp_list_int[i])
            total_grist_dp = round(sum(grist_dp_list) / self.wt_total)
            gdp_list_str = ' '.join(map(str, grist_dp_list))

        self.query_one("#grist_dp").update(f"Grist DP per grain addition: {gdp_list_str}")
        self.query_one("#total_grist_dp").update(f"### Total Grist DP = {total_grist_dp} L/#")
        self.query_one("#calc_dp").display = False
        self.query_one("#grist_results").styles.visibility = "visible"

    # ------ display table of common grist diastatic power --------------

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*ROWS[0])
        table.add_rows(ROWS[1:])

def run() -> None:
    """Run the calculator application."""
    DiastaticApp().run()

if __name__ == "__main__":
    run()
