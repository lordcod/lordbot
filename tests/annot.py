

from typing import Literal


class GreedyUser(str):
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}['{self}']"

    def __class_getitem__(cls, param: str) -> 'GreedyUser':
        return cls(param)


AllReactionsType = Literal[GreedyUser['airkiss'], 'angrystare', GreedyUser['bite'], 'bleh', 'blush', 'brofist', 'celebrate', 'cheers', 'clap', 'confused', GreedyUser['cool'], 'cry', GreedyUser['cuddle'], 'dance', 'drool', 'evillaugh', 'facepalm', GreedyUser['handhold'], 'happy', 'headbang', GreedyUser['hug'], GreedyUser['kiss'], 'laugh', GreedyUser['lick'], GreedyUser['love'], 'mad', 'nervous', 'no', 'nom', 'nosebleed',  # type: ignore
                           GreedyUser['nuzzle'], 'nyah', GreedyUser['pat'], 'peek', GreedyUser['pinch'], GreedyUser['poke'], 'pout', GreedyUser['punch'], 'roll', 'run', 'sad', 'scared', 'shout', 'shrug', 'shy', 'sigh', 'sip', 'slap', 'sleep', 'slowclap', GreedyUser['smack'], 'smile', 'smug', 'sneeze', GreedyUser['sorry'], 'stare', 'stop', 'surprised', 'sweat', 'thumbsup', GreedyUser['tickle'], 'tired', GreedyUser['wave'], GreedyUser['wink'], 'woah', 'yawn', 'yay', 'yes']  # type: ignore
