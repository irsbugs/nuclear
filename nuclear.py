#!/usr/bin/env python3
#!
# nuclear.py
#
# load a csv file based on the UN voting on
# Draft treaty on the prohibition of nuclear weapons
# Original documents...
# https://s3.amazonaws.com/unoda-web/wp-content/uploads/2017/07/A.Conf_.229.2017.L.3.Rev_.1.pdf
#
# Display the voting with radio button filtering.
#
# Dependency:
# The file UN Nuclear Ban Treaty.csv must be in the current working directory.
import sys
import os
from gi import require_version
require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Pango, Gdk, GObject
import subprocess
import time

# Instantiation 
loop = Gtk.main

# Variables/constants
TITLE = "Draft Treaty on the Prohibition of Nuclear Weapons"
HELP_FILE = "help_client.md"
HELP_FILE_FULL = "help_client_full.md"
PROJECTOR = True
PROJECTOR_FONT = "FreeSans, 15"

# csv file of voting results, etc.
csv_file = "UN Nuclear Ban Treaty.csv"

# Column headings for the csv file.
Headings = ["Not Part",	"Participated",	"For", "Against", "Abstain", "Perm SC",	
"N NTP", "N Weapon", "N Share",	"Nato",	"UN State",	"UN Observer",	
"UN African", "UN Asia-Pac", "UN East E", "Latin A Caribbean", "W.Euro", 
"Other", "None"]

# Frame 1 for 
FRAME_1 = "Select United Nations Voting and Participation"
F1_RADIOBUTTON_1 = "United Nation member and observer states"
F1_RADIOBUTTON_2 = "Voted For Treaty"
F1_RADIOBUTTON_3 = "Voted Against Treaty"
F1_RADIOBUTTON_4 = "Abstained from Voting"
F1_RADIOBUTTON_5 = "Did not participate"

# Frame 2 for filtering
FRAME_2 = "Frame 2"
F2_RADIOBUTTON_1 = "All"
F2_RADIOBUTTON_2 = "Permanent Member of the United Nations Security Council"
F2_RADIOBUTTON_3 = "Non NTP"
F2_RADIOBUTTON_4 = "Nuclear Weapon State"
F2_RADIOBUTTON_5 = "Nuclear Weapon Share State"
F2_RADIOBUTTON_6 = "NATO Member"

# Frame 3 for Scrolled Text box
FRAME_3 = "United Nation States"

def read_csv_file_to_list():
    """
    Read the csv file and place into a list of lists.
    """
    data_list = []
    directory = os.getcwd()
    #print(directory)
    with open(directory + os.sep + csv_file, "r") as f:
        my_file = f.readlines()
        for line in my_file:
            #print(line)
            data = line.split(",")
            data_list.append(data)
            #for item in data:
            #    print(item)   
    return data_list

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title=TITLE, name="ClientWindow")
        self.set_default_size(600, 100)
        style_provider = Gtk.CssProvider()
        css = "#ClientWindow{background-color: #ccffcc;}" 
        style_provider.load_from_data(bytes(css.encode()))
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        # Modify the overall font name and size, for use with video projection.
        if PROJECTOR:  
            pangoFont = Pango.FontDescription(PROJECTOR_FONT)
            self.modify_font(pangoFont)

        # call function to read the data to a list of lists.
        self.data = read_csv_file_to_list() 
        #print(self.data)       

        # Setup GUI Window
        grid_main = Gtk.Grid()
        self.add(grid_main)

        self.label_1 = Gtk.Label(margin=10)
        grid_main.attach(self.label_1, 0, 0, 1, 1,)

        # Create Frame_1
        frame_1 = Gtk.Frame(margin=10)
        frame_1.set_label(FRAME_1)
        grid_main.attach(frame_1, 0 , 0, 1, 1)
        grid_sub_1 = Gtk.Grid()
        frame_1.add(grid_sub_1)

        # Radio Button Set for Frame 1
        self.f1_radio_button_1 = Gtk.RadioButton.new_from_widget(None)
        self.f1_radio_button_1.set_label(F1_RADIOBUTTON_1)
        self.f1_radio_button_1.connect("toggled", self.f1_radio_button_set_1_cb, "1")
        self.f1_radio_button_1.set_margin_left(10)
        grid_sub_1.attach(self.f1_radio_button_1, 0, 1, 1, 1,) 

        self.f1_radio_button_2 = Gtk.RadioButton.new_from_widget(self.f1_radio_button_1)
        self.f1_radio_button_2.set_label(F1_RADIOBUTTON_2)
        self.f1_radio_button_2.connect("toggled", self.f1_radio_button_set_1_cb, "2")
        self.f1_radio_button_2.set_margin_left(10)
        grid_sub_1.attach(self.f1_radio_button_2, 0, 2, 1, 1,)

        self.f1_radio_button_3 = Gtk.RadioButton.new_from_widget(self.f1_radio_button_1)
        self.f1_radio_button_3.set_label(F1_RADIOBUTTON_3)
        self.f1_radio_button_3.connect("toggled", self.f1_radio_button_set_1_cb, "3")
        self.f1_radio_button_3.set_margin_left(10)
        grid_sub_1.attach(self.f1_radio_button_3, 0, 3, 1, 1,)

        self.f1_radio_button_4 = Gtk.RadioButton.new_from_widget(self.f1_radio_button_1)
        self.f1_radio_button_4.set_label(F1_RADIOBUTTON_4)
        self.f1_radio_button_4.connect("toggled", self.f1_radio_button_set_1_cb, "4")
        self.f1_radio_button_4.set_margin_left(10)
        grid_sub_1.attach(self.f1_radio_button_4, 0, 4, 1, 1,)
 
        self.f1_radio_button_5 = Gtk.RadioButton.new_from_widget(self.f1_radio_button_1)
        self.f1_radio_button_5.set_label(F1_RADIOBUTTON_5)
        self.f1_radio_button_5.connect("toggled", self.f1_radio_button_set_1_cb, "5")
        self.f1_radio_button_5.set_margin_left(10)
        grid_sub_1.attach(self.f1_radio_button_5, 0, 5, 1, 1,)

        """
        # Create Frame_2
        frame_2 = Gtk.Frame(margin=10)
        frame_2.set_label(FRAME_2)
        grid_main.attach(frame_2, 0 , 1, 1, 1)
        grid_sub_1 = Gtk.Grid()
        frame_2.add(grid_sub_1)

        # Radio Button Set for Frame 2
        #self.radio_button_1 = Gtk.RadioButton.new_with_label_from_widget(
        #                      None, "Button 1")
        self.f2_radio_button_1 = Gtk.RadioButton.new_from_widget(None)
        self.f2_radio_button_1.set_label(F2_RADIOBUTTON_1)
        self.f2_radio_button_1.connect("toggled", self.f2_radio_button_set_1_cb, "1")
        self.f2_radio_button_1.set_margin_left(10)
        grid_sub_1.attach(self.f2_radio_button_1, 0, 1, 1, 1,) 

        self.f2_radio_button_2 = Gtk.RadioButton.new_from_widget(self.f2_radio_button_1)
        self.f2_radio_button_2.set_label(F2_RADIOBUTTON_2)
        self.f2_radio_button_2.connect("toggled", self.f2_radio_button_set_1_cb, "2")
        self.f2_radio_button_2.set_margin_left(10)
        grid_sub_1.attach(self.f2_radio_button_2, 0, 2, 1, 1,)

        self.f2_radio_button_3 = Gtk.RadioButton.new_from_widget(self.f2_radio_button_1)
        self.f2_radio_button_3.set_label(F2_RADIOBUTTON_3)
        self.f2_radio_button_3.connect("toggled", self.f2_radio_button_set_1_cb, "3")
        self.f2_radio_button_3.set_margin_left(10)
        grid_sub_1.attach(self.f2_radio_button_3, 0, 3, 1, 1,)

        # kick start
        self.f2_radio_button_1.set_active(True)
        """
        
        # Create Frame_3
        frame_3 = Gtk.Frame(margin=10)
        frame_3.set_label(FRAME_3)
        grid_main.attach(frame_3, 0, 5, 1, 1)
        grid_sub_1 = Gtk.Grid()
        frame_3.add(grid_sub_1)

        # Add two labels to display the totals.
        self.label_1 = Gtk.Label(margin=10)
        self.label_1.set_text("Total")
        grid_sub_1.attach(self.label_1, 0, 0, 1, 1,)

        self.label_2 = Gtk.Label(margin=10)
        grid_sub_1.attach(self.label_2, 1, 0, 1, 1,)
        self.label_2.set_text("")

        # Scrolled window to disploay the countries.
        self.scrolledwindow = Gtk.ScrolledWindow(margin=10)
        self.scrolledwindow.set_hexpand(True)
        self.scrolledwindow.set_vexpand(True)
        grid_sub_1.attach(self.scrolledwindow, 0, 2, 2, 1)

        self.textview = Gtk.TextView()
        #  dir(Gtk.WrapMode) ['CHAR', 'NONE', 'WORD', 'WORD_CHAR'
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD)  # set_wrap_mode
        self.scrolledwindow.set_size_request(200,300)  # OK

        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text("") 
        self.scrolledwindow.add(self.textview)

        self.tag_bold = self.textbuffer.create_tag("bold",
            weight=Pango.Weight.BOLD)
        self.tag_italic = self.textbuffer.create_tag("italic",
            style=Pango.Style.ITALIC)
        self.tag_underline = self.textbuffer.create_tag("underline",
            underline=Pango.Underline.SINGLE)
        self.tag_found = self.textbuffer.create_tag("found",
            background="yellow")

       # kick start
        self.f1_radio_button_2.set_active(True)
        self.f1_radio_button_1.set_active(True)

    # ===== Frame #1 radio buttons.
    def f1_radio_button_set_1_cb(self, button, name):
        "Determine which button was clicked"
        if button.get_active():
            state = "on"
            if name == "1":
                self.f1_button_1()
            if name == "2":
                self.f1_button_2()
            if name == "3":
                self.f1_button_3()
            if name == "4":
                self.f1_button_4()
            if name == "5":
                self.f1_button_5()
        else:
            state = "off"
        #print("Button", name, "was turned", state)
        

    def f1_button_1(self):
        "List of all UN states"
        #print("F1_Button_1")
        s = ""
        count = 0
        for state in self.data:
            s += state[18] + "\n"
            count +=1
        self.label_2.set_text(str(count))
        self.textbuffer.set_text(s)
        
    def f1_button_2(self):
        "List of all UN Voted Yes"
        #print("F1_Button_2")
        s = ""
        count = 0
        for state in self.data:
            if state[1] == "1":
                s += state[18] + "\n"
                count +=1
        self.label_2.set_text(str(count))
        self.textbuffer.set_text(s)


    def f1_button_3(self):
        "List of all UN Voted No"
        #print("F1_Button_3")
        s = ""
        count = 0
        for state in self.data:
            if state[3] == "1":
                s += state[18] + "\n"
                count +=1
        self.label_2.set_text(str(count))
        self.textbuffer.set_text(s)

    def f1_button_4(self):
        "List of all UN Abstained."
        #print("F1_Button_4")
        s = ""
        count = 0
        for state in self.data:
            if state[4] == "1":
                s += state[18] + "\n"
                count +=1
        self.label_2.set_text(str(count))
        self.textbuffer.set_text(s)

    def f1_button_5(self):
        "List of all UN Did not participate."
        #print("F1_Button_5")
        s = ""
        count = 0
        for state in self.data:
            if state[0] == "1":
                s += state[18] + "\n"
                count +=1
        self.label_2.set_text(str(count))
        self.textbuffer.set_text(s)

    # ===== Frame #2 set of buttons for filtering. Not implemented.
    def f2_radio_button_set_1_cb(self, button, name):
        if button.get_active():
            state = "on"
            if name == "1":
                self.f2_button_1()
            if name == "2":
                self.f2_button_2()
            if name == "3":
                self.f2_button_3()
        else:
            state = "off"
        #print("Button", name, "was turned", state)

    def f2_button_1(self):
        print("F2_Button_1")
    def f2_button_2(self):
        print("F2_Button_2")
    def f2_button_3(self):
        print("F2_Button_3")


if __name__=="__main__":
    # Startup
    # Check python is at 3.5 of higher. Prerequisite for subprocess.run()
    if float(sys.version[0:3]) <  3.5:
        sys.exit("Requires Python 3.5 or higher. Exiting...")1

    #print("Starting Client.")
    #print("Start with -h for brief help, or --help for full help information\n")
    # Invoke sys.argv arguments 
    # Flags: -h or --help
    for item in sys.argv:
        #flags:
        if "-h" in item[0:3]:
            if len(item) < 3 : 
                try:
                    with open(HELP_FILE, "r") as f:
                        for line in f.readlines():
                            print(line.rstrip('\n'))
                except FileNotFoundError as e:
                    print("Help file {} not found".format(HELP_FILE))
                sys.exit("Exiting...")
            else:
                try:
                    with open(HELP_FILE_FULL, "r") as f:
                        for line in f.readlines():
                            print(line.rstrip('\n'))
                except FileNotFoundError as e:
                    print("Help file {} not found".format(HELP_FILE_FULL))
                sys.exit("Exiting...")
            
    print("Launching GUI")

    # Launch Client GUI application.
    win = MainWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    loop()


"""
Notes / Links:

Press release
http://www.un.org/apps/news/story.asp?NewsID=57139#.WXw1pCexXfQ

http://www.ipb.org/news/nuclear-weapons-ban-treaty-adopted/

The text of the treaty is available here: http://www.undocs.org/en/a/conf.229/2017/L.3/Rev.1

The conference may be followed on the conference website: https://www.un.org/disarmament/ptnw/

Voting Results: https://s3.amazonaws.com/unoda-web/wp-content/uploads/2017/07/A.Conf_.229.2017.L.3.Rev_.1.pdf

Final Text
http://undocs.org/A/CONF.229/2017/8

Nato
http://www.icanw.org/
http://www.icanw.org/treaty-on-the-prohibition-of-nuclear-weapons/
http://www.icanw.org/campaign-news/us-pressures-nato-states-to-vote-no-to-the-ban-treaty/
http://www.icanw.org/wp-content/uploads/2016/10/NATO_OCT2016.pdf


One hundred and thirty-five (135) nations participated in the negotiations, according to official records:

Afghanistan, Algeria, Andorra, Angola, Antigua & Barbuda, Argentina, Armenia, Austria, Azerbaijan, Bahamas, Bahrain, Bangladesh, Barbados, Belize, Benin, Bhutan, Bolivia, Botswana, Brazil, Brunei, Burkina Faso, Burundi, Cabo Verde, Cambodia, Cameroon, Chad, Chile, Colombia, Congo, Costa Rica, Côte d’Ivoire, Cuba, Cyprus, Djibouti, Dominican Republic, DRC (Congo), Ecuador, Egypt, El Salvador, Equatorial Guinea, Eritrea, Ethiopia, Fiji, Gambia, Ghana, Grenada, Guatemala, Guinea, Guyana, Haiti, Holy See, Honduras, Indonesia, Iran, Iraq, Ireland, Jamaica, Jordan, Kazakhstan, Kenya, Kiribati, Kuwait, Laos, Lebanon, Lesotho, Liberia, Libya, Liechtenstein, Macedonia, Madagascar, Malawi, Malaysia, Malta, Marshall Islands, Mauritania, Mauritius, Mexico, Moldova, Monaco, Mongolia, Morocco, Mozambique, Myanmar, Namibia, Nauru, Nepal, Netherlands, New Zealand, Nicaragua, Nigeria, Oman, Palau, Palestine, Panama, Papua New Guinea, Paraguay, Peru, Philippines, Qatar, Saint Kitts & Nevis, Saint Lucia, Saint Vincent & the Grenadines, Samoa, San Marino, São Tomé & Principe, Saudi Arabia, Senegal, Seychelles, Sierra Leone, Singapore, Solomon Islands, South Africa, Sri Lanka, Sudan, Suriname, Swaziland, Sweden, Switzerland, Syria, Tanzania, Thailand, Timor-Leste, Togo, Tonga, Trinidad & Tobago, Tunisia, Uganda, United Arab Emirates, Uruguay, Vanuatu, Venezuela, Vietnam, Yemen, Zambia, Zimbabwe.

In addition, several nations participated informally. Their officials were never accredited, but they did attend parts of the negotiations. According to ICAN’s records, these nations included:

Central African Republic, Comoros, Dominica, Gabon, Guinea-Bissau, Japan, Kyrgyzstan, Maldives, Mali, Niger, Somalia, South Sudan, Tajikistan, Uzbekistan.


"""
