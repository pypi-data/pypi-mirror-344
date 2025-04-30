"""Homepage (index) of GUI."""

from pathlib import Path

from oe_python_template.utils import BasePageBuilder, GUILocalFilePicker

from ._service import Service


async def pick_file() -> None:
    """Open a file picker dialog and show notifier when closed again."""
    from nicegui import ui  # noqa: PLC0415

    result = await GUILocalFilePicker(str(Path.cwd() / "examples"), multiple=True)  # type: ignore
    ui.notify(f"You chose {result}")


class PageBuilder(BasePageBuilder):
    @staticmethod
    def register_pages() -> None:
        from nicegui import ui  # noqa: PLC0415

        @ui.page("/")
        def page_index() -> None:
            """Homepage of GUI."""
            service = Service()

            ui.button("Choose file", on_click=pick_file, icon="folder").mark("BUTTON_CHOOSE_FILE")

            ui.button("Click me", on_click=lambda: ui.notify(service.get_hello_world()), icon="check").mark(
                "BUTTON_CLICK_ME"
            )

            from importlib.util import find_spec  # noqa: PLC0415

            if find_spec("matplotlib") and find_spec("numpy"):
                import numpy as np  # noqa: PLC0415

                with ui.card().tight().mark("CARD_PLOT"):  # noqa: SIM117
                    with ui.matplotlib(figsize=(4, 3)).figure as fig:
                        x = np.linspace(0.0, 5.0)
                        y = np.cos(2 * np.pi * x) * np.exp(-x)
                        ax = fig.gca()
                        ax.plot(x, y, "-")

            ui.link("Info", "/info").mark("LINK_INFO")
