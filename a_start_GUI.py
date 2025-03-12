from tkinter import *
from functools import partial # to prevent unwanted windows


class StartGame:
    """
    Initial Game interface (asks users how many rounds they
    want to play)
    """

    def __init__(self):
        """
        Gets number of rounds from user
        """

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # strings for labels
        intro_string = "In each round you will be invited to choose a colour. Your goal is " \
                       "to beat the target score and win the round (and keep your points)."

        choose_string = "How many rounds do you want to play?"

        # List of labels to be made (text | font | fg)
        start_labels_list =[
            ["Colour Quest", ("Arial", "16"), "bold", None],
            [intro_string, ("Arial", "12", None)],
            [choose_string, ("Arial", "12", "bold"), "#17b317"]
        ]

        # Create labels and add them to the reference list...

        start_labels_ref = []
        for count, item in enumerate(start_labels_list):
            make_label = Label(self.start_frame, text=item[0], font=item[1],
                               fg=item[2], wraplength=350,
                               justify="left", pady=10, padx=20)
            make_label.grid(row=count)

            start_labels_ref.append(make_label)


if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    StartGame()
    root.mainloop()
