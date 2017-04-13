from __future__ import division
from __future__ import print_function
# Simple test program to debug + play with assassination models.
from builtins import str
from os import path
import sys
from pprint import pprint
sys.path.append(path.abspath(path.join(path.dirname(__file__), '..')))

from shadowcraft.calcs.rogue.Aldriana import AldrianasRogueDamageCalculator
from shadowcraft.calcs.rogue.Aldriana import settings

from shadowcraft.objects import buffs
from shadowcraft.objects import race
from shadowcraft.objects import stats
from shadowcraft.objects import procs
from shadowcraft.objects import talents
from shadowcraft.objects import artifact

from shadowcraft.core import i18n

# Set up language. Use 'en_US', 'es_ES', 'fr' for specific languages.
test_language = 'local'
i18n.set_language(test_language)

# Set up level/class/race
test_level = 110
test_race = race.Race('blood_elf', 'rogue', 110)
test_class = 'rogue'
test_spec = 'assassination'

# Set up buffs.
test_buffs = buffs.Buffs(
    'short_term_haste_buff',
    'flask_legion_agi',
    'food_legion_mastery_375'
)

# Set up weapons.
test_mh = stats.Weapon(7063.0, 1.8, 'dagger', None)
test_oh = stats.Weapon(7063.0, 1.8, 'dagger', None)

# Set up procs.
#test_procs = procs.ProcsList(('scales_of_doom', 691), ('beating_heart_of_the_mountain', 701),
#                             'draenic_agi_pot', 'draenic_agi_prepot', 'archmages_greater_incandescence')
test_procs = procs.ProcsList('old_war_pot', 'old_war_prepot',
    #'convergence_of_fates',
    ('draught_of_souls', 910),
    #('chaos_talisman', 890),
    ('nightblooming_frond', 910),
)

# Set up gear buffs.
test_gear_buffs = stats.GearBuffs('gear_specialization',
#'the_dreadlords_deceit',
'rogue_t19_2pc',
'rogue_t19_4pc',
'zoldyck_family_training_shackles',
'mantle_of_the_master_assassin',
#'duskwalkers_footpads',
#'cinidaria_the_symbiote',
)

# Set up a calcs object..
test_stats = stats.Stats(test_mh, test_oh, test_procs, test_gear_buffs,
                         agi=21964,
                         stam=32801,
                         crit=8749,
                         haste=1935,
                         mastery=9729,
                         versatility=4382,)
# Initialize talents..
#test_talents = talents.Talents('2110031', test_spec, test_class, level=test_level)
test_talents = talents.Talents('1230011', test_spec, test_class, level=test_level)

#initialize artifact traits..
test_traits = artifact.Artifact(test_spec, test_class, trait_dict={
    'kingsbane':                 1,
    'assassins_blades':          1,
    'toxic_blades':              3,
    'poison_knives':             3,
    'urge_to_kill':              1,
    'balanced_blades ':          3,
    'surge_of_toxins':           1,
    'shadow_walker':             3,
    'master_assassin':           3+2,
    'shadow_swiftness':          1,
    'serrated_edge':             3,
    'bag_of_tricks':             1,
    'master_alchemist':          3,
    'gushing_wounds':            3+1,
    'fade_into_shadows':         3,
    'from_the_shadows':          1,
    'blood_of_the_assassinated': 1,
    'slayers_precision':         1,
    'silence_of_the_uncrowned':  1,
    'strangler': 4,
    'dense_concoction': 0,
    'sinister_circulation': 0,
    'concordance_of_the_legionfall': 0,
})

# Set up settings.
test_cycle = settings.AssassinationCycle()
test_settings = settings.Settings(test_cycle, response_time=.5, duration=300,
                                  finisher_threshold=4)

# Build a DPS object.
calculator = AldrianasRogueDamageCalculator(test_stats, test_talents, test_traits, test_buffs, test_race, test_spec, test_settings, test_level)

print(str(calculator.stats.get_character_stats(calculator.race)))

# Compute DPS Breakdown.
dps_breakdown = calculator.get_dps_breakdown()
total_dps = sum(entry[1] for entry in list(dps_breakdown.items()))

# Compute EP values.
ep_values = calculator.get_ep(baseline_dps=total_dps)
tier_ep_values = calculator.get_other_ep(['rogue_t19_4pc', 'rogue_t19_2pc',
'duskwalkers_footpads', 'zoldyck_family_training_shackles', 'mantle_of_the_master_assassin'
])


#talent_ranks = calculator.get_talents_ranking()
#trait_ranks = calculator.get_trait_ranking()

def max_length(dict_list):
    max_len = 0
    for i in dict_list:
        dict_values = list(i.items())
        if max_len < max(len(entry[0]) for entry in dict_values):
            max_len = max(len(entry[0]) for entry in dict_values)

    return max_len

def pretty_print(dict_list):
    max_len = max_length(dict_list)

    for i in dict_list:
        dict_values = list(i.items())
        dict_values.sort(key=lambda entry: entry[1], reverse=True)
        for value in dict_values:
            if ("{0:.2f}".format(value[1] / total_dps)) != '0.00':
                print(value[0] + ':' + ' ' * (max_len - len(value[0])), str(value[1]) + ' ('+str( "{0:.2f}".format(100*float(value[1])/total_dps) )+'%)')
            else:
                print(value[0] + ':' + ' ' * (max_len - len(value[0])), str(value[1]))
        print('-' * (max_len + 15))

dicts_for_pretty_print = [
    ep_values,
    tier_ep_values,
    #talent_ranks,
    #trinkets_ep_value,
    dps_breakdown,
    #trait_ranks
]
pretty_print(dicts_for_pretty_print)

#pretty_print([dps_breakdown], total_sum=total_dps, show_percent=True)
print(' ' * (max_length([dps_breakdown]) + 1), total_dps, ("total damage per second."))

#pprint(talent_ranks)
