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

        # strings for labels
        intro_string = "In each round you will be invited to choose a colour. Your goal is " \
                       "to beat the target score and win the round (and keep your points)."

        choose_string = "How many rounds do you want to play?"

        # List of labels to be made (text | font | fg)
        start_labels_list = [
            ["Colour Quest", ("Arial", "16", "bold"), None],
            [intro_string, ("Arial", "12"), None],
            [choose_string, ("Arial", "12", "bold"), "#17b317"]
        ]

        # Create labels and add them to the reference list...

        start_labels_ref = []
        for count, item in enumerate(start_labels_list):
            make_label = Label(self.start_frame, text=item[0], font=item[1],
                               fg=item[2],
                               wraplength=350, justify="left", pady=10, padx=20)
            make_label.grid(row=count)

            start_labels_ref.append(make_label)

        # extract choice label so that it can be changed into an error message
        self.choose_label = start_labels_ref[2]

        # frame so that entry box and bottom can be in the same row
        self.entry_area_frame = Frame(self.start_frame)
        self.entry_area_frame.grid(row=3)

        self.num_rounds_entry = Entry(self.entry_area_frame,
                                      font=("Arial", "20", "bold",),
                                      width=10)
        self.num_rounds_entry.grid(row=0, column=0, padx=10, pady=10)

        # create play button
        self.play_button = Button(self.entry_area_frame, font=("Arial", "16", "bold"),
                                  fg="#FFFFFF", bg="#0057D8", text="Play",
                                  width=10, command=self.check_rounds)
        self.play_button.grid(row=0, column=1)

    def check_rounds(self):
        """
        Checks that users have entered 1 or more rounds
        """
        # Retrieve temperature to be converted
        rounds_wanted = self.num_rounds_entry.get()

        # reset label and entry box (for when users come back to home screen)
        self.choose_label.config(fg="#17b317", font=("Arial", "12", "bold"))
        self.num_rounds_entry.config(bg="#FFFFFF")

        error = "Oops - please choose a whole number more than zero."
        has_errors = "no"

        # checks that the amount wanted is a number above absolute zero
        try:
            rounds_wanted = int(rounds_wanted)
            if rounds_wanted > 0:
                # Clear entry box and reset instruction label so that
                # when users play a new game, they don't see an error message
                self.num_rounds_entry.delete(0, END)
                self.choose_label.config(text="How many rounds do you want to play?")

                # invoke play class (and take across number of rounds)
                Play(rounds_wanted)
                # invoke root window (ie: hide rounds choice window)
                root.withdraw()
            else:
                has_errors = "yes"
        except ValueError:
            has_errors = "yes"

        # display the error if necessary
        if has_errors == "yes":
            self.choose_label.config(text=error, fg="#990000",
                                     font=("Arial", "10", "bold"))
            self.num_rounds_entry.config(bg="#F4CCCC")
            self.num_rounds_entry.delete(0, END)


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
            [self.game_frame, "Next Round", "#0057D8", self.new_round, 21, 5, None],
            [self.hints_stats_frame, "Hints", "#FF8000", self.to_hints, 10, 0, 0],
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

        # Retrieve next, stats, hints, and end button so that they can be configured
        self.next_button = control_ref_list[0]
        self.stats_button = control_ref_list[2]
        self.hints_button = control_ref_list[1]
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

    def round_results(self, user_choice):
        """
        Retrieves which button was pushed (index 0 - 3), retrieves
        score and then compares it with median, updates results
        and adds results to stats list.
        """

        # Get user score and colour based on button press
        score = int(self.round_colour_list[user_choice][1])

        # alternate way to get button name. good for if buttons have been scrambled
        colour_name = self.colour_button_ref[user_choice].cget('text')

        target = self.target_score.get()
        self.all_medians_list.append(target)

        if score >= target:
            result_text = f"Success! {colour_name} earned you {score} points."
            result_bg = "#82B366"
            self.all_scores_list.append(score)
        else:
            result_text = f"oops {colour_name} ({score}) is less than the target."
            result_bg = "#F8CECC"
            self.all_scores_list.append(0)

        self.results_label.config(text=result_text, bg=result_bg)

        # enable stats & next buttons, disable colour buttons
        self.next_button.config(state=NORMAL)
        self.stats_button.config(state=NORMAL)

        # check to see if game is over
        rounds_played = self.rounds_played.get()
        rounds_wanted = self.rounds_wanted.get()

        if rounds_played == rounds_wanted:
            self.next_button.config(state=DISABLED, text="GAME OVER")
            self.end_game_button.config(text="Play again", bg="#039903")

        for item in self.colour_button_ref:
            item.config(state=DISABLED)

    def close_play(self):
        # reshow root (ie: choose rounds) and end current
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()

    def to_hints(self):
        DisplayHints(self)


class DisplayHints:

    def __init__(self, partner):
        # set up dialogue box and background colour
        background = "#ffe6cc"
        self.hints_box = Toplevel()

        # disable hints button
        partner.hints_button.config(state=DISABLED)

        # If users press the cross at the top, closes and 'releases' the hints button
        self.hints_box.protocol('WM_DELETE_WINDOW',
                                partial(self.close_hints, partner)
                                )

        self.hints_frame = Frame(self.hints_box, width=300,
                                 height=200)
        self.hints_frame.grid()

        self.hints_heading_label = Label(self.hints_frame,
                                         text="Hints",
                                         font=("Arial", "16", "bold"))
        self.hints_heading_label.grid(row=0)

        hints_text = "The score for each colour relates to it;s hexadecimal code.\n\n" \
                     "Remember, the hex code foe white id #FFFFFF - which is the best\n" \
                     " possible score.\n\n" \
                     "The hex code for black is #000000 which is the worst possible\n score" \
                     "\n\nThe first colour in the code is red, so if you had to choose\n" \
                     " between red (#FF0000), green (#00FF00), and blue (#0000FF), then\n " \
                     "red would be the best choice.\n\n" \
                     "GOOD LUCK!\n"

        self.hints_text_label = Label(self.hints_frame,
                                      text=hints_text,
                                      wraplength=350,
                                      justify="left",
                                      font=("Arial", "10"))
        self.hints_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.hints_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF", command=partial(self.close_hints, partner)
                                     )
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        # List and loop to set up background colour on everything except the buttons
        recolour_list = [self.hints_frame, self.hints_heading_label,
                         self.hints_text_label]

        for item in recolour_list:
            item.config(bg=background)

    def close_hints(self, partner):
        """
        Closes hints dialogue box and enables hints button
        """
        # Put hints button back to normal
        partner.hints_button.config(state=NORMAL)
        self.hints_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    StartGame()
    root.mainloop()
