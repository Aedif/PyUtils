import random
import matplotlib.pyplot as plt
from pandas import DataFrame, concat


def get_damage(dmg_dice):
    damage = 0
    for dice in dmg_dice:
        if len(dice) == 3:
            num, dmg, mod = dice
        else:
            num, dmg = dice
            mod = 0

        for _ in range(num):
            damage += random.randint(1, dmg) + mod

    return damage


def dice_to_string(dice, inc_mod=True):
    ret_str = f"{dice[0]}d{dice[1]}"
    if inc_mod and len(dice) == 3:
        ret_str += f" + {dice[2]}"
    return ret_str


def dice_list_to_string(dice_list):
    modifier_sum = 0
    for dice in dice_list:
        if len(dice) == 3:
            modifier_sum += dice[2]

    dice_list_str = [dice_to_string(d, False) for d in dice_list]
    dice_list_str = " + ".join(dice_list_str)

    if modifier_sum > 0:
        dice_list_str += " + " + str(modifier_sum)
    return dice_list_str


def simul_plot(fig, num_rolls=1000, num_plots=1, sub_plot=1):

    roll_dice = CONFIGS["comp_1"]["roll_dice"]
    all_comp_1_rolls = []
    for _ in range(num_rolls):
        all_comp_1_rolls.append(get_damage(roll_dice))

    roll_dice = CONFIGS["comp_2"]["roll_dice"]
    all_comp_2_rolls = []
    for _ in range(num_rolls):
        all_comp_2_rolls.append(get_damage(roll_dice))

    comp_1_name = (
        CONFIGS["comp_1"]["name"]
        + ": "
        + dice_list_to_string(CONFIGS["comp_1"]["roll_dice"])
    )
    comp_2_name = (
        CONFIGS["comp_2"]["name"]
        + ": "
        + dice_list_to_string(CONFIGS["comp_2"]["roll_dice"])
    )
    df_hb = DataFrame(all_comp_1_rolls, columns=[comp_1_name])
    df_og = DataFrame(all_comp_2_rolls, columns=[comp_2_name])

    s1 = df_hb[comp_1_name].value_counts().sort_index().to_frame()
    s2 = df_og[comp_2_name].value_counts().sort_index().to_frame()
    occ_df = concat([s1, s2], axis=1,).fillna(0)

    ax = fig.add_subplot(3, 1, sub_plot)
    occ_df.plot(kind="bar", stacked=False, alpha=0.5, ax=ax)

    plt.ylabel(f"Rolls out of #{num_rolls}")
    plt.legend(loc="upper right")


# Corresponds to
# Mace + 1 : 1d6 + 5
# Crossbow + 1 : 1d8 + 4
CONFIGS = {
    "comp_1": {"name": "Mace + 1", "roll_dice": [(1, 6, 5)]},
    "comp_2": {"name": "Crossbow + 1", "roll_dice": [(1, 8, 4)]},
}


fig = plt.figure()
num_rolls = 400000
num_plots = 3

simul_plot(fig, num_rolls, num_plots, 1)

plt.show()
