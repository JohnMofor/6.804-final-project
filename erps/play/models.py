from django.db import models
import random

# Create your models here.


table = {
"step":{"R":70,"P":80,"S":90,"N":33},
"switch":{
    "R":(0,60,75,90,100),
    "P":(0,10,70,90,100),
    "S":(0,15,30,90,100),
    "N":(0, 1, 2, 3,100),
    "order":("R","P","S","N"),
    }
}

def step(group):
    if group=="N":
        return ["R","P","S"][random.randint(0,2)]

    r = random.randint(1,100)
    if 1 <= r <= table["step"][group]:
        return group
    else:
        return [i for i in ["R","P","S"] if i!=group][random.randint(0,1)]


def switch(start):
    switch_list = table["switch"][start]
    r = random.randint(1,100)
    i,j = 0,2
    while i < 4:
        low,high = switch_list[i:j]
        if low < r <= high:
            return table["switch"]["order"][i]
        i+=1
        j+=1
    return r,start,False


class Player(models.Model):

    #4 scenarios, Each with 20 Sequences. Each 20 Seq have answers, = 4*40 space + dividers
    scenarioR = models.CharField(max_length=45,null=True)
    scenarioP = models.CharField(max_length=45,null=True)
    scenarioS = models.CharField(max_length=45,null=True)
    scenarioN = models.CharField(max_length=45,null=True)
    #hash number of session
    id_number = models.IntegerField(primary_key=True,unique=True)

    def build(self):
        self.build_scenarios()

    def __unicode__(self):
        return "Player with ID:"+str(self.id_number)

    def add_scenario(self,scenario):
        if self.scenarioR==None: self.scenarioR=scenario
        elif self.scenarioP==None: self.scenarioP=scenario
        elif self.scenarioS==None: self.scenarioS=scenario
        elif self.scenarioN==None: self.scenarioN=scenario
        self.save()

    def get_scenario(self,group):
        if not group in table["switch"]["order"]: return False
        self.save()
        if group=="R":
            return str(self.scenarioR)
        elif group=="P":
            return str(self.scenarioP)
        elif group=="S":
            return str(self.scenarioS)
        elif group=="N":
            return str(self.scenarioN)

    def build_scenarios(self):
        for start in table["switch"]["order"]:
            sequence = [step(start)]
            group = [start]
            for i in xrange(19):
                group.append(switch(group[-1]))
                sequence.append(step(group[-2]))
            scenario = ",".join(["".join(sequence),"".join(group)])
            self.add_scenario(scenario)

    def get(self,scenario,index):
        if not (0 <= index <= 19): return False
        s = self.get_scenario(scenario)
        if s: return s[index]
        return False

    def show_groups(self, scenario):
        if not (0 <= index <= 19): return False
        s = self.get_scenario(scenario)
        if s: return s.split(",")[1]
        return False



    def show(self):
        return "id={0}<br>R:{1}<br>P:{2}<br>S:{3}<br>N:{4}".format(self.id_number,self.scenarioR,self.scenarioP,self.scenarioS,self.scenarioN)