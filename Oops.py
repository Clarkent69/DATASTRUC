class Animal:
    def __init__(self, name, species):
        self.name = name
        self.species = species
        self._age = 0
    
    def make_sound(self):
        print(f"{self.name} makes an animal sound")
    
    def get_age(self):
        return self._age
    
    def set_age(self, age):
        if age < 0:
            raise ValueError("Age cannot be negative")
        self._age = age
    
    def __str__(self):
        return f"{self.name} is a {self.species}, {self._age} years old"


class Dog(Animal):
    def __init__(self, name, breed, age=0):
        super().__init__(name, "Dog")
        self.breed = breed
        self.set_age(age)
    

    def make_sound(self):
        print(f"{self.name} says: Woof!")
        
    def __str__(self):
        return f"{self.name} is a {self.breed} dog, {self.get_age()} years old"


class Cat(Animal):
    def __init__(self, name, favorite_toy, age=0):
        super().__init__(name, "Cat")
        self.favorite_toy = favorite_toy
        self.set_age(age)
    

    def make_sound(self):
        print(f"{self.name} says: Meow!")
    
    def __str__(self):
        return f"{self.name} is a cat who loves {self.favorite_toy}, {self.get_age()} years old"

def main():
    dog1 = Dog("Buddy", "Golden Retriever", 3)
    cat1 = Cat("Whiskers", "yarn ball", 2)
    
    print(f"{dog1.name}'s age is: {dog1.get_age()}")
    
    print("Trying to set negative age:")
    dog1.set_age(-5)
    
    dog1.set_age(4)
    print(f"New age for {dog1.name}: {dog1.get_age()}")
    
    animals = [
        dog1,
        cat1,
        Dog("Rex", "German Shepherd", 5),
        Cat("Mittens", "toy mouse", 1)
    ]
    
    print("\nDemonstrating polymorphism:")
    for animal in animals:
        animal.make_sound()
    
    print("\nAnimal details:")
    for animal in animals:
        print(animal)

if __name__ == "__main__":
    main()