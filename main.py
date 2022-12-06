# main.py

import sys

sys.path.insert(0, ".\\utils")

import PySimpleGUI as sg
import aram, reveal, refund

reveal_tab = [
    [sg.Text("Current team:", font=("System"), background_color="gray11", text_color="gray97")],
    [
        sg.Multiline(
            reveal.get_names(),
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
        sg.Button("Porofessor", enable_events=True, key="-search-", font="System"),
        sg.Button("Dodge", enable_events=True, key="-dodge-", font="System"),
    ],
]

aram_tab = [
    [sg.Text("State:", font=("System"), background_color="gray11", text_color="gray97")],
    [
        sg.Multiline(
            aram.get_jwt(),
            disabled=True,
            no_scrollbar=True,
            key="-state-",
            size=(20, 5),
            font=("System", 17),
            background_color="gray8",
            text_color="gray97",
        )
    ],
    [
        sg.Button("Boost", enable_events=True, key="-boost-", font="System"),
        sg.Button("Refresh JWT", enable_events=True, key="-jwt-", font="System", tooltip="Only if RP >= 95"),
    ],
]

transactions = refund.get_transactions()
refund_tab = [
    [sg.Text("Info:", font=("System"), background_color="gray11", text_color="gray97")],
    [
        sg.Multiline(
            "",
            disabled=True,
            no_scrollbar=True,
            key="-info-",
            size=(20, 5),
            font=("System", 17),
            background_color="gray8",
            text_color="gray97",
        )
    ],
    [
        sg.Combo(
            list(transactions.keys()),
            key="-transactions-",
            enable_events=True,
            readonly=True,
            font=("System"),
            text_color="gray97",
            background_color="gray8",
            button_background_color="gray8",
            button_arrow_color="gray97",
        ),
        sg.Button("Refund", enable_events=True, key="-refund-", font="System"),
        sg.Button("Refresh", enable_events=True, key="-refresh-", font="System"),
    ],
]

layout = [
    [
        sg.TabGroup(
            [
                [sg.Tab("Reveal", reveal_tab, background_color="gray11")],
                [sg.Tab("ARAM", aram_tab, background_color="gray11")],
                [sg.Tab("Refund", refund_tab, background_color="gray11")],
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

window = sg.Window(
    "LCU Utilities",
    layout,
    icon="utils\\eye.ico",
    titlebar_font="System",
    background_color="gray11",
    button_color="gray8",
    finalize=True,
)

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
            window["-state-"].update(aram.get_jwt())
        case "-transactions-":
            info = transactions.get(values["-transactions-"])
            info = "{}{}\n{}{}".format("WILL USE TOKEN!\n" if info["requiresToken"] else "", info["inventoryType"], info["amountSpent"], info["currencyType"])
            window["-info-"].update(info)
            pass
        case "-refund-":
            refund.refund(values["-transactions-"])
            names = list(refund.get_transactions().keys())
            window["-transactions-"].update(values=names)
            window["-info-"].update("")
        case "-refresh-":
            refund.update_transactions()
            window["-transactions-"].update(values=list(refund.get_transactions().keys()))
        case sg.WIN_CLOSED:
            break
