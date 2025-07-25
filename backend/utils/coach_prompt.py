def get_motivational_prompt(domain):
    prompts = {
        "engineering": "Every innovation begins with curiosity. Keep pushing boundaries!",
        "medicine": "You’re learning to heal lives. That’s a mission beyond yourself.",
        "design": "Creativity takes courage—let your imagination lead the way.",
        "law": "Justice needs brave minds like yours. Stay sharp, stay strong.",
        "business": "Entrepreneurship is about solving problems. Keep creating solutions.",
        "education": "Shaping minds is no small feat—your influence lasts a lifetime.",
        "agriculture": "You nourish the nation—sow effort, and reap purpose.",
        "science": "Every theory you explore uncovers a new reality. Keep discovering!",
        "technology": "Your code may just power the next big thing. Build boldly!"
    }

    return prompts.get(domain, "Stay curious, stay resilient, and never stop growing!")
