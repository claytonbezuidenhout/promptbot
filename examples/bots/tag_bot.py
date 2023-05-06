from promptbot import PromptBot
from promptbot.tools.logger import get_logger

log = get_logger()


class TagBot(PromptBot):
    """
    A class for creating creative tags for products based on text descriptions
    using linguistics to convey meaning in tags.
    Rules:
    1. Must output only in valid CSV format.
    2. Cannot provide any dialog or request additional info.
    3. Cannot change the product ID.
    Methods:
    yield_batches(list_of_products, batch_size) --> divides products into batches
    run(list_of_products) --> generates tags for each product batch
    Attributes:
    None
    """

    def __init__(self):
        super().__init__("TagBot")
        self.add_cmd("I create creative tags for products based on text descriptions.")
        self.add_cmd(
            "I am an expert at linguistics and can easily ensure meaning is conveyed at tag creation."
        )
        self.add_rule("I must output only in valid CSV format")
        self.add_rule("I cannot provide any dialog or request additional info")
        self.add_rule("I cannot change the product ID")
        self.set_example_input(
            '{"id":"B04", "text":"Glittered Hammock Shirt with stylish buttons"}\n')
        self.set_example_output(
            '123|Glittered Hammock Shirt with stylish buttons|shirt, glitter, stylish')

    @staticmethod
    def yield_batches(list_of_products: list, batch_size: int = 10) -> None:
        """
        Divides a list of products into batches.
        :param list_of_products: A list of products for which to generate tags.
        :param batch_size: The number of products in each batch. Default is 10.
        :return: None
        """
        for i in range(0, len(list_of_products), batch_size):
            yield list_of_products[i:i + batch_size]

    def run(self, list_of_products) -> list[str]:
        """
        Generates tags for each batch of products and returns the results.
        :param list_of_products: A list of products for which to generate tags.
        :return: A list containing the generated tags for each batch of products.
        """
        results = []
        for batch in self.yield_batches(list_of_products, batch_size=10):
            log.info(f"Processing batch of {len(batch)} tag requests")
            self.set_goal(f"GENERATE TAGS FOR:\n{batch}")
            result = self.run_ai()
            results.append(result)
        return results


if __name__ == "__main__":
    bot = TagBot()
    product_list = [
        {"id": "B001",
         "text": "Road Bike - A lightweight bike designed for speed on paved roads, with narrow tires and drop "
                 "handlebars."},
        {"id": "B002",
         "text": "Mountain Bike - A sturdy bike built for off-road terrain, with wide tires and suspension for shock "
                 "absorption."},
        {"id": "B003",
         "text": "Hybrid Bike - A versatile bike that combines features of road and mountain bikes, ideal for urban "
                 "commuting and light trail riding."},
        {"id": "B004",
         "text": "Folding Bike - A compact bike that can be folded and stored easily, perfect for city dwellers with "
                 "limited storage space."},
        {"id": "B005",
         "text": "Cruiser Bike - A comfortable bike with a relaxed, upright riding position and wide, cushioned seat, "
                 "ideal for leisurely rides."},
        {"id": "B006",
         "text": "Electric Bike - A bike with an electric motor and battery, offering pedal assistance or full electric"
                 " power, ideal for longer commutes or hilly terrain."},
        {"id": "B007",
         "text": "BMX Bike - A small, lightweight bike with a strong frame and large handlebars, ideal for performing "
                 "tricks and stunts."},
        {"id": "B008",
         "text": "Touring Bike - A bike designed for long-distance travel, with a comfortable riding position, durable "
                 "frame, and racks for carrying gear."},
        {"id": "B009",
         "text": "Gravel Bike - A versatile bike designed for riding on mixed terrain, with wider tires and a more "
                 "relaxed riding position than a road bike."},
        {"id": "B010",
         "text": "Tandem Bike - A bike designed for two riders, with two sets of pedals and a longer frame, ideal for "
                 "couples or friends who want to ride together."}
    ]

    bot.run(product_list)
    log.info(f"Result: {bot.result}")
    bot.start_improvements()
    with open("tags_result.csv", "w") as f:
        f.write(bot.result)

# Example output:
# B001|Road Bike - A lightweight bike designed for speed on paved roads, with narrow tires and drop handlebars.|road bike, lightweight, speed, paved, narrow, drop handlebars
# B002|Mountain Bike - A sturdy bike built for off-road terrain, with wide tires and suspension for shock absorption.|mountain bike, sturdy, off-road, wide tires, suspension, shock absorption
# B003|Hybrid Bike - A versatile bike that combines features of road and mountain bikes, ideal for urban commuting and light trail riding.|hybrid bike, versatile, road bike, mountain bike, urban commuting, light trail riding
# B004|Folding Bike - A compact bike that can be folded and stored easily, perfect for city dwellers with limited storage space.|folding bike, compact, stored easily, city dwellers, limited storage space
# B005|Cruiser Bike - A comfortable bike with a relaxed, upright riding position and wide, cushioned seat, ideal for leisurely rides.|cruiser bike, comfortable, relaxed riding position, wide cushioned seat, leisurely rides
# B006|Electric Bike - A bike with an electric motor and battery, offering pedal assistance or full electric power, ideal for longer commutes or hilly terrain.|electric bike, electric motor, battery, pedal assistance, full electric power, longer commutes, hilly terrain
# B007|BMX Bike - A small, lightweight bike with a strong frame and large handlebars, ideal for performing tricks and stunts.|BMX bike, small, lightweight, strong frame, large handlebars, performing tricks, stunts
# B008|Touring Bike - A bike designed for long-distance travel, with a comfortable riding position, durable frame, and racks for carrying gear.|touring bike, long-distance travel, comfortable riding position, durable frame, racks, carrying gear
# B009|Gravel Bike - A versatile bike designed for riding on mixed terrain, with wider tires and a more relaxed riding position than a road bike.|gravel bike, versatile, mixed terrain, wider tires, relaxed riding position, road bike
# B010|Tandem Bike - A bike designed for two riders, with two sets of pedals and a longer frame, ideal for couples or friends who want to ride together.|tandem bike, two riders, two sets of pedals, longer frame, couples, friends, ride together
