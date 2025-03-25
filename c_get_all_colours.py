import csv
import random


def round_ans(val):
    """
    Rounds temperatures to the nearest degree
    """
    var_rounded = (val * 2 + 1) // 2
    return "{:.0f}".format(var_rounded)


# Retrieve colours from csv file and put them in a list
file = open("00_colour_list_hex_v3.csv", "r")
all_colours = list(csv.reader(file, delimiter=","))
file.close()

all_colours.pop(0)

round_colours = []
colour_scores = []

# loop until we have four colours with different scores
while len(round_colours) < 4:
    potential_colour = random.choice(all_colours)

    # get the scores and check it's not a duplicate
    if potential_colour[1] not in colour_scores:
        round_colours.append(potential_colour)
        colour_scores.append(potential_colour[1])


print(round_colours)
print(colour_scores)

int_scores = [int(x) for x in colour_scores]
int_scores.sort()

median = (int_scores[1] + int_scores[2] / 2)
print(f"unrounded median: {median}")
print(f"median: {median:.0f}")
