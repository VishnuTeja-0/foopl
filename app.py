import tkinter as tk
from ttkbootstrap.scrolled import ScrolledText
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.icons import Emoji
from wtsapp import getGroups, getCountryCodeList

def isConnected():
    return True

def getWAGroups():
    groups, message = getGroups()
    if len(groups) == 0:
        print(message)

    return groups

def addContact():
    number = input_single_string.get()

theme_name = 'cosmo' #'superhero'
window = tb.Window(themename = theme_name)
window.resizable(width = False, height = False)
window.title('FooPL')
window.geometry('1000x600')

# Header
label_text = "Set your contacts and message to send" if isConnected() else "Login to WhatsApp using QR"
title_label = tb.Label(master = window,
                        text = label_text, 
                        font= 'Calibri 16')
title_label.pack()

if isConnected():
    # Contacts
    contact_frame = tb.Frame(master = window)
    select_contact_frame = tb.Frame(master = contact_frame)
    button_frame = tb.Frame(master = contact_frame)
    selected_contact_frame = tb.Frame(master = contact_frame)
    message_options_frame = tb.Frame(master = window)
    message_frame = tb.Frame(master = message_options_frame)
    status_frame = tb.Frame(master = message_options_frame)
    schedule_frame = tb.Frame(master = message_options_frame)
    # Select Contacts
    single_contact_frame = tb.Frame(master = select_contact_frame)
    group_contract_frame = tb.Frame(master = select_contact_frame)
    
    label_single = tb.Label(master = single_contact_frame, 
                            text = 'Enter WhatsApp number of contact', 
                            font = 'Calibri 10 bold')
    country_code_list = getCountryCodeList()
    input_country_code = tb.Combobox(master = single_contact_frame,
                                    values = country_code_list,
                                    width = 8)
    input_single_string = tk.StringVar()
    input_single = tb.Entry(master = single_contact_frame, 
                            textvariable = input_single_string,
                            width = 15)
    label_group = tb.Label(master = group_contract_frame,
                            text = 'Select WhatsApp group',
                            font = 'Calibri 10 bold') 
    group_list = tk.Variable(value = [group.name for group in getWAGroups()])
    select_group = tk.Listbox(master = group_contract_frame,
                            selectmode=tk.MULTIPLE,
                            listvariable = group_list)
    label_single.pack(fill = X, pady = 2)
    input_country_code.pack(side = LEFT, padx = 5)
    input_single.pack(side = LEFT, fill = X)
    label_group.pack(fill = X, pady = 2)
    select_group.pack(fill = X)
    single_contact_frame.pack(fill = X)
    group_contract_frame.pack(fill = X)
    select_contact_frame.pack(side = LEFT, expand = True, fill = BOTH, padx = 10)
    # Buttons
    insert_frame = tb.Frame(master = button_frame)
    remove_frame = tb.Frame(master = button_frame)
    left_1 = tb.Label(master = insert_frame, text = Emoji.get("BLACK RIGHTWARDS ARROW"), font = "Calibri 20", bootstyle = SUCCESS)
    select_contact = tb.Button(master = insert_frame, 
                            text = 'Select ' + str(Emoji.get("HEAVY PLUS SIGN")), 
                            bootstyle = SUCCESS, 
                            command = addContact)
    left_2 = tb.Label(master = insert_frame, text = Emoji.get("BLACK RIGHTWARDS ARROW"), font = "Calibri 20", bootstyle = SUCCESS)
    right_1 = tb.Label(master = remove_frame, text = Emoji.get("LEFTWARDS BLACK ARROW"), font = "Calibri 20", bootstyle = DANGER)
    remove_contact = tb.Button(master = remove_frame,
                               text = 'Remove ' + str(Emoji.get("HEAVY MINUS SIGN")),
                               bootstyle = DANGER)
    right_2 = tb.Label(master = remove_frame, text = Emoji.get("LEFTWARDS BLACK ARROW"), font = "Calibri 20", bootstyle = DANGER)
    left_1.pack(side = LEFT), select_contact.pack(pady = 10, expand = True, fill = X, side = LEFT), left_2.pack(side = LEFT)
    right_1.pack(side = LEFT), remove_contact.pack(pady = 10, expand = True, fill = X, side = LEFT), right_2.pack(side = LEFT)
    insert_frame.pack(expand = True, fill = X)
    remove_frame.pack(expand = True, fill = X)
    button_frame.pack(side = LEFT)
    # Selected Contacts
    label_selected = tb.Label(master = selected_contact_frame,
                               text = 'Selected Contacts',
                               font = 'Calibri 10 bold')
    selected_list = tk.Variable(value = ["a", "b", "c"])
    selected_group = tk.Listbox(master = selected_contact_frame,
                                selectmode=tk.MULTIPLE,
                                listvariable=selected_list)
    label_selected.pack(pady = 2)
    selected_group.pack(expand = True, fill = BOTH, padx = 10)
    selected_contact_frame.pack(side = LEFT, expand = True, fill = BOTH)

    contact_frame.pack(expand = True, fill = BOTH)

    # Message Box
    label_message = tb.Label(master = message_frame,
                              text = 'Message to be sent',
                              font = 'Calibri 10 bold')
    message = tk.StringVar()
    entry_message = ScrolledText(master = message_frame,
                                 font = 'Calibri 12',
                                 wrap = WORD,
                                 autohide = True,
                                 width = 1)
    label_message.pack(fill = X, pady = 2)
    entry_message.pack(expand = True, fill = BOTH)
    message_frame.pack(side = LEFT, expand = True, fill = BOTH, padx = (10, 2), pady = 10)
    # Schedule
    label_schedule = tb.Label(master = schedule_frame, 
                              text = 'Set Schedule',
                              font = 'Calibri 10 bold')
    time_frame = tb.Frame(master = schedule_frame)
    hour_frame = tb.Frame(master = time_frame)
    minute_frame = tb.Frame(master = time_frame)
    label_hour = tb.Label(master = hour_frame, text = 'Hours', font = 'Calibri 8')
    hour = tk.StringVar(value = "0")
    entry_hour = tb.Entry(master = hour_frame, font = 'Calibri 12', width = 5, textvariable = hour)
    label_minute = tb.Label(master = minute_frame, text = 'Minute', font = 'Calibri 8')
    minute = tk.StringVar(value = "0")
    entry_minute = tb.Entry(master = minute_frame, font = 'Calibri 12', width = 5, textvariable = minute)
    label_schedule.pack(fill = X, pady = 2)
    time_frame.pack(fill = X, pady = (0, 10))
    label_hour.pack(pady = 2)
    entry_hour.pack()
    label_minute.pack(pady = 2)
    entry_minute.pack()
    hour_frame.pack(side = LEFT, expand = True, fill = X)
    minute_frame.pack(side = LEFT, expand = True, fill = X)
    schedule_mode_options = {
        "Hours before deadline" : 1,
        "Time before deadline (24-hour clock)" : 2
    }
    mode_selected = tb.IntVar()
    for sc_key, sc_value in schedule_mode_options.items():
        tb.Radiobutton(master = schedule_frame, variable = mode_selected, text = sc_key, value = sc_value).pack(fill = X, padx = 2, pady = (5,0))
    mode_selected.set(1)
    schedule_frame.pack(side = LEFT, fill = Y, padx = 2, pady = 10)
    # Status
    labelframe_status = tb.Labelframe(master = status_frame, 
                                  bootstyle = SECONDARY, 
                                  text = "Status")
    text_status = tk.Text(master = labelframe_status,
                          relief = SUNKEN, 
                          font = 'TkFixedFont', 
                          width = 20,
                          height = 1)
    button_save = tb.Button(master = labelframe_status, 
                            text = 'Save Changes', 
                            bootstyle = LIGHT,
                            state = DISABLED)
    button_discard = tb.Button(master = labelframe_status,
                               text = 'Discard Changes',
                               bootstyle = WARNING,
                               state = DISABLED) 
    labelframe_status.pack(expand = True, fill = BOTH)
    text_status.pack(expand = True, fill = BOTH, padx = 2, pady = 2)
    button_save.pack(fill = X)
    button_discard.pack(fill = X)
    status_frame.pack(side = LEFT, fill = Y, padx = (2, 10), pady = 10)

    message_options_frame.pack(expand = True, fill = BOTH)

else:
    print("wow")

window.mainloop()