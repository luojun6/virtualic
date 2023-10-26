from rules.AbstractStrategies import AbstractStrategy


class TurnLight(AbstractStrategy):
    
    def execute(self, context):
        
        switch = context.signal_cluster.turn_light_sw
        left_light = context.signal_cluster.left_turnning_light_sts
        right_light = context.signal_cluster.right_turnning_light_sts
        
        if switch.value == switch.signal.off.value:
            left_light.value = left_light.signal.OFF.value
            right_light.value = right_light.signal.OFF.value
            
        if switch.value == switch.signal.Left_On.value:
            left_light.value = left_light.signal.ON.value
            
        if switch.value == switch.signal.Right_On.value:
            right_light.value = right_light.signal.ON.value
    