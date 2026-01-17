from dataclasses import dataclass

@dataclass()
class Team:
    id: int
    team_code: str
    name: str

    def __str__(self):
        return f'{self.team_code} ({self.name})'

    def __repr__(self):
        return f'{self.team_code} ({self.name})'

    def __hash__(self):
        return hash(self.id)
