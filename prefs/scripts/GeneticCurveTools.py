import maya.cmds as cmds
from pymel.core import *
import random


class CurveOrganism:
    keyCurve = None
    cost = 0.0

    def __init__(self, keys):
        self.keyCurve = keys
        self.cost = 0.0

    def UpdateCost(self, Target):
        self.cost = 0.0
        for i in range(int(cmds.playbackOptions(query=True, min=True)),
                       int(cmds.playbackOptions(query=True, max=True) + 1)):
            cost = cmds.keyframe(GetBredCurves(), attribute=self.keyCurve, query=True, time=(i, i), eval=True)[0] - \
                   cmds.keyframe(Target, query=True, time=(i, i), eval=True)[0]
            self.cost += cost * cost


class Population:
    def __init__(self, count, mutChance, mutAmount, champCount):
        self.maxCount = count
        self.mutationChance = mutChance
        self.mutAmount = mutAmount
        self.champCount = champCount
        self.organisms = []
        keyTimes = [0, 2, 8, 15, 22, 30]
        keyValues = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        for ident in range(0, count):
            name = 'Bred_id' + str(ident)
            cmds.addAttr(GetBredCurves(), attributeType="float", ln=name, keyable=True)
        for a in cmds.listAttr(GetBredCurves()):
            if a.__contains__('Bred'):
                for k in range(len(keyTimes)):
                    mutation = -mutAmount + (
                                random.random() * mutAmount * 2) if random.random() < self.mutationChance else 0.0
                    cmds.setKeyframe(GetBredCurves(), attribute=a, time=keyTimes[k], value=keyValues[k] + mutation)
                self.organisms.append(CurveOrganism(a))

    def Sort(self):
        self.organisms = sorted(self.organisms, cmp=lambda x, y: cmp(x.cost, y.cost))

    def BreedChild(self, p1, p2):
        child = CurveOrganism(p1.keys, p1.tangentAngles, p1.tangentWeights)
        for k in range(len(p1.tangentAngles)):
            # child.keys[k] = p1.keys[k] if random.randint(0,1) else p2.keys[k]
            child.tangentAngles[k] = p1.tangentAngles[k] if random.randint(0, 1) else p2.tangentAngles[k]
            child.tangentWeights[k] = p1.tangentWeights[k] if random.randint(0, 1) else p2.tangentWeights[k]
            # if random.random() < self.mutationChance:
            #	child.keys[k] += -self.mutAmount + (random.random() * self.mutAmount * 2)
            if random.random() < self.mutationChance:
                child.tangentAngles[k] += -self.mutAmount + (random.random() * self.mutAmount * 2)
            if random.random() < self.mutationChance:
                child.tangentWeights[k] += -self.mutAmount + (random.random() * self.mutAmount * 2)
        return child

    def BreedNextGen(self):
        for o in range(0, self.maxCount):
            # p1 = champions[random.randint(0, self.champCount)]
            # p2 = champions[random.randint(0, self.champCount)]
            self.organisms.append(self.BreedChild(champ, champ))


def GetBredCurves():
    return 'pCube1'
    for item in cmds.ls(type='animCurveUU'):
        if item == 'BredCurves':
            return item
    return cmds.createNode('animCurveUU', name='BredCurves')


def NextGen():
    for o in pop.organisms:
        o.UpdateCost(origCurve)
    pop.Sort()
    cmds.copyKey(GetBredCurves(), attribute=pop.organisms[0].keyCurve)
    for o in range(pop.champCount, pop.maxCount):
        cmds.pasteKey(GetBredCurves(), attribute=pop.organisms[o].keyCurve, option='replace')
        for k in range(0, cmds.keyframe(GetBredCurves(), attribute=pop.organisms[o].keyCurve, query=True,
                                        keyframeCount=True)):
            if random.random() < pop.mutationChance:
                cmds.keyframe(GetBredCurves(), attribute=pop.organisms[o].keyCurve, edit=True, index=(k, k),
                              relative=True, valueChange=-pop.mutAmount + (random.random() * pop.mutAmount * 2))


origCurve = cmds.animCurveEditor('graphEditor1GraphEd', query=True, curvesShown=True)
pop = None
pop = Population(30, 0.5, 2.5, 3)

pop.mutChance = 0.25
pop.mutAmount = 1

while pop.organisms[0].cost > 0.25:
    NextGen()
    pop.mutAmount = 1 * pop.organisms[0].cost if pop.organisms[0].cost < 3 else 1
