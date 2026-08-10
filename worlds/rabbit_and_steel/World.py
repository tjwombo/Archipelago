from typing import Dict, Any

from Options import OptionError
from worlds.AutoWorld import World

from . import Items, Locations, Options, Regions, Rules, Web_world
from .Constants import OUTSKIRTS, KEEP, PINNACLE, GEODE, HALLWAY, POOL, CLASS_NAMES, KINGDOM_NAMES, \
    EXTRA_KINGDOM_NAMES, KINGDOM_ORDER_KINGDOM_NAMES, EXTRA_KINGDOM_ORDER_KINGDOM_NAMES, \
    ALL_KINGDOM_ORDER_KINGDOM_NAMES, SHIRA_DEFEAT_NAMES, WITCH_DEFEAT_NAMES

client_version = 1


class RabbitAndSteelWorld(World):
    """
     Rabbit and Steel game description.
    """

    game = "Rabbit and Steel"

    topology_present = True

    web = Web_world.RabbitAndSteelWeb()

    options_dataclass = Options.RabbitAndSteelOptions
    options: Options.RabbitAndSteelOptions

    item_name_to_id = Items.item_table
    location_name_to_id = Locations.location_table

    origin_region_name = "Lobby"

    item_name_groups = {
        "Kingdoms": KINGDOM_NAMES,
        "OrderedKingdoms": ALL_KINGDOM_ORDER_KINGDOM_NAMES,
        "BaseKingdoms": KINGDOM_ORDER_KINGDOM_NAMES,
        "ExtraKingdoms": EXTRA_KINGDOM_ORDER_KINGDOM_NAMES,
        "Classes": CLASS_NAMES,
        "Items": Items.itemset_names + Items.specific_items_names,
        "Upgrades": Items.upgrade_names + Items.specific_upgrade_names,
        "Potions": Items.potion_names,
        "ShiraVictory": SHIRA_DEFEAT_NAMES,
        "WitchVictory": WITCH_DEFEAT_NAMES
    }

    starting_class_name = ""
    starting_hallway_name = ""

    def create_regions(self) -> None:
        Regions.create_and_connect_regions(self)
        Locations.create_all_locations(self)

    def set_rules(self) -> None:
        Rules.set_all_rules(self)

    def create_item(self, name: str) -> Items.RabbitAndSteelItem:
        return Items.create_item_with_classification(self, name)

    def create_item_with_type(self, name: str, type_name: str) -> Items.RabbitAndSteelItem:
        item = Items.create_item_with_classification(self, name)
        item.set_type(type_name)
        return item

    def create_items(self) -> None:
        Items.create_all_items(self)

    def get_filler_item_name(self) -> str:
        return Items.get_random_filler_item_name(self)

    def assign_kingdom_order_groups(self) -> None:
        run_type = self.options.run_type.value

        if run_type == self.options.run_type.option_combined:
            self.assign_kingdom_order(ALL_KINGDOM_ORDER_KINGDOM_NAMES)
        elif run_type == self.options.run_type.option_kingdom:
            self.assign_kingdom_order(KINGDOM_ORDER_KINGDOM_NAMES)
        elif run_type == self.options.run_type.option_extra:
            self.assign_kingdom_order(EXTRA_KINGDOM_ORDER_KINGDOM_NAMES)
        elif run_type == self.options.run_type.option_either:
            self.assign_kingdom_order(KINGDOM_ORDER_KINGDOM_NAMES)
            self.assign_kingdom_order(EXTRA_KINGDOM_ORDER_KINGDOM_NAMES)

    def assign_kingdom_order(self, kingdoms_to_set: list[str]) -> None:
        max_kingdoms_per_run = self.options.max_kingdoms_per_run.value
        kingdom_order = self.options.kingdom_order.value
        excluded_kingdoms = self.options.excluded_kingdoms.value

        unset_kingdoms = [kingdom for (kingdom, order) in kingdom_order.items() if
                          order == 0 and kingdom not in excluded_kingdoms and kingdom in kingdoms_to_set]
        order_amounts = dict.fromkeys([order for order in range(1, max_kingdoms_per_run + 1)], 0)

        # Ensure we have enough valid kingdoms and assign the kingdoms that have a specific value
        valid_placements = 0
        for (kingdom, value) in kingdom_order.items():
            if kingdom not in kingdoms_to_set:
                continue
            if kingdom in excluded_kingdoms:
                continue
            if value <= 0:
                if value == 0:
                    valid_placements += 1
                continue
            if value > max_kingdoms_per_run:
                raise OptionError(f"Player {self.player_name} has an order value above the number of visitable "
                                  f"kingdoms in a run: \n"
                                  f"{kingdom} has value {value} and needs to be at most {max_kingdoms_per_run}")
            order_amounts[value] = order_amounts.get(value, 0) + 1
            valid_placements += 1

        if valid_placements < max_kingdoms_per_run:
            raise OptionError(f"Player {self.player_name} has too many inaccessible kingdoms: "
                              f"\n{kingdom_order}\nhas {valid_placements} and needs at least {max_kingdoms_per_run}")

        # Place the regions with order 0
        while len(unset_kingdoms) > 0:
            kingdom_to_set = self.random.choice(unset_kingdoms)
            unset_kingdoms.remove(kingdom_to_set)

            smallest_order_len = 1
            smallest_occurrence = 10
            for (order, amount) in reversed(order_amounts.items()):
                if amount < smallest_occurrence:
                    smallest_order_len = order
                    smallest_occurrence = amount

            kingdom_order[kingdom_to_set] = smallest_order_len
            order_amounts[smallest_order_len] += 1

        # Ensure there are at least one kingdom per accessible order
        buffer = 0
        for i in range(1, max_kingdoms_per_run + 1):
            buffer += order_amounts[i]
            buffer -= 1
            if buffer < 0:
                raise OptionError(f"Player {self.player_name} can not reach all valid kingdoms: \n{kingdom_order}")

        # TODO: IF RUN TYPE IS NOT CHAOTIC, ENSURE KINGDOM ORDER RESPECTS ORIGIN
        print(kingdom_order)

    def generate_early(self) -> None:
        # Check if there are enough classes for the options
        if self.options.checks_per_class.__contains__("_ALL"):
            self.options.checks_per_class.value = set(CLASS_NAMES) - set(self.options.exclude_class)

        remaining_classes = (set(CLASS_NAMES) - set(self.options.exclude_class)) - self.options.checks_per_class.value
        if len(remaining_classes) < self.options.random_class:
            raise OptionError(f"Player {self.player_name} are randomly adding more classes than left available, "
                              f"Randomly including: {self.options.random_class}, remaining classes: "
                              f"{remaining_classes}")
        for i in range(self.options.random_class):
            new_class = self.random.choice(list(remaining_classes))
            self.options.checks_per_class.value.add(new_class)
            remaining_classes.remove(new_class)

        shared_classes = list(set(self.options.checks_per_class) & set(self.options.exclude_class))
        if len(shared_classes) != 0:
            raise OptionError(f"Player {self.player_name} is excluding classes, but expects to get checks with the "
                              f"class: {shared_classes}")

        if len(self.options.exclude_class.value) == len(CLASS_NAMES):
            raise OptionError(f"Player {self.player_name} is excluding all classes, but at least one is needed to play")

        # Move unused kingdoms to excluded kingdoms
        run_type = self.options.run_type.value
        if run_type == self.options.run_type.option_extra:
            self.options.excluded_kingdoms.value = self.options.excluded_kingdoms.value | set(KINGDOM_NAMES)
        elif run_type == self.options.run_type.option_kingdom:
            self.options.excluded_kingdoms.value = self.options.excluded_kingdoms.value | set(EXTRA_KINGDOM_NAMES)

        excluded_base_kingdoms = self.options.excluded_kingdoms.value & set(KINGDOM_NAMES)
        excluded_extra_kingdoms = self.options.excluded_kingdoms.value & set(EXTRA_KINGDOM_NAMES)
        if run_type == self.options.run_type.option_extra or run_type == self.options.run_type.option_either:
            if self.options.max_kingdoms_per_run.value > 3 - len(excluded_extra_kingdoms):
                raise OptionError(f"Player {self.player_name} needs to visit more extra kingdoms than possible."
                                  f" Set run type to chaos if you want to visit base and extra kingdoms in the same run")
        elif run_type == self.options.run_type.option_kingdom:
            if self.options.max_kingdoms_per_run.value > 5 - len(excluded_base_kingdoms):
                raise OptionError(f"Player {self.player_name} needs to visit more base kingdoms than possible."
                                  f" Set run type to chaos if you want to visit base and extra kingdoms in the same run")

        # Check to ensure each boss can be killed enough times
        if (self.options.goal_condition == self.options.goal_condition.option_shira or
                self.options.goal_condition == self.options.goal_condition.option_both):
            if self.options.shira_defeats.value > len(CLASS_NAMES) - len(self.options.exclude_class.value):
                raise OptionError(f"Player {self.player_name} needs to kill Shira more times than available classes")

            if len(self.options.excluded_kingdoms.value & {PINNACLE}) == 1:
                raise OptionError(f"Player {self.player_name} has excluded the " + PINNACLE + ", "
                                                                                              f"despite have Shira kills as a goal")

        if (self.options.goal_condition == self.options.goal_condition.option_witch or
                self.options.goal_condition == self.options.goal_condition.option_both):
            if self.options.witch_defeats.value > len(CLASS_NAMES) - len(self.options.exclude_class.value):
                raise OptionError(f"Player {self.player_name} needs to kill Witch more times than available classes")

            if len(self.options.excluded_kingdoms.value & {POOL}) == 1:
                raise OptionError(f"Player {self.player_name} has excluded the " + POOL + ", "
                                                                                          f"despite have Witch kills as a goal")

        # Check to ensure we can enter the starting, penultimate, and boss hallway
        excluded_starting_hallways = self.options.excluded_kingdoms.value & {OUTSKIRTS, GEODE}
        if len(excluded_starting_hallways) == 2:
            raise OptionError(f"Player {self.player_name} does not have a starting hallway in the item pool."
                              f" They are either excluded or the run type does not pass through them")

        if len(excluded_starting_hallways) == 1 and run_type == self.options.run_type.option_either:
            raise OptionError(f"Player {self.player_name} does not have both starting hallway in the item pool."
                              f" When playing on either run type, neither starting hallway may be excluded")

        excluded_penultimate_hallways = self.options.excluded_kingdoms.value & {KEEP, HALLWAY}
        if len(excluded_penultimate_hallways) == 2:
            raise OptionError(f"Player {self.player_name} does not have a penultimate hallway in the item pool."
                              f" They are either excluded or the run type does not pass through them")

        if len(excluded_penultimate_hallways) == 1 and run_type == self.options.run_type.option_either:
            raise OptionError(f"Player {self.player_name} does not have both penultimate hallway in the item pool."
                              f" When playing on either run type, neither penultimate hallway may be excluded")

        excluded_final_hallways = self.options.excluded_kingdoms.value & {PINNACLE, POOL}
        if len(excluded_final_hallways) == 2:
            raise OptionError(f"Player {self.player_name} does not have a final hallway in the item pool."
                              f" They are either excluded or the run type does not pass through them")

        if len(excluded_final_hallways) == 1 and run_type == self.options.run_type.option_either:
            raise OptionError(f"Player {self.player_name} does not have both final hallway in the item pool."
                              f" When playing on either run type, neither final hallway may be excluded")

        # Assign the kingdom order to included kingdoms
        if ((self.options.progressive_regions and not self.options.kingdom_sanity) or
                (self.options.kingdom_sanity and self.options.kingdom_sanity_kingdom_order)):
            self.assign_kingdom_order_groups()

        # Assign the starting class
        if self.options.class_sanity:
            self.starting_class_name = self.random.choice(tuple(set(CLASS_NAMES) - set(self.options.exclude_class)))
            self.multiworld.push_precollected(self.create_item_with_type(self.starting_class_name, "Classes"))

        # Assign the starting hallway
        if len(excluded_starting_hallways) == 0:
            self.starting_hallway_name = self.random.choice([OUTSKIRTS, GEODE])
            self.multiworld.push_precollected(self.create_item_with_type(self.starting_hallway_name, "Kingdoms"))
        elif len(excluded_starting_hallways) == 1:
            self.starting_hallway_name = {OUTSKIRTS, GEODE} - excluded_starting_hallways
            self.multiworld.push_precollected(self.create_item_with_type(self.starting_hallway_name.pop(), "Kingdoms"))

        # Make the excluded hallways order -1
        kingdom_order = self.options.kingdom_order.value
        excluded_kingdoms = self.options.excluded_kingdoms.value
        for kingdom in kingdom_order.keys():
            if kingdom in excluded_kingdoms:
                kingdom_order[kingdom] = -1

    def fill_slot_data(self) -> Dict[str, Any]:
        return self.options.as_dict(
            "kingdom_sanity", "run_type", "max_kingdoms_per_run", "progressive_regions", "excluded_kingdoms",
            "kingdom_sanity_kingdom_order", "kingdom_order", "class_sanity", "checks_per_class", "item_sanity",
            "checks_per_item_in_chest", "upgrade_sanity", "potion_sanity", "goal_condition", "shira_defeats",
            "witch_defeats", "shop_sanity")
