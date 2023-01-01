# main.py

import sys
import webbrowser

sys.path.insert(0, ".\\utils")

import PySimpleGUI as sg
import aram, reveal, refund, rename, misc

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
        sg.ButtonMenu(
            "Search",
            [["OPGG", "Porofessor", "U.GG"], ["OPGG", "Porofessor", "U.GG"]],
            key="-search-",
            font="System",
        ),
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

transactions = {}
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

name = ""
new = rename.get_new()
sniping = False
rename_tab = [
    [sg.Text("Info:", font=("System"), background_color="gray11", text_color="gray97")],
    [
        sg.Multiline(
            "New account" if new else "",
            disabled=True,
            no_scrollbar=True,
            key="-nameinfo-",
            size=(20, 5),
            font=("System", 17),
            background_color="gray8",
            text_color="gray97",
        )
    ],
    [
        sg.InputText(
            "",
            enable_events=True,
            key="-name-",
            font="System",
            size=(17, 1),
            text_color="gray97",
            background_color="gray8",
            disabled_readonly_background_color="red",
            use_readonly_for_disable=False,
        ),
        sg.Button("Check", enable_events=True, key="-check-", font="System"),
        sg.Button("Change", enable_events=True, key="-change-", font="System", disabled=True),
        sg.Button(
            "Snipe",
            enable_events=True,
            key="-snipe-",
            font="System",
            tooltip="Interrupt manually with Ctrl+C on terminal",
        ),
    ],
]

ux = True
misc_tab = [
    [sg.Button("Remove Tokens", enable_events=True, key="-removetokens-", font="System")],
    [
        sg.InputText("", key="-id-", size=(7, 1), font="System", text_color="gray97", background_color="gray8"),
        sg.Button("Change background", enable_events=True, key="-changebg-", font="System"),
    ],
    [sg.Button("Kill UX", enable_events=True, key="-ux-", font="System")],
    [sg.Button("Cleaner", enable_events=True, key="-cleaner-", font="System", tooltip="Works only on Windows!")],
]

layout = [
    [
        sg.TabGroup(
            [
                [sg.Tab("Reveal", reveal_tab, background_color="gray11")],
                [sg.Tab("ARAM", aram_tab, background_color="gray11")],
                [sg.Tab("Refund", refund_tab, background_color="gray11")],
                [sg.Tab("Rename", rename_tab, background_color="gray11")],
                [sg.Tab("Misc", misc_tab, background_color="gray11")],
            ],
            background_color="gray11",
            tab_background_color="gray11",
            focus_color="gray11",
            title_color="gray50",
            selected_title_color="gray97",
            selected_background_color="gray11",
        ),
    ],
    [
        sg.Stretch(background_color="gray11"),
        sg.Text(
            "https://github.com/vondyhaar/LCU-Utilities",
            enable_events=True,
            key="-repo-",
            font=("System", 12, "underline"),
            text_color="gray97",
            background_color="gray11",
        ),
        sg.Stretch(background_color="gray11"),
    ],
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
window["-name-"].widget["disabledbackground"] = "gray8"
window.BringToFront()


while True:
    event, values = window.read()
    match event:
        case "-search-":
            participants = reveal.get_names()
            reveal.search(values["-search-"])
            window["-chat-"].update(participants)
        case "-dodge-":
            if reveal.match_phase("ChampSelect"):
                event, v = sg.Window(
                    f"Confirm dodge?",
                    [
                        [
                            sg.Stretch(background_color="gray11"),
                            sg.Text("Penalties still apply!", font="System", background_color="gray11"),
                            sg.Stretch(background_color="gray11"),
                        ],
                        [
                            sg.Button("No", s=12, button_color=("gray97", "gray8"), font="System"),
                            sg.Button("Yes", s=12, button_color=("gray97", "#731a1a"), font="System"),
                        ],
                    ],
                    modal=True,
                    background_color="gray11",
                    icon="utils\\eye.ico",
                ).read(close=True)
                if event == "Yes":
                    reveal.dodge()
        case "-boost-":
            r = aram.boost()
            window["-state-"].update(r)
            if r == "Expired":
                window["-state-"].update(aram.get_jwt())
        case "-jwt-":
            window["-state-"].update(aram.get_jwt())
        case "-transactions-":
            info = transactions.get(values["-transactions-"])
            info = "{}{}\n{}{}".format(
                "WILL USE TOKEN!\n" if info["requiresToken"] else "",
                info["inventoryType"],
                info["amountSpent"],
                info["currencyType"],
            )
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
        case "-check-":
            name = values["-name-"]
            r = rename.check_name(name)
            name_info = (
                (f"{name} is available!" if r else f"{name} is either taken or unallowed!")
                if 3 <= len(name) <= 16
                else f"{name} is too long or too short."
            )
            window["-nameinfo-"].update(name_info)
            window["-change-"].update(disabled=not r)
        case "-change-":
            event, v = sg.Window(
                f"Confirm name change?",
                [
                    [
                        sg.Stretch(background_color="gray11"),
                        sg.Text(
                            ("Free of cost!" if new else "13900 BE Cost!") + " Continue?",
                            font="System",
                            background_color="gray11",
                        ),
                        sg.Stretch(background_color="gray11"),
                    ],
                    [
                        sg.Button("No", s=12, button_color=("gray97", "gray8"), font="System"),
                        sg.Button("Yes", s=12, button_color=("gray97", "#731a1a"), font="System"),
                    ],
                ],
                modal=True,
                background_color="gray11",
                icon="utils\\eye.ico",
            ).read(close=True)
            if event == "Yes":
                r = rename.change_name(name)
                window["-nameinfo-"].update(r)
        case "-removetokens-":
            misc.remove_tokens()
        case "-changebg-":
            misc.change_background(values["-id-"])
        case "-cleaner-":
            event, v = sg.Window(
                f"Confirm cleaner",
                [
                    [
                        sg.Stretch(background_color="gray11"),
                        sg.Text(
                            "This will close all League processes! Continue?", font="System", background_color="gray11"
                        ),
                        sg.Stretch(background_color="gray11"),
                    ],
                    [
                        sg.Button("No", s=12, button_color=("gray97", "gray8"), font="System"),
                        sg.Button("Yes", s=12, button_color=("gray97", "#731a1a"), font="System"),
                    ],
                ],
                modal=True,
                background_color="gray11",
                icon="utils\\eye.ico",
            ).read(close=True)
            if event == "Yes":
                misc.cleaner()
                break
        case "-snipe-":
            name = values["-name-"]
            r = rename.check_name(name)
            if r:
                event, v = sg.Window(
                    f"Name already available",
                    [
                        [
                            sg.Stretch(background_color="gray11"),
                            sg.Text(
                                ("Free of cost!" if new else "13900 BE Cost!") + " Continue?",
                                font="System",
                                background_color="gray11",
                            ),
                            sg.Stretch(background_color="gray11"),
                        ],
                        [
                            sg.Button("No", s=12, button_color=("gray97", "gray8"), font="System"),
                            sg.Button("Yes", s=12, button_color=("gray97", "#731a1a"), font="System"),
                        ],
                    ],
                    modal=True,
                    background_color="gray11",
                    icon="utils\\eye.ico",
                ).read(close=True)
                if event == "Yes":
                    r = rename.change_name(name)
                    window["-nameinfo-"].update(r)
            else:
                if not sniping:
                    sniping = True
                    rename.toggle_snipe()
                    window[event].update("Stop")
                    window["-nameinfo-"].update(f"Sniping {values['-name-']}")
                    window.perform_long_operation(lambda: rename.snipe(values["-name-"]), "-sniped-")
                else:
                    sniping = False
                    rename.toggle_snipe()
                    window[event].update("Snipe")
                window["-name-"].update(disabled=sniping)
                window["-check-"].update(disabled=sniping)
        case "-sniped-":
            window["-nameinfo-"].update(values[event])
            window["-name-"].update(disabled=False)
            window["-check-"].update(disabled=False)
            window.BringToFront()
        case "-ux-":
            if ux: # /riotclient/ux-state ?
                misc.kill_ux()
                ux = False
                window["-ux-"].update("Restore UX")
            else:
                misc.restore_ux()
                ux = True
                window["-ux-"].update("Kill UX")
        case sg.WIN_CLOSED:
            if not ux:
                misc.kill_ux()
            break
        case "-repo-":
            webbrowser.open("https://github.com/vondyhaar/LCU-Utilities")

window.close()
