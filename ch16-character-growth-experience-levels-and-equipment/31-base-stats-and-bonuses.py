@property
def power(self):
    equipment = self.entity.equipment if self.entity else None
    return self.base_power + (equipment.power_bonus if equipment else 0)
