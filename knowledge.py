rules = [
    # Chain 1: Dry soil and dehydration
    {
        "name": "R1",
        "conditions": {"soil_dry", "plant_type_rose", "leaf_condition_wilting"},
        "add": "dehydration_risk",
        "priority": 10
    },
    {
        "name": "R2",
        "conditions": {"dehydration_risk", "temp_high"},
        "add": "plant_stress",
        "priority": 9
    },
    {
        "name": "R3",
        "conditions": {"plant_stress", "light_high"},
        "add": "recommend_watering_and_shade",
        "priority": 8
    },

    # Chain 2: Excessive soil moisture
    {
        "name": "R4",
        "conditions": {"soil_wet", "plant_type_cactus"},
        "add": "poor_soil_drying",
        "priority": 10
    },
    {
        "name": "R5",
        "conditions": {"poor_soil_drying", "light_low"},
        "add": "fungal_risk",
        "priority": 9
    },
    {
        "name": "R6",
        "conditions": {"fungal_risk", "humidity_high"},
        "add": "recommend_improve_ventilation_and_pest_control",
        "priority": 8
    },
    {
        "name": "R7",
        "conditions": {"fungal_risk", "leaf_condition_brown spots"},
        "add": "recommend_improve_ventilation_and_pest_control",
        "priority": 8
    },

    # Chain 3: Unfavourable temperature
    {
        "name": "R8",
        "conditions": {"temp_high", "humidity_high"},
        "add": "environmental_stress",
        "priority": 10
    },
    {
        "name": "R9",
        "conditions": {"plant_type_rose"},
        "add": "not_desert_plant",
        "priority": 9
    },
    {
        "name": "R10",
        "conditions": {"plant_type_chilli"},
        "add": "not_desert_plant",
        "priority": 9
    },
    {
        "name": "R11",
        "conditions": {"environmental_stress", "soil_dry", "not_desert_plant"},
        "add": "recommend_environment_adjustment",
        "priority": 8
    },

    # Chain 4: Nutrient deficiency
    {
        "name": "R12",
        "conditions": {"soil_suitable", "temp_suitable"},
        "add": "basic_conditions_suitable",
        "priority": 7
    },
    {
        "name": "R13",
        "conditions": {"basic_conditions_suitable", "leaf_condition_yellowing"},
        "add": "nutrient_deficiency_risk",
        "priority": 6
    },
    {
        "name": "R14",
        "conditions": {"nutrient_deficiency_risk", "plant_type_chilli"},
        "add": "recommend_fertilization",
        "priority": 5
    },
    {
        "name": "R15",
        "conditions": {"nutrient_deficiency_risk", "plant_type_rose"},
        "add": "recommend_fertilization",
        "priority": 5
    },

    # Chain 5: Suitable plant conditions
    # basic_condition_suitable can be derived from R12, which checks for suitable soil and temperature conditions
    {
        "name": "R17",
        "conditions": {"basic_conditions_suitable", "humidity_suitable", "light_suitable"},
        "add": "environment_suitable",
        "priority": 6
    },
    {
        "name": "R18",
        "conditions": {"environment_suitable", "leaf_condition_healthy"},
        "add": "recommend_plant_conditions_healthy",
        "priority": 5
    }
]