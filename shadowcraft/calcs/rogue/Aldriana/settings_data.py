# This file contains all rogue settings that are advertised to the react UI and later passed
# into the settings object before calculation.

def get_default_settings(block_name, spec, settings_data):
    defaults = {}
    for category in settings_data:
        if category['name'] == block_name:
            for option in category['items']:
                if isinstance(option['default'], dict):
                    defaults[option['name']] = option['default'][spec]
                else:
                    defaults[option['name']] = option['default']
            break
    return defaults

rogue_settings = [
    {
        'spec': 'a',
        'heading': 'Assassination Rotation Settings',
        'name': 'rotation.assassination',
        'items': [
            {
                'name': 'kingsbane',
                'label': 'Kingsbane w/ Vendetta',
                'description': '',
                'type': 'dropdown',
                'default': 'just',
                'options': {
                    'just': "Use cooldown if it aligns, but don't delay usage",
                    'only': 'Only use cooldown with Vendetta'
                }
            },
            {
                'name': 'exsang',
                'label': 'Exsang w/ Vendetta',
                'description': '',
                'type': 'dropdown',
                'default': 'just',
                'options': {
                    'just': "Use cooldown if it aligns, but don't delay usage",
                    'only': 'Only use cooldown with Vendetta'
                }
            },
            {
                'name': 'cp_builder',
                'label': 'CP Builder',
                'description': '',
                'type': 'dropdown',
                'default': 'mutilate',
                'options': {
                    'mutilate': 'Mutilate',
                    'fan_of_knives': 'Fan of Knives'
                }
            },
            {
                'name': 'lethal_poison',
                'label': 'Lethal Poison',
                'description': '',
                'type': 'dropdown',
                'default': 'dp',
                'options': {
                    'dp': 'Deadly Poison',
                    'wp': 'Wound Poison'
                }
            },
        ]
    },
    {
        'spec': 'Z',
        'heading': 'Outlaw Rotation Settings',
        'name': 'rotation.outlaw',
        'items': [
            {
                'name': 'blade_flurry',
                'label': 'Blade Flurry',
                'description': 'Use Blade Flurry',
                'type': 'checkbox',
                'default': False
            },
            {
                'name': 'between_the_eyes_policy',
                'label': 'BtE Policy',
                'description': '',
                'type': 'dropdown',
                'default': 'never',
                'options': {
                    'shark': 'Only use with Shark',
                    'always': 'Use BtE on cooldown',
                    'never': 'Never use BtE',
                }
            },
            {
                'name': 'reroll_policy',
                'label': 'RtB Reroll Policy',
                'description': '',
                'type': 'dropdown',
                'default': 'custom',
                'options': {
                    '1': 'Reroll single buffs',
                    '2': 'Reroll two or fewer buffs',
                    '3': 'Reroll three or fewer buffs',
                    'custom': 'Custom setup per buff (see below)',
                }
            },
            {
                'name': 'jolly_roger_reroll',
                'label': 'Jolly Roger',
                'description': '',
                'type': 'dropdown',
                'default': '2',
                'options': {
                    '0': '0 - Never reroll combos with this buff',
                    '1': '1 - Reroll single buff rolls of this buff',
                    '2': '2 - Reroll double-buff rolls containing this buff',
                    '3': '3 - Reroll triple-buff rolls containing this buff'
                }
            },
            {
                'name': 'grand_melee_reroll',
                'label': 'Grand Melee',
                'description': '',
                'type': 'dropdown',
                'default': '2',
                'options': {
                    '0': '0 - Never reroll combos with this buff',
                    '1': '1 - Reroll single buff rolls of this buff',
                    '2': '2 - Reroll double-buff rolls containing this buff',
                    '3': '3 - Reroll triple-buff rolls containing this buff'
                }
            },
            {
                'name': 'shark_reroll',
                'label': 'Shark-Infested Waters',
                'description': '',
                'type': 'dropdown',
                'default': '2',
                'options': {
                    '0': '0 - Never reroll combos with this buff',
                    '1': '1 - Reroll single buff rolls of this buff',
                    '2': '2 - Reroll double-buff rolls containing this buff',
                    '3': '3 - Reroll triple-buff rolls containing this buff'
                }
            },
            {
                'name': 'true_bearing_reroll',
                'label': 'True Bearing',
                'description': '',
                'type': 'dropdown',
                'default': '0',
                'options': {
                    '0': '0 - Never reroll combos with this buff',
                    '1': '1 - Reroll single buff rolls of this buff',
                    '2': '2 - Reroll double-buff rolls containing this buff',
                    '3': '3 - Reroll triple-buff rolls containing this buff'
                }
            },
            {
                'name': 'buried_treasure_reroll',
                'label': 'Buried Treasure',
                'description': '',
                'type': 'dropdown',
                'default': '2',
                'options': {
                    '0': '0 - Never reroll combos with this buff',
                    '1': '1 - Reroll single buff rolls of this buff',
                    '2': '2 - Reroll double-buff rolls containing this buff',
                    '3': '3 - Reroll triple-buff rolls containing this buff'
                }
            },
            {
                'name': 'broadsides_reroll',
                'label': 'Broadsides',
                'description': '',
                'type': 'dropdown',
                'default': '2',
                'options': {
                    '0': '0 - Never reroll combos with this buff',
                    '1': '1 - Reroll single buff rolls of this buff',
                    '2': '2 - Reroll double-buff rolls containing this buff',
                    '3': '3 - Reroll triple-buff rolls containing this buff'
                }
            }
        ]
    },
    {
        'spec': 'b',
        'heading': 'Subtlety Rotation Settings',
        'name': 'rotation.subtlety',
        'items': [
            {
                'name': 'cp_builder',
                'label': 'CP Builder',
                'description': '',
                'type': 'dropdown',
                'default': 'backstab',
                'options': {
                    'backstab': 'Backstab',
                    'shuriken_storm': 'Shuriken Storm',
                }
            },
            {
                'name': 'symbols_policy',
                'label': 'SoD Policy',
                'description': '',
                'type': 'dropdown',
                'default': 'just',
                'options': {
                    'always': 'Use on cooldown',
                    'just': 'Only use SoD when needed to refresh',
                }
            },
            {
                'name': 'dance_finishers_allowed',
                'label': 'Use Finishers during Dance',
                'description': '',
                'type': 'checkbox',
                'default': True
            },
            {
                'name': 'positional_uptime_percent',
                'label': 'Backstab uptime',
                'description': 'Percentage of the fight you are behind the target (0-100). This has no effect if Gloomblade is selected as a talent.',
                'type': 'text',
                'default': '100'
            },
            {
                'name': 'compute_cp_waste',
                'label': 'Compute CP Waste',
                'description': 'EXPERIMENTAL FEATURE: Compute combo point waste',
                'type': 'checkbox',
                'default': False
            }
        ]
    },
    {
        'spec': 'All',
        'heading': 'Raid Buffs',
        'name': 'buffs',
        'items': [
            {
                'name': 'flask_legion_agi',
                'label': 'Legion Agility Flask',
                'description': 'Flask of the Seventh Demon (1300 Agility)',
                'type': 'checkbox',
                'default': False
            },
            {
                'name': 'short_term_haste_buff',
                'label': '+30% Haste/40 sec',
                'description': 'Heroism/Bloodlust/Time Warp',
                'type': 'checkbox',
                'default': False
            },
            {
                'name': 'food_buff',
                'label': 'Food',
                'description': '',
                'type': 'dropdown',
                'default': 'food_legion_feast_500',
                'options': {
                    'food_legion_crit_375': 'The Hungry Magister (375 Crit)',
                    'food_legion_haste_375': 'Azshari Salad (375 Haste)',
                    'food_legion_mastery_375': 'Nightborne Delicacy Platter (375 Mastery)',
                    'food_legion_versatility_375': 'Seed-Battered Fish Plate (375 Versatility)',
                    'food_legion_feast_500': 'Lavish Suramar Feast (500 Agility)',
                    'food_legion_damage_3': 'Fishbrul Special (High Fire Proc)',
                }
            },
            {
                'name': 'prepot',
                'label': 'Pre-pot',
                'description': '',
                'type': 'dropdown',
                'default': 'old_war_pot',
                'options': {
                    'old_war_pot': 'Potion of the Old War',
                    'prolonged_power_pot': 'Potion of Prolonged Power',
                    'potion_none': 'None',
                }
            },
            {
                'name': 'potion',
                'label': 'Combat Potion',
                'description': '',
                'type': 'dropdown',
                'default': 'old_war_prepot',
                'options': {
                    'old_war_prepot': 'Potion of the Old War',
                    'prolonged_power_prepot': 'Potion of Prolonged Power',
                    'potion_none': 'None',
                }
            }
        ]
    },
    {
        'spec': 'All',
        'heading': 'General Settings',
        'name': 'general.settings',
        'items': [
            {
                'name': 'is_demon',
                'label': 'Enemy is Demon',
                'description': 'Enables damage buff from heirloom trinket against demons',
                'type': 'checkbox',
                'default': False
            },
            {
                'name': 'patch',
                'label': 'Patch/Engine',
                'description': '',
                'type': 'dropdown',
                'default': '7.0',
                'options': {
                    '7.0': '7.0',
                    'fierys_strange_voodoo': 'fierys strange voodoo',
                }
            },
            {
                'name': 'race',
                'label': 'Race',
                'description': '',
                'type': 'dropdown',
                'default': 'human',
                'options': {
                    'human': 'Human',
                    'dwarf': 'Dwarf',
                    'orc': 'Orc',
                    'blood_elf': 'Blood Elf',
                    'gnome': 'Gnome',
                    'worgen': 'Worgen',
                    'troll': 'Troll',
                    'night_elf': 'Night Elf',
                    'undead': 'Undead',
                    'goblin': 'Goblin',
                    'pandren': 'Pandaren',
                }
            },
            {
                'name': 'is_day',
                'label': 'Night Elf Racial',
                'description': '',
                'type': 'dropdown',
                'default': False,
                'options': {
                    False: 'Night',
                    True: 'Day',
                }
            },
            {
                'name': 'finisher_threshold',
                'label': 'Finisher Threshold',
                'description': 'Minimum CPs to use finisher',
                'type': 'dropdown',
                'default': {
                    'assassination': '4',
                    'outlaw': '5',
                    'subtlety': '5'
                },
                'options': {
                    '4': '4',
                    '5': '5',
                    '6': '6'
                }
            },
            {
                'name': 'level',
                'label': 'Level',
                'description': '',
                'type': 'text',
                'default': '110'
            },
            {
                'name': 'duration',
                'label': 'Fight Duration',
                'description': '',
                'type': 'text',
                'default': '300'
            },
            {
                'name': 'response_time',
                'label': 'Response Time',
                'description': '',
                'type': 'text',
                'default': '0.5',
            },
            {
                'name': 'num_boss_adds',
                'label': 'Number of Boss Adds',
                'description': '',
                'type': 'text',
                'default': '0',
            },
            {
                'name': 'marked_for_death_resets',
                'label': 'MfD Resets Per Minute',
                'description': '',
                'type': 'text',
                'default': '0',
            }
        ]
    },
    {
        'spec': 'All',
        'heading': 'Other',
        'name': 'other',
        'items': [
            {
                'name': 'latency',
                'label': 'Latency',
                'description': '',
                'type': 'text',
                'default': '0.03'
            },
            {
                'name': 'adv_params',
                'label': 'Advanced Parameters',
                'description': '',
                'type': 'text',
                'default': ''
            }
        ]
    }
]
