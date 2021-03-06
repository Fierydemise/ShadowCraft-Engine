from builtins import object
from shadowcraft.core import exceptions
from shadowcraft.objects import proc_data
from shadowcraft.objects import class_data

import sys, traceback

import gettext
_ = gettext.gettext

class InvalidProcException(exceptions.InvalidInputException):
    pass


class Proc(object):
    def __init__(self, stat, value, duration, proc_name, max_stacks=1, can_crit=True, stats=None, upgradable=False, scaling=None,
                 buffs=None, base_value=0, type='rppm', icd=0, proc_rate=1.0, trigger='all_attacks', haste_scales=False, item_level=1,
                 on_crit=False, on_procced_strikes=True, proc_rate_modifier=1., source='generic', att_spd_scales=False,
                 ap_coefficient=0., dmg_school=None, crm_scales=False, aoe=False, dot_ticks=1, dot_initial_tick=False):
        self.stat = stat
        if stats is not None:
            self.stats = set(stats)
        self.value = value
        self.base_value = base_value
        self.buffs = buffs
        self.can_crit = can_crit
        self.duration = duration
        self.max_stacks = max_stacks
        self.upgradable = upgradable
        self.scaling = scaling
        self.proc_name = proc_name
        self.proc_type = type
        self.icd = icd
        self.type = type
        self.source = source
        self.proc_rate = proc_rate
        self.trigger = trigger
        self.haste_scales = haste_scales
        self.att_spd_scales = att_spd_scales
        self.item_level = item_level
        self.on_crit = on_crit
        self.on_procced_strikes = on_procced_strikes
        self.proc_rate_modifier = proc_rate_modifier
        self.ap_coefficient = ap_coefficient
        self.dmg_school = dmg_school
        self.crm_scales = crm_scales
        self.aoe = aoe
        self.dot_ticks = dot_ticks
        self.dot_initial_tick = dot_initial_tick

        if self.dmg_school is None and stat in ['physical_damage', 'physical_dot']:
            self.dmg_school = 'physical'

        #separate method just to keep the constructor clean
        self.update_proc_value()

    def update_proc_value(self):
        tools = class_data.Util()
        #http://forums.elitistjerks.com/topic/130561-shadowcraft-for-mists-of-pandaria/page-3
        #see above for stat value initialization
        #not sure if this is the correct way to handle damage procs. Most seem to have both disabled scaling and raw value or both enabled scaling and an {object:value},
        #they should probably all use the same notation either way. If we want both, the scaling property should probably be set by value property instead of manually configured.
        #the other option is to always handle it deeper into the calc module, but that is coupling object responsibilities and not ideal.
        if self.scaling and self.source in ('trinket',):
            crm = tools.get_combat_rating_multiplier(self.item_level) if self.crm_scales else 1. # apply combat rating modifier
            scaled_value = round(self.scaling * tools.get_random_prop_point(self.item_level) * crm)
            if hasattr(self.value,'__iter__'): #handle object value
                for e in self.value:
                    self.value[e] = scaled_value
            else: #handle raw value
                self.value = scaled_value

    def procs_off_auto_attacks(self):
        if self.trigger in ('all_attacks', 'auto_attacks', 'all_spells_and_attacks', 'all_melee_attacks'):
            return True
        else:
            return False

    def procs_off_strikes(self):
        if self.trigger in ('all_attacks', 'strikes', 'all_spells_and_attacks', 'all_melee_attacks'):
            return True
        else:
            return False

    def procs_off_harmful_spells(self):
        if self.trigger in ('all_spells', 'damaging_spells', 'all_spells_and_attacks'):
            return True
        else:
            return False

    def procs_off_heals(self):
        if self.trigger in ('all_spells', 'healing_spells', 'all_spells_and_attacks'):
            return True
        else:
            return False

    def procs_off_periodic_spell_damage(self):
        if self.trigger in ('all_periodic_damage', 'periodic_spell_damage'):
            return True
        else:
            return False

    def procs_off_periodic_heals(self):
        if self.trigger == 'hots':
            return True
        else:
            return False

    def procs_off_bleeds(self):
        if self.trigger in ('all_periodic_damage', 'bleeds'):
            return True
        else:
            return False

    def procs_off_crit_only(self):
        if self.on_crit:
            return True
        else:
            return False

    def procs_off_apply_debuff(self):
        if self.trigger in ('all_spells_and_attacks', 'all_attacks', 'all_melee_attacks'):
            return True
        else:
            return False

    def procs_off_procced_strikes(self):
        if self.on_procced_strikes:
            return True
        else:
            return False

    def get_base_proc_rate_for_spec(self, spec):
        proc_rate = self.proc_rate
        if hasattr(self.proc_rate,'__iter__'): # list of proc rates by spec
            if not spec:
                raise InvalidProcException(_('Spec expected for the proc rate of {proc}').format(proc=self.proc_name))
            if not spec in self.proc_rate:
                if 'other' in self.proc_rate:
                    spec = 'other'
                else:
                    raise InvalidProcException(_('Proc rate of {proc} not found for current spec').format(proc=self.proc_name))
            proc_rate = self.proc_rate[spec]
        return proc_rate

    def get_rppm_proc_rate(self, haste=1., spec=None):
        if not self.haste_scales: #Failsafe to allow passing haste for non-scling procs
            haste = 1.
        if self.is_real_ppm():
            proc_rate = self.get_base_proc_rate_for_spec(spec)
            return haste * proc_rate * self.proc_rate_modifier
        raise InvalidProcException(_('Invalid proc handling for proc {proc}').format(proc=self.proc_name))

    def get_proc_rate(self, speed=None, haste=1.0, spec=None):
        proc_rate = self.get_base_proc_rate_for_spec(spec)
        if self.is_ppm():
            if speed is None:
                raise InvalidProcException(_('Weapon speed needed to calculate the proc rate of {proc}').format(proc=self.proc_name))
            else:
                return proc_rate * speed / 60.
        elif self.is_real_ppm():
            return haste * proc_rate / 60.
        else:
            return proc_rate

    def is_ppm(self):
        if self.type == 'ppm':
            return True
        else:
            return False
        # probably should configure this somehow, but type check is probably enough
        raise InvalidProcException(_('Invalid data for proc {proc}').format(proc=self.proc_name))

    def is_rppm(self):
        return self.is_real_ppm()
    def is_real_ppm(self):
        if self.type == 'rppm':
            return True
        else:
            return False
        # probably should configure this somehow, but type check is probably enough
        raise InvalidProcException(_('Invalid data for proc {proc}').format(proc=self.proc_name))

class ProcsList(object):
    allowed_procs = proc_data.allowed_procs

    def __init__(self, *args):
        for arg in args:
            if not isinstance(arg, (list,tuple)):
                arg = (arg,100)
            if arg[0] in self.allowed_procs:
                proc_data = self.allowed_procs[arg[0]]
                proc_data['item_level'] = arg[1]
                setattr(self, arg[0], Proc(**proc_data))
            else:
                raise InvalidProcException(_('No data for proc {proc}').format(proc=arg[0]))

    def set_proc(self, proc):
        setattr(self, proc, Proc(**self.allowed_procs[proc]))

    def del_proc(self, proc):
        setattr(self, proc, False)

    def __getattr__(self, proc):
        # Any proc we haven't assigned a value to, we don't have.
        if proc in self.allowed_procs:
            return False
        object.__getattribute__(self, proc)

    def get_all_procs_for_stat(self, stat=None):
        procs = []
        for proc_name in self.allowed_procs:
            proc = getattr(self, proc_name)
            if proc:
                if stat is None:
                    procs.append(proc)
                elif proc.stat in ('stats', 'highest', 'random') and stat in proc.value:
                    procs.append(proc)
        return procs

    def get_all_damage_procs(self):
        procs = []
        for proc_name in self.allowed_procs:
            proc = getattr(self, proc_name)
            if proc:
                if proc.stat in ('spell_damage', 'physical_damage', 'physical_dot', 'spell_dot'):
                    procs.append(proc)

        return procs
