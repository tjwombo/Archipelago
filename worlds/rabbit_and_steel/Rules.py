from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasGroup, Rule, HasGroupUnique, True_, HasFromListUnique, False_, CanReachRegion
from . import Items

from BaseClasses import ItemClassification
from .Options import KingdomSanity, ProgressiveRegions, UseKingdomOrderWithKingdomSanity, ClassSanity, RunType
from .Constants import OUTSKIRTS, GEODE, NEST, ARSENAL, DARKHOUSE, STREETS, LAKESIDE, DEPTHS, \
    AURUM, SANCTUM, KEEP, HALLWAY, PINNACLE, POOL, WIZARD, ASSASSIN, HEAVYBLADE, DANCER, DRUID, \
    SPELLSWORD, SNIPER, BRUISER, DEFENDER, ANCIENT, HAMMERMAID, PYROMANCER, GRENADIER, SHADOW, \
    kingdom_names, extra_kingdom_names, shira_defeat_names, witch_defeat_names

if TYPE_CHECKING:
    from .World import RabbitAndSteelWorld


def set_all_rules(world: RabbitAndSteelWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: RabbitAndSteelWorld) -> None:
    kingdom_sanity_is_off = OptionFilter(KingdomSanity, False)
    run_type = world.options.run_type
    progressive_regions_is_off = OptionFilter(ProgressiveRegions, False)
    excluded_kingdoms = world.options.excluded_kingdoms
    kingdom_sanity_kingdom_order = OptionFilter(UseKingdomOrderWithKingdomSanity, True)
    kingdom_sanity_kingdom_order_is_off = OptionFilter(UseKingdomOrderWithKingdomSanity, False)
    kingdom_order = world.options.kingdom_order
    max_kingdoms_per_run = world.options.max_kingdoms_per_run
    checks_per_class = world.options.checks_per_class
    class_sanity_is_off = OptionFilter(ClassSanity, False)

    # Require a class to be unlocked if playing on class sanity
    if OUTSKIRTS not in world.options.excluded_kingdoms:
        lobby_to_outskirts = world.get_entrance(world.origin_region_name + " to " + OUTSKIRTS)
        world.set_rule(lobby_to_outskirts, (kingdom_sanity_is_off | Has(OUTSKIRTS)) &
                       (class_sanity_is_off | HasGroup("Classes")))

    if GEODE not in world.options.excluded_kingdoms:
        lobby_to_geode = world.get_entrance(world.origin_region_name + " to " + GEODE)
        world.set_rule(lobby_to_geode, (kingdom_sanity_is_off | Has(GEODE)) &
                       (class_sanity_is_off | HasGroup("Classes")))

    def has_kingdom_sanity_items_to_reach_order(our_order: int, our_kingdom: str) -> Rule:
        if our_order == 0:
            return True_()
        rule = False_()
        for kingdom in [k for k, v in kingdom_order.items() if v == our_order]:
            if run_type != world.options.run_type.option_combined:
                if kingdom in kingdom_names and our_kingdom not in kingdom_names:
                    continue
                elif kingdom in extra_kingdom_names and our_kingdom not in extra_kingdom_names:
                    continue
            rule = rule | CanReachRegion(kingdom)
        return rule

    def set_kingdoms_connection_rules(kingdom: str) -> Rule:
        kingdom_check = (kingdom_sanity_is_off |
                         (Has(kingdom) & (has_kingdom_sanity_items_to_reach_order(kingdom_order[kingdom] - 1, kingdom)
                                          | kingdom_sanity_kingdom_order_is_off)))

        regions_required = 1
        if kingdom_sanity_is_off and kingdom_sanity_kingdom_order:
            regions_required = kingdom_order[kingdom]

        regions_check = progressive_regions_is_off | Has("Progressive Region", count=regions_required)

        return kingdom_check & regions_check

    kingdom_outskirts = None
    if OUTSKIRTS not in world.options.excluded_kingdoms:
        kingdom_outskirts = world.get_region(OUTSKIRTS)

    crack_in_the_geode = None
    if GEODE not in world.options.excluded_kingdoms:
        crack_in_the_geode = world.get_region(GEODE)

    if NEST not in excluded_kingdoms:
        if kingdom_outskirts is not None:
            outskirts_to_nest = world.get_entrance(OUTSKIRTS + " to " + NEST)
            world.set_rule(outskirts_to_nest, set_kingdoms_connection_rules(NEST))
        if crack_in_the_geode is not None and run_type == RunType.option_combined:
            geode_to_nest = world.get_entrance(GEODE + " to " + NEST)
            world.set_rule(geode_to_nest, set_kingdoms_connection_rules(NEST))

    if ARSENAL not in excluded_kingdoms:
        if kingdom_outskirts is not None:
            outskirts_to_arsenal = world.get_entrance(OUTSKIRTS + " to " + ARSENAL)
            world.set_rule(outskirts_to_arsenal, set_kingdoms_connection_rules(ARSENAL))
        if crack_in_the_geode is not None and run_type == RunType.option_combined:
            geode_to_arsenal = world.get_entrance(GEODE + " to " + ARSENAL)
            world.set_rule(geode_to_arsenal, set_kingdoms_connection_rules(ARSENAL))

    if DARKHOUSE not in excluded_kingdoms:
        if kingdom_outskirts is not None:
            outskirts_to_darkhouse = world.get_entrance(OUTSKIRTS + " to " + DARKHOUSE)
            world.set_rule(outskirts_to_darkhouse, set_kingdoms_connection_rules(DARKHOUSE))
        if crack_in_the_geode is not None and run_type == RunType.option_combined:
            geode_to_darkhouse = world.get_entrance(GEODE + " to " + DARKHOUSE)
            world.set_rule(geode_to_darkhouse, set_kingdoms_connection_rules(DARKHOUSE))

    if STREETS not in excluded_kingdoms:
        if kingdom_outskirts is not None:
            outskirts_to_streets = world.get_entrance(OUTSKIRTS + " to " + STREETS)
            world.set_rule(outskirts_to_streets, set_kingdoms_connection_rules(STREETS))
        if crack_in_the_geode is not None and run_type == RunType.option_combined:
            geode_to_streets = world.get_entrance(GEODE + " to " + STREETS)
            world.set_rule(geode_to_streets, set_kingdoms_connection_rules(STREETS))

    if LAKESIDE not in excluded_kingdoms:
        if kingdom_outskirts is not None:
            outskirts_to_lakeside = world.get_entrance(OUTSKIRTS + " to " + LAKESIDE)
            world.set_rule(outskirts_to_lakeside, set_kingdoms_connection_rules(LAKESIDE))
        if crack_in_the_geode is not None and run_type == RunType.option_combined:
            geode_to_lakeside = world.get_entrance(GEODE + " to " + LAKESIDE)
            world.set_rule(geode_to_lakeside, set_kingdoms_connection_rules(LAKESIDE))

    if DEPTHS not in excluded_kingdoms:
        if kingdom_outskirts is not None and run_type == RunType.option_combined:
            outskirts_to_depths = world.get_entrance(OUTSKIRTS + " to " + DEPTHS)
            world.set_rule(outskirts_to_depths, set_kingdoms_connection_rules(DEPTHS))
        if crack_in_the_geode is not None:
            geode_to_depths = world.get_entrance(GEODE + " to " + DEPTHS)
            world.set_rule(geode_to_depths, set_kingdoms_connection_rules(DEPTHS))

    if AURUM not in excluded_kingdoms:
        if kingdom_outskirts is not None and run_type == RunType.option_combined:
            outskirts_to_aurum = world.get_entrance(OUTSKIRTS + " to " + AURUM)
            world.set_rule(outskirts_to_aurum, set_kingdoms_connection_rules(AURUM))
        if crack_in_the_geode is not None:
            geode_to_aurum = world.get_entrance(GEODE + " to " + AURUM)
            world.set_rule(geode_to_aurum, set_kingdoms_connection_rules(AURUM))

    if SANCTUM not in excluded_kingdoms:
        if kingdom_outskirts is not None and run_type == RunType.option_combined:
            outskirts_to_sanctum = world.get_entrance(OUTSKIRTS + " to " + SANCTUM)
            world.set_rule(outskirts_to_sanctum, set_kingdoms_connection_rules(SANCTUM))
        if crack_in_the_geode is not None:
            geode_to_sanctum = world.get_entrance(GEODE + " to " + SANCTUM)
            world.set_rule(geode_to_sanctum, set_kingdoms_connection_rules(SANCTUM))

    # Set the entrance rule for starting kingdom to penultimate kingdom
    outskirts_to_keep = None
    geode_to_keep = None
    if KEEP not in excluded_kingdoms:
        if OUTSKIRTS not in excluded_kingdoms:
            outskirts_to_keep = world.get_entrance(OUTSKIRTS + " to " + KEEP)
        if GEODE not in excluded_kingdoms and run_type == RunType.option_combined:
            geode_to_keep = world.get_entrance(GEODE + " to " + KEEP)

    outskirts_to_hallway = None
    geode_to_hallway = None
    if HALLWAY not in excluded_kingdoms:
        if GEODE not in excluded_kingdoms:
            geode_to_hallway = world.get_entrance(GEODE + " to " + HALLWAY)
        if OUTSKIRTS not in excluded_kingdoms and run_type == RunType.option_combined:
            outskirts_to_hallway = world.get_entrance(OUTSKIRTS + " to " + HALLWAY)

    def set_penultimate_rules(kingdom) -> Rule:
        # Ensure the penultimate kingdom only counts kingdoms that are possible to show up on its route
        satisfies_run_type = False_()
        if world.options.run_type == world.options.run_type.option_combined:
            satisfies_run_type = HasGroupUnique("OrderedKingdoms", max_kingdoms_per_run + 0)
        elif kingdom == KEEP:
            satisfies_run_type = HasGroupUnique("BaseKingdoms", max_kingdoms_per_run + 0)
        elif kingdom == HALLWAY:
            satisfies_run_type = HasGroupUnique("ExtraKingdoms", max_kingdoms_per_run + 0)

        satisfies_kingdom_checks = (kingdom_sanity_is_off |
                                    (Has(kingdom) & kingdom_sanity_kingdom_order &
                                     has_kingdom_sanity_items_to_reach_order(max_kingdoms_per_run + 0, kingdom)) |
                                    (Has(kingdom) & kingdom_sanity_kingdom_order_is_off & satisfies_run_type))

        satisfies_progressive_checks = (progressive_regions_is_off |
                                        Has("Progressive Region", count=max_kingdoms_per_run + 1))

        return satisfies_kingdom_checks & satisfies_progressive_checks

    if outskirts_to_keep is not None:
        world.set_rule(outskirts_to_keep, set_penultimate_rules(KEEP))
    if geode_to_keep is not None:
        world.set_rule(geode_to_keep, set_penultimate_rules(KEEP))
    if outskirts_to_hallway is not None:
        world.set_rule(outskirts_to_hallway, set_penultimate_rules(HALLWAY))
    if geode_to_hallway is not None:
        world.set_rule(geode_to_hallway, set_penultimate_rules(HALLWAY))

    # Set the entrance rule for penultimate to ultimate kingdoms
    keep_to_pinnacle = None
    hallway_to_pinnacle = None
    if PINNACLE not in excluded_kingdoms:
        if KEEP not in excluded_kingdoms:
            keep_to_pinnacle = world.get_entrance(KEEP + " to " + PINNACLE)
        if HALLWAY not in excluded_kingdoms and run_type == RunType.option_combined:
            hallway_to_pinnacle = world.get_entrance(HALLWAY + " to " + PINNACLE)

    keep_to_pool = None
    hallway_to_pool = None
    if POOL not in excluded_kingdoms:
        if HALLWAY not in excluded_kingdoms:
            hallway_to_pool = world.get_entrance(HALLWAY + " to " + POOL)
        if KEEP not in excluded_kingdoms and run_type == RunType.option_combined:
            keep_to_pool = world.get_entrance(KEEP + " to " + POOL)

    def set_ultimate_rules(kingdom) -> Rule:
        kingdom_check = kingdom_sanity_is_off | Has(kingdom)

        progressive_check = progressive_regions_is_off | Has("Progressive Region", count=max_kingdoms_per_run + 2)

        return kingdom_check & progressive_check

    if keep_to_pinnacle is not None:
        world.set_rule(keep_to_pinnacle, set_ultimate_rules(PINNACLE))
    if hallway_to_pinnacle is not None:
        world.set_rule(hallway_to_pinnacle, set_ultimate_rules(PINNACLE))
    if keep_to_pool is not None:
        world.set_rule(keep_to_pool, set_ultimate_rules(POOL))
    if hallway_to_pool is not None:
        world.set_rule(hallway_to_pool, set_ultimate_rules(POOL))

    # Manually setting class rules, as it doesn't seem to work otherwise
    if WIZARD in checks_per_class:
        # Set the remaining kingdoms rules
        for kingdom_name in (Items.kingdom_names + Items.extra_kingdom_names):
            # Skip Moonlit Pinnacle and Reflecting Pool as it has special class rules
            if kingdom_name == PINNACLE or kingdom_name == POOL:
                continue

            if kingdom_name not in excluded_kingdoms:
                kingdom_to_class = world.get_entrance(kingdom_name + " - " + WIZARD)
                world.set_rule(kingdom_to_class, class_sanity_is_off | Has(WIZARD))

    if ASSASSIN in checks_per_class:
        # Set the remaining kingdoms rules
        for kingdom_name in (Items.kingdom_names + Items.extra_kingdom_names):
            # Skip Moonlit Pinnacle and Reflecting Pool as it has special class rules
            if kingdom_name == PINNACLE or kingdom_name == POOL:
                continue

            if kingdom_name not in excluded_kingdoms:
                kingdom_to_class = world.get_entrance(kingdom_name + " - " + ASSASSIN)
                world.set_rule(kingdom_to_class, class_sanity_is_off | Has(ASSASSIN))

    if HEAVYBLADE in checks_per_class:
        # Set the remaining kingdoms rules
        for kingdom_name in (Items.kingdom_names + Items.extra_kingdom_names):
            # Skip Moonlit Pinnacle and Reflecting Pool as it has special class rules
            if kingdom_name == PINNACLE or kingdom_name == POOL:
                continue

            if kingdom_name not in excluded_kingdoms:
                kingdom_to_class = world.get_entrance(kingdom_name + " - " + HEAVYBLADE)
                world.set_rule(kingdom_to_class, class_sanity_is_off | Has(HEAVYBLADE))

    if DANCER in checks_per_class:
        # Set the remaining kingdoms rules
        for kingdom_name in (Items.kingdom_names + Items.extra_kingdom_names):
            # Skip Moonlit Pinnacle and Reflecting Pool as it has special class rules
            if kingdom_name == PINNACLE or kingdom_name == POOL:
                continue

            if kingdom_name not in excluded_kingdoms:
                kingdom_to_class = world.get_entrance(kingdom_name + " - " + DANCER)
                world.set_rule(kingdom_to_class, class_sanity_is_off | Has(DANCER))

    if DRUID in checks_per_class:
        # Set the remaining kingdoms rules
        for kingdom_name in (Items.kingdom_names + Items.extra_kingdom_names):
            # Skip Moonlit Pinnacle and Reflecting Pool as it has special class rules
            if kingdom_name == PINNACLE or kingdom_name == POOL:
                continue

            if kingdom_name not in excluded_kingdoms:
                kingdom_to_class = world.get_entrance(kingdom_name + " - " + DRUID)
                world.set_rule(kingdom_to_class, class_sanity_is_off | Has(DRUID))

    if SPELLSWORD in checks_per_class:
        # Set the remaining kingdoms rules
        for kingdom_name in (Items.kingdom_names + Items.extra_kingdom_names):
            # Skip Moonlit Pinnacle and Reflecting Pool as it has special class rules
            if kingdom_name == PINNACLE or kingdom_name == POOL:
                continue

            if kingdom_name not in excluded_kingdoms:
                kingdom_to_class = world.get_entrance(kingdom_name + " - " + SPELLSWORD)
                world.set_rule(kingdom_to_class, class_sanity_is_off | Has(SPELLSWORD))

    if SNIPER in checks_per_class:
        # Set the remaining kingdoms rules
        for kingdom_name in (Items.kingdom_names + Items.extra_kingdom_names):
            # Skip Moonlit Pinnacle and Reflecting Pool as it has special class rules
            if kingdom_name == PINNACLE or kingdom_name == POOL:
                continue

            if kingdom_name not in excluded_kingdoms:
                kingdom_to_class = world.get_entrance(kingdom_name + " - " + SNIPER)
                world.set_rule(kingdom_to_class, class_sanity_is_off | Has(SNIPER))

    if BRUISER in checks_per_class:
        # Set the remaining kingdoms rules
        for kingdom_name in (Items.kingdom_names + Items.extra_kingdom_names):
            # Skip Moonlit Pinnacle and Reflecting Pool as it has special class rules
            if kingdom_name == PINNACLE or kingdom_name == POOL:
                continue

            if kingdom_name not in excluded_kingdoms:
                kingdom_to_class = world.get_entrance(kingdom_name + " - " + BRUISER)
                world.set_rule(kingdom_to_class, class_sanity_is_off | Has(BRUISER))

    if DEFENDER in checks_per_class:
        # Set the remaining kingdoms rules
        for kingdom_name in (Items.kingdom_names + Items.extra_kingdom_names):
            # Skip Moonlit Pinnacle and Reflecting Pool as it has special class rules
            if kingdom_name == PINNACLE or kingdom_name == POOL:
                continue

            if kingdom_name not in excluded_kingdoms:
                kingdom_to_class = world.get_entrance(kingdom_name + " - " + DEFENDER)
                world.set_rule(kingdom_to_class, class_sanity_is_off | Has(DEFENDER))

    if ANCIENT in checks_per_class:
        # Set the remaining kingdoms rules
        for kingdom_name in (Items.kingdom_names + Items.extra_kingdom_names):
            # Skip Moonlit Pinnacle and Reflecting Pool as it has special class rules
            if kingdom_name == PINNACLE or kingdom_name == POOL:
                continue

            if kingdom_name not in excluded_kingdoms:
                kingdom_to_class = world.get_entrance(kingdom_name + " - " + ANCIENT)
                world.set_rule(kingdom_to_class, class_sanity_is_off | Has(ANCIENT))

    if HAMMERMAID in checks_per_class:
        # Set the remaining kingdoms rules
        for kingdom_name in (Items.kingdom_names + Items.extra_kingdom_names):
            # Skip Moonlit Pinnacle and Reflecting Pool as it has special class rules
            if kingdom_name == PINNACLE or kingdom_name == POOL:
                continue

            if kingdom_name not in excluded_kingdoms:
                kingdom_to_class = world.get_entrance(kingdom_name + " - " + HAMMERMAID)
                world.set_rule(kingdom_to_class, class_sanity_is_off | Has(HAMMERMAID))

    if PYROMANCER in checks_per_class:
        # Set the remaining kingdoms rules
        for kingdom_name in (Items.kingdom_names + Items.extra_kingdom_names):
            # Skip Moonlit Pinnacle and Reflecting Pool as it has special class rules
            if kingdom_name == PINNACLE or kingdom_name == POOL:
                continue

            if kingdom_name not in excluded_kingdoms:
                kingdom_to_class = world.get_entrance(kingdom_name + " - " + PYROMANCER)
                world.set_rule(kingdom_to_class, class_sanity_is_off | Has(PYROMANCER))

    if GRENADIER in checks_per_class:
        # Set the remaining kingdoms rules
        for kingdom_name in (Items.kingdom_names + Items.extra_kingdom_names):
            # Skip Moonlit Pinnacle and Reflecting Pool as it has special class rules
            if kingdom_name == PINNACLE or kingdom_name == POOL:
                continue

            if kingdom_name not in excluded_kingdoms:
                kingdom_to_class = world.get_entrance(kingdom_name + " - " + GRENADIER)
                world.set_rule(kingdom_to_class, class_sanity_is_off | Has(GRENADIER))

    if SHADOW in checks_per_class:
        # Set the remaining kingdoms rules
        for kingdom_name in (Items.kingdom_names + Items.extra_kingdom_names):
            # Skip Moonlit Pinnacle and Reflecting Pool as it has special class rules
            if kingdom_name == PINNACLE or kingdom_name == POOL:
                continue

            if kingdom_name not in excluded_kingdoms:
                kingdom_to_class = world.get_entrance(kingdom_name + " - " + SHADOW)
                world.set_rule(kingdom_to_class, class_sanity_is_off | Has(SHADOW))

    # Find the classes that will have checks in the last kingdom
    class_checks_for_boss = [class_names for class_names in Items.class_names
                             if class_names not in world.options.exclude_class.value]
    # TODO: Use below if finishing runs aren't a goal condition
    # class_checks_for_boss = world.options.checks_per_class

    if PINNACLE not in excluded_kingdoms:
        for moonlit_class in class_checks_for_boss:
            class_moonlit = world.get_entrance(PINNACLE + " - " + moonlit_class)
            world.set_rule(class_moonlit, class_sanity_is_off | Has(moonlit_class))

    if POOL not in excluded_kingdoms:
        for moonlit_class in class_checks_for_boss:
            class_moonlit = world.get_entrance(POOL + " - " + moonlit_class)
            world.set_rule(class_moonlit, class_sanity_is_off | Has(moonlit_class))


def set_all_location_rules(world: RabbitAndSteelWorld) -> None:
    # TODO: MAKE THESE EVENT ITEMS
    if world.options.goal_condition == world.options.goal_condition.option_shira or \
            world.options.goal_condition == world.options.goal_condition.option_both:
        for class_name in Items.class_names:
            if class_name in world.options.exclude_class:
                continue
            class_victory = world.get_location("Shira - " + class_name)
            class_item = Items.RabbitAndSteelItem("Shira Defeat - " + class_name, ItemClassification.progression,
                                                  Items.shira_defeat_items["Shira Defeat - " + class_name],
                                                  world.player)
            class_victory.place_locked_item(class_item)
    if world.options.goal_condition == world.options.goal_condition.option_witch or \
            world.options.goal_condition == world.options.goal_condition.option_both:
        for class_name in Items.class_names:
            if class_name in world.options.exclude_class:
                continue
            class_victory = world.get_location("Witch - " + class_name)
            class_item = Items.RabbitAndSteelItem("Witch Defeat - " + class_name, ItemClassification.progression,
                                                  Items.witch_defeat_items["Witch Defeat - " + class_name],
                                                  world.player)
            class_victory.place_locked_item(class_item)


def set_completion_condition(world: RabbitAndSteelWorld) -> None:
    goal = world.options.goal_condition

    victory = world.get_location("Victory")

    if goal == world.options.goal_condition.option_shira:
        shira_defeats = world.options.shira_defeats.value

        world.set_rule(victory, HasFromListUnique(*shira_defeat_names, count=shira_defeats))
    elif goal == world.options.goal_condition.option_witch:
        witch_defeats = world.options.witch_defeats.value

        world.set_rule(victory, HasFromListUnique(*witch_defeat_names, count=witch_defeats))
    elif goal == world.options.goal_condition.option_both:
        shira_defeats = world.options.shira_defeats.value
        witch_defeats = world.options.witch_defeats.value

        world.set_rule(victory, HasFromListUnique(*shira_defeat_names, count=shira_defeats) &
                       HasFromListUnique(*witch_defeat_names, count=witch_defeats))

    world.set_completion_rule(Has("Victory"))
