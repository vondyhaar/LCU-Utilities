import PySimpleGUI as sg
import reveal
import aram

reveal_tab = [
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

aram_tab = [
    [sg.Text("State:", font=("System"), background_color="gray11", text_color="gray97")],
    [        
        sg.Multiline(
            "",
            disabled=True,
            no_scrollbar=True,
            key="-state-",
            size=(20, 5),
            font=("System", 17),
            background_color="gray8",
            text_color="gray97",
        )
    ],
    [sg.Button("Boost", enable_events=True, key="-boost-", font="System"),
    sg.Button("Refresh JWT", enable_events=True, key="-jwt-", font="System")],
]

layout = [
    [
        sg.TabGroup(
            [
                [sg.Tab("Reveal", reveal_tab, background_color="gray11")],
                [sg.Tab("ARAM", aram_tab, background_color="gray11")],
                [sg.Tab("Refund", [], background_color="gray11")],
            ],
            background_color="gray11",
            tab_background_color="gray11",
            focus_color="gray11",
            title_color="gray50",
            selected_title_color="gray97",
            selected_background_color="gray11",
        )
    ]
]

window = sg.Window("LCU Util", layout, background_color="gray11", button_color="gray8")

while True:
    event, values = window.read()
    match event:
        case "-search-":
            participants = reveal.get_names()
            reveal.search()
            window["-chat-"].update(participants)
        case "-dodge-":
            if reveal.match_phase("ChampSelect"):
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
                    reveal.dodge()
        case "-boost-":
            aram.boost()
        case "-jwt-":
            aram.get_jwt()
        case sg.WIN_CLOSED:
            break
