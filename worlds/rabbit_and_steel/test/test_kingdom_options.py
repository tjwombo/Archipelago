from .bases import RabbitAndSteelTestBase
from ..Constants import ALL_KINGDOM_ORDER_KINGDOM_NAMES, KEEP, HALLWAY, PINNACLE, POOL
from ..Options import KingdomSanity, ProgressiveRegions, UseKingdomOrderWithKingdomSanity


class TestKingdomOptions(RabbitAndSteelTestBase):
    run_default_tests = False
    kingdoms = ALL_KINGDOM_ORDER_KINGDOM_NAMES

    # Turn the kingdom order into an order lookup table
    def getOrderedKingdoms(self, kingdom_order: dict[str, int]) -> dict[int, list[str]]:
        ordered_kingdom = {}
        for kingdom in self.kingdoms:
            order = kingdom_order[kingdom]
            if order in ordered_kingdom:
                ordered_kingdom[order].append(kingdom)
            else:
                ordered_kingdom[order] = [kingdom]
        return ordered_kingdom

    # Assert that collecting the kingdom and/or progressive region allows each kingdom in the list to be reachable
    def assertKingdoms(self, kingdoms: list[str], collect_kingdom: bool = False, collect_region: bool = False):
        if collect_region:
            progressive_region = self.get_items_by_name("Progressive Region")[0]

            for kingdom in kingdoms:
                self.assertFalse(self.can_reach_region(kingdom),
                                 f"Able to reach {kingdom} with only "
                                 f"{self.count('Progressive Region')} out of "
                                 f"{self.options['max_kingdoms_per_run']} progressive regions")

            self.collect(progressive_region)

            if not collect_kingdom:
                for kingdom in kingdoms:
                    self.assertTrue(self.can_reach_region(kingdom),
                                    f"Unable to reach {kingdom} with only "
                                    f"{self.count('Progressive Region')} out of "
                                    f"{self.options['max_kingdoms_per_run']} progressive regions")
        if collect_kingdom:
            for kingdom in kingdoms:
                self.assertFalse(self.can_reach_region(kingdom),
                                 f"Able to reach {kingdom} without any kingdoms")

                self.collect_by_name(kingdom)

                self.assertTrue(self.can_reach_region(kingdom),
                                f"Unable to reach {kingdom} with the kingdom item")

    # Assert that a path from order [1, order-1] comprised of reachable regions is required
    def assertOrderedPathNeeded(self, ordered_kingdom: dict[int, list[str]], order: int):
        for kingdom in ordered_kingdom[order]:
            added_kingdoms: list[str] = []

            # Test to make sure you need the full forward path
            for i in range(1, order):
                self.assertFalse(self.can_reach_region(kingdom),
                                 f"Able to reach {kingdom} without any other kingdoms")

                added_kingdoms.append(self.multiworld.random.choice(ordered_kingdom[i]))
                self.collect_by_name(added_kingdoms[-1])

            self.assertTrue(self.can_reach_region(kingdom),
                            f"Unable to reach {kingdom} with valid kingdom path")

            for kingdom_path in added_kingdoms:
                self.remove_by_name(kingdom_path)
            added_kingdoms = []

            # Test to make sure you need the full backwards path
            for i in range(order - 1, 0, -1):
                self.assertFalse(self.can_reach_region(kingdom),
                                 f"Able to reach {kingdom} without any other kingdoms")

                added_kingdoms.append(self.multiworld.random.choice(ordered_kingdom[i]))
                self.collect_by_name(added_kingdoms[-1])

            self.assertTrue(self.can_reach_region(kingdom),
                            f"Unable to reach {kingdom} with valid kingdom path")

            for kingdom_path in added_kingdoms:
                self.remove_by_name(kingdom_path)

    def test_random_kingdom_order_with_all_true(self):
        self.options['kingdom_sanity'] = KingdomSanity.option_true
        self.options['progressive_regions'] = ProgressiveRegions.option_true
        self.options['kingdom_sanity_kingdom_order'] = UseKingdomOrderWithKingdomSanity.option_true

        for i in range(1, len(self.kingdoms) + 1):
            self.options['max_kingdoms_per_run'] = i
            self.world_setup()

            kingdom_order = self.multiworld.worlds[self.player].options.as_dict('kingdom_order')['kingdom_order']

            ordered_kingdom = self.getOrderedKingdoms(kingdom_order)

            self.assertFalse(0 in ordered_kingdom, "Some kingdoms were not assigned an order")

            for j in range(1, i + 1):
                self.assertKingdoms(ordered_kingdom[j], True, True)

            self.assertKingdoms([KEEP, HALLWAY], True, True)

            self.assertKingdoms([PINNACLE, POOL], True, True)

    def test_random_kingdom_order_without_kingdom_sanity(self):
        self.options['kingdom_sanity'] = KingdomSanity.option_false
        self.options['progressive_regions'] = ProgressiveRegions.option_true
        self.options['kingdom_sanity_kingdom_order'] = UseKingdomOrderWithKingdomSanity.option_true

        for i in range(1, len(self.kingdoms) + 1):
            self.options['max_kingdoms_per_run'] = i
            self.world_setup()

            kingdom_order = self.multiworld.worlds[self.player].options.as_dict('kingdom_order')['kingdom_order']

            ordered_kingdom = self.getOrderedKingdoms(kingdom_order)

            self.assertFalse(0 in ordered_kingdom, "Some kingdoms were not assigned an order")

            for j in range(1, i + 1):
                self.assertKingdoms(ordered_kingdom[j], False, True)

            self.assertKingdoms([KEEP, HALLWAY], False, True)

            self.assertKingdoms([PINNACLE, POOL], False, True)

    def test_random_kingdom_order_without_progressive_regions(self):
        self.options['kingdom_sanity'] = KingdomSanity.option_true
        self.options['progressive_regions'] = ProgressiveRegions.option_false
        self.options['kingdom_sanity_kingdom_order'] = UseKingdomOrderWithKingdomSanity.option_true

        for i in range(1, len(self.kingdoms) + 1):
            self.options['max_kingdoms_per_run'] = i
            self.world_setup()

            kingdom_order = self.multiworld.worlds[self.player].options.as_dict('kingdom_order')['kingdom_order']

            self.assertTrue(len(self.get_items_by_name("Progressive Region")) == 0,
                            f"Progressive Regions were created when option was false")

            ordered_kingdom = self.getOrderedKingdoms(kingdom_order)
            # Pretend the Penultimate and Ultimate hallways are part of kingdom order
            ordered_kingdom[i + 1] = [KEEP, HALLWAY]
            ordered_kingdom[i + 2] = [PINNACLE, POOL]

            self.assertFalse(0 in ordered_kingdom, "Some kingdoms were not assigned an order")

            self.assertKingdoms(ordered_kingdom[1], True, False)

            for j in range(2, i + 3):  # Include the two new 'orders'
                for k in range(1, j):
                    for kingdom in ordered_kingdom[k]:
                        self.remove_by_name(kingdom)

                # Assert that just the kingdom isn't enough
                for kingdom in ordered_kingdom[j]:
                    self.assertFalse(self.can_reach_region(kingdom),
                                     f"Able to reach {kingdom} without any kingdoms")

                    self.collect_by_name(kingdom)
                    self.assertFalse(self.can_reach_region(kingdom),
                                     f"Able to reach {kingdom} without any other kingdoms")

                self.assertOrderedPathNeeded(ordered_kingdom, j)

    def test_random_kingdom_order_without_kingdom_order(self):
        self.options['kingdom_sanity'] = KingdomSanity.option_true
        self.options['progressive_regions'] = ProgressiveRegions.option_true
        self.options['kingdom_sanity_kingdom_order'] = UseKingdomOrderWithKingdomSanity.option_false

        for i in range(1, len(self.kingdoms) + 1):
            self.options['max_kingdoms_per_run'] = i
            self.world_setup()

            kingdom_order = self.multiworld.worlds[self.player].options.as_dict('kingdom_order')['kingdom_order']
            progressive_region = self.get_items_by_name("Progressive Region")[0]

            ordered_kingdom = self.getOrderedKingdoms(kingdom_order)

            self.assertTrue(len(ordered_kingdom[0]) == len(self.kingdoms), "Some kingdoms were assigned an order")

            for kingdom in ordered_kingdom[0]:
                self.assertFalse(self.can_reach_region(kingdom),
                                 f"Able to reach {kingdom} without obtaining the kingdom item")
                self.collect_by_name(kingdom)
                self.assertFalse(self.can_reach_region(kingdom),
                                 f"Able to reach {kingdom} without a progressive region")

            self.collect(progressive_region)

            for kingdom in ordered_kingdom[0]:
                self.assertTrue(self.can_reach_region(kingdom),
                                f"Unable to reach {kingdom} with the kingdom item and 1 progressive region")

            # Get max_run_count - 1 progressive regions, so penultimate kingdoms still fail before giving another region
            for _ in range(i - self.count("Progressive Region")):
                self.collect(progressive_region)

            self.assertKingdoms([KEEP, HALLWAY], True, True)

            self.assertKingdoms([PINNACLE, POOL], True, True)

    def test_random_kingdom_order_with_kingdom_sanity(self):
        self.options['kingdom_sanity'] = KingdomSanity.option_true
        self.options['progressive_regions'] = ProgressiveRegions.option_false
        self.options['kingdom_sanity_kingdom_order'] = UseKingdomOrderWithKingdomSanity.option_false

        for i in range(1, len(self.kingdoms) + 1):
            self.options['max_kingdoms_per_run'] = i
            self.world_setup()

            kingdom_order = self.multiworld.worlds[self.player].options.as_dict('kingdom_order')['kingdom_order']

            self.assertTrue(len(self.get_items_by_name("Progressive Region")) == 0,
                            f"Progressive Regions were created when option was false")

            ordered_kingdom = self.getOrderedKingdoms(kingdom_order)

            self.assertTrue(len(ordered_kingdom[0]) == len(self.kingdoms), "Some kingdoms were assigned an order")

            self.assertKingdoms(ordered_kingdom[0], True, False)

            self.assertKingdoms([KEEP, HALLWAY], True, False)

            self.assertKingdoms([PINNACLE, POOL], True, False)

    def test_random_kingdom_order_with_progressive_region(self):
        self.options['kingdom_sanity'] = KingdomSanity.option_false
        self.options['progressive_regions'] = ProgressiveRegions.option_true
        self.options['kingdom_sanity_kingdom_order'] = UseKingdomOrderWithKingdomSanity.option_false

        for i in range(1, len(self.kingdoms) + 1):
            self.options['max_kingdoms_per_run'] = i
            self.world_setup()

            kingdom_order = self.multiworld.worlds[self.player].options.as_dict('kingdom_order')['kingdom_order']

            ordered_kingdom = self.getOrderedKingdoms(kingdom_order)

            self.assertTrue(0 not in ordered_kingdom,
                            f"Kingdom Order was not applied during just progressive regions")

            for j in range(1, i + 1):
                self.assertKingdoms(ordered_kingdom[j], False, True)

            self.assertKingdoms([KEEP, HALLWAY], False, True)

            self.assertKingdoms([PINNACLE, POOL], False, True)

    def test_random_kingdom_order_with_kingdom_order(self):
        self.options['kingdom_sanity'] = KingdomSanity.option_false
        self.options['progressive_regions'] = ProgressiveRegions.option_false
        self.options['kingdom_sanity_kingdom_order'] = UseKingdomOrderWithKingdomSanity.option_true

        for i in range(1, len(self.kingdoms) + 1):
            self.options['max_kingdoms_per_run'] = i
            self.world_setup()

            kingdom_order = self.multiworld.worlds[self.player].options.as_dict('kingdom_order')['kingdom_order']

            self.assertTrue(len(self.get_items_by_name("Progressive Region")) == 0,
                            f"Progressive Regions were created when option was false")

            ordered_kingdom = self.getOrderedKingdoms(kingdom_order)

            # Kingdom Order is only applied if progressive regions or kingdom sanity and this kingdom order value is on
            self.assertTrue(len(ordered_kingdom[0]) == len(self.kingdoms), "Some kingdoms were assigned an order")

            for kingdom in self.kingdoms:
                self.assertTrue(self.can_reach_region(kingdom), f"Unable to reach {kingdom} with nothing")

            self.assertTrue(self.can_reach_region(KEEP), f"Unable to reach {KEEP} with nothing")
            self.assertTrue(self.can_reach_region(HALLWAY), f"Unable to reach {HALLWAY} with nothing")

            self.assertTrue(self.can_reach_region(PINNACLE), f"Unable to reach {PINNACLE} with nothing")
            self.assertTrue(self.can_reach_region(POOL), f"Unable to reach {POOL} with nothing")

    def test_random_kingdom_order_with_nothing(self):
        self.options['kingdom_sanity'] = KingdomSanity.option_false
        self.options['progressive_regions'] = ProgressiveRegions.option_false
        self.options['kingdom_sanity_kingdom_order'] = UseKingdomOrderWithKingdomSanity.option_false

        for i in range(1, len(self.kingdoms) + 1):
            self.options['max_kingdoms_per_run'] = i
            self.world_setup()

            kingdom_order = self.multiworld.worlds[self.player].options.as_dict('kingdom_order')['kingdom_order']

            self.assertTrue(len(self.get_items_by_name("Progressive Region")) == 0,
                            f"Progressive Regions were created when option was false")

            ordered_kingdom = self.getOrderedKingdoms(kingdom_order)

            self.assertTrue(len(ordered_kingdom[0]) == len(self.kingdoms), "Some kingdoms were assigned an order")

            for kingdom in self.kingdoms:
                self.assertTrue(self.can_reach_region(kingdom), f"Unable to reach {kingdom} with nothing")

            self.assertTrue(self.can_reach_region(KEEP), f"Unable to reach {KEEP} with nothing")
            self.assertTrue(self.can_reach_region(HALLWAY), f"Unable to reach {HALLWAY} with nothing")

            self.assertTrue(self.can_reach_region(PINNACLE), f"Unable to reach {PINNACLE} with nothing")
            self.assertTrue(self.can_reach_region(POOL), f"Unable to reach {POOL} with nothing")
