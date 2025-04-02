from tkinter import *
from functools import partial  # to prevent unwanted windows


# classes start here
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

        # create play button
        self.play_button = Button(self.start_frame, font=("Arial", "16", "bold"),
                                  fg="#FFFFFF", bg="#0057D8", text="Play",
                                  width=10, command=self.check_rounds)
        self.play_button.grid(row=0, column=1)

    def check_rounds(self):
        """
        Checks that users have entered 1 or more rounds
        """
        # Retrieve temperature to be converted
        rounds_wanted = 5
        self.to_play(rounds_wanted)

    def to_play(self, num_rounds):
        """
        Invokes game GUI and takes across #  of rounds to be played
        """
        Play(num_rounds)
        # root.withdraw()


class Play:
    """
    Interface for playing the Colour Quest game
    """

    def __init__(self, how_many):
        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        self.heading_label = Label(self.game_frame, text="Colour Quest", font=("Arial", "16", "bold"),
                                   pady=5, padx=5)
        self.heading_label.grid(row=0)

        # create stats button
        self.stats_button = Button(self.game_frame, font=("Arial", "16", "bold"),
                                   fg="#FFFFFF", bg="#FF8000", text="Stats",
                                   width=10, command=self.to_stats)
        self.stats_button.grid(row=1)

    def to_stats(self):
        DisplayStatistics(self)


class DisplayStatistics:

    def __init__(self, partner):
        # set up dialogue box and background colour
        background = "#ffe6cc"
        self.stats_box = Toplevel()

        # disable stats button
        partner.stats_button.config(state=DISABLED)

        # If users press the cross at the top, closes and 'releases' the stats button
        self.stats_box.protocol('WM_DELETE_WINDOW',
                                partial(self.close_stats, partner)
                                )

        self.stats_frame = Frame(self.stats_box, width=300,
                                 height=200)
        self.stats_frame.grid()

        self.stats_heading_label = Label(self.stats_frame,
                                         text="Stats",
                                         font=("Arial", "16", "bold"))
        self.stats_heading_label.grid(row=0)

        stats_text = "idk if i need this"

        self.stats_text_label = Label(self.stats_frame,
                                      text=stats_text,
                                      wraplength=350,
                                      justify="left",
                                      font=("Arial", "10"))
        self.stats_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.stats_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF", command=partial(self.close_stats, partner)
                                     )
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        # List and loop to set up background colour on everything except the buttons
        recolour_list = [self.stats_frame, self.stats_heading_label,
                         self.stats_text_label]

        for item in recolour_list:
            item.config(bg=background)

    def close_stats(self, partner):
        """
        Closes stats dialogue box and enables stats button
        """
        # Put stats
        # button back to normal
        partner.stats_button.config(state=NORMAL)
        self.stats_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    StartGame()
    root.mainloop()
