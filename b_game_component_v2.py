import csv
import random
from tkinter import *
from functools import partial  # to prevent unwanted windows


# helper functions go here
def get_colours():
    """
    Retrieves colours from csv file
    """
    file = open("00_colour_list_hex_v3.csv", "r")
    all_colours = list(csv.reader(file, delimiter=","))
    file.close()

    all_colours.pop(0)

    return all_colours


def get_round_colours():
    """
    Choose four colours from larger list ensuring that the scores are all different
    """

    all_colour_list = get_colours()

    round_colours = []
    colour_scores = []

    # loop until we have four colours with different scores
    while len(round_colours) < 4:
        potential_colour = random.choice(all_colour_list)

        # get the scores and check it's not a duplicate
        if potential_colour[1] not in colour_scores:
            round_colours.append(potential_colour)

            colour_scores.append(potential_colour[1])

    int_scores = [int(x) for x in colour_scores]
    int_scores.sort()

    median = (int_scores[1] + int_scores[2] / 2)
    median = int(round_ans(median))

    return round_colours, median


def round_ans(val):
    """
    Rounds temperatures to the nearest degree
    """
    var_rounded = (val * 2 + 1) // 2
    return "{:.0f}".format(var_rounded)


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
        Play(5)
        root.withdraw()


class Play:
    """
    Interface for playing the Colour Quest game
    """

    def __init__(self, how_many):

        self.target_score = IntVar()

        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        # colour list and score lists
        self.round_colour_list = []
        self.all_scores_list = []
        self.all_medians_list = []

        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        # body font for most labels
        body_font = ("Arial", "12")

        # List for label details (text | font | background | row)
        play_labels_list = [
            ["Round # of #", ("Arial", "16", "bold"), None, 0],
            ["Score to beat: #", body_font, "#FFF2CC", 1],
            ["Choose a colour below. Good Luck. 🍀", body_font, "#D5E8D4", 2],
            ["You chose, ______", body_font, "#D5E8D4", 4]
        ]

        play_labels_ref = []
        for item in play_labels_list:
            self.make_label = Label(self.game_frame, text=item[0], font=item[1],
                                    bg=item[2], wraplength=300, justify="left")
            self.make_label.grid(row=item[3], padx=10, pady=10)

            play_labels_ref.append(self.make_label)

        # retrieve labels so they can be configured later
        self.heading_label = play_labels_ref[0]
        self.target_label = play_labels_ref[1]
        self.results_label = play_labels_ref[3]

        # set up colour buttons
        self.colour_frame = Frame(self.game_frame)
        self.colour_frame.grid(row=3)

        self.colour_button_ref = []
        self.button_colours_list = []

        # create 4 buttons in a  2 x 2 grid
        for item in range(0, 4):
            self.colour_button = Button(self.colour_frame, font=("Arial", "12"),
                                        text="Colour Name", width=15,
                                        command=partial(self.round_results, item))
            self.colour_button.grid(row=item // 2,
                                    column=item % 2, padx=5, pady=5)

            self.colour_button_ref.append(self.colour_button)

        # frame to hold hints and stats button
        self.hints_stats_frame = Frame(self.game_frame)
        self.hints_stats_frame.grid(row=6)

        # list for buttons (frame | text | bg | command | width | row | column)
        control_buttons_list = [
            [self.game_frame, "Next Round", "#0057D8", "", 21, 5, None],
            [self.hints_stats_frame, "Hints", "#FF8000", "", 10, 0, 0],
            [self.hints_stats_frame, "Stats", "#333333", "", 10, 0, 1],
            [self.game_frame, "End", "#990000", self.close_play, 22, 7, None]
        ]

        # create buttons and add to list
        control_ref_list = []
        for item in control_buttons_list:
            make_control_button = Button(item[0], text=item[1], bg=item[2], command=item[3],
                                         font=("Arial", 16, "bold"),
                                         width=item[4], fg="#FFFFFF")
            make_control_button.grid(row=item[5], column=item[6], padx=5, pady=5)

            control_ref_list.append(make_control_button)

        # Retrieve next, stats and end button so that they can be configured
        self.next_button = control_ref_list[0]
        self.stats_button = control_ref_list[2]
        self.end_game_button = control_ref_list[3]

        self.new_round()

    def new_round(self):
        """
        Choose 4 colours, work out median for score to beat.
        configured buttons with chosen colours
        """

        # retrieve number of rounds played, add one to it and configure heading
        rounds_played = self.rounds_played.get()
        rounds_played += 1
        self.rounds_played.set(rounds_played)

        rounds_wanted = self.rounds_wanted.get()
        self.round_colour_list, median = get_round_colours()

        # set target score as median (for later comparison)
        self.target_score.set(median)

        # update heading and score to beat labels. hide result label
        self.heading_label.config(text=f"{rounds_played} of {rounds_wanted}")
        self.target_label.config(text=f"Target score: {median}",
                                 font=("Arial", "14", "bold"))
        self.results_label.config(text=f"{'=' * 7}", bg="#F0F0F0")

        # configure buttons using foreground and background colours from list
        # enable colour buttons (disabled at the end of last round)
        for count, item in enumerate(self.colour_button_ref):
            item.config(fg=self.round_colour_list[count][2],
                        bg=self.round_colour_list[count][0],
                        text=self.round_colour_list[count][0],
                        state=NORMAL)

        self.next_button.config(state=DISABLED)

    def close_play(self):
        # reshow root (ie: choose rounds) and end current
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    StartGame()
    root.mainloop()
