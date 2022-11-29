import PySimpleGUI as sg
import funcs

layout = [
    [sg.Text("Current team:", font=("System"), background_color="gray11", text_color="gray97")],
    [
        sg.Multiline(
            "",
            disabled=True,
            no_scrollbar=True,
            key="-chat-",
            size=(20, 5),
            font=("System", 17),
            background_color="gray8",
            text_color="gray97",
        )
    ],
    [
        sg.Button("Porofessor", enable_events=True, key="-search-", font=("System")),
        sg.Button("Dodge", enable_events=True, key="-dodge-", font=("System")),
    ],
]

window = sg.Window("View lobby names", layout, background_color="gray11", button_color="gray8")

while True:
    event, values = window.read()
    match event:
        case "-search-":
            participants = funcs.search()
            window["-chat-"].update(participants)
        case "-dodge-":
            if funcs.match_phase("ChampSelect"):
                event, v = sg.Window(
                    f"Confirm dodge?",
                    [
                        [
                            sg.Stretch(background_color="gray11"),
                            sg.Text("Penalties still apply!", font=("System"), background_color="gray11"),
                            sg.Stretch(background_color="gray11"),
                        ],
                        [
                            sg.Button("Yes", s=12, button_color=("gray97", "#731a1a"), font="System"),
                            sg.Button("No", s=12, button_color=("gray97", "gray8"), font="System"),
                        ],
                    ],
                    modal=True,
                    background_color="gray11",
                ).read(close=True)
                if event == "Yes":
                    funcs.dodge()
        case sg.WIN_CLOSED:
            break
