import magic.domain as domain

class BirdBase(domain.kingdom.animal.IAnimal):
    def sound(self):
        return "Kaaw"
