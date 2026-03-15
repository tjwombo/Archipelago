from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location
from . import Items
from .Constants import WIZARD, ASSASSIN, HEAVYBLADE, DANCER, DRUID, SPELLSWORD, SNIPER, BRUISER, \
                DEFENDER, ANCIENT, HAMMERMAID, PYROMANCER, GRENADIER, SHADOW, OUTSKIRTS, NEST, ARSNEAL, \
                DARKHOUSE, STREETS, LAKESIDE, KEEP, PINNACLE, GEODE, DEPTHS, AURUM, SANCTUM, HALLWAY, POOL

if TYPE_CHECKING:
    from .World import RabbitAndSteelWorld


class RabbitAndSteelLocation(Location):
    game: str = "Rabbit and Steel"


def create_all_locations(world: RabbitAndSteelWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: RabbitAndSteelWorld) -> None:
    # Create the base kingdom locations
    kingdom_outskirts = None
    if OUTSKIRTS not in world.options.excluded_kingdoms:
        kingdom_outskirts = world.get_region(OUTSKIRTS)
        kingdom_outskirts.add_locations(kingdom_outskirts_table, RabbitAndSteelLocation)

    # Add the generic locations for the 5 main kingdoms
    for kingdom, locations in kingdom_to_locations.items():
        if kingdom not in world.options.excluded_kingdoms:
            kingdom_region = world.get_region(kingdom)
            kingdom_region.add_locations(locations, RabbitAndSteelLocation)

    if KEEP not in world.options.excluded_kingdoms:
        pale_keep = world.get_region(KEEP)
        pale_keep.add_locations(pale_keep_table, RabbitAndSteelLocation)

    if PINNACLE not in world.options.excluded_kingdoms:
        moonlit_pinnacle = world.get_region(PINNACLE)
        moonlit_pinnacle.add_locations(moonlit_pinnacle_table, RabbitAndSteelLocation)

    # Create the extra kingdom locations
    crack_in_the_geode = None
    if GEODE not in world.options.excluded_kingdoms:
        crack_in_the_geode = world.get_region(GEODE)
        crack_in_the_geode.add_locations(crack_in_the_geode_table, RabbitAndSteelLocation)

    # Add the generic locations for the 3 main extra kingdoms
    for kingdom, locations in extra_kingdom_to_locations.items():
        if kingdom not in world.options.excluded_kingdoms:
            kingdom_region = world.get_region(kingdom)
            kingdom_region.add_locations(locations, RabbitAndSteelLocation)

    if HALLWAY not in world.options.excluded_kingdoms:
        looping_hallway = world.get_region(HALLWAY)
        looping_hallway.add_locations(looping_hallway_table, RabbitAndSteelLocation)

    if POOL not in world.options.excluded_kingdoms:
        reflecting_pool = world.get_region(POOL)
        reflecting_pool.add_locations(reflecting_pool_table, RabbitAndSteelLocation)

    # Add the class specific locations for all the kingdoms, except for the last kingdoms
    if world.options.checks_per_class:
        for class_name in world.options.checks_per_class:
            class_table = class_tables[class_name]

            for kingdom in class_table:
                # Skip Moonlit Pinnacle and Reflecting Pool as there are cases where more or less characters have
                # checks there
                if kingdom == PINNACLE or kingdom == POOL:
                    continue

                if kingdom not in world.options.excluded_kingdoms:
                    class_kingdom = world.get_region(kingdom + " - " + class_name)
                    class_kingdom.add_locations(class_table[kingdom], RabbitAndSteelLocation)

    # Find the classes that will have checks in the last kingdom
    class_checks_for_boss = Items.class_names
    # TODO: Use below if finishing runs aren't a goal condition
    # class_checks_for_boss = world.options.checks_per_class

    # Add the class locations for the Moonlit Pinnacle
    if PINNACLE not in world.options.excluded_kingdoms:
        if world.options.goal_condition == world.options.goal_condition.option_shira or \
                world.options.goal_condition == world.options.goal_condition.option_both:
            for class_name in class_checks_for_boss:
                if class_name in world.options.exclude_class:
                    continue
                class_moonlit = world.get_region(PINNACLE + " - " + class_name)
                class_moonlit.add_locations(class_tables[class_name][PINNACLE], RabbitAndSteelLocation)

    # Add the class locations for the Reflecting Pool
    if POOL not in world.options.excluded_kingdoms:
        if world.options.goal_condition == world.options.goal_condition.option_witch or \
                world.options.goal_condition == world.options.goal_condition.option_both:
            for class_name in class_checks_for_boss:
                if class_name in world.options.exclude_class:
                    continue
                class_pool = world.get_region(POOL + " - " + class_name)
                class_pool.add_locations(class_tables[class_name][POOL], RabbitAndSteelLocation)

    # Add the locations for the checks in a chest
    if world.options.checks_per_item_in_chest:
        if OUTSKIRTS not in world.options.excluded_kingdoms:
            kingdom_outskirts.add_locations(kingdom_outskirts_chest_item_table, RabbitAndSteelLocation)

        if GEODE not in world.options.excluded_kingdoms:
            crack_in_the_geode.add_locations(crack_in_the_geode_chest_item_table, RabbitAndSteelLocation)

        # Add the chests in the remaining kingdoms
        for kingdom_name, chest_table in kingdom_to_chest_locations.items():
            if kingdom_name not in world.options.excluded_kingdoms:
                kingdom_region = world.get_region(kingdom_name)
                kingdom_region.add_locations(chest_table)

    # Add the locations for the checks in a shop
    if world.options.shop_sanity == world.options.shop_sanity.option_global:
        shop_region = world.get_region("Shops")
        shop_region.add_locations(global_shop_table)
    elif world.options.shop_sanity == world.options.shop_sanity.option_regional:
        for kingdom_name, chest_table in kingdom_to_shop_locations.items():
            if kingdom_name not in world.options.excluded_kingdoms:
                kingdom_region = world.get_region(kingdom_name)
                kingdom_region.add_locations(chest_table)


def create_events(world: RabbitAndSteelWorld) -> None:
    if PINNACLE not in world.options.excluded_kingdoms:
        moonlit_pinnacle = world.get_region(PINNACLE)
        moonlit_pinnacle.add_event("Shira Spell Broken", location_type=RabbitAndSteelLocation,
                                   item_type=Items.RabbitAndSteelItem)

    if POOL not in world.options.excluded_kingdoms:
        reflecting_pool = world.get_region(POOL)
        reflecting_pool.add_event("Witch Spell Broken", location_type=RabbitAndSteelLocation,
                                  item_type=Items.RabbitAndSteelItem)

    lobby = world.get_region(world.origin_region_name)
    lobby.add_event("Victory", location_type=RabbitAndSteelLocation, item_type=Items.RabbitAndSteelItem)


location_id = 1

# Locations that should be awarded during the run through Kingdom Outskirts
outskirts_locations = [OUTSKIRTS + " Battle 1", OUTSKIRTS + " Chest 1", OUTSKIRTS + " Battle 2",
                       OUTSKIRTS + " Chest 2", OUTSKIRTS + " Battle 3"]
kingdom_outskirts_table = {}
for location in outskirts_locations:
    kingdom_outskirts_table[location] = location_id
    location_id += 1

# Locations that should be awarded during the run through Crack In The Geode
geode_locations = [GEODE + " Battle 1", GEODE + " Chest 1", GEODE + " Battle 2",
                   GEODE + " Chest 2", GEODE + " Battle 3"]
crack_in_the_geode_table = {}
for location in geode_locations:
    crack_in_the_geode_table[location] = location_id
    location_id += 1

# The 5+3 main kingdoms have the same structure
# So fill them with the locations that should be awarded during the run through the kingdom
generic_kingdom_locations = ["Battle 1", "Battle 2", "Battle 3", "Chest", "Boss"]
scholars_nest_table = {}
for location in generic_kingdom_locations:
    scholars_nest_table[NEST + " " + location] = location_id
    location_id += 1

kings_arsenal_table = {}
for location in generic_kingdom_locations:
    kings_arsenal_table[ARSNEAL + " " + location] = location_id
    location_id += 1

red_darkhouse_table = {}
for location in generic_kingdom_locations:
    red_darkhouse_table[DARKHOUSE + " " + location] = location_id
    location_id += 1

churchmouse_streets_table = {}
for location in generic_kingdom_locations:
    churchmouse_streets_table[STREETS + " " + location] = location_id
    location_id += 1

emerald_lakeside_table = {}
for location in generic_kingdom_locations:
    emerald_lakeside_table[LAKESIDE + " " + location] = location_id
    location_id += 1

darkhouse_depths_table = {}
for location in generic_kingdom_locations:
    darkhouse_depths_table[DEPTHS + " " + location] = location_id
    location_id += 1

atelier_aurum_table = {}
for location in generic_kingdom_locations:
    atelier_aurum_table[AURUM + " " + location] = location_id
    location_id += 1

subterra_sanctum_table = {}
for location in generic_kingdom_locations:
    subterra_sanctum_table[SANCTUM + " " + location] = location_id
    location_id += 1

# Helper dictionary to get the locations from the 5+3 main kingdoms from their name
kingdom_to_locations = {NEST: scholars_nest_table, ARSNEAL: kings_arsenal_table,
                        DARKHOUSE: red_darkhouse_table, STREETS: churchmouse_streets_table,
                        LAKESIDE: emerald_lakeside_table}

extra_kingdom_to_locations = {DEPTHS: darkhouse_depths_table, AURUM: atelier_aurum_table,
                              SANCTUM: subterra_sanctum_table}

# Locations that should be awarded during the run through The Pale Keep
keep_locations = [KEEP + " Battle 1", KEEP + " Battle 2", KEEP + " Battle 3", KEEP + " Chest"]
pale_keep_table = {}
for location in keep_locations:
    pale_keep_table[location] = location_id
    location_id += 1

# Locations that should be awarded during the run through the Looping Hallway
hallway_locations = [HALLWAY + " Battle 1", HALLWAY + " Battle 2", HALLWAY + " Battle 3", HALLWAY + " Chest"]
looping_hallway_table = {}
for location in hallway_locations:
    looping_hallway_table[location] = location_id
    location_id += 1

# Locations that should be awarded during the run through the Moonlit Pinnacle
moonlit_pinnacle_table = {
    "Shira": location_id
}
location_id += 1

# Locations that should be awarded during the run through the Reflecting Pool
reflecting_pool_table = {
    "Witch": location_id
}
location_id += 1

# Locations that should be awarded for obtaining a specific chest item if chest sanity is on
item_locations = ["Top Left", "Bottom Left", "Middle", "Top Right", "Bottom Right"]

kingdom_outskirts_chest_locations = [OUTSKIRTS + " Chest 1", OUTSKIRTS + " Chest 2"]
kingdom_outskirts_chest_item_table = {}
for chest in kingdom_outskirts_chest_locations:
    for location in item_locations:
        kingdom_outskirts_chest_item_table[chest + " " + location] = location_id
        location_id += 1

crack_in_the_geode_chest_locations = [GEODE + " Chest 1", GEODE + " Chest 2"]
crack_in_the_geode_chest_item_table = {}
for chest in crack_in_the_geode_chest_locations:
    for location in item_locations:
        crack_in_the_geode_chest_item_table[chest + " " + location] = location_id
        location_id += 1

scholars_nest_chest_item_table = {}
for location in item_locations:
    scholars_nest_chest_item_table[NEST + " Chest " + location] = location_id
    location_id += 1

kings_arsenal_chest_item_table = {}
for location in item_locations:
    kings_arsenal_chest_item_table[ARSNEAL + " Chest " + location] = location_id
    location_id += 1

red_darkhouse_chest_item_table = {}
for location in item_locations:
    red_darkhouse_chest_item_table[DARKHOUSE + " Chest " + location] = location_id
    location_id += 1

churchmouse_streets_chest_item_table = {}
for location in item_locations:
    churchmouse_streets_chest_item_table[STREETS + " Chest " + location] = location_id
    location_id += 1

emerald_lakeside_chest_item_table = {}
for location in item_locations:
    emerald_lakeside_chest_item_table[LAKESIDE + " Chest " + location] = location_id
    location_id += 1

darkhouse_depths_chest_item_table = {}
for location in item_locations:
    darkhouse_depths_chest_item_table[DEPTHS + " Chest " + location] = location_id
    location_id += 1

atelier_aurum_chest_item_table = {}
for location in item_locations:
    atelier_aurum_chest_item_table[AURUM + " Chest " + location] = location_id
    location_id += 1

subterra_sanctum_chest_item_table = {}
for location in item_locations:
    subterra_sanctum_chest_item_table[SANCTUM + " Chest " + location] = location_id
    location_id += 1

pale_keep_chest_item_table = {}
for location in item_locations:
    pale_keep_chest_item_table[KEEP + " Chest " + location] = location_id
    location_id += 1

looping_hallway_chest_item_table = {}
for location in item_locations:
    looping_hallway_chest_item_table[HALLWAY + " Chest " + location] = location_id
    location_id += 1

kingdom_to_chest_locations = {NEST: scholars_nest_chest_item_table,
                              ARSNEAL: kings_arsenal_chest_item_table,
                              DARKHOUSE: red_darkhouse_chest_item_table,
                              STREETS: churchmouse_streets_chest_item_table,
                              LAKESIDE: emerald_lakeside_chest_item_table,
                              DEPTHS: darkhouse_depths_chest_item_table,
                              AURUM: atelier_aurum_chest_item_table,
                              SANCTUM: subterra_sanctum_chest_item_table,
                              KEEP: pale_keep_chest_item_table,
                              HALLWAY: looping_hallway_chest_item_table}


# Helper function to create the class specific locations for the given kingdom locations
# Excludes chests as those aren't character specific checks ever
def create_class_kingdom_locations(class_name, kingdom_table):
    global location_id

    class_location_table = {}
    for kingdom_location in kingdom_table:
        class_location_table[kingdom_location + " - " + class_name] = location_id
        location_id += 1
    return class_location_table


# Helper dictionary to get the locations for the wizard from the kingdom name
wizard_outskirts_table = create_class_kingdom_locations(WIZARD, kingdom_outskirts_table)
wizard_geode_table = create_class_kingdom_locations(WIZARD, crack_in_the_geode_table)
wizard_nest_table = create_class_kingdom_locations(WIZARD, scholars_nest_table)
wizard_arsenal_table = create_class_kingdom_locations(WIZARD, kings_arsenal_table)
wizard_darkhouse_table = create_class_kingdom_locations(WIZARD, red_darkhouse_table)
wizard_streets_table = create_class_kingdom_locations(WIZARD, churchmouse_streets_table)
wizard_lakeside_table = create_class_kingdom_locations(WIZARD, emerald_lakeside_table)
wizard_depths_table = create_class_kingdom_locations(WIZARD, darkhouse_depths_table)
wizard_aurum_table = create_class_kingdom_locations(WIZARD, atelier_aurum_table)
wizard_sanctum_table = create_class_kingdom_locations(WIZARD, subterra_sanctum_table)
wizard_keep_table = create_class_kingdom_locations(WIZARD, pale_keep_table)
wizard_pinnacle_table = create_class_kingdom_locations(WIZARD, moonlit_pinnacle_table)
wizard_hallway_table = create_class_kingdom_locations(WIZARD, looping_hallway_table)
wizard_pool_table = create_class_kingdom_locations(WIZARD, reflecting_pool_table)
wizard_tables = {
    OUTSKIRTS: wizard_outskirts_table,
    GEODE: wizard_geode_table,
    NEST: wizard_nest_table,
    ARSNEAL: wizard_arsenal_table,
    DARKHOUSE: wizard_darkhouse_table,
    STREETS: wizard_streets_table,
    LAKESIDE: wizard_lakeside_table,
    DEPTHS: wizard_depths_table,
    AURUM: wizard_aurum_table,
    SANCTUM: wizard_sanctum_table,
    KEEP: wizard_keep_table,
    PINNACLE: wizard_pinnacle_table,
    HALLWAY: wizard_hallway_table,
    POOL: wizard_pool_table
}

# Helper dictionary to get the locations for the assassin from the kingdom name
assassin_outskirts_table = create_class_kingdom_locations(ASSASSIN, kingdom_outskirts_table)
assassin_geode_table = create_class_kingdom_locations(ASSASSIN, crack_in_the_geode_table)
assassin_nest_table = create_class_kingdom_locations(ASSASSIN, scholars_nest_table)
assassin_arsenal_table = create_class_kingdom_locations(ASSASSIN, kings_arsenal_table)
assassin_darkhouse_table = create_class_kingdom_locations(ASSASSIN, red_darkhouse_table)
assassin_streets_table = create_class_kingdom_locations(ASSASSIN, churchmouse_streets_table)
assassin_lakeside_table = create_class_kingdom_locations(ASSASSIN, emerald_lakeside_table)
assassin_depths_table = create_class_kingdom_locations(ASSASSIN, darkhouse_depths_table)
assassin_aurum_table = create_class_kingdom_locations(ASSASSIN, atelier_aurum_table)
assassin_sanctum_table = create_class_kingdom_locations(ASSASSIN, subterra_sanctum_table)
assassin_keep_table = create_class_kingdom_locations(ASSASSIN, pale_keep_table)
assassin_pinnacle_table = create_class_kingdom_locations(ASSASSIN, moonlit_pinnacle_table)
assassin_hallway_table = create_class_kingdom_locations(ASSASSIN, looping_hallway_table)
assassin_pool_table = create_class_kingdom_locations(ASSASSIN, reflecting_pool_table)
assassin_tables = {
    OUTSKIRTS: assassin_outskirts_table,
    GEODE: assassin_geode_table,
    NEST: assassin_nest_table,
    ARSNEAL: assassin_arsenal_table,
    DARKHOUSE: assassin_darkhouse_table,
    STREETS: assassin_streets_table,
    LAKESIDE: assassin_lakeside_table,
    DEPTHS: assassin_depths_table,
    AURUM: assassin_aurum_table,
    SANCTUM: assassin_sanctum_table,
    KEEP: assassin_keep_table,
    PINNACLE: assassin_pinnacle_table,
    HALLWAY: assassin_hallway_table,
    POOL: assassin_pool_table
}

# Helper dictionary to get the locations for the heavyblade from the kingdom name
heavyblade_outskirts_table = create_class_kingdom_locations(HEAVYBLADE, kingdom_outskirts_table)
heavyblade_geode_table = create_class_kingdom_locations(HEAVYBLADE, crack_in_the_geode_table)
heavyblade_nest_table = create_class_kingdom_locations(HEAVYBLADE, scholars_nest_table)
heavyblade_arsenal_table = create_class_kingdom_locations(HEAVYBLADE, kings_arsenal_table)
heavyblade_darkhouse_table = create_class_kingdom_locations(HEAVYBLADE, red_darkhouse_table)
heavyblade_streets_table = create_class_kingdom_locations(HEAVYBLADE, churchmouse_streets_table)
heavyblade_lakeside_table = create_class_kingdom_locations(HEAVYBLADE, emerald_lakeside_table)
heavyblade_depths_table = create_class_kingdom_locations(HEAVYBLADE, darkhouse_depths_table)
heavyblade_aurum_table = create_class_kingdom_locations(HEAVYBLADE, atelier_aurum_table)
heavyblade_sanctum_table = create_class_kingdom_locations(HEAVYBLADE, subterra_sanctum_table)
heavyblade_keep_table = create_class_kingdom_locations(HEAVYBLADE, pale_keep_table)
heavyblade_pinnacle_table = create_class_kingdom_locations(HEAVYBLADE, moonlit_pinnacle_table)
heavyblade_hallway_table = create_class_kingdom_locations(HEAVYBLADE, looping_hallway_table)
heavyblade_pool_table = create_class_kingdom_locations(HEAVYBLADE, reflecting_pool_table)
heavyblade_tables = {
    OUTSKIRTS: heavyblade_outskirts_table,
    GEODE: heavyblade_geode_table,
    NEST: heavyblade_nest_table,
    ARSNEAL: heavyblade_arsenal_table,
    DARKHOUSE: heavyblade_darkhouse_table,
    STREETS: heavyblade_streets_table,
    LAKESIDE: heavyblade_lakeside_table,
    DEPTHS: heavyblade_depths_table,
    AURUM: heavyblade_aurum_table,
    SANCTUM: heavyblade_sanctum_table,
    KEEP: heavyblade_keep_table,
    PINNACLE: heavyblade_pinnacle_table,
    HALLWAY: heavyblade_hallway_table,
    POOL: heavyblade_pool_table
}

# Helper dictionary to get the locations for the dancer from the kingdom name
dancer_outskirts_table = create_class_kingdom_locations(DANCER, kingdom_outskirts_table)
dancer_geode_table = create_class_kingdom_locations(DANCER, crack_in_the_geode_table)
dancer_nest_table = create_class_kingdom_locations(DANCER, scholars_nest_table)
dancer_arsenal_table = create_class_kingdom_locations(DANCER, kings_arsenal_table)
dancer_darkhouse_table = create_class_kingdom_locations(DANCER, red_darkhouse_table)
dancer_streets_table = create_class_kingdom_locations(DANCER, churchmouse_streets_table)
dancer_lakeside_table = create_class_kingdom_locations(DANCER, emerald_lakeside_table)
dancer_depths_table = create_class_kingdom_locations(DANCER, darkhouse_depths_table)
dancer_aurum_table = create_class_kingdom_locations(DANCER, atelier_aurum_table)
dancer_sanctum_table = create_class_kingdom_locations(DANCER, subterra_sanctum_table)
dancer_keep_table = create_class_kingdom_locations(DANCER, pale_keep_table)
dancer_pinnacle_table = create_class_kingdom_locations(DANCER, moonlit_pinnacle_table)
dancer_hallway_table = create_class_kingdom_locations(DANCER, looping_hallway_table)
dancer_pool_table = create_class_kingdom_locations(DANCER, reflecting_pool_table)
dancer_tables = {
    OUTSKIRTS: dancer_outskirts_table,
    GEODE: dancer_geode_table,
    NEST: dancer_nest_table,
    ARSNEAL: dancer_arsenal_table,
    DARKHOUSE: dancer_darkhouse_table,
    STREETS: dancer_streets_table,
    LAKESIDE: dancer_lakeside_table,
    DEPTHS: dancer_depths_table,
    AURUM: dancer_aurum_table,
    SANCTUM: dancer_sanctum_table,
    KEEP: dancer_keep_table,
    PINNACLE: dancer_pinnacle_table,
    HALLWAY: dancer_hallway_table,
    POOL: dancer_pool_table
}

# Helper dictionary to get the locations for the druid from the kingdom name
druid_outskirts_table = create_class_kingdom_locations(DRUID, kingdom_outskirts_table)
druid_geode_table = create_class_kingdom_locations(DRUID, crack_in_the_geode_table)
druid_nest_table = create_class_kingdom_locations(DRUID, scholars_nest_table)
druid_arsenal_table = create_class_kingdom_locations(DRUID, kings_arsenal_table)
druid_darkhouse_table = create_class_kingdom_locations(DRUID, red_darkhouse_table)
druid_streets_table = create_class_kingdom_locations(DRUID, churchmouse_streets_table)
druid_lakeside_table = create_class_kingdom_locations(DRUID, emerald_lakeside_table)
druid_depths_table = create_class_kingdom_locations(DRUID, darkhouse_depths_table)
druid_aurum_table = create_class_kingdom_locations(DRUID, atelier_aurum_table)
druid_sanctum_table = create_class_kingdom_locations(DRUID, subterra_sanctum_table)
druid_keep_table = create_class_kingdom_locations(DRUID, pale_keep_table)
druid_pinnacle_table = create_class_kingdom_locations(DRUID, moonlit_pinnacle_table)
druid_hallway_table = create_class_kingdom_locations(DRUID, looping_hallway_table)
druid_pool_table = create_class_kingdom_locations(DRUID, reflecting_pool_table)
druid_tables = {
    OUTSKIRTS: druid_outskirts_table,
    GEODE: druid_geode_table,
    NEST: druid_nest_table,
    ARSNEAL: druid_arsenal_table,
    DARKHOUSE: druid_darkhouse_table,
    STREETS: druid_streets_table,
    LAKESIDE: druid_lakeside_table,
    DEPTHS: druid_depths_table,
    AURUM: druid_aurum_table,
    SANCTUM: druid_sanctum_table,
    KEEP: druid_keep_table,
    PINNACLE: druid_pinnacle_table,
    HALLWAY: druid_hallway_table,
    POOL: druid_pool_table
}

# Helper dictionary to get the locations for the spellsword from the kingdom name
spellsword_outskirts_table = create_class_kingdom_locations(SPELLSWORD, kingdom_outskirts_table)
spellsword_geode_table = create_class_kingdom_locations(SPELLSWORD, crack_in_the_geode_table)
spellsword_nest_table = create_class_kingdom_locations(SPELLSWORD, scholars_nest_table)
spellsword_arsenal_table = create_class_kingdom_locations(SPELLSWORD, kings_arsenal_table)
spellsword_darkhouse_table = create_class_kingdom_locations(SPELLSWORD, red_darkhouse_table)
spellsword_streets_table = create_class_kingdom_locations(SPELLSWORD, churchmouse_streets_table)
spellsword_lakeside_table = create_class_kingdom_locations(SPELLSWORD, emerald_lakeside_table)
spellsword_depths_table = create_class_kingdom_locations(SPELLSWORD, darkhouse_depths_table)
spellsword_aurum_table = create_class_kingdom_locations(SPELLSWORD, atelier_aurum_table)
spellsword_sanctum_table = create_class_kingdom_locations(SPELLSWORD, subterra_sanctum_table)
spellsword_keep_table = create_class_kingdom_locations(SPELLSWORD, pale_keep_table)
spellsword_pinnacle_table = create_class_kingdom_locations(SPELLSWORD, moonlit_pinnacle_table)
spellsword_hallway_table = create_class_kingdom_locations(SPELLSWORD, looping_hallway_table)
spellsword_pool_table = create_class_kingdom_locations(SPELLSWORD, reflecting_pool_table)
spellsword_tables = {
    OUTSKIRTS: spellsword_outskirts_table,
    GEODE: spellsword_geode_table,
    NEST: spellsword_nest_table,
    ARSNEAL: spellsword_arsenal_table,
    DARKHOUSE: spellsword_darkhouse_table,
    STREETS: spellsword_streets_table,
    LAKESIDE: spellsword_lakeside_table,
    DEPTHS: spellsword_depths_table,
    AURUM: spellsword_aurum_table,
    SANCTUM: spellsword_sanctum_table,
    KEEP: spellsword_keep_table,
    PINNACLE: spellsword_pinnacle_table,
    HALLWAY: spellsword_hallway_table,
    POOL: spellsword_pool_table
}

# Helper dictionary to get the locations for the sniper from the kingdom name
sniper_outskirts_table = create_class_kingdom_locations(SNIPER, kingdom_outskirts_table)
sniper_geode_table = create_class_kingdom_locations(SNIPER, crack_in_the_geode_table)
sniper_nest_table = create_class_kingdom_locations(SNIPER, scholars_nest_table)
sniper_arsenal_table = create_class_kingdom_locations(SNIPER, kings_arsenal_table)
sniper_darkhouse_table = create_class_kingdom_locations(SNIPER, red_darkhouse_table)
sniper_streets_table = create_class_kingdom_locations(SNIPER, churchmouse_streets_table)
sniper_lakeside_table = create_class_kingdom_locations(SNIPER, emerald_lakeside_table)
sniper_depths_table = create_class_kingdom_locations(SNIPER, darkhouse_depths_table)
sniper_aurum_table = create_class_kingdom_locations(SNIPER, atelier_aurum_table)
sniper_sanctum_table = create_class_kingdom_locations(SNIPER, subterra_sanctum_table)
sniper_keep_table = create_class_kingdom_locations(SNIPER, pale_keep_table)
sniper_pinnacle_table = create_class_kingdom_locations(SNIPER, moonlit_pinnacle_table)
sniper_hallway_table = create_class_kingdom_locations(SNIPER, looping_hallway_table)
sniper_pool_table = create_class_kingdom_locations(SNIPER, reflecting_pool_table)
sniper_tables = {
    OUTSKIRTS: sniper_outskirts_table,
    GEODE: sniper_geode_table,
    NEST: sniper_nest_table,
    ARSNEAL: sniper_arsenal_table,
    DARKHOUSE: sniper_darkhouse_table,
    STREETS: sniper_streets_table,
    LAKESIDE: sniper_lakeside_table,
    DEPTHS: sniper_depths_table,
    AURUM: sniper_aurum_table,
    SANCTUM: sniper_sanctum_table,
    KEEP: sniper_keep_table,
    PINNACLE: sniper_pinnacle_table,
    HALLWAY: sniper_hallway_table,
    POOL: sniper_pool_table
}

# Helper dictionary to get the locations for the bruiser from the kingdom name
bruiser_outskirts_table = create_class_kingdom_locations(BRUISER, kingdom_outskirts_table)
bruiser_geode_table = create_class_kingdom_locations(BRUISER, crack_in_the_geode_table)
bruiser_nest_table = create_class_kingdom_locations(BRUISER, scholars_nest_table)
bruiser_arsenal_table = create_class_kingdom_locations(BRUISER, kings_arsenal_table)
bruiser_darkhouse_table = create_class_kingdom_locations(BRUISER, red_darkhouse_table)
bruiser_streets_table = create_class_kingdom_locations(BRUISER, churchmouse_streets_table)
bruiser_lakeside_table = create_class_kingdom_locations(BRUISER, emerald_lakeside_table)
bruiser_depths_table = create_class_kingdom_locations(BRUISER, darkhouse_depths_table)
bruiser_aurum_table = create_class_kingdom_locations(BRUISER, atelier_aurum_table)
bruiser_sanctum_table = create_class_kingdom_locations(BRUISER, subterra_sanctum_table)
bruiser_keep_table = create_class_kingdom_locations(BRUISER, pale_keep_table)
bruiser_pinnacle_table = create_class_kingdom_locations(BRUISER, moonlit_pinnacle_table)
bruiser_hallway_table = create_class_kingdom_locations(BRUISER, looping_hallway_table)
bruiser_pool_table = create_class_kingdom_locations(BRUISER, reflecting_pool_table)
bruiser_tables = {
    OUTSKIRTS: bruiser_outskirts_table,
    GEODE: bruiser_geode_table,
    NEST: bruiser_nest_table,
    ARSNEAL: bruiser_arsenal_table,
    DARKHOUSE: bruiser_darkhouse_table,
    STREETS: bruiser_streets_table,
    LAKESIDE: bruiser_lakeside_table,
    DEPTHS: bruiser_depths_table,
    AURUM: bruiser_aurum_table,
    SANCTUM: bruiser_sanctum_table,
    KEEP: bruiser_keep_table,
    PINNACLE: bruiser_pinnacle_table,
    HALLWAY: bruiser_hallway_table,
    POOL: bruiser_pool_table
}

# Helper dictionary to get the locations for the defender from the kingdom name
defender_outskirts_table = create_class_kingdom_locations(DEFENDER, kingdom_outskirts_table)
defender_geode_table = create_class_kingdom_locations(DEFENDER, crack_in_the_geode_table)
defender_nest_table = create_class_kingdom_locations(DEFENDER, scholars_nest_table)
defender_arsenal_table = create_class_kingdom_locations(DEFENDER, kings_arsenal_table)
defender_darkhouse_table = create_class_kingdom_locations(DEFENDER, red_darkhouse_table)
defender_streets_table = create_class_kingdom_locations(DEFENDER, churchmouse_streets_table)
defender_lakeside_table = create_class_kingdom_locations(DEFENDER, emerald_lakeside_table)
defender_depths_table = create_class_kingdom_locations(DEFENDER, darkhouse_depths_table)
defender_aurum_table = create_class_kingdom_locations(DEFENDER, atelier_aurum_table)
defender_sanctum_table = create_class_kingdom_locations(DEFENDER, subterra_sanctum_table)
defender_keep_table = create_class_kingdom_locations(DEFENDER, pale_keep_table)
defender_pinnacle_table = create_class_kingdom_locations(DEFENDER, moonlit_pinnacle_table)
defender_hallway_table = create_class_kingdom_locations(DEFENDER, looping_hallway_table)
defender_pool_table = create_class_kingdom_locations(DEFENDER, reflecting_pool_table)
defender_tables = {
    OUTSKIRTS: defender_outskirts_table,
    GEODE: defender_geode_table,
    NEST: defender_nest_table,
    ARSNEAL: defender_arsenal_table,
    DARKHOUSE: defender_darkhouse_table,
    STREETS: defender_streets_table,
    LAKESIDE: defender_lakeside_table,
    DEPTHS: defender_depths_table,
    AURUM: defender_aurum_table,
    SANCTUM: defender_sanctum_table,
    KEEP: defender_keep_table,
    PINNACLE: defender_pinnacle_table,
    HALLWAY: defender_hallway_table,
    POOL: defender_pool_table
}

# Helper dictionary to get the locations for the ancient from the kingdom name
ancient_outskirts_table = create_class_kingdom_locations(ANCIENT, kingdom_outskirts_table)
ancient_geode_table = create_class_kingdom_locations(ANCIENT, crack_in_the_geode_table)
ancient_nest_table = create_class_kingdom_locations(ANCIENT, scholars_nest_table)
ancient_arsenal_table = create_class_kingdom_locations(ANCIENT, kings_arsenal_table)
ancient_darkhouse_table = create_class_kingdom_locations(ANCIENT, red_darkhouse_table)
ancient_streets_table = create_class_kingdom_locations(ANCIENT, churchmouse_streets_table)
ancient_lakeside_table = create_class_kingdom_locations(ANCIENT, emerald_lakeside_table)
ancient_depths_table = create_class_kingdom_locations(ANCIENT, darkhouse_depths_table)
ancient_aurum_table = create_class_kingdom_locations(ANCIENT, atelier_aurum_table)
ancient_sanctum_table = create_class_kingdom_locations(ANCIENT, subterra_sanctum_table)
ancient_keep_table = create_class_kingdom_locations(ANCIENT, pale_keep_table)
ancient_pinnacle_table = create_class_kingdom_locations(ANCIENT, moonlit_pinnacle_table)
ancient_hallway_table = create_class_kingdom_locations(ANCIENT, looping_hallway_table)
ancient_pool_table = create_class_kingdom_locations(ANCIENT, reflecting_pool_table)
ancient_tables = {
    OUTSKIRTS: ancient_outskirts_table,
    GEODE: ancient_geode_table,
    NEST: ancient_nest_table,
    ARSNEAL: ancient_arsenal_table,
    DARKHOUSE: ancient_darkhouse_table,
    STREETS: ancient_streets_table,
    LAKESIDE: ancient_lakeside_table,
    DEPTHS: ancient_depths_table,
    AURUM: ancient_aurum_table,
    SANCTUM: ancient_sanctum_table,
    KEEP: ancient_keep_table,
    PINNACLE: ancient_pinnacle_table,
    HALLWAY: ancient_hallway_table,
    POOL: ancient_pool_table
}

# Helper dictionary to get the locations for the hammermaid from the kingdom name
hammermaid_outskirts_table = create_class_kingdom_locations(HAMMERMAID, kingdom_outskirts_table)
hammermaid_geode_table = create_class_kingdom_locations(HAMMERMAID, crack_in_the_geode_table)
hammermaid_nest_table = create_class_kingdom_locations(HAMMERMAID, scholars_nest_table)
hammermaid_arsenal_table = create_class_kingdom_locations(HAMMERMAID, kings_arsenal_table)
hammermaid_darkhouse_table = create_class_kingdom_locations(HAMMERMAID, red_darkhouse_table)
hammermaid_streets_table = create_class_kingdom_locations(HAMMERMAID, churchmouse_streets_table)
hammermaid_lakeside_table = create_class_kingdom_locations(HAMMERMAID, emerald_lakeside_table)
hammermaid_depths_table = create_class_kingdom_locations(HAMMERMAID, darkhouse_depths_table)
hammermaid_aurum_table = create_class_kingdom_locations(HAMMERMAID, atelier_aurum_table)
hammermaid_sanctum_table = create_class_kingdom_locations(HAMMERMAID, subterra_sanctum_table)
hammermaid_keep_table = create_class_kingdom_locations(HAMMERMAID, pale_keep_table)
hammermaid_pinnacle_table = create_class_kingdom_locations(HAMMERMAID, moonlit_pinnacle_table)
hammermaid_hallway_table = create_class_kingdom_locations(HAMMERMAID, looping_hallway_table)
hammermaid_pool_table = create_class_kingdom_locations(HAMMERMAID, reflecting_pool_table)
hammermaid_tables = {
    OUTSKIRTS: hammermaid_outskirts_table,
    GEODE: hammermaid_geode_table,
    NEST: hammermaid_nest_table,
    ARSNEAL: hammermaid_arsenal_table,
    DARKHOUSE: hammermaid_darkhouse_table,
    STREETS: hammermaid_streets_table,
    LAKESIDE: hammermaid_lakeside_table,
    DEPTHS: hammermaid_depths_table,
    AURUM: hammermaid_aurum_table,
    SANCTUM: hammermaid_sanctum_table,
    KEEP: hammermaid_keep_table,
    PINNACLE: hammermaid_pinnacle_table,
    HALLWAY: hammermaid_hallway_table,
    POOL: hammermaid_pool_table
}

# Helper dictionary to get the locations for the pyromancer from the kingdom name
pyromancer_outskirts_table = create_class_kingdom_locations(PYROMANCER, kingdom_outskirts_table)
pyromancer_geode_table = create_class_kingdom_locations(PYROMANCER, crack_in_the_geode_table)
pyromancer_nest_table = create_class_kingdom_locations(PYROMANCER, scholars_nest_table)
pyromancer_arsenal_table = create_class_kingdom_locations(PYROMANCER, kings_arsenal_table)
pyromancer_darkhouse_table = create_class_kingdom_locations(PYROMANCER, red_darkhouse_table)
pyromancer_streets_table = create_class_kingdom_locations(PYROMANCER, churchmouse_streets_table)
pyromancer_lakeside_table = create_class_kingdom_locations(PYROMANCER, emerald_lakeside_table)
pyromancer_depths_table = create_class_kingdom_locations(PYROMANCER, darkhouse_depths_table)
pyromancer_aurum_table = create_class_kingdom_locations(PYROMANCER, atelier_aurum_table)
pyromancer_sanctum_table = create_class_kingdom_locations(PYROMANCER, subterra_sanctum_table)
pyromancer_keep_table = create_class_kingdom_locations(PYROMANCER, pale_keep_table)
pyromancer_pinnacle_table = create_class_kingdom_locations(PYROMANCER, moonlit_pinnacle_table)
pyromancer_hallway_table = create_class_kingdom_locations(PYROMANCER, looping_hallway_table)
pyromancer_pool_table = create_class_kingdom_locations(PYROMANCER, reflecting_pool_table)
pyromancer_tables = {
    OUTSKIRTS: pyromancer_outskirts_table,
    GEODE: pyromancer_geode_table,
    NEST: pyromancer_nest_table,
    ARSNEAL: pyromancer_arsenal_table,
    DARKHOUSE: pyromancer_darkhouse_table,
    STREETS: pyromancer_streets_table,
    LAKESIDE: pyromancer_lakeside_table,
    DEPTHS: pyromancer_depths_table,
    AURUM: pyromancer_aurum_table,
    SANCTUM: pyromancer_sanctum_table,
    KEEP: pyromancer_keep_table,
    PINNACLE: pyromancer_pinnacle_table,
    HALLWAY: pyromancer_hallway_table,
    POOL: pyromancer_pool_table
}

# Helper dictionary to get the locations for the pyromancer from the kingdom name
grenadier_outskirts_table = create_class_kingdom_locations(GRENADIER, kingdom_outskirts_table)
grenadier_geode_table = create_class_kingdom_locations(GRENADIER, crack_in_the_geode_table)
grenadier_nest_table = create_class_kingdom_locations(GRENADIER, scholars_nest_table)
grenadier_arsenal_table = create_class_kingdom_locations(GRENADIER, kings_arsenal_table)
grenadier_darkhouse_table = create_class_kingdom_locations(GRENADIER, red_darkhouse_table)
grenadier_streets_table = create_class_kingdom_locations(GRENADIER, churchmouse_streets_table)
grenadier_lakeside_table = create_class_kingdom_locations(GRENADIER, emerald_lakeside_table)
grenadier_depths_table = create_class_kingdom_locations(GRENADIER, darkhouse_depths_table)
grenadier_aurum_table = create_class_kingdom_locations(GRENADIER, atelier_aurum_table)
grenadier_sanctum_table = create_class_kingdom_locations(GRENADIER, subterra_sanctum_table)
grenadier_keep_table = create_class_kingdom_locations(GRENADIER, pale_keep_table)
grenadier_pinnacle_table = create_class_kingdom_locations(GRENADIER, moonlit_pinnacle_table)
grenadier_hallway_table = create_class_kingdom_locations(GRENADIER, looping_hallway_table)
grenadier_pool_table = create_class_kingdom_locations(GRENADIER, reflecting_pool_table)
grenadier_tables = {
    OUTSKIRTS: grenadier_outskirts_table,
    GEODE: grenadier_geode_table,
    NEST: grenadier_nest_table,
    ARSNEAL: grenadier_arsenal_table,
    DARKHOUSE: grenadier_darkhouse_table,
    STREETS: grenadier_streets_table,
    LAKESIDE: grenadier_lakeside_table,
    DEPTHS: grenadier_depths_table,
    AURUM: grenadier_aurum_table,
    SANCTUM: grenadier_sanctum_table,
    KEEP: grenadier_keep_table,
    PINNACLE: grenadier_pinnacle_table,
    HALLWAY: grenadier_hallway_table,
    POOL: grenadier_pool_table
}

# Helper dictionary to get the locations for the shadow from the kingdom name
shadow_outskirts_table = create_class_kingdom_locations(SHADOW, kingdom_outskirts_table)
shadow_geode_table = create_class_kingdom_locations(SHADOW, crack_in_the_geode_table)
shadow_nest_table = create_class_kingdom_locations(SHADOW, scholars_nest_table)
shadow_arsenal_table = create_class_kingdom_locations(SHADOW, kings_arsenal_table)
shadow_darkhouse_table = create_class_kingdom_locations(SHADOW, red_darkhouse_table)
shadow_streets_table = create_class_kingdom_locations(SHADOW, churchmouse_streets_table)
shadow_lakeside_table = create_class_kingdom_locations(SHADOW, emerald_lakeside_table)
shadow_depths_table = create_class_kingdom_locations(SHADOW, darkhouse_depths_table)
shadow_aurum_table = create_class_kingdom_locations(SHADOW, atelier_aurum_table)
shadow_sanctum_table = create_class_kingdom_locations(SHADOW, subterra_sanctum_table)
shadow_keep_table = create_class_kingdom_locations(SHADOW, pale_keep_table)
shadow_pinnacle_table = create_class_kingdom_locations(SHADOW, moonlit_pinnacle_table)
shadow_hallway_table = create_class_kingdom_locations(SHADOW, looping_hallway_table)
shadow_pool_table = create_class_kingdom_locations(SHADOW, reflecting_pool_table)
shadow_tables = {
    OUTSKIRTS: shadow_outskirts_table,
    GEODE: shadow_geode_table,
    NEST: shadow_nest_table,
    ARSNEAL: shadow_arsenal_table,
    DARKHOUSE: shadow_darkhouse_table,
    STREETS: shadow_streets_table,
    LAKESIDE: shadow_lakeside_table,
    DEPTHS: shadow_depths_table,
    AURUM: shadow_aurum_table,
    SANCTUM: shadow_sanctum_table,
    KEEP: shadow_keep_table,
    PINNACLE: shadow_pinnacle_table,
    HALLWAY: shadow_hallway_table,
    POOL: shadow_pool_table
}

# Helper dictionary to get the locations for a class from their class name
class_tables = {
    WIZARD: wizard_tables,
    ASSASSIN: assassin_tables,
    HEAVYBLADE: heavyblade_tables,
    DANCER: dancer_tables,
    DRUID: druid_tables,
    SPELLSWORD: spellsword_tables,
    SNIPER: sniper_tables,
    BRUISER: bruiser_tables,
    DEFENDER: defender_tables,
    ANCIENT: ancient_tables,
    HAMMERMAID: hammermaid_tables,
    PYROMANCER: pyromancer_tables,
    GRENADIER: grenadier_tables,
    SHADOW: shadow_tables
}

shop_locations = ["Full Heal Potion Slot", "Level Up Slot", "Potion 1 Slot", "Potion 2 Slot", "Potion 3 Slot",
                  "Primary Upgrade Slot", "Secondary Upgrade Slot", "Special Upgrade Slot", "Defensive Upgrade Slot"]
global_shop_table = {}
for location in shop_locations:
    global_shop_table[location] = location_id
    location_id += 1
scholars_nest_shop_table = {}
for location in shop_locations:
    scholars_nest_shop_table[NEST + " Shop " + location] = location_id
    location_id += 1
kings_arsenal_shop_table = {}
for location in shop_locations:
    kings_arsenal_shop_table[ARSNEAL + " Shop " + location] = location_id
    location_id += 1
red_darkhouse_shop_table = {}
for location in shop_locations:
    red_darkhouse_shop_table[DARKHOUSE + " Shop " + location] = location_id
    location_id += 1
churchmouse_streets_shop_table = {}
for location in shop_locations:
    churchmouse_streets_shop_table[STREETS + " Shop " + location] = location_id
    location_id += 1
emerald_lakeside_shop_table = {}
for location in shop_locations:
    emerald_lakeside_shop_table[LAKESIDE + " Shop " + location] = location_id
    location_id += 1
darkhouse_depths_shop_table = {}
for location in shop_locations:
    darkhouse_depths_shop_table[DEPTHS + " Shop " + location] = location_id
    location_id += 1
atelier_aurum_shop_table = {}
for location in shop_locations:
    atelier_aurum_shop_table[AURUM + " Shop " + location] = location_id
    location_id += 1
subterra_sanctum_shop_table = {}
for location in shop_locations:
    subterra_sanctum_shop_table[SANCTUM + " Shop " + location] = location_id
    location_id += 1
pale_keep_shop_table = {}
for location in shop_locations:
    pale_keep_shop_table[KEEP + " Shop " + location] = location_id
    location_id += 1
looping_hallway_shop_table = {}
for location in shop_locations:
    looping_hallway_shop_table[HALLWAY + " Shop " + location] = location_id
    location_id += 1

kingdom_to_shop_locations = {NEST: scholars_nest_shop_table,
                             ARSNEAL: kings_arsenal_shop_table,
                             DARKHOUSE: red_darkhouse_shop_table,
                             STREETS: churchmouse_streets_shop_table,
                             LAKESIDE: emerald_lakeside_shop_table,
                             DEPTHS: darkhouse_depths_shop_table,
                             AURUM: atelier_aurum_shop_table,
                             SANCTUM: subterra_sanctum_shop_table,
                             KEEP: pale_keep_shop_table,
                             HALLWAY: looping_hallway_shop_table}

# Dictionary that contains all the locations
location_table = kingdom_outskirts_table | crack_in_the_geode_table | scholars_nest_table | kings_arsenal_table | \
                 red_darkhouse_table | churchmouse_streets_table | emerald_lakeside_table | darkhouse_depths_table | \
                 atelier_aurum_table | subterra_sanctum_table | pale_keep_table | moonlit_pinnacle_table | \
                 looping_hallway_table | reflecting_pool_table | kingdom_outskirts_chest_item_table | \
                 crack_in_the_geode_chest_item_table | scholars_nest_chest_item_table | \
                 kings_arsenal_chest_item_table | red_darkhouse_chest_item_table | \
                 churchmouse_streets_chest_item_table | emerald_lakeside_chest_item_table | \
                 darkhouse_depths_chest_item_table | atelier_aurum_chest_item_table | \
                 subterra_sanctum_chest_item_table | pale_keep_chest_item_table | looping_hallway_chest_item_table | \
                 wizard_outskirts_table | wizard_geode_table | wizard_nest_table | wizard_arsenal_table | \
                 wizard_darkhouse_table | wizard_streets_table | wizard_lakeside_table | wizard_depths_table | \
                 wizard_aurum_table | wizard_sanctum_table | wizard_keep_table | wizard_pinnacle_table | \
                 wizard_hallway_table | wizard_pool_table | assassin_outskirts_table | assassin_geode_table | \
                 assassin_nest_table | assassin_arsenal_table | assassin_darkhouse_table | assassin_streets_table | \
                 assassin_lakeside_table | assassin_depths_table | assassin_aurum_table | assassin_sanctum_table | \
                 assassin_keep_table | assassin_pinnacle_table | assassin_hallway_table | assassin_pool_table | \
                 heavyblade_outskirts_table | heavyblade_geode_table | heavyblade_nest_table | \
                 heavyblade_arsenal_table | heavyblade_darkhouse_table | heavyblade_streets_table | \
                 heavyblade_lakeside_table | heavyblade_depths_table | heavyblade_aurum_table | \
                 heavyblade_sanctum_table | heavyblade_keep_table | heavyblade_pinnacle_table | \
                 heavyblade_hallway_table | heavyblade_pool_table | dancer_outskirts_table | dancer_geode_table | \
                 dancer_nest_table | dancer_arsenal_table | dancer_darkhouse_table | dancer_streets_table | \
                 dancer_lakeside_table | dancer_depths_table | dancer_aurum_table | dancer_sanctum_table | \
                 dancer_keep_table | dancer_pinnacle_table | dancer_hallway_table | dancer_pool_table | \
                 druid_outskirts_table | druid_geode_table | druid_nest_table | druid_arsenal_table | \
                 druid_darkhouse_table | druid_streets_table | druid_lakeside_table | druid_depths_table | \
                 druid_aurum_table | druid_sanctum_table | druid_keep_table | druid_pinnacle_table | \
                 druid_hallway_table | druid_pool_table | spellsword_outskirts_table | spellsword_geode_table | \
                 spellsword_nest_table | spellsword_arsenal_table | spellsword_darkhouse_table | \
                 spellsword_streets_table | spellsword_lakeside_table | spellsword_depths_table | \
                 spellsword_aurum_table | spellsword_sanctum_table | spellsword_keep_table | \
                 spellsword_pinnacle_table | spellsword_hallway_table | spellsword_pool_table | \
                 sniper_outskirts_table | sniper_geode_table | sniper_nest_table | sniper_arsenal_table | \
                 sniper_darkhouse_table | sniper_streets_table | sniper_lakeside_table | sniper_depths_table | \
                 sniper_aurum_table | sniper_sanctum_table | sniper_keep_table | sniper_pinnacle_table | \
                 sniper_hallway_table | sniper_pool_table | bruiser_outskirts_table | bruiser_geode_table | \
                 bruiser_nest_table | bruiser_arsenal_table | bruiser_darkhouse_table | bruiser_streets_table | \
                 bruiser_lakeside_table | bruiser_depths_table | bruiser_aurum_table | bruiser_sanctum_table | \
                 bruiser_keep_table | bruiser_pinnacle_table | bruiser_hallway_table | bruiser_pool_table | \
                 defender_outskirts_table | defender_geode_table | defender_nest_table | defender_arsenal_table | \
                 defender_darkhouse_table | defender_streets_table | defender_lakeside_table | defender_depths_table | \
                 defender_aurum_table | defender_sanctum_table | defender_keep_table | defender_pinnacle_table | \
                 defender_hallway_table | defender_pool_table | ancient_outskirts_table | ancient_geode_table | \
                 ancient_nest_table | ancient_arsenal_table | ancient_darkhouse_table | ancient_streets_table | \
                 ancient_lakeside_table | ancient_depths_table | ancient_aurum_table | ancient_sanctum_table | \
                 ancient_keep_table | ancient_pinnacle_table | ancient_hallway_table | ancient_pool_table | \
                 hammermaid_outskirts_table | hammermaid_geode_table | hammermaid_nest_table | \
                 hammermaid_arsenal_table | hammermaid_darkhouse_table | hammermaid_streets_table | \
                 hammermaid_lakeside_table | hammermaid_depths_table | hammermaid_aurum_table | \
                 hammermaid_sanctum_table | hammermaid_keep_table | hammermaid_pinnacle_table | \
                 hammermaid_hallway_table | hammermaid_pool_table | pyromancer_outskirts_table | \
                 pyromancer_geode_table | pyromancer_nest_table | pyromancer_arsenal_table | \
                 pyromancer_darkhouse_table | pyromancer_streets_table | pyromancer_lakeside_table | \
                 pyromancer_depths_table | pyromancer_aurum_table | pyromancer_sanctum_table | pyromancer_keep_table | \
                 pyromancer_pinnacle_table | pyromancer_hallway_table | pyromancer_pool_table | \
                 grenadier_outskirts_table | grenadier_geode_table | grenadier_nest_table | grenadier_arsenal_table | \
                 grenadier_darkhouse_table | grenadier_streets_table | grenadier_lakeside_table | \
                 grenadier_depths_table | grenadier_aurum_table | grenadier_sanctum_table | grenadier_keep_table | \
                 grenadier_pinnacle_table | grenadier_hallway_table | grenadier_pool_table | shadow_outskirts_table | \
                 shadow_geode_table | shadow_nest_table | shadow_arsenal_table | shadow_darkhouse_table | \
                 shadow_streets_table | shadow_lakeside_table | shadow_depths_table | shadow_aurum_table | \
                 shadow_sanctum_table | shadow_keep_table | shadow_pinnacle_table | shadow_hallway_table | \
                 shadow_pool_table | global_shop_table | scholars_nest_shop_table | kings_arsenal_shop_table | \
                 red_darkhouse_shop_table | churchmouse_streets_shop_table | emerald_lakeside_shop_table | \
                 darkhouse_depths_shop_table | atelier_aurum_shop_table | subterra_sanctum_shop_table | \
                 pale_keep_shop_table | looping_hallway_shop_table
