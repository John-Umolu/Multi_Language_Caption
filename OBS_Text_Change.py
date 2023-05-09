from tkinter import *
import googletrans
from googletrans import Translator
translator = Translator()

count = 0
max_index = 0
n = 60

# Set check box default value
add_english = 0
add_scroll = 0

# get translator language values and keys
language_list_values = list(googletrans.LANGUAGES.values())
language_list_keys = list(googletrans.LANGUAGES.keys())

# Set the default language
language = language_list_keys[0]

# create the tkinter dialogue
root = Tk()
root.resizable(False, False)
root.title("OBS Multilanguage Subtitle Developed By Umolu John Chukwuemeka")


# function to translate and update new text
def update_obs(get_text):
    # Get the translation
    translation = translator.translate(get_text, src='en', dest=language).text
    with open("obs_subtitles.txt", "w", encoding='utf-8') as text_file:
        if add_english == 1 and add_scroll == 0:
            text_file.write(get_text.strip() + '\n\n' + str(translation).strip())
        elif add_english == 0 and add_scroll == 1:
            text_file.write("<< " + str(translation).strip() + " >>     ")
        elif add_english == 1 and add_scroll == 1:
            text_file.write("<< " + get_text.strip() + ' | ' + str(translation).strip() + " >>     ")
        else:
            text_file.write(str(translation).strip())

    # Update preview text
    prev_text.configure(state='normal')
    prev_text.delete("1.0", "end")  # remove the old data
    prev_text.insert('end',
                     'Current Position: Line ' + str((count - 1) + 1) + '\nLanguage In Use: ' +
                     language_list_values[language_list_keys.index(language)] +
                     '\nText In Use:\n' + get_text.strip())
    prev_text.configure(state='disabled')
    # display output on console
    print(f'Current Position: Line {(count - 1) + 1}', '\nLanguage In Use: ' +
          language_list_values[language_list_keys.index(language)] +
          '\nText In Use:\n' + get_text.strip())
    return


def prev_button():
    global count, language, n

    all_text = text.get("1.0", 'end-1c')

    if len(all_text) == 0:
        print("Please Enter Main Text")
        return

    if '\n' in all_text:
        all_text = all_text.replace('\n', '$')

    rows_to_print = []
    prev_item = ''

    all_text = all_text.split('$')

    for item in range(len(all_text)):
        if len(all_text[item]) == 0 and len(prev_item) > 0:
            rows_to_print.append('#')
        elif len(all_text[item]) > 0:
            rows_to_print.append('$' + all_text[item])
        prev_item = all_text[item]

    if '#' in rows_to_print:
        rows_to_print = ''.join(rows_to_print)
        rows_to_print = rows_to_print.split('#')

    count = count - 1
    if count <= 0:
        count = 1

    if count >= 1:
        get_text = rows_to_print[count - 1]
        if get_text[0] == '$':
            get_text = get_text[1:]
            if '$' in get_text:
                get_text = get_text.replace('$', '\n')
        if not '\n' in get_text:
            get_text = [get_text[i:i + n] for i in range(0, len(get_text), n)]
            get_text = '\n'.join(get_text)

        update_obs(get_text)
    return


def next_button():
    global count, language, n

    all_text = text.get("1.0", 'end-1c')

    if len(all_text) == 0:
        print("Please Enter Main Text")
        return

    if '\n' in all_text:
        all_text = all_text.replace('\n', '$')

    rows_to_print = []
    prev_item = ''

    all_text = all_text.split('$')

    for item in range(len(all_text)):
        if len(all_text[item]) == 0 and len(prev_item) > 0:
            rows_to_print.append('#')
        elif len(all_text[item]) > 0:
            rows_to_print.append('$' + all_text[item])
        prev_item = all_text[item]

    if '#' in rows_to_print:
        rows_to_print = ''.join(rows_to_print)
        rows_to_print = rows_to_print.split('#')

    if max_index != 0 and count >= max_index:
        count = max_index

    count = count + 1
    if count > len(rows_to_print):
        count = len(rows_to_print)

    if count < len(rows_to_print) + 1:
        get_text = rows_to_print[count - 1]
        if get_text[0] == '$':
            get_text = get_text[1:]
            if '$' in get_text:
                get_text = get_text.replace('$', '\n')
        if not '\n' in get_text:
            get_text = [get_text[i:i + n] for i in range(0, len(get_text), n)]
            get_text = '\n'.join(get_text)

        update_obs(get_text)
    return


# datatype of menu text
clicked = StringVar()
mystr = StringVar()
var1 = IntVar()
var2 = IntVar()
# initial menu text
clicked.set(language_list_values[0])


# Functions to get selected language and check box values
def callback(selection):
    global language
    language = language_list_keys[language_list_values.index(selection)]


def display_input():
    global add_english
    add_english = var1.get()


def scroll_input():
    global add_scroll
    add_scroll = var2.get()


# https://stackoverflow.com/questions/66512222/how-do-i-enable-right-click-in-entry-and-output-widget-for-pasting-and-copying-r
# Enable Copy and Paste
def popup(event):
    try:
        menu.tk_popup(event.x_root, event.y_root)  # Pop the menu up in the given coordinates
    finally:
        menu.grab_release()  # Release it once an option is selected


# insert button function
def callback2(button_text):
    global count
    # get the selected button text and split it
    input_text = str(button_text).strip(':')
    # get the index value
    count = int(input_text[0]) + 1
    # remove the attached index value
    new_text = input_text.replace(input_text[0] + ':', '')
    # update new text value
    update_obs(new_text)


def paste():
    global max_index, count

    # reset the line value to 0
    count = 0

    # Get the copied item from system clipboard
    clipboard = root.clipboard_get()

    # display OpenAI response message
    for i, item in enumerate(str(clipboard).split('\n\n')):
        max_index = i
        item = str(i) + ':' + item
        text.insert(END, item.replace(str(i) + ':', '') + "\t\n")
        button = Button(text, text=f"Line {i + 1}", padx=2, pady=2,
                        cursor="left_ptr",
                        bd=1, highlightthickness=0,
                        command=lambda text=item: callback2(text), fg="black", bg="gainsboro", font=('Times', 12))
        text.window_create("end-2c", window=button)
        # output a newline
        text.insert(END, '\n', "left")


def copy():
    inp = text.get("1.0", 'end-1c')  # Get the text inside entry widget
    root.clipboard_clear()  # Clear the tkinter clipboard
    root.clipboard_append(inp)  # Append to system clipboard


menu = Menu(root, tearoff=0)  # Create a menu
menu.add_command(label='Copy', command=copy)  # Create labels and commands
menu.add_command(label='Paste', command=paste)

####################################################################################
# Create Buttons
b = Button(root, text="Prev Subtitle", command=prev_button, fg="black", bg="gainsboro", font=('Times', 12))
c = Button(root, text="Next Subtitle", command=next_button, fg="black", bg="gainsboro", font=('Times', 12))
# Create Checkboxes
t1 = Checkbutton(root, text="Add English Subtitle", variable=var1, onvalue=1, offvalue=0, command=display_input,
                 fg="black", bg="gainsboro", font=('Times', 12))
t2 = Checkbutton(root, text="Scroll Message", variable=var2, onvalue=1, offvalue=0, command=scroll_input,
                 fg="black", bg="gainsboro", font=('Times', 12))
# Create Dropdown menu
drop = OptionMenu(root, clicked, *language_list_values, command=callback)
drop.config(width=20, fg="black", bg="gainsboro", font=('Times', 12))
# Create Labels
main_label = Label(root, text="Enter Main Text Here", font=('Helvetica bold', 14), fg="brown")
prev_label = Label(root, text="Output Text Preview", font=('Helvetica bold', 14), fg="brown")

b.grid(row=0, column=0, padx=10, pady=5, sticky=W)
t1.grid(row=0, column=1, padx=10, pady=5, sticky=W)
t2.grid(row=0, column=2, padx=10, pady=5, sticky=W)
drop.grid(row=0, column=3, padx=10, pady=5, sticky=W)
c.grid(row=0, column=4, padx=10, pady=5, sticky=W)
main_label.grid(in_=root, row=1, column=0, columnspan=5, padx=5, pady=5, sticky=NSEW)
prev_label.grid(in_=root, row=3, column=0, columnspan=5, padx=5, pady=5, sticky=NSEW)

# Create frame
textframe = Frame(root)
textframe.grid(in_=root, row=2, column=0, columnspan=5, padx=5, pady=5, sticky=NSEW)
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
# Create main text box
text = Text(root, width=30, height=25)
scrollbar = Scrollbar(root)
scrollbar.config(command=text.yview)
text.config(yscrollcommand=scrollbar.set)
scrollbar.pack(in_=textframe, side=RIGHT, fill=Y)
text.pack(in_=textframe, side=LEFT, fill=BOTH, expand=True)
text.bind('<Button-3>', popup)  # Bind a func to right-click

# Create frame
textframe2 = Frame(root)
textframe2.grid(in_=root, row=4, column=0, columnspan=5, padx=5, pady=5, sticky=NSEW)
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
# Create preview text box
prev_text = Text(root, width=30, height=10, bg="light cyan")
prev_scrollbar = Scrollbar(root)
prev_scrollbar.config(command=prev_text.yview)
prev_text.config(yscrollcommand=prev_scrollbar.set)
prev_scrollbar.pack(in_=textframe2, side=RIGHT, fill=Y)
prev_text.pack(in_=textframe2, side=LEFT, fill=BOTH, expand=True)

root.mainloop()
