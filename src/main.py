from control.GAAgent import GAAgent
from control.NNAgent import NNAgent
from control.astarAgent import AStarAgent
from control.rulebasedAgent import RBAgent
from model.model import Model
from view.tkView import TkView

from timeit import default_timer as timer

ORDER_SIZE = 200
UNIT_TIME = 2400

# model & view
model = Model((12, 12), 5, ORDER_SIZE)
view = TkView(model)

# control
control = RBAgent()
# control = AStarAgent()
# control = NNAgent()
# control = GAAgent()

control.initialise(model)

start = timer()
while model.timeStep < UNIT_TIME:
    control.moveAgents()
    view.render()
    print(f"{model.timeStep}: {model.printAgents()}")

    # break loop no agent working (all finished or all dead)
    if all(agent.orderItem is None for agent in model.agents):
        break
end = timer()


### Print out results ###

print(f"Total Real Time Taken: {end - start}")

print(f"Total Time Unit: {model.timeStep}")

deadAgentNum = 0
for agent in model.agents:
    if agent.energy == 0:
        deadAgentNum += 1

print(f"Total Dead agents: {deadAgentNum}")

orderDone = ORDER_SIZE-len(model.order_list)
orderPercent = (orderDone/ORDER_SIZE)*100
print(f"Total Orders dropped off: {orderDone}/{ORDER_SIZE}")
print(f"                           {orderPercent:.2f}%")

view.root.mainloop()