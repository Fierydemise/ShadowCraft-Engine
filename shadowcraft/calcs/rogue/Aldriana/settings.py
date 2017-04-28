from builtins import object
from shadowcraft.core import exceptions
from shadowcraft.calcs.rogue.Aldriana import settings_data

class Settings(object):
    # Settings object for AldrianasRogueDamageCalculator.

    def __init__(self, cycle, **kwargs):
        self.cycle = cycle
        self.default_ep_stat = kwargs.get('default_ep_stat', 'ap')
        self.feint_interval = int(kwargs.get('feint_interval', 0))

        #Get defaults from settings_data
        defaults = settings_data.get_default_settings(settings_data.rogue_settings)

        suffix = '_' + self.cycle._cycle_type
        #Spec overrides from defaults
        for setting in list(defaults.keys()):
            if setting.endswith(suffix):
                override_key = setting.replace(suffix, '')
                defaults[override_key] = defaults[setting]
        #Spec overrides from params
        for setting in kwargs:
            if setting.endswith(suffix):
                override_key = setting.replace(suffix, '')
                defaults[override_key] = kwargs[setting]

        self.response_time = float(kwargs.get('response_time', defaults['response_time']))
        self.latency = float(kwargs.get('latency', defaults['latency']))
        self.duration = int(kwargs.get('duration', defaults['duration']))
        self.is_day = kwargs.get('is_day', defaults['is_day'])
        self.is_demon = kwargs.get('is_demon', defaults['is_demon'])
        self.num_boss_adds = max(int(kwargs.get('num_boss_adds', defaults['num_boss_adds'])), 0)
        self.adv_params = self.interpret_adv_params(kwargs.get('adv_params', defaults['adv_params']))
        self.marked_for_death_resets = int(kwargs.get('marked_for_death_resets', defaults['marked_for_death_resets']))
        self.finisher_threshold = int(kwargs.get('finisher_threshold', defaults['finisher_threshold']))

    def interpret_adv_params(self, s=""):
        data = {}
        max_effects = 8
        current_effects = 0
        if s != "" and s:
            for e in s.split(';'):
                if e != "":
                    tmp = e.split(':')
                    try:
                        data[tmp[0].strip().lower()] = tmp[1].strip().lower() #strip() and lower() needed so that everyone is on the same page                        print data[tmp[0].strip().lower()] + ' : ' + tmp[0].strip().lower()
                        current_effects += 1
                        if current_effects == max_effects:
                            return data
                    except:
                        raise exceptions.InvalidInputException(_('Advanced Parameter ' + e + ' found corrupt. Properly structure params and try again.'))
        return data

    def is_assassination_rogue(self):
        return self.cycle._cycle_type == 'assassination'

    def is_outlaw_rogue(self):
        return self.cycle._cycle_type == 'outlaw'

    def is_subtlety_rogue(self):
        return self.cycle._cycle_type == 'subtlety'

class Cycle(object):
    # Base class for cycle objects.  Can't think of anything that particularly
    # needs to go here yet, but it seems worth keeping options open in that
    # respect.

    # When subclassing, define _cycle_type to be one of 'assassination',
    # 'outlaw', or 'subtlety' - this is how the damage calculator makes sure
    # you have an appropriate cycle object to go with your talent trees, etc.
    _cycle_type = ''


class AssassinationCycle(Cycle):
    _cycle_type = 'assassination'

    def __init__(self, **kwargs):
        defaults = settings_data.get_default_settings(settings_data.rogue_settings)
        self.cp_builder = kwargs.get('cp_builder', defaults['cp_builder'])
        self.kingsbane_with_vendetta = kwargs.get('kingsbane', defaults['kingsbane'])
        self.exsang_with_vendetta = kwargs.get('exsang', defaults['exsang'])
        self.lethal_poison = kwargs.get('lethal_poison', defaults['lethal_poison'])

class OutlawCycle(Cycle):
    _cycle_type = 'outlaw'
    #Generated by:
    #from itertools import combinations
    #single = ['jr', 'gm', 's', 'tb', 'bt', 'b']
    #list(combinations(single, 6)) + list(combinations(single, 3)) + list(combinations(single, 2)) + list(combinations(single, 1))
    rtb_combos = [('jr', 'gm', 's', 'tb', 'bt', 'b'),
                  #3 buffs
                  ('jr', 'gm', 's'), ('jr', 'gm', 'tb'),
                  ('jr', 'gm', 'bt'), ('jr', 'gm', 'b'),
                  ('jr', 's', 'tb'), ('jr', 's', 'bt'),
                  ('jr', 's', 'b'), ('jr', 'tb', 'bt'),
                  ('jr', 'tb', 'b'), ('jr', 'bt', 'b'),
                  ('gm', 's', 'tb'), ('gm', 's', 'bt'),
                  ('gm', 's', 'b'), ('gm', 'tb', 'bt'),
                  ('gm', 'tb', 'b'), ('gm', 'bt', 'b'),
                  ('s', 'tb', 'bt'), ('s', 'tb', 'b'),
                  ('s', 'bt', 'b'), ('tb', 'bt', 'b'),
                  #2 buffs
                  ('jr', 'gm'), ('jr', 's'), ('jr', 'tb'),
                  ('jr', 'bt'), ('jr', 'b'), ('gm', 's'),
                  ('gm', 'tb'), ('gm', 'bt'), ('gm', 'b'),
                  ('s', 'tb'), ('s', 'bt'), ('s', 'b'),
                  ('tb', 'bt'), ('tb', 'b'), ('bt', 'b'),
                  #single buffs
                  ('jr',), ('gm',), ('s',), ('tb',), ('bt',), ('b',)]

    def __init__(self, **kwargs):
        defaults = settings_data.get_default_settings(settings_data.rogue_settings)
        self.blade_flurry = kwargs.get('blade_flurry', defaults['blade_flurry'])
        self.between_the_eyes_policy = kwargs.get('between_the_eyes_policy', defaults['between_the_eyes_policy'])
        self.jolly_roger_reroll = int(kwargs.get('jolly_roger_reroll', defaults['jolly_roger_reroll']))
        self.grand_melee_reroll = int(kwargs.get('grand_melee_reroll', defaults['grand_melee_reroll']))
        self.shark_reroll = int(kwargs.get('shark_reroll', defaults['shark_reroll']))
        self.true_bearing_reroll = int(kwargs.get('true_bearing_reroll', defaults['true_bearing_reroll']))
        self.buried_treasure_reroll = int(kwargs.get('buried_treasure_reroll', defaults['buried_treasure_reroll']))
        self.broadsides_reroll = int(kwargs.get('broadsides_reroll', defaults['broadsides_reroll']))

        # RtB reroll thresholds, 0, 1, 2, 3
        # 0 means never reroll combos with this buff
        # 1 means reroll singles of buff
        # 2 means reroll doubles containing this buff
        # 3 means reroll triples containing this buff
        #build reroll lists here
        self.reroll_list = []
        self.keep_list = []
        for combo in self.rtb_combos:
            buffs = len(combo)
            if 'jr' in combo and buffs <= self.jolly_roger_reroll:
                self.reroll_list.append(combo)
                continue
            if 'gm' in combo and buffs <= self.grand_melee_reroll:
                self.reroll_list.append(combo)
                continue
            if 's' in combo and buffs <= self.shark_reroll:
                self.reroll_list.append(combo)
                continue
            if 'tb' in combo and buffs <= self.true_bearing_reroll:
                self.reroll_list.append(combo)
                continue
            if 'bt' in combo and buffs <= self.buried_treasure_reroll:
                self.reroll_list.append(combo)
                continue
            if 'b' in combo and buffs <= self.broadsides_reroll:
                self.reroll_list.append(combo)
                continue
            self.keep_list.append(combo)

class SubtletyCycle(Cycle):
    _cycle_type = 'subtlety'

    def __init__(self, **kwargs):
        defaults = settings_data.get_default_settings(settings_data.rogue_settings)
        self.cp_builder = kwargs.get('cp_builder', defaults['cp_builder'])
        self.symbols_policy = kwargs.get('symbols_policy', defaults['symbols_policy'])
        self.dance_finishers_allowed = kwargs.get('dance_finishers_allowed', defaults['dance_finishers_allowed'])
        self.compute_cp_waste = kwargs.get('compute_cp_waste', defaults['compute_cp_waste'])

        #Handle percent vs float automatically
        self.positional_uptime = int(kwargs.get('positional_uptime_percent', defaults['positional_uptime_percent'])) / 100
        self.positional_uptime = float(kwargs.get('positional_uptime', self.positional_uptime))
