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
        self.rounds_won = IntVar()

        # highest score test data
        self.all_scores_list = [20, 20, 20, 16, 19]
        self.all_high_score_list = [20, 20, 20, 16, 19]
        self.rounds_won.set(5)

        # # Lowest score test data
        # self.all_scores_list = [0, 0, 0, 0, 0]
        # self.all_high_score_list = [20, 20, 20, 16, 19]
        # self.rounds_won.set(0)
        #
        # # random score test data
        # self.all_scores_list = [0, 15, 16, 0, 16]
        # self.all_high_score_list = [20, 19, 18, 20, 20]
        # self.rounds_won.set(0)

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
        """
        Retrieves everything we need to display the game / round statistics
        """

        # IMPORTANT: retrieve number of rounds won
        # as a number (rather than the 'self' container)
        rounds_won = self.rounds_won.get()
        stats_bundle = [rounds_won, self.all_high_score_list,
                        self.all_high_score_list]
        DisplayStatistics(self, stats_bundle)


class DisplayStatistics:

    def __init__(self, partner, all_stats_info):

        # Extract information from master list
        rounds_won = all_stats_info[0]
        user_score = all_stats_info[1]
        high_scores = all_stats_info[2]

        # sort user scores to find high score
        user_score.sort()

        # set up dialogue box
        self.stats_box = Toplevel()

        # disable stats button
        partner.stats_button.config(state=DISABLED)

        # If users press the cross at the top, closes and 'releases' the stats button
        self.stats_box.protocol('WM_DELETE_WINDOW',
                                partial(self.close_stats, partner))

        self.stats_frame = Frame(self.stats_box, width=300, height=200)
        self.stats_frame.grid()

        # Math to populate Stats dialogue
        rounds_played = len(user_score)

        success_rate = rounds_won / rounds_played * 100
        total_score = sum(user_score)
        max_possible = sum(high_scores)

        best_score = user_score[-1]
        average_score = total_score / rounds_played

        # strings for stats label
        success_string = (f"Success Rate: {rounds_won} / {rounds_played}"
                          f"({success_rate:.0f}%)")
        total_score_string = f"Total score: {total_score}"
        max_possible_string = f"Maximum possible score: {max_possible}"
        best_score_string = f"Best score: {best_score}"

        # custom comments text and formatting
        if total_score == max_possible:
            comment_string = "Amazing! You got the highest possible score"
            comment_colour = "#D5E8D4"

        elif total_score == 0:
            comment_string = "Yikes - You have every single round\n" \
                             "You might want to look at the hints."
            comment_colour = "#F8CECC"
            best_score_string = f"Best score: n/a"

        else:
            comment_string = ""
            comment_colour = "#F0F0F0"

        average_score_string = f"Average SCore: {average_score:.0f}\n"

        heading_font = ("Arial", "16", "bold")
        normal_font = ("Arial", "14")
        comment_font = ("Arial", "13")

        # Label list (text colour | font | Sticky)
        all_stats_string = [
            
        ]

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
            item.config(bg="#ffe6cc")

    def close_stats(self, partner):
        """
        Closes stats dialogue box and enables stats button
        """
        # Put stats button back to normal
        partner.stats_button.config(state=NORMAL)
        self.stats_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    StartGame()
    root.mainloop()
