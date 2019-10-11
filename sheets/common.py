class CommonSheet:
    def __init__(self, id):
        self.set_field("user_id", id)
        self.set_field("type", "common")
        self.set_field("name", None)    
        self.set_field("age",  None)
        self.set_field("race",  None)
        self.set_field("class",  None)
        self.set_field("str",  None)
        self.set_field("agi",  None)
        self.set_field("int",  None)
        self.set_field("vit",  None)
        self.set_field("questions_schema", {
            "name": "Qual seu nome?",
            "age": "Qual sua idade?",
            "race":  "Qual sua raça?",
            "class": "Qual sua classe?",
            "str":  "Quanto é sua força?",
            "agi":  "Quanto é sua agilidade?",
            "int":  "Quanto é sua inteligencia?",
            "vit":  "Quanto é sua vitalidade?"
        })

    def get_question(self, field):
        if field not in self.questions_schema.keys():
            return
        return self.questions_schema[field]

    def get_next_question(self):
        return self.get_question(self.get_next_field())
        
    
    def set_field(self,field,value):
        setattr(self,field,value)
    
    def get_fields(self):
        return self.to_dict().keys()
    
    def to_dict(self):
        return {
            "user_id": getattr(self, "user_id"),
            "type": getattr(self, "type"),
            "name": getattr(self, "name"),
            "age": getattr(self, "age"),
            "race": getattr(self, "race"),
            "class": getattr(self, "class"),
            "str": getattr(self, "str"),
            "agi": getattr(self, "agi"),
            "int": getattr(self, "int"),
            "vit": getattr(self, "vit"),
        }

    def get_next_field(self):
        for key in self.get_fields():
            if getattr(self, key) is None:
                return key
        return None