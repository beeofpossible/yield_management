###installation
import gurobipy as gp
from gurobipy import GRB

# Lists of classes, price options, and scenarios.

classes = ['First', 'Business', 'Economy']

options = ['option1', 'option2', 'option3']

scenarios = ['sce1', 'sce2', 'sce3']

#  Classes, price options, and prices value for week 1, 2, and 3.

ch, price1, price2, price3  = gp.multidict({
    ('First', 'option1'): [1200, 1400, 1500],
    ('Business', 'option1'): [900, 1100, 820],
    ('Economy', 'option1'): [500, 700, 480],
    ('First', 'option2'): [1000, 1300, 900],
    ('Business', 'option2'): [800, 900, 800],
    ('Economy', 'option2'): [300, 400, 470],
    ('First', 'option3'): [950, 1150, 850],
    ('Business', 'option3'): [600, 750, 500],
    ('Economy', 'option3'): [200, 350, 450]
})

# Probablity of each scenario

prob ={'sce1': 0.1, 'sce2': 0.7, 'sce3': 0.2}

# Forecasted demand for each class, price option, and scenario at week 1

ich, fcst1, fcst2, fcst3 = gp.multidict({
    ('sce1', 'First', 'option1'): [10, 20, 30],
    ('sce1', 'Business', 'option1'): [20, 42, 40],
    ('sce1', 'Economy', 'option1'): [45, 50, 50],
    ('sce1', 'First', 'option2'): [15, 25, 35],
    ('sce1', 'Business', 'option2'): [25, 45, 50],
    ('sce1', 'Economy', 'option2'): [55, 52, 60],
    ('sce1', 'First', 'option3'): [20, 35, 40],
    ('sce1', 'Business', 'option3'): [35, 46, 55],
    ('sce1', 'Economy', 'option3'): [60, 60, 80],
    ('sce2', 'First', 'option1'): [20, 10, 30],
    ('sce2', 'Business', 'option1'): [40, 50, 10],
    ('sce2', 'Economy', 'option1'): [50, 60, 50],
    ('sce2', 'First', 'option2'): [25, 40, 40],
    ('sce2', 'Business', 'option2'): [42, 60, 40],
    ('sce2', 'Economy', 'option2'): [52, 65, 60],
    ('sce2', 'First', 'option3'): [35, 50, 60],
    ('sce2', 'Business', 'option3'): [45, 80, 45],
    ('sce2', 'Economy', 'option3'): [63, 90, 70],
    ('sce3', 'First', 'option1'): [45, 50, 50],
    ('sce3', 'Business', 'option1'): [45, 20, 40],
    ('sce3', 'Economy', 'option1'): [55, 10, 60],
    ('sce3', 'First', 'option2'): [50, 55, 70],
    ('sce3', 'Business', 'option2'): [46, 30, 45],
    ('sce3', 'Economy', 'option2'): [56, 40, 65],
    ('sce3', 'First', 'option3'): [60, 80, 80],
    ('sce3', 'Business', 'option3'): [47, 50, 60],
    ('sce3', 'Economy', 'option3'): [64, 60, 70]
})

#  Actual demand at weeks 1, 2, and 3.

ch, demand1, demand2, demand3  = gp.multidict({
    ('First', 'option1'): [25, 22, 45],
    ('Business', 'option1'): [50, 45, 20],
    ('Economy', 'option1'): [50, 50, 55],
    ('First', 'option2'): [30, 45, 60],
    ('Business', 'option2'): [40, 55, 40],
    ('Economy', 'option2'): [53, 60, 60],
    ('First', 'option3'): [40, 50, 75],
    ('Business', 'option3'): [45, 75, 50],
    ('Economy', 'option3'): [65, 80, 75]
})

# Class capacity

cap ={'First': 37, 'Business': 38, 'Economy': 47}

# cost per plane

cost = 50000


# Preprocessing

# week 1 data structures
list_ch = []

for c in classes:
    for h in options:
        tp = c,h
        list_ch.append(tp)

ch = gp.tuplelist(list_ch)

list_ich = []

for i in scenarios:
    for c in classes:
        for h in options:
            tp = i,c,h
            list_ich.append(tp)

ich = gp.tuplelist(list_ich)

# week 2 data structure

list_ijch = []

for i in scenarios:
    for j in scenarios:
        for c in classes:
            for h in options:
                tp = i,j,c,h
                list_ijch.append(tp)

ijch = gp.tuplelist(list_ijch)

# week 3 data structure

list_ijkch = []

for i in scenarios:
    for j in scenarios:
        for k in scenarios:
            for c in classes:
                for h in options:
                    tp = i,j,k,c,h
                    list_ijkch.append(tp)

ijkch = gp.tuplelist(list_ijkch)

# scenarios data structure

list_ijk = []

for i in scenarios:
    for j in scenarios:
        for k in scenarios:
            tp = i,j,k,
            list_ijk.append(tp)

ijk = gp.tuplelist(list_ijk)

# capacity constraints data structure

list_ijkc = []

for i in scenarios:
    for j in scenarios:
        for k in scenarios:
            for c in classes:
                tp = i,j,k,c
                list_ijkc.append(tp)

ijkc = gp.tuplelist(list_ijkc)

model = gp.Model('YieldManagement')

# Set global parameters.
model.params.nonConvex = 2

# Decision variables

# price option binary variables at each week
p1ch = model.addVars(ch, vtype=GRB.BINARY, name="p1ch")
p2ich = model.addVars(ich, vtype=GRB.BINARY, name="p2ich")
p3ijch = model.addVars(ijch, vtype=GRB.BINARY, name="p3ijch")

# tickets to be sold at each week
s1ich = model.addVars(ich, name="s1ich")
s2ijch = model.addVars(ijch, name="s2ijch")
s3ijkch = model.addVars(ijkch, name="s3ijkch")

# number of planes to fly
n = model.addVar(ub=6, vtype=GRB.INTEGER, name="planes")

# Price option constraints for week 1

priceOption1 = model.addConstrs( (gp.quicksum(p1ch[c,h] for h in options ) == 1 for c in classes ), name='priceOption1' )

# sales constraints for week 1

sales1 = model.addConstrs( (s1ich[i,c,h] <= fcst1[i,c,h]*p1ch[c,h] for i,c,h in ich ), name='sales1' )

# Price option constraints for week 2

priceOption2 = model.addConstrs( (gp.quicksum(p2ich[i,c,h] for h in options )
                                  == 1 for i in scenarios for c in classes ), name='priceOption2' )

# sales constraints for week 2

sales2 = model.addConstrs( (s2ijch[i,j,c,h] <= fcst2[j,c,h]*p2ich[i,c,h] for i,j,c,h in ijch ), name='sales2' )

# Price option constraints for week 3

priceOption3 = model.addConstrs( (gp.quicksum(p3ijch[i,j,c,h] for h in options )
                                  == 1 for i in scenarios for j in scenarios for c in classes ), name='priceOption3' )

# sales constraints for week 3

sales3 = model.addConstrs( (s3ijkch[i,j,k,c,h] <= fcst3[k,c,h]*p3ijch[i,j,c,h] for i,j,k,c,h in ijkch ), name='sales3' )

# Class capacity constraints

classCap = model.addConstrs( (gp.quicksum(s1ich[i,c,h] for h in options)
                              + gp.quicksum(s2ijch[i,j,c,h] for h in options)
                              + gp.quicksum(s3ijkch[i,j,k,c,h] for h in options)
                              <= cap[c]*n for i,j,k,c in ijkc ) , name='classCap')

# Objective function
obj = gp.quicksum(prob[i]*price1[c,h]*p1ch[c,h]*s1ich[i,c,h] for i,c,h in ich ) \
+ gp.quicksum(prob[i]*prob[j]*price2[c,h]*p2ich[i,c,h]*s2ijch[i,j,c,h] for i,j,c,h in ijch ) \
+ gp.quicksum(prob[i]*prob[j]*prob[k]*price3[c,h]*p3ijch[i,j,c,h]*s3ijkch[i,j,k,c,h] for i,j,k,c,h in ijkch) - cost*n

model.setObjective( obj, GRB.MAXIMIZE)

# Verify model formulation

model.write('YieldManagement.lp')

# Run optimization engine

model.optimize()

#############################################################
#            Print results of model for week 1
#############################################################

print("\n\n\n____________________Week 1 solution___________________________")

print(f"The expected total profit is: £{round(model.objVal,2): ,}")
print(f"Number of planes to book: {n.x}")

# Week 1 prices for seat class

# optimal values of option prices at week 1
opt_p1ch = {}

print("\n____________________Week 1 prices_______________________________")
for c,h in ch:
    opt_p1ch[c,h] = 0
    if p1ch[c,h].x > 0.5:
        opt_p1ch[c,h] = round(p1ch[c,h].x)
        price_ch = opt_p1ch[c,h]*price1[c,h]
        print(f"({c},{h}) = £{price_ch: ,}")
#

# Week 2 provisional prices

print("\n_____________Week 2 provisional prices____________________________")
for i,c,h in ich:
    if p2ich[i,c,h].x > 0.5:
        price_ch = round(p2ich[i,c,h].x)*price2[c,h]
        print(f"({i}, {c}, {h}) = £{price_ch: ,}")

# Week 3 provisional prices

print("\n_____________Week 3 provisional prices____________________________")
for i,j,c,h in ijch:
    if p3ijch[i,j,c,h].x > 0.5:
        price_ch = round(p3ijch[i,j,c,h].x)*price3[c,h]
        print(f"({i}, {j}, {c}, {h}) = £{price_ch: ,}")