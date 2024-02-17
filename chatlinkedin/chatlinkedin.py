import reflex as rx
from model import ask_question


class State(rx.State):
    query: str = ""
    answer: str = ""
    res = ask_question(query)

    def sumbit_query(self):
        res = ask_question(self.query)
        self.answer = res


def index() -> rx.Component:
    return rx.container(
        rx.color_mode_button(rx.color_mode_icon(), float="right", margin_right="1rem"),
        rx.vstack(
            rx.heading(
                "Chat with your ",
                rx.span("LinkedIn", color="blue.500"),
                " data.",
                font_size="2rem",
                margin_bottom="2rem"
            ),
            rx.form(
                rx.hstack(
                    rx.input(
                        placeholder="Ask your question...",
                        on_change=State.set_query,
                        width="40rem",
                    ),
                    rx.icon_button(
                        icon=rx.icon(tag="arrow_forward"),
                        height="2.6rem",
                        bg="blue.500",
                        color="white",
                        type="submit",
                        on_click=State.sumbit_query
                    ),
                    reset_on_submit=True,
                ),
                margin_top="5rem"
            ),
            margin_top="5rem"
        ),
        rx.text(State.answer),
    )


# Create app instance and add index page.
app = rx.App()
app.add_page(index)
