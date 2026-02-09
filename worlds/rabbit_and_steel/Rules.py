from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasGroup, Rule, HasGroupUnique, True_, HasAny, HasFromListUnique
from . import Items
from BaseClasses import ItemClassification
from .Items import class_names, shira_defeat_names
from .Options import KingdomSanity, ProgressiveRegions, UseKingdomOrderWithKingdomSanity, ClassSanity

if TYPE_CHECKING:
    from .World import RabbitAndSteelWorld

NEST = "Scholar's Nest"
ARSNEAL = "King's Arsenal"
DARKHOUSE = "Red Darkhouse"
STREETS = "Churchmouse Streets"
LAKESIDE = "Emerald Lakeside"
KEEP = "The Pale Keep"
PINNACLE = "Moonlit Pinnacle"

WIZARD = "Wizard"
ASSASSIN = "Assassin"
HEAVYBLADE = "Heavyblade"
DANCER = "Dancer"
DRUID = "Druid"
SPELLSWORD = "Spellsword"
SNIPER = "Sniper"
BRUISER = "Bruiser"
DEFENDER = "Defender"
ANCIENT = "Ancient"


def set_all_rules(world: RabbitAndSteelWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: RabbitAndSteelWorld) -> None:
    kingdom_sanity_is_off = OptionFilter(KingdomSanity, False)
    progressive_regions_is_off = OptionFilter(ProgressiveRegions, False)
    excluded_kingdoms = world.options.excluded_kingdoms
    kingdom_sanity_kingdom_order = OptionFilter(UseKingdomOrderWithKingdomSanity, True)
    kingdom_sanity_kingdom_order_is_off = OptionFilter(UseKingdomOrderWithKingdomSanity, False)
    kingdom_order = world.options.kingdom_order
    max_kingdoms_per_run = world.options.max_kingdoms_per_run
    checks_per_class = world.options.checks_per_class
    class_sanity_is_off = OptionFilter(ClassSanity, False)

    # Require a class to be unlocked if playing on class sanity
    lobby_to_outskirts = world.get_entrance("Lobby to Kingdom Outskirts")
    world.set_rule(lobby_to_outskirts, class_sanity_is_off | HasGroup("Classes"))

    def has_kingdom_sanity_items_to_reach_order(our_order: int) -> Rule:
        if our_order <= 1:
            return True_()
        kingdoms_of_order = []
        for (kingdom, order) in kingdom_order.items():
            if kingdom in excluded_kingdoms or order == -1:
                continue
            if order >= our_order:
                continue
            if order == our_order:
                kingdoms_of_order += [kingdom]
        return HasAny(*kingdoms_of_order) & has_kingdom_sanity_items_to_reach_order(our_order-1)

    def set_kingdoms_connection_rules(kingdom: str) -> Rule:
        satisfies_kingdom_checks = (kingdom_sanity_is_off |
                                    (Has(kingdom) & has_kingdom_sanity_items_to_reach_order(kingdom_order[kingdom])) |
                                    (Has(kingdom) & kingdom_sanity_kingdom_order_is_off))
        '''
        if kingdom_sanity:
            if not state.has(kingdom, world.player):
                return False

            if kingdom_sanity_kingdom_order and not has_kingdom_sanity_items_to_reach_order(state, kingdom_order[kingdom]):
                return False
                
        kingdom_sanity -> 
            !Has(kingdom) -> False
            (kingdom_sanity_kingdom_order & !has_kingdom_sanity_items_to_reach_order) -> False

        !A | (B & D) | (B & !C)
        '''

        regions_required = 1
        if kingdom_sanity_is_off or not kingdom_sanity_kingdom_order_is_off:
            regions_required = kingdom_order[kingdom]

        satisfies_progressive_checks = progressive_regions_is_off | Has("Progressive Region", count=regions_required)

        return satisfies_kingdom_checks & satisfies_progressive_checks

    if NEST not in excluded_kingdoms:
        outskirts_to_nest = world.get_entrance("Kingdom Outskirts to " + NEST)
        world.set_rule(outskirts_to_nest, set_kingdoms_connection_rules(NEST))

    if ARSNEAL not in excluded_kingdoms:
        outskirts_to_king = world.get_entrance("Kingdom Outskirts to " + ARSNEAL)
        world.set_rule(outskirts_to_king, set_kingdoms_connection_rules(ARSNEAL))

    if DARKHOUSE not in excluded_kingdoms:
        outskirts_to_red = world.get_entrance("Kingdom Outskirts to " + DARKHOUSE)
        world.set_rule(outskirts_to_red, set_kingdoms_connection_rules(DARKHOUSE))

    if STREETS not in excluded_kingdoms:
        outskirts_to_churchmouse = world.get_entrance("Kingdom Outskirts to " + STREETS)
        world.set_rule(outskirts_to_churchmouse, set_kingdoms_connection_rules(STREETS))

    if LAKESIDE not in excluded_kingdoms:
        outskirts_to_emerald = world.get_entrance("Kingdom Outskirts to " + LAKESIDE)
        world.set_rule(outskirts_to_emerald, set_kingdoms_connection_rules(LAKESIDE))

    # Set the entrance rule for kingdom outskirts to The Pale Keep
    outskirts_to_pale = world.get_entrance("Kingdom Outskirts to " + KEEP)

    def set_pale_keep_rules() -> Rule:
        satisfies_kingdom_checks = (kingdom_sanity_is_off |
           (Has(KEEP) & kingdom_sanity_kingdom_order & has_kingdom_sanity_items_to_reach_order(max_kingdoms_per_run + 1)) |
           (Has(KEEP) & kingdom_sanity_kingdom_order_is_off & HasGroupUnique("Kingdoms", max_kingdoms_per_run + 0)))
        '''
        if kingdom_sanity:
            if not state.has(KEEP, world.player):
                return False

            if kingdom_sanity_kingdom_order and not has_kingdom_sanity_items_to_reach_order(state, max_kingdoms_per_run + 1):
                return False

            if not kingdom_sanity_kingdom_order and not state.has_group_unique("Kingdoms", world.player, max_kingdoms_per_run + 0):
                return False
                
        kingdom_sanity ->
            !Has(KEEP) -> False
            (kingdom_sanity_kingdom_order & !has_kingdom_sanity_items_to_reach_order) -> False
            (!kingdom_sanity_kingdom_oredr & !HasGroupUnique("kingdoms") -> False
            
        !A | (B & C & D) | (B & E & !C)
        '''

        satisfies_progressive_checks = (progressive_regions_is_off |
                                        Has("Progressive Region", count=max_kingdoms_per_run + 1))

        return satisfies_kingdom_checks & satisfies_progressive_checks

    world.set_rule(outskirts_to_pale, set_pale_keep_rules())

    # Set the entrance rule for The Pale Keep to the Moonlit Pinnacle
    pale_to_moonlit = world.get_entrance(KEEP + " to " + PINNACLE)

    def set_moonlit_pinnacle_rules() -> Rule:
        satisfies_kingdom_checks = kingdom_sanity_is_off | Has(PINNACLE)

        satisfies_progressive_checks = progressive_regions_is_off | Has("Progressive Region", count=max_kingdoms_per_run + 2)

        return satisfies_kingdom_checks & satisfies_progressive_checks

    world.set_rule(pale_to_moonlit, set_moonlit_pinnacle_rules())

    # Manually setting class rules, as it doesn't seem to work otherwise
    if WIZARD in checks_per_class:
        outskirts_to_class = world.get_entrance("Kingdom Outskirts - " + WIZARD)
        world.set_rule(outskirts_to_class, class_sanity_is_off | Has(WIZARD))

        # Set the remaining kingdoms rules
        for kingdom_name in Items.kingdom_names:
            # Skip Moonlit Pinnacle as it has special class rules
            if kingdom_name == PINNACLE:
                continue

            if kingdom_name not in excluded_kingdoms:
                kingdom_to_class = world.get_entrance(kingdom_name + " - " + WIZARD)
                world.set_rule(kingdom_to_class, class_sanity_is_off | Has(WIZARD))

    if ASSASSIN in checks_per_class:
        outskirts_to_class = world.get_entrance("Kingdom Outskirts - " + ASSASSIN)
        world.set_rule(outskirts_to_class, class_sanity_is_off | Has(ASSASSIN))

        # Set the remaining kingdoms rules
        for kingdom_name in Items.kingdom_names:
            # Skip Moonlit Pinnacle as it has special class rules
            if kingdom_name == PINNACLE:
                continue

            if kingdom_name not in excluded_kingdoms:
                kingdom_to_class = world.get_entrance(kingdom_name + " - " + ASSASSIN)
                world.set_rule(kingdom_to_class, class_sanity_is_off | Has(ASSASSIN))

    if HEAVYBLADE in checks_per_class:
        outskirts_to_class = world.get_entrance("Kingdom Outskirts - " + HEAVYBLADE)
        world.set_rule(outskirts_to_class, class_sanity_is_off | Has(HEAVYBLADE))

        # Set the remaining kingdoms rules
        for kingdom_name in Items.kingdom_names:
            # Skip Moonlit Pinnacle as it has special class rules
            if kingdom_name == PINNACLE:
                continue

            if kingdom_name not in excluded_kingdoms:
                kingdom_to_class = world.get_entrance(kingdom_name + " - " + HEAVYBLADE)
                world.set_rule(kingdom_to_class, class_sanity_is_off | Has(HEAVYBLADE))

    if DANCER in checks_per_class:
        outskirts_to_class = world.get_entrance("Kingdom Outskirts - " + DANCER)
        world.set_rule(outskirts_to_class, class_sanity_is_off | Has(DANCER))

        # Set the remaining kingdoms rules
        for kingdom_name in Items.kingdom_names:
            # Skip Moonlit Pinnacle as it has special class rules
            if kingdom_name == PINNACLE:
                continue

            if kingdom_name not in excluded_kingdoms:
                kingdom_to_class = world.get_entrance(kingdom_name + " - " + DANCER)
                world.set_rule(kingdom_to_class, class_sanity_is_off | Has(DANCER))

    if DRUID in checks_per_class:
        outskirts_to_class = world.get_entrance("Kingdom Outskirts - " + DRUID)
        world.set_rule(outskirts_to_class, class_sanity_is_off | Has(DRUID))

        # Set the remaining kingdoms rules
        for kingdom_name in Items.kingdom_names:
            # Skip Moonlit Pinnacle as it has special class rules
            if kingdom_name == PINNACLE:
                continue

            if kingdom_name not in excluded_kingdoms:
                kingdom_to_class = world.get_entrance(kingdom_name + " - " + DRUID)
                world.set_rule(kingdom_to_class, class_sanity_is_off | Has(DRUID))

    if SPELLSWORD in checks_per_class:
        outskirts_to_class = world.get_entrance("Kingdom Outskirts - " + SPELLSWORD)
        world.set_rule(outskirts_to_class, class_sanity_is_off | Has(SPELLSWORD))

        # Set the remaining kingdoms rules
        for kingdom_name in Items.kingdom_names:
            # Skip Moonlit Pinnacle as it has special class rules
            if kingdom_name == PINNACLE:
                continue

            if kingdom_name not in excluded_kingdoms:
                kingdom_to_class = world.get_entrance(kingdom_name + " - " + SPELLSWORD)
                world.set_rule(kingdom_to_class, class_sanity_is_off | Has(SPELLSWORD))

    if SNIPER in checks_per_class:
        outskirts_to_class = world.get_entrance("Kingdom Outskirts - " + SNIPER)
        world.set_rule(outskirts_to_class, class_sanity_is_off | Has(SNIPER))

        # Set the remaining kingdoms rules
        for kingdom_name in Items.kingdom_names:
            # Skip Moonlit Pinnacle as it has special class rules
            if kingdom_name == PINNACLE:
                continue

            if kingdom_name not in excluded_kingdoms:
                kingdom_to_class = world.get_entrance(kingdom_name + " - " + SNIPER)
                world.set_rule(kingdom_to_class, class_sanity_is_off | Has(SNIPER))

    if BRUISER in checks_per_class:
        outskirts_to_class = world.get_entrance("Kingdom Outskirts - " + BRUISER)
        world.set_rule(outskirts_to_class, class_sanity_is_off | Has(BRUISER))

        # Set the remaining kingdoms rules
        for kingdom_name in Items.kingdom_names:
            # Skip Moonlit Pinnacle as it has special class rules
            if kingdom_name == PINNACLE:
                continue

            if kingdom_name not in excluded_kingdoms:
                kingdom_to_class = world.get_entrance(kingdom_name + " - " + BRUISER)
                world.set_rule(kingdom_to_class, class_sanity_is_off | Has(BRUISER))

    if DEFENDER in checks_per_class:
        outskirts_to_class = world.get_entrance("Kingdom Outskirts - " + DEFENDER)
        world.set_rule(outskirts_to_class, class_sanity_is_off | Has(DEFENDER))

        # Set the remaining kingdoms rules
        for kingdom_name in Items.kingdom_names:
            # Skip Moonlit Pinnacle as it has special class rules
            if kingdom_name == PINNACLE:
                continue

            if kingdom_name not in excluded_kingdoms:
                kingdom_to_class = world.get_entrance(kingdom_name + " - " + DEFENDER)
                world.set_rule(kingdom_to_class, class_sanity_is_off | Has(DEFENDER))

    if ANCIENT in checks_per_class:
        outskirts_to_class = world.get_entrance("Kingdom Outskirts - " + ANCIENT)
        world.set_rule(outskirts_to_class, class_sanity_is_off | Has(ANCIENT))

        # Set the remaining kingdoms rules
        for kingdom_name in Items.kingdom_names:
            # Skip Moonlit Pinnacle as it has special class rules
            if kingdom_name == PINNACLE:
                continue

            if kingdom_name not in excluded_kingdoms:
                kingdom_to_class = world.get_entrance(kingdom_name + " - " + ANCIENT)
                world.set_rule(kingdom_to_class, class_sanity_is_off | Has(ANCIENT))

    # Find the classes that will have checks in the Moonlit Pinnacle
    moonlit_classes = []
    if world.options.goal_condition == world.options.goal_condition.option_shira:
        moonlit_classes = class_names
    elif world.options.checks_per_class:
        moonlit_classes = world.options.checks_per_class

    for moonlit_class in moonlit_classes:
        class_moonlit = world.get_entrance("Moonlit Pinnacle - " + moonlit_class)
        world.set_rule(class_moonlit, class_sanity_is_off | Has(moonlit_class))


def set_all_location_rules(world: RabbitAndSteelWorld) -> None:
    if world.options.goal_condition == world.options.goal_condition.option_shira:
        for class_name in Items.class_names:
            if class_name in world.options.exclude_class:
                continue
            class_victory = world.get_location("Shira - " + class_name)
            class_item = Items.RabbitAndSteelItem("Victory - " + class_name, ItemClassification.progression,
                                                  Items.shira_defeat_items["Victory - " + class_name], world.player)
            class_victory.place_locked_item(class_item)


def set_completion_condition(world: RabbitAndSteelWorld) -> None:
    goal = world.options.goal_condition

    victory = world.get_location("Victory")

    if goal == world.options.goal_condition.option_shira:
        shira_defeats = world.options.shira_defeats.value

        world.set_rule(victory, HasFromListUnique(*shira_defeat_names, count=shira_defeats))

    world.set_completion_rule(Has("Victory"))
