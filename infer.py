def derive_init_facts(soil_moisture, temperature, humidity, light_intensity, previous_facts=None):
    
    if previous_facts is None:
        previous_facts = set()

    facts = set()

    #-----------------------------------
    # Soil moisture
    #-----------------------------------
    if "soil_dry" in previous_facts:
        if soil_moisture <= 32:
            facts.add("soil_dry")
        elif soil_moisture >= 72:
            facts.add("soil_wet")
        else:
            facts.add("soil_suitable")

    elif "soil_suitable" in previous_facts:
        if soil_moisture < 28:
            facts.add("soil_dry")
        elif soil_moisture > 72:
            facts.add("soil_wet")
        else:
            facts.add("soil_suitable")

    elif "soil_wet" in previous_facts:
        if soil_moisture <= 28:
            facts.add("soil_dry")
        elif soil_moisture >= 68:
            facts.add("soil_wet")
        else:
            facts.add("soil_suitable")

    else:
        if soil_moisture < 30:
            facts.add("soil_dry")
        elif soil_moisture > 70:
            facts.add("soil_wet")
        else:
            facts.add("soil_suitable")

    #-----------------------------------
    # Temperature
    #-----------------------------------
    if "temp_low" in previous_facts:
        if temperature < 16:
            facts.add("temp_low")
        else:
            facts.add("temp_suitable")

    elif "temp_high" in previous_facts:
        if temperature > 29:
            facts.add("temp_high")
        else:
            facts.add("temp_suitable")

    else:
        if temperature < 14:
            facts.add("temp_low")
        elif temperature > 31:
            facts.add("temp_high")
        else:
            facts.add("temp_suitable")

    #-----------------------------------
    # Humidity
    #-----------------------------------
    if "humidity_low" in previous_facts:
        if humidity < 42:
            facts.add("humidity_low")
        else:
            facts.add("humidity_suitable")

    elif "humidity_high" in previous_facts:
        if humidity > 78:
            facts.add("humidity_high")
        else:
            facts.add("humidity_suitable")

    else:
        if humidity < 38:
            facts.add("humidity_low")
        elif humidity > 82:
            facts.add("humidity_high")
        else:
            facts.add("humidity_suitable")

    #-----------------------------------
    # Light intensity
    #-----------------------------------
    if "light_low" in previous_facts:
        if light_intensity < 32:
            facts.add("light_low")
        else:
            facts.add("light_suitable")

    elif "light_high" in previous_facts:
        if light_intensity > 68:
            facts.add("light_high")
        else:
            facts.add("light_suitable")

    else:
        if light_intensity < 28:
            facts.add("light_low")
        elif light_intensity > 72:
            facts.add("light_high")
        else:
            facts.add("light_suitable")

    return facts

def matching_rules(rules, facts):

    return [
        rule for rule in rules
        if rule["conditions"].issubset(facts)
        and rule["add"] not in facts
    ]


def select_rule(agenda):

    return sorted(
        agenda,
        key=lambda rule: (-rule["priority"], rule["name"])
    )[0]

def infer(rules, initial_facts):

    facts = set(initial_facts)
    fired_rules = []

    while True:

        agenda = matching_rules(rules, facts)

        if not agenda:
            break

        chosen = select_rule(agenda)

        facts.add(chosen["add"])
        fired_rules.append(chosen)

    recommendations = {
        fact for fact in facts
        if fact.startswith("recommend_")
    }

    return recommendations, fired_rules