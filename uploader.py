# %%
import download_library as dlb  # Propietary libary
import os
import datetime
import threading
import tkinter
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt

# TODO: Change the "parser.add_argument('-d', '--destination', type=str, help='name for destination folder/study')" destination parameter
#       and make it NOT get the destination argument from the user when they run the code, but when typing it in the GUI.
# TODO: End of of the implementation in "FIRST" and "SECOND" todo, starting at line 298
# ------------------------------- CONSTANTS ---------------------------------- #
BACKGROUND_C = "#D3E0EA"
# FONT_NAME = "Courier"
FONT_NAME = "Impact"
TIMER_INIT = None
DETAILS_OUTPUT = []
THREAD_LIST = []
DIR_PATH = ""
# ------------------------------- CONSTANTS ---------------------------------- #

FILES_DONE = []
UPLOADED = 0  # This is the total uploaded files by all the threads.
PATIENT_NAME = ""


# ------------------------------ DETAILS WINDOW --------------------------------- #
def details_window():
    if len(DETAILS_OUTPUT) > 0:
        window2 = tkinter.Toplevel()
        window2.title("Detailed output")
        window2.config(padx=50, pady=50, bg=BACKGROUND_C)

        # Canvas:
        canvas2 = tkinter.Canvas(window2, width=800, height=526, bg=BACKGROUND_C, highlightthickness=0)

        # Text box:
        text_box = tkinter.Text(window2, height=25, width=80)
        # == Words into 1 string ==
        string_output = ""
        for item in DETAILS_OUTPUT:
            string_output += item
        # == Words into 1 string ==
        text_box.insert("end", string_output)

        # Adding it all to the new window:
        canvas2.grid(row=0, column=0)
        text_box.grid(row=0, column=0)

        window2.mainloop()
    else:
        messagebox.showerror(title="Nothing uploaded yet",
                             message="You need to give the threads time to upload.")

# ------------------------------ DETAILS WINDOW --------------------------------- #


# ----------------------------- DONUT CHART -----------------------------
def donut_chart(num_threads=10):
    # create data
    colors_hex = ["#FFD460",
                  "#F07B3F",
                  "#EA5455",
                  "#2D4059",
                  "#5D9C59",
                  "#ABEDD8",
                  "#46CDCF",
                  "#3D84A8",
                  "#48466D",
                  "#804674",
                  "white"]

    graph_label = ["T1",
                   "T2",
                   "T3",
                   "T4",
                   "T5",
                   "T6",
                   "T7",
                   "T8",
                   "T9",
                   "T10",
                   ""]

    separator_distance = [0.1,
                          0.1,
                          0.1,
                          0.1,
                          0.1,
                          0.1,
                          0.1,
                          0.1,
                          0.1,
                          0.1,
                          0.1]

    # With this, the user will be able to decide the number of threads,
    # and the graph will adjust accordingly.
    thread_dict = {}
    for item in range(num_threads):
        thread_dict[item + 1] = {"colors_hex": colors_hex[0:item + 1],
                                 "graph_label": graph_label[0:item + 1],
                                 "separator_distance": separator_distance[0:item + 1]}

        thread_dict[item + 1]["colors_hex"].append(colors_hex[-1])
        thread_dict[item + 1]["graph_label"].append(graph_label[-1])
        thread_dict[item + 1]["separator_distance"].append(separator_distance[-1])

    # Create a pieplot
    plt.figure(figsize=[4, 4])

    # If autopct is not None, return the tuple (patches, texts,
    # autotexts), where patches and texts are as above, and
    # autotexts is a list of Text instances for the numeric labels.
    patches, text, autotexts = plt.pie(THREAD_LIST,
                                       radius=1.25,
                                       counterclock=False,
                                       colors=thread_dict[num_threads]["colors_hex"],
                                       textprops={"fontsize": 10,
                                                  "weight": "bold"},
                                       wedgeprops={"linewidth": 1,
                                                   "edgecolor": "#276678"},
                                       explode=thread_dict[num_threads]["separator_distance"],
                                       labels=thread_dict[num_threads]["graph_label"],
                                       pctdistance=0.8,
                                       autopct="%.1f%%")
    for autotext in autotexts:
        autotext.set_color("white")

    # add a circle at the center to transform it in a donut chart
    my_circle = plt.Circle((0, 0), 0.85, color="white")
    fig = plt.gcf()  # This variable is a non-GUI backend, and can be used for anything related to the generated graph.
    fig.gca().add_artist(my_circle)

    # plt.show()
    fig.savefig("graph.png", bbox_inches="tight", transparent=True)
    # time.sleep(4)
# ----------------------------- DONUT CHART -----------------------------


# ------------------------------- GRAPH UI SETUP ---------------------------------- #
def graph_gui():

    def run_spider():
        for threads in range(1, thread_value.get() + 1):
            threading.Thread(target=spider, args=[threads, DIR_PATH]).start()

    # ---------------------------- SPIDER ----------------------------
    def spider(thread_number, root_dir):
        global THREAD_LIST
        global UPLOADED

        # Get the cloud client:
        cloud = dlb.Proprietary_Class  # This is an instance of the class "PRIVATE" from "download_library" module. (proprietary)

        # Get your project of interest:
        project = cloud.proprietary_method('Private')
        print('Project name: ', project.name)

        # Get your institute of interest:
        institute = project.proprietary_method('Private')
        print('Institute name: ', institute.name)

        # Cloud
        patient = institute.proprietary_method(PATIENT_NAME)
        files_in_cloud = patient.proprietary_method()

        date_start = datetime.datetime.now().strftime("%b-%d-%Y")
        print('******************************************')
        print(f'Uploading {os.path.split(DIR_PATH)[1].upper()} images')
        print(f"Starting: {date_start}")
        print('******************************************')

        counter = 0
        total_f_size = 0
        for root, dirs, files in os.walk(root_dir):
            for item in files:
                if item not in files_in_cloud and item not in FILES_DONE:
                    counter += 1
                    FILES_DONE.append(item)
                    file_root = os.path.join(root, item)
                    file_size = os.path.getsize(file_root)
                    total_f_size += file_size
                    time_start = datetime.datetime.now().strftime("%H:%M:%S")

                    print(f" Tag starting: {os.path.splitext(file_root)[0][-5:]}")
                    patient.upload_file(file_root)

                    if len(str(file_size)) < 10:
                        file_print = f"F.Size: {file_size/1000000:.1f} Megabytes"
                    else:
                        file_print = f"F.Size: {file_size/1000000000:.3f} Gigabytes"

                    if len(str(total_f_size)) < 10:
                        total_print = f"Total uploaded: {total_f_size/1000000:.1f} Megabytes"
                    else:
                        total_print = f"Total uploaded: {total_f_size/1000000000:.3f} Gigabytes"

                    time_end = datetime.datetime.now().strftime("%H:%M:%S")

                    UPLOADED += counter
                    THREAD_LIST[thread_number], THREAD_LIST[-1] = counter, len(files) - UPLOADED  # Updates the specific thread file-upload-count, and the total number of files in the directory

                    donut_chart(len(THREAD_LIST) - 1)

                    canvas.itemconfig(canvas_image, image=tkinter.PhotoImage(file="graph.png"))  # It needs to be updated with new graph values.
                    canvas.itemconfig(leftover_files_text, text=f"{THREAD_LIST[-1]}% \n left", fill=BACKGROUND_C)

                    files_in_cloud = patient.list_files()
                    print(f"Thread #{thread_number}"
                          f" U.Start Time: {time_start} |"
                          f" U.End Time: {time_end} |"
                          f" Uploading dir_2 file {counter} of T.Local:{len(files)} & T.Cloud:{len(files_in_cloud)} |"
                          f" tag: {os.path.splitext(file_root)[0][-5:]} |"
                          f" {file_print} |"
                          f" {total_print}\n"
                          f" {files_in_cloud}/{len(files)}\n\n")

        date_end = datetime.datetime.now().strftime("%b-%d-%Y")
        print('******************************************')
        print('Upload Finished.')
        print(f"Thread #{thread_number}")
        print(f"Started: {date_start}")
        print(f"Ending: {date_end}")
        print('******************************************')
    # ---------------------------- SPIDER ----------------------------

    def test(check_thread_num="default", counter=0):
        '''
        This function is used to test the overwrite of the 'THREAD_LIST' global variable, graphing the Donut chart,
        and checking the output on the main screen.

        The overwites works as:
        From the default [0,0,0,0] to new values depending on the uploads done by the different threads
        (Or user defined values in this simulation). Then creating a graph out of them, saving the graph, and
        outputing it to the main window.
        '''
        import random

        global THREAD_LIST

        if check_thread_num == "default":  # This will output 10 threads, with its donut chart's division by default.
            num_threads = thread_value.get()
            THREAD_LIST = [1 for threads in range(num_threads + 1)]  # You cannot have a list of 0 -> [0,0,0,0]. Ortherwise, the graphing will crash the program. Therefore, overwrite the list [0,0,0,0] -> [1,1,1,1].

            donut_chart(len(THREAD_LIST) - 1)

            graph_img = tkinter.PhotoImage(file="graph.png")

            canvas.itemconfig(canvas_image, image=graph_img)  # It needs to be updated with new graph values.
            canvas.itemconfig(leftover_files_text, text=f"{THREAD_LIST[-1]}% \n left", fill=BACKGROUND_C)
        elif isinstance(check_thread_num, int) and counter > 0:  # Start looping if you see a number.
            THREAD_LIST = [random.randint(1, 30) for threads in range(check_thread_num + 1)]  # Create a list of 0, where the total number is the total threads + the last index: total files.

            donut_chart(len(THREAD_LIST) - 1)

            graph_img = tkinter.PhotoImage(file="graph.png")

            canvas.itemconfig(canvas_image, image=graph_img)  # It needs to be updated with new graph values.
            canvas.itemconfig(leftover_files_text, text=f"{THREAD_LIST[-1]}% \n left", fill=BACKGROUND_C)

            window_graph.after(1500, test, check_thread_num, counter - 1)
        elif isinstance(check_thread_num, int) and check_thread_num <= 0 or counter <= 0:  # The loop finished running.
            return
        else:
            messagebox.showerror(title="Wrong argument", message="Try using the default value for 'test()', or an integer.")

    window_info.destroy()

    window_graph = tkinter.Tk()
    window_graph.title("Octo-grabber")
    window_graph.config(padx=50, pady=50, bg=BACKGROUND_C)

    # Graph:
    canvas = tkinter.Canvas(window_graph, width=392, height=390, bg=BACKGROUND_C, highlightthickness=0)
    graph_img = tkinter.PhotoImage(file="")
    canvas_image = canvas.create_image(196, 195, image=graph_img)
    leftover_files_text = canvas.create_text(200, 205, text="", fill="#7D5A5A", font=(FONT_NAME, 35, "bold"))
    canvas.grid(column=0, row=1)

    # Label: Cloud pusher
    timer = tkinter.Label(window_graph, text="Cloud pusher", bg=BACKGROUND_C, fg="#1687A7", font=(FONT_NAME, 40, "bold"), highlightthickness=0)
    timer.grid(column=0, row=0)

    # Button: Details
    spacer = tkinter.Label(window_graph, text="", bg=BACKGROUND_C, highlightthickness=0)
    button1 = tkinter.Button(window_graph, text="Details", highlightthickness=0, command=details_window)
    spacer.grid(column=0, row=2)
    button1.grid(column=0, row=3)

    window_graph.after(100, run_spider)
    # # ------------- TESTS -------------
    # # Run test when you don't want to upload any files, but still want to check integrity of the code.
    # window_graph.after(1000, test, 4, 4)
    # window_graph.after(1000, test)
    # window_graph.after(1000, test, thread_value.get(), 3)
    # # ------------- TESTS -------------

    window_graph.mainloop()
# ------------------------------- GRAPH UI SETUP ---------------------------------- #


def get_dir_names():
    dir_list = []
    for root, dirs, files in os.walk("D:"):
        for name in dirs:
            if "dir_1" in name or "dir_2" in name:
                dir_list.append(os.path.join(root, name))

    return dir_list


def retrieve():
    global THREAD_LIST
    global DIR_PATH
    global PATIENT_NAME

    user_answer = combo_dir_path.get()
    num_threads = thread_value.get()
    PATIENT_NAME = user_entry.get()

    if user_answer == "Pick an Option":
        messagebox.showerror(title="Choose an option",
                             message="You need to choose a folder path.")
    else:
        THREAD_LIST = [0 for threads in range(num_threads + 1)]  # Create a list of 0, where the total number is the total threads + the last index: total files.

        if user_answer == "D:dir_2":
            DIR_PATH = r"D:\dir_2"
        else:
            DIR_PATH = r"D:\dir_1"

        # print(combo_dir_path.get())
        # print(thread_value.get())

        graph_gui()
# ------------------------------ DETAILS WINDOW --------------------------------- #

# total_threads = []
# thread_input = input("How many threads do you want?")
# for number in range(1, int(thread_input) + 1):
#     t = threading.Thread(target=spider, args=[number, "D:\\dir_2"])
#     total_threads.append(t)
#     t.start()
#     time.sleep(5)

# for thread in total_threads:
#     thread.join()


# ------------------------------- INFO UI SETUP ---------------------------------- #
window_info = tkinter.Tk()
window_info.title("Octo-grabber")
window_info.config(padx=50, pady=50, bg=BACKGROUND_C)

# Label: Entry label
entry_label = tkinter.Label(window_info, text="What is the patient's name: ", bg=BACKGROUND_C, fg="#1687A7", font=(FONT_NAME, 20, "bold"), highlightthickness=0)
entry_label.grid(column=0, row=0, columnspan=10)

# Entry: Patient in the cloud
user_entry = tkinter.Entry(window_info, width=25)
user_entry.grid(column=0, row=1, columnspan=10)

# Label: Path label
path_label = tkinter.Label(window_info, text="Directory's Path: ", bg=BACKGROUND_C, fg="#1687A7", font=(FONT_NAME, 20, "bold"), highlightthickness=0)
path_label.grid(column=0, row=2, columnspan=10)

# Combobox: Directories path
combo_dir_path = ttk.Combobox(window_info, values=get_dir_names(), width=20)
combo_dir_path.set("Pick an Option")
combo_dir_path.grid(column=0, row=3, columnspan=10)

# Label: Number of threads
spacer_label = tkinter.Label(window_info, text="", bg=BACKGROUND_C, fg="#1687A7", font=(FONT_NAME, 20, "bold"), highlightthickness=0)
spacer_label.grid(column=0, row=4)
num_threads = tkinter.Label(window_info, text="Number of threads: ", bg=BACKGROUND_C, fg="#1687A7", font=(FONT_NAME, 20, "bold"), highlightthickness=0)
num_threads.grid(column=0, row=5, columnspan=10)

# Radio buttons: How many threads:
thread_value = tkinter.IntVar()

thread_1 = tkinter.Radiobutton(window_info, text="1", variable=thread_value, value=1)
thread_2 = tkinter.Radiobutton(window_info, text="2", variable=thread_value, value=2)
thread_3 = tkinter.Radiobutton(window_info, text="3", variable=thread_value, value=3)
thread_4 = tkinter.Radiobutton(window_info, text="4", variable=thread_value, value=4)
thread_5 = tkinter.Radiobutton(window_info, text="5", variable=thread_value, value=5)
thread_6 = tkinter.Radiobutton(window_info, text="6", variable=thread_value, value=6)
thread_7 = tkinter.Radiobutton(window_info, text="7", variable=thread_value, value=7)
thread_8 = tkinter.Radiobutton(window_info, text="8", variable=thread_value, value=8)
thread_9 = tkinter.Radiobutton(window_info, text="9", variable=thread_value, value=9)
thread_10 = tkinter.Radiobutton(window_info, text="10", variable=thread_value, value=10)

thread_1.grid(column=1, row=6, columnspan=4)
thread_2.grid(column=2, row=6, columnspan=4)
thread_3.grid(column=3, row=6, columnspan=4)
thread_4.grid(column=4, row=6, columnspan=4)
thread_5.grid(column=5, row=6, columnspan=4)
thread_6.grid(column=1, row=7, columnspan=4)
thread_7.grid(column=2, row=7, columnspan=4)
thread_8.grid(column=3, row=7, columnspan=4)
thread_9.grid(column=4, row=7, columnspan=4)
thread_10.grid(column=5, row=7, columnspan=4)

# Button: Submit
path_label = tkinter.Label(window_info, text="", bg=BACKGROUND_C, fg="#1687A7", font=(FONT_NAME, 20, "bold"), highlightthickness=0)
path_label.grid(column=0, row=8)
submit = tkinter.Button(window_info, text="Submit", highlightthickness=0, command=retrieve)
submit.grid(column=1, row=9, columnspan=10)

window_info.mainloop()
# ------------------------------- UI SETUP ---------------------------------- #
# %%
# Debugging:
if __name__ == "__main__":
    pass
# %%
