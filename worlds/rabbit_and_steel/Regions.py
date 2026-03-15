from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Region
from . import Items
from .Options import RunType
from .Constants import OUTSKIRTS, KEEP, PINNACLE, GEODE, HALLWAY, POOL

if TYPE_CHECKING:
    from .World import RabbitAndSteelWorld


def create_and_connect_regions(world: RabbitAndSteelWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: RabbitAndSteelWorld) -> None:
    lobby = Region(world.origin_region_name, world.player, world.multiworld)
    regions = [lobby]

    # Creates all kingdom regions
    for kingdom_name in (Items.kingdom_names + Items.extra_kingdom_names):
        if kingdom_name not in world.options.excluded_kingdoms:
            region = Region(kingdom_name, world.player, world.multiworld)
            regions.append(region)

    # Creates the regions for the class checks minus the Moonlit Pinnacle and Reflecting Pool
    if world.options.checks_per_class:
        for kingdom_name in (Items.kingdom_names + Items.extra_kingdom_names):
            if kingdom_name == PINNACLE or kingdom_name == POOL:
                continue

            if kingdom_name not in world.options.excluded_kingdoms:
                for class_name in world.options.checks_per_class:
                    region = Region(kingdom_name + " - " + class_name, world.player, world.multiworld)
                    regions.append(region)

    # Find the classes that will have checks in the last kingdom
    class_checks_for_boss = Items.class_names
    # TODO: Use below if finishing runs aren't a goal condition
    # class_checks_for_boss = world.options.checks_per_class

    # Add the class regions for the Moonlit Pinnacle
    if PINNACLE not in world.options.excluded_kingdoms:
        for class_name in class_checks_for_boss:
            if class_name in world.options.exclude_class:
                continue
            region = Region(PINNACLE + " - " + class_name, world.player, world.multiworld)
            regions.append(region)

    # Add the class regions for the Reflecting Pool
    if POOL not in world.options.excluded_kingdoms:
        for class_name in class_checks_for_boss:
            if class_name in world.options.exclude_class:
                continue
            region = Region(POOL + " - " + class_name, world.player, world.multiworld)
            regions.append(region)

    # Create shop region if all shops share locations
    if world.options.shop_sanity == world.options.shop_sanity.option_global:
        region = Region("Shops", world.player, world.multiworld)
        regions.append(region)

    world.multiworld.regions += regions


def connect_regions(world: RabbitAndSteelWorld) -> None:
    run_type = world.options.run_type

    lobby = world.get_region(world.origin_region_name)

    kingdom_outskirts = None
    if OUTSKIRTS not in world.options.excluded_kingdoms:
        kingdom_outskirts = world.get_region(OUTSKIRTS)
        lobby.connect(kingdom_outskirts, world.origin_region_name + " to " + OUTSKIRTS)

    crack_in_the_geode = None
    if GEODE not in world.options.excluded_kingdoms:
        crack_in_the_geode = world.get_region(GEODE)
        lobby.connect(crack_in_the_geode, world.origin_region_name + " to " + GEODE)

    # Connects the base regions minus the Moonlit Pinnacle to Kingdom Outskirts or Crack In The Geode if Chaotic
    for kingdom_name in Items.kingdom_names:
        if kingdom_name == OUTSKIRTS or kingdom_name == PINNACLE:
            continue

        if kingdom_name not in world.options.excluded_kingdoms:
            kingdom_region = world.get_region(kingdom_name)
            if kingdom_outskirts is not None:
                kingdom_outskirts.connect(kingdom_region, OUTSKIRTS + " to " + kingdom_name)
            if crack_in_the_geode is not None and run_type == RunType.option_chaotic:
                crack_in_the_geode.connect(kingdom_region, GEODE + " to " + kingdom_name)

    # Connects the extra regions minus the Reflecting Pool to Crack In The Geode or Kingdom Outskirts if Chaotic
    for kingdom_name in Items.extra_kingdom_names:
        if kingdom_name == GEODE or kingdom_name == POOL:
            continue

        if kingdom_name not in world.options.excluded_kingdoms:
            kingdom_region = world.get_region(kingdom_name)
            if kingdom_outskirts is not None and run_type == RunType.option_chaotic:
                kingdom_outskirts.connect(kingdom_region, OUTSKIRTS + " to " + kingdom_name)
            if crack_in_the_geode is not None:
                crack_in_the_geode.connect(kingdom_region, GEODE + " to " + kingdom_name)

    moonlit_pinnacle = None
    reflecting_pool = None

    # Connects The Pale Keep to the Moonlit Pinnacle and the Reflecting Pool if Chaotic
    if KEEP not in world.options.excluded_kingdoms:
        pale_keep = world.get_region(KEEP)
        if PINNACLE not in world.options.excluded_kingdoms:
            moonlit_pinnacle = world.get_region(PINNACLE)
            pale_keep.connect(moonlit_pinnacle, KEEP + " to " + PINNACLE)
        if POOL not in world.options.excluded_kingdoms and run_type == RunType.option_chaotic:
            reflecting_pool = world.get_region(POOL)
            pale_keep.connect(reflecting_pool, KEEP + " to " + POOL)

    # Connects the Looping Hallway to the Reflecting Pool and the Moonlit Pinnacle if Chaotic
    if HALLWAY not in world.options.excluded_kingdoms:
        looping_hallway = world.get_region(HALLWAY)
        if PINNACLE not in world.options.excluded_kingdoms and run_type == RunType.option_chaotic:
            moonlit_pinnacle = world.get_region(PINNACLE)
            looping_hallway.connect(moonlit_pinnacle, HALLWAY + " to " + PINNACLE)
        if POOL not in world.options.excluded_kingdoms:
            reflecting_pool = world.get_region(POOL)
            looping_hallway.connect(reflecting_pool, HALLWAY + " to " + POOL)

    # Connects the regions for the class checks for the regions Scholar's Nest - The Pale Keep to their parent region
    if world.options.checks_per_class:
        for kingdom_name in (Items.kingdom_names + Items.extra_kingdom_names):
            if kingdom_name == PINNACLE or kingdom_name == POOL:
                continue

            if kingdom_name not in world.options.excluded_kingdoms:
                kingdom_region = world.get_region(kingdom_name)

                for class_name in world.options.checks_per_class:
                    kingdom_class_region = world.get_region(kingdom_name + " - " + class_name)
                    kingdom_region.connect(kingdom_class_region, kingdom_name + " - " + class_name)

    # Find the classes that will have checks in the last kingdom
    class_checks_for_boss = Items.class_names
    # TODO: Use below if finishing runs aren't a goal condition
    # class_checks_for_boss = world.options.checks_per_class

    # Connect the regions for those classes to the Moonlit Pinnacle
    if moonlit_pinnacle is not None:
        for class_name in class_checks_for_boss:
            moonlit_class_region = world.get_region(PINNACLE + " - " + class_name)
            moonlit_pinnacle.connect(moonlit_class_region, PINNACLE + " - " + class_name)

    # Connect the regions for those classes to the Reflecting Pool
    if reflecting_pool is not None:
        for class_name in class_checks_for_boss:
            reflecting_class_region = world.get_region(POOL + " - " + class_name)
            reflecting_pool.connect(reflecting_class_region, POOL + " - " + class_name)

    # Connect shop region if all shops share locations
    if world.options.shop_sanity == world.options.shop_sanity.option_global:
        shop_region = world.get_region("Shops")

        for kingdom_name in (Items.kingdom_names + Items.extra_kingdom_names):
            if kingdom_name == OUTSKIRTS or kingdom_name == GEODE:
                continue

            if kingdom_name == PINNACLE or kingdom_name == POOL:
                continue

            if kingdom_name not in world.options.excluded_kingdoms:
                kingdom_region = world.get_region(kingdom_name)
                kingdom_region.connect(shop_region, kingdom_name + " to Shop")
