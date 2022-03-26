import random


def dora(a):
    if a in bad_things:
        if a == "graffiti":
            b = "Paint"
        else:
            b = random.choice(good_things)
            b = str(b).capitalize()
        return f"Seriously? Unless you\'re joking, {a}ing sounds like a bad idea :( " \
               f"\n      {b}ing is a much better alternative, although Chuck would probably disagree..."
    elif a in good_things:
        if a == "paint":
            b = "graffiti"
        else:
            b = random.choice(bad_things)
        return f"Finally, a good suggestion! We should all {a} together, and not do something stupid like {b}ing."
    elif a in boring_things:
        return f"I don't really want to {a}. Sounds pretty boring, don\'t you think?"
    else:
        return f"If you wanna {a} then I\'ll happily join in! It's good to try new things."


def chuck(a):
    if a in bad_things:
        return f"YESS! I don't care what goody two-shoes Dora thinks, it\'s time for some {a}ing!"
    elif a in good_things:
        if a == "talk":
            b = "yell"
        elif a == "paint":
            b = "graffiti"
        else:
            b = random.choice(bad_things)
        return f"What? {a}ing sounds sooooo boring. I'll be out {b}ing while you losers do that"
    elif a in boring_things:
        return f"boring, Boring, BORING!!! That sounds like something only Alice would enjoy." \
               f"\n       Why would anyone want to {a} when you can do something fun instead xD"
    else:
        return f"Not too sure about {a}ing. Unless it involves doing something bad, this guy ain\'t interested"


def alice(a):
    b = random.choice(boring_things)
    if a in boring_things:
        return f"I, personally, think {a}ing sounds great! I\'ll join you once I\'m done {b}ing by myself!"
    elif a in good_things:
        if a == "relax":
            b = "study"
        return f"To be honest, I\'m not really good at {a}ing . I\'m much better at {b}ing so I\'ll leave it to Dora."
    elif a in bad_things:
        a = str(a).capitalize()
        return f"{a}ing sounds scary... I\'d rather be at home, doing something productive."
    else:
        return f"I\'ve never tried {a}ing before. Maybe I should expand my horizons and give it a go?"


def bob(a):
    a2 = str(a).capitalize()    # Capitalized duplicate of the parameter, for grammatically correct replies
    if a in good_things:
        return f"{a2}ing sounds fun! But maybe we could do some boring stuff first to include Alice?"
    elif a in bad_things:
        return f"{a2}ing sounds kinda bad, but if Chuck\'s doing it I might reconsider. No man left behind!"
    elif a in boring_things:
        return f"I\'m down for a change of pace. It's important to {a} every once in a while!"
    else:
        b = random.choice(actions)
        return f"That\'s a no from me. {a2}ing isn't how I roll. You\'ll find me {b}ing if you need me!"


def user(a):
    inp = input("Input your answer: ")
    reply = inp + "\t"
    return reply


# 5 Random actions in each category for some variation.
bad_things = ["fight", "bicker", "yell", "steal", "graffiti"]
good_things = ["relax", "play", "paint", "talk", "draw"]
boring_things = ["work", "study", "cry", "worry", "read"]

actions = bad_things + good_things + boring_things  # All actions from all three categories


def random_action():    # Method for getting a random action. Used mainly by the server program
    return random.choice(actions)


def get_reply(bot_name, s):  # Method for getting a reply from the correct bot
    if bot_name == "alice":
        return alice(s)
    elif bot_name == "bob":
        return bob(s)
    elif bot_name == "dora":
        return dora(s)
    elif bot_name == "chuck":
        return chuck(s)
    else:
        return user(s)
