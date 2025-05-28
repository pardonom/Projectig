class Voter:
    def __init__(self, name, voter_id):
        self.__name = name
        self.__voter_id = voter_id
        self.__already_voted = False
        print(f"[born]Voter {self.__name}, id: {self.__voter_id}, has been registered.")

    def get_name(self):
        return self.__name
    def get_voter_id(self):
        return self.__voter_id


    def __del__(self):
        print(f"[killed]Voter {self.__name}, id: {self.__voter_id}, has been removed from the system.")
person1 = Voter("Boron", 1)

class InPersonVoter:
    def __init__(self, name, voter_id):
        self.__name = name