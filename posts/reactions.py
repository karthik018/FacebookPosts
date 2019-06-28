import enum


class Reaction(enum.Enum):
    love = "LOVE"
    like = "LIKE"
    wow = "WOW"
    haha = "HAHA"
    sad = "SAD"
    angry = "ANGRY"

    @classmethod
    def getreactions(cls):
        reactions = []
        for reaction in (Reaction):
            reactions.append((reaction.value, reaction.value))
        return tuple(reactions)
