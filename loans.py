import json
import csv
from zipfile import ZipFile
from io import TextIOWrapper

race_lookup = {
    "1": "American Indian or Alaska Native",
    "2": "Asian",
    "21": "Asian Indian",
    "22": "Chinese",
    "23": "Filipino",
    "24": "Japanese",
    "25": "Korean",
    "26": "Vietnamese",
    "27": "Other Asian",
    "3": "Black or African American",
    "4": "Native Hawaiian or Other Pacific Islander",
    "41": "Native Hawaiian",
    "42": "Guamanian or Chamorro",
    "43": "Samoan",
    "44": "Other Pacific Islander",
    "5": "White",
}

class Applicant:
    def __init__(self, age, race):
        self.age = age
        self.race = set()
        for r in race:
            if r in race_lookup:
                self.race.add(race_lookup[r])
    def __repr__(self):
        sorted_race_list = sorted(list(self.race))
        return f"Applicant({self.age.__repr__()}, {sorted_race_list.__repr__()})"
    def lower_age(self):
        if "<" in self.age: 
            return int(self.age.split("<")[1])
        elif ">" in self.age:
            return int(self.age.split(">")[1])
        else:
            return int(self.age.split("-")[0])
    
    def __lt__(self, other):
        return (self.lower_age() < other.lower_age())
    
class Loan:
    def __init__(self, values):
        self.applicants = []
        #these lists keep track of all possible races of the applicants
        applicant_races = []
        coapplicant_races = []
        for key in values:
            #these 3 lines convert loan amount, prop. value, and int. rate to floats if they DONT exist 
            if (key == "loan_amount") or (key == "property_value") or (key == "interest_rate"):
                if (values[key] == "NA") or (values[key] == "Exempt"):
                    values[key] = -1
            #append applicants attribute with applicant objects, race and age
            if ("applicant_race-" in key) and ("co" not in key) and (values[key] != ""):
                applicant_races.append(values[key])
        self.applicants.append(Applicant(values["applicant_age"], applicant_races))
        
        #check if a co-applicant exists
        if values["co-applicant_age"] != "9999":
            for key in values:
                #append applicants attribute with co-applicant objects, race and age
                if ("co-applicant_race-" in key) and (values[key] != ""):
                    coapplicant_races.append(values[key])
            self.applicants.append(Applicant(values["co-applicant_age"], coapplicant_races))
               
        self.loan_amount = float(values["loan_amount"])
        # add lines here
        self.property_value = float(values["property_value"])
        self.interest_rate = float(values["interest_rate"])
        
    #reference for str and repr methods: https://www.digitalocean.com/community/tutorials/python-str-repr-functions 
    def __str__(self):
        return f"<Loan: {self.interest_rate}% on ${self.property_value} with {len(self.applicants)} applicant(s)>"
    
    def __repr__(self):
        return f"<Loan: {self.interest_rate}% on ${self.property_value} with {len(self.applicants)} applicant(s)>"
    
    def yearly_amounts(self, yearly_payment):
    # TODO: assert interest and amount are positive
        assert (self.interest_rate > 0) and (self.loan_amount > 0)
        amt = self.loan_amount

        while amt > 0:
            yield amt
            # TODO: add interest rate multiplied by amt to amt
            amt += (self.interest_rate/100) * amt
            # TODO: subtract yearly payment from amt
            amt -= yearly_payment

         

f = open("banks.json")
#banks_data is a list of dictionaries
banks_data = json.load(f)
class Bank:
    def __init__(self, name):
        self.lei = None
        #loan dicts that match should get converted to Loan objects and appended to a list stored as 
        #an attribute in Bank
        #self.loans is the list that gets appended
        self.loans = []
        #banks_list = []
        
        # checks if given name appears in banks.json
        # then looks up the lei and stores it in an lei attribute
        for bank in banks_data:
            if bank["name"] == name:
                self.lei = bank["lei"]
        
        # skip banks that dont match the given bank's (name) lei
        # read loans from the wi.csv in wi.zip
        with ZipFile("wi.zip") as zf:
            with zf.open("wi.csv") as csv_file:
                reader = csv.DictReader(TextIOWrapper(csv_file))
                for row in reader:
                #check if the loan lei matches self.lei (the passed bank's lei)
                    if row["lei"] == self.lei:
                        self.loans.append(Loan(row))
                        
    # special methods:
    # a method that allows you to print the last loan with [-1] (indexing)
    #reference: https://stackoverflow.com/questions/43627405/understanding-getitem-method
    def __getitem__(self, i):
        #reference for IndexError: https://www.pythonforbeginners.com/basics/indexerror-in-python#:~:text=What%20is%20an%20IndexError%20in,the%20range%200%20to%209.
        if i >= len(self.loans):
            return "IndexError: index is not present in list"
        return self.loans[i]
    # a method that allows you to check how many loans there are
    #reference: https://www.geeksforgeeks.org/python-__len__-magic-method/
    def __len__(self):
        return len(self.loans)
        
        
        