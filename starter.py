from defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

BODY_0 = [MOVE, WORK, CARRY]
BODY_1 = [MOVE, WORK, WORK, CARRY]
BODY_2 = [MOVE, WORK, WORK, WORK, CARRY, CARRY]


def get_target(me):
    spawn = Game.spawns['Spawn1']
    controller = me.room.controller

    if spawn.energy < spawn.energyCapacity:
        return spawn
    elif len(Game.constructionSites) > 0:
        return me.pos.findClosestByPath(FIND_CONSTRUCTION_SITES)
    else:
        return controller


def run(me):
    # Switch task if necessary:
    if me.carry.energy == 0:
        if me.memory.depositing:
            me.say('Mining')
        me.memory.depositing = False
    elif me.carry.energy == me.carryCapacity:
        if not me.memory.depositing:
            me.say('Dropping')
        me.memory.depositing = True

    # If depositing
    if me.memory.depositing:
        target = get_target(me)

        # If construction
        if str(target)[1:18] == 'construction site':
            code = me.build(target)
            if code == OK:
                me.memory.target = False
            elif code == ERR_NOT_IN_RANGE:
                me.moveTo(target)

        # If spawn
        elif target.structureType == STRUCTURE_SPAWN:
            code = me.transfer(target, RESOURCE_ENERGY)
            if code == OK:
                me.memory.target = False
            elif code == ERR_NOT_IN_RANGE:
                me.moveTo(target)

        # If controller
        elif target.structureType == STRUCTURE_CONTROLLER:
            code = me.upgradeController(target)
            if code == OK:
                me.memory.target = False
            elif code == ERR_NOT_IN_RANGE:
                me.moveTo(target)

    # If collecting
    else:
        target = me.pos.findClosestByPath(FIND_SOURCES_ACTIVE)
        code = me.harvest(target)
        if code == OK:
            pass
        elif code == ERR_NOT_IN_RANGE:
            me.moveTo(target)
