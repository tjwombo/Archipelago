from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification
from .Constants import kingdom_names, class_names, extra_kingdom_names, shira_defeat_names, witch_defeat_names

if TYPE_CHECKING:
    from .World import RabbitAndSteelWorld


class RabbitAndSteelItem(Item):
    game: str = "Rabbit and Steel"
    item_type: str = ""

    def set_type(self, type_name: str):
        self.item_type = type_name

    def is_type(self, type_name: str):
        return self.item_type == type_name


def get_random_filler_item_name(world: RabbitAndSteelWorld) -> str:
    if world.random.randint(0, 99) < -1:
        return "future trap"

    # TODO: split between all filler items
    return "Gold"


def create_item_with_classification(world: RabbitAndSteelWorld, name: str) -> RabbitAndSteelItem:
    classification = get_classification(name)

    # TODO update classification that change with options

    return RabbitAndSteelItem(name, classification, item_table[name], world.player)


def get_classification(name: str) -> ItemClassification:
    if name in kingdom_items.keys():
        return ItemClassification.progression
    elif name in extra_kingdom_items.keys():
        return ItemClassification.progression
    elif name in class_items.keys():
        return ItemClassification.progression
    elif name in other_progression_items.keys():
        return ItemClassification.progression_skip_balancing
    elif name in useful_items.keys():
        return ItemClassification.useful
    elif name in itemset_items.keys():
        return ItemClassification.useful
    elif name in specific_item_items.keys():
        return ItemClassification.useful
    elif name in upgrade_items.keys():
        return ItemClassification.useful
    elif name in specific_upgrade_items.keys():
        return ItemClassification.useful
    elif name in potion_items.keys():
        return ItemClassification.useful
    return ItemClassification.filler


def create_all_items(world: RabbitAndSteelWorld) -> None:
    kingdom_sanity = world.options.kingdom_sanity.value
    excluded_kingdoms = world.options.excluded_kingdoms.value
    exclude_class = world.options.exclude_class.value

    itempool: list[RabbitAndSteelItem] = []

    if kingdom_sanity:
        for kingdom in kingdom_items:
            if kingdom in excluded_kingdoms:
                continue
            if kingdom == world.starting_hallway_name:
                continue
            itempool += [world.create_item_with_type(kingdom, "Kingdoms")]

        for extra_kingdom in extra_kingdom_items:
            if extra_kingdom in excluded_kingdoms:
                continue
            if extra_kingdom == world.starting_hallway_name:
                continue
            itempool += [world.create_item_with_type(extra_kingdom, "Kingdoms")]

    progressive_regions = world.options.progressive_regions.value
    max_kingdoms_per_run = world.options.max_kingdoms_per_run.value

    if progressive_regions:
        for i in range(max_kingdoms_per_run + 2):
            itempool += [world.create_item("Progressive Region")]

    class_sanity = world.options.class_sanity.value

    if class_sanity:
        for class_item in class_items:
            if class_item in exclude_class:
                continue
            if class_item == world.starting_class_name:
                continue
            itempool += [world.create_item_with_type(class_item, "Classes")]

    item_sanity = world.options.item_sanity
    if item_sanity == "itemset":
        for itemset_item in itemset_items:
            itempool += [world.create_item_with_type(itemset_item, "Items")]
    elif item_sanity == "full":
        for specific_item in specific_item_items:
            itempool += [world.create_item_with_type(specific_item, "Item")]

    create_real_item_chests = world.options.checks_per_item_in_chest.value

    num_real_chests = 6  # Might want to adjust this for combat logic, among other things
    if create_real_item_chests:
        for i in range(num_real_chests):
            itempool += [world.create_item("Treasuresphere")]

    upgrade_sanity = world.options.upgrade_sanity
    if upgrade_sanity == "simple":
        for upgrade_item in upgrade_items:
            itempool += [world.create_item_with_type(upgrade_item, "Upgrades")]
    elif upgrade_sanity == "full":
        for upgrade_item in specific_upgrade_items:
            itempool += [world.create_item_with_type(upgrade_item, "Upgrades")]

    potion_sanity = world.options.potion_sanity
    if potion_sanity != "none":
        for potion_item in potion_items:
            itempool += [world.create_item_with_type(potion_item, "Potions")]

    number_of_items = len(itempool)

    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))

    if world.options.goal_condition == world.options.goal_condition.option_both:
        number_of_unfilled_locations -= (len(class_items) - len(exclude_class)) * 2
    else:
        number_of_unfilled_locations -= (len(class_items) - len(exclude_class))

    itempool += [world.create_filler() for _ in range(number_of_unfilled_locations - number_of_items)]

    world.multiworld.itempool += itempool


item_id = 1

kingdom_items = {}
for item in kingdom_names:
    kingdom_items[item] = item_id
    item_id += 1

extra_kingdom_items = {}
for item in extra_kingdom_names:
    extra_kingdom_items[item] = item_id
    item_id += 1

class_items = {}
for item in class_names:
    class_items[item] = item_id
    item_id += 1

itemset_names = ["Arcane Set", "Night Set", "Timespace Set", "Wind Set", "Bloodwolf Set", "Assassin Set",
                 "Rockdragon Set", "Flame Set", "Gem Set", "Lightning Set", "Shrine Set", "Lucky Set", "Life Set",
                 "Poison Set", "Depth Set", "Darkbite Set", "Timegem Set", "Youkai Set", "Haunted Set", "Gladiator Set",
                 "Sparkblade Set", "Swiftflight Set", "Sacredflame Set", "Ruins Set", "Lakeshrine Set", "Glacier Set",
                 "Memory Set", "Cultist Set", "Painters Set", "Daynight Set", "Sharpedge Set", "Oceans Set",
                 "Performers Set", "Miners Set", "Teaparty Set"]
itemset_items = {}
for item in itemset_names:
    itemset_items[item] = item_id
    item_id += 1

specific_items_names = ["Raven Grimoire", "Blackwing Staff", "Curse Talon", "Darkmagic Blade", "Witchs Cloak",
                        "Crowfeather Hairpin", "Redblack Ribbon", "Opal Necklace", "Sleeping Greatbow",
                        "Crescentmoon Dagger", "Lullaby Harp", "Nightstar Grimoire", "Moon Pendant", "Pajama Hat",
                        "Stuffed Rabbit", "Nightingale Gown", "Eternity Flute", "Timewarp Wand", "Chrome Shield",
                        "Clockwork Tome", "Metronome Boots", "Timemage Cap", "Starry Cloak", "Gemini Necklace",
                        "Hawkfeather Fan", "Windbite Dagger", "Pidgeon Bow", "Shinsoku Katana", "Eaglewing Charm",
                        "Sparrow Feather", "Winged Cap", "Thiefs Coat", "Vampric Dagger", "Bloody Bandage",
                        "Leech Staff", "Bloodhound Greatsword", "Reaper Cloak", "Bloodflower Brooch", "Wolf Hood",
                        "Blood Vial", "Black Wakizashi", "Throwing Dagger", "Assassins Knife", "Ninjutsu Scroll",
                        "Shadow Bracelet", "Ninja Robe", "Kunoichi Hood", "Shinobi Tabi", "Dragonhead Spear",
                        "Granite Greatsword", "Greysteel Shield", "Stonebreaker Staff", "Tough Gauntlet",
                        "Rockdragon Mail", "Obsidian Hairpin", "Iron Greaves", "Volcano Spear", "Reddragon Blade",
                        "Flame Bow", "Meteor Staff", "Phoenix Charm", "Firescale Corset", "Demon Horns",
                        "Flamewalker Boots", "Diamond Shield", "Peridot Rapier", "Garnet Staff", "Sapphire Violin",
                        "Emerald Chestplate", "Amethyst Bracelet", "Topaz Charm", "Ruby Circlet", "Brightstorm Spear",
                        "Bolt Staff", "Lightning Bow", "Darkstorm Knife", "Darkcloud Necklace", "Crown Of Storms",
                        "Thunderclap Gloves", "Storm Petticoat", "Holy Greatsword", "Sacred Bow", "Purification Rod",
                        "Ornamental Bell", "Shrinemaidens Kosode", "Redwhite Ribbon", "Divine Mirror", "Golden Chime",
                        "Book Of Cheats", "Golden Katana", "Glittering Trumpet", "Royal Staff", "Ballroom Gown",
                        "Silver Coin", "Queens Crown", "Mimick Rabbitfoot", "Butterfly Ocarina", "Fairy Spear",
                        "Moss Shield", "Floral Bow", "Blue Rose", "Sunflower Crown", "Midsummer Dress",
                        "Grasswoven Bracelet", "Snakefang Dagger", "Ivy Staff", "Deathcap Tome", "Spiderbite Bow",
                        "Compound Gloves", "Poisonfrog Charm", "Venom Hood", "Chemists Coat", "Seasheel Shield",
                        "Necronomicon", "Tidal Greatsword", "Occult Dagger", "Mermaid Scalemail", "Hydrous Blob",
                        "Abyss Artifact", "Lost Pendant", "Sawtooth Cleaver", "Ravens Dagger", "Killing Note",
                        "Blacksteel Buckler", "Nightguard Gloves", "Snipers Eyeglasses", "Darkmage Charm",
                        "Firststrike Bracelet", "Obsidian Rod", "Darkglass Spear", "Timespace Dagger",
                        "Quartz Shield", "Pocketwatch", "Nova Crown", "Blackhole Charm", "Twinstar Earrings",
                        "Kyou No Omikuji", "Youkai Bracelet", "Oni Staff", "Kappa Shield", "Usagi Kamen",
                        "Red Tanzaku", "Vega Spear", "Altair Dagger", "Ghost Spear", "Phantom Dagger",
                        "Cursed Candlestaff", "Haunted Gloves", "Old Bonnet", "Maid Outfit", "Calling Bell",
                        "Smoke Shield", "Grandmaster Spear", "Teacher Knife", "Tactician Rod", "Spiked Shield",
                        "Battlemaiden Armor", "Gladiator Helmet", "Lancer Gauntlets", "Lion Charm", "Bluebolt Staff",
                        "Lapis Sword", "Shockwave Tome", "Battery Shield", "Raiju Crown", "Staticshock Earrings",
                        "Stormdance Gown", "Blackbolt Ribbon", "Crane Katana", "Falconfeather Dagger",
                        "Tornado Staff", "Cloud Guard", "Hermes Bow", "Talon Charm", "Tiny Wings",
                        "Feathered Overcoat", "Sandpriestess Spear", "Flamedancer Dagger", "Whiteflame Staff",
                        "Sacred Shield", "Marble Clasp", "Sun Pendant", "Tiny Hourglass", "Desert Earrings",
                        "Giant Stone Club", "Ruins Sword", "Mountain Staff", "Boulder Shield", "Golems Claymore",
                        "Stoneplate Armor", "Sacredstone Charm", "Clay Rabbit", "Waterfall Polearm", "Vorpal Dao",
                        "Jade Staff", "Reflection Shield", "Butterfly Hairpin", "Watermage Pendant",
                        "Raindrop Earrings", "Aquamarine Bracelet", "Glacier Spear", "Frost Dagger", "Frozen Staff",
                        "Coldsteel Shield", "Polar Coat", "Icicle Earrings", "Winter Hat", "Snow Boots",
                        "Spear Of Remorse", "Memory Greatsword", "Staff Of Sorrow", "Shield Of Smiles",
                        "Lonesome Pendant", "Spark Of Determination", "Crown Of Love", "Comforting Coat",
                        "Righthand Cast", "Lefthand Cast", "Hexed Blindfold", "Angels Halo", "Unsacred Pendant",
                        "Whitewing Bracelet", "Darkcrystal Rose", "Dark Wings", "Giant Paintbrush", "Sewing Sword",
                        "Sketchbook", "Palette Shield", "Handmade Charm", "Painters Beret", "Artist Smock",
                        "Colorful Earrings", "Daylight Sword", "Nightgleam Sword", "Spear Of Winds", "Spear Of Rains",
                        "Heavens Codex", "Hells Codex", "Robe Of Lights", "Robe Of Dark", "Hooked Staff",
                        "Springloaded Scythe", "Hidden Blade", "Sharpedged Shield", "Pointed Ring",
                        "Crown Of Swords", "Bladed Cload", "Greatsword Pendant", "Rusted Greatsword", "Sand Shovel",
                        "Saltwater Staff", "Large Umbrella", "Onepiece Swimsuit", "Straw Hat", "Large Anchor",
                        "Beach Sandals", "Strongmans Bard", "Spinning Chakram", "Ribboned Staff", "Trick Shield",
                        "Rosered Leotard", "Jesters Hat", "Rainbow Cape", "Performers Shoes", "Iron Pickaxe",
                        "Dynamite Staff", "Fossil Dagger", "Drill Shield", "Canary Charm", "Pyrite Earrings",
                        "Cavers Cloak", "Miners Headlamp", "Tiny Fork", "Stirring Spoon", "Fanciful Book",
                        "Apple Plate", "Vanilla Wafers", "Caramel Tea", "Strawberry Cake", "Sweet Taffy"]
specific_item_items = {}
for item in specific_items_names:
    specific_item_items[item] = item_id
    item_id += 1

upgrade_names = ["Emerald Gem", "Garnet Gem", "Ruby Gem", "Sapphire Gem", "Opal Gem"]
upgrade_items = {}
for item in upgrade_names:
    upgrade_items[item] = item_id
    item_id += 1

specific_upgrade_names = ["Primary Emerald Gem", "Primary Garnet Gem", "Primary Ruby Gem", "Primary Sapphire Gem",
                          "Primary Opal Gem",
                          "Secondary Emerald Gem", "Secondary Garnet Gem", "Secondary Ruby Gem",
                          "Secondary Sapphire Gem", "Secondary Opal Gem",
                          "Special Emerald Gem", "Special Garnet Gem", "Special Ruby Gem", "Special Sapphire Gem",
                          "Special Opal Gem",
                          "Defensive Emerald Gem", "Defensive Garnet Gem", "Defensive Ruby Gem",
                          "Defensive Sapphire Gem", "Defensive Opal Gem"]
specific_upgrade_items = {}
for item in specific_upgrade_names:
    specific_upgrade_items[item] = item_id
    item_id += 1

potion_names = ["Full Heal Potion", "Level Up Potion", "Regen Potion", "Essence of Spell", "Darkness Potion",
                "Quickening Potion", "Winged Potion", "Essence of Wit", "Swifthand Potion", "Fire Potion",
                "Strength Potion", "Gold Potion", "Luck Potion", "Essence of Steel", "Evasion Potion", "Longarm Potion",
                "Vitality Potion"]
potion_items = {}
for item in potion_names:
    potion_items[item] = item_id
    item_id += 1

shira_defeat_items = {}
for item in shira_defeat_names:
    shira_defeat_items[item] = item_id
    item_id += 1

witch_defeat_items = {}
for item in witch_defeat_names:
    witch_defeat_items[item] = item_id
    item_id += 1

other_progression_items = {
    "Progressive Region": item_id,
}
item_id += 1

useful_items = {
    "XP": item_id,
    "Treasuresphere": item_id + 1,
}
item_id += 2

filler_item = {
    "Gold": item_id,
}
item_id += 1

item_table = kingdom_items | class_items | itemset_items | specific_item_items | other_progression_items | \
             useful_items | filler_item | upgrade_items | specific_upgrade_items | potion_items | shira_defeat_items | \
             witch_defeat_items | extra_kingdom_items
