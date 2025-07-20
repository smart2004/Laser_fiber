# this example as per python describes basic structure of classes and methods,
# theese modeling operation logic of fiber laser. In actual system there will be
# more details, while this example reflects bgasic components and interaction.

import math

class PumpLaser:
    '''
    Pump source for fiber laser.
    
    Источник накачки для волоконного лазера.
    '''
    def __init__(self, power_watts):
        self.power = power_watts  # Pump power in watts(мощность накачки в ватах)

    def get_power(self):
        return self.power
    

class ActiveFiber:
    '''
    Active fiber with amplifier and length params.
    
    Активное волокно с параметрами усиления и длины.
    '''
    def __init__(self, length_m, absorption_coeff, emission_coeff, doping_concentration):
        self.length = length_m
        self.absorption_coeff = absorption_coeff  # absorption_factor (коэффициент поглощения) (1/m)
        self.emission_coeff = emission_coeff  # emission_factor (коэффициент эмиссии) (1/m)
        self.doping_concentration = doping_concentration  # active ions concentration (концентрация активных ионов)

    def calculate_gain(self, pump_power):
        '''
        Fiber reinforcement approximate model.

        Примерная модель усиления в волокне.
        '''
        gain = math.exp(self.emission_coeff * self.doping_concentration * self.length * pump_power)
        return gain
        # Simple model: proportional amplification of power and the wavelength (простая модель: усиление пропорционально мощности накачки и длине волны.


class FiberLaserCavity:
    '''
    Fiber laser resonator consisting of an active fiber and mirrors.

    Резонатор волоконного лазера, состоящий из активного волокна и зеркал.
    '''
    def __init__(self, active_fiber, reflectivity_mirror1, reflectivity_mirror2):
        self.active_fiber = active_fiber
        self.reflectivity_mirror1 = reflectivity_mirror1  # Коэффициент отражения первого зеркала
        self.reflectivity_mirror2 = reflectivity_mirror2  # Коэффициент отражения второго зеркала

    def calculate_threshold(self):
        '''
        Threshold amplication calculation for laser radiation generation.

        Расчет порогового усиления для генерации лазерного излучения.
        '''
        losses = (1 - self.reflectivity_mirror1) + (1 - self.reflectivity_mirror2)
        threshold_gain = 1 / (1 - losses)
        return threshold_gain

    def is_lasting(self, pump_power):
        gain = self.active_fiber.calculate_gain(pump_power)
        threshold = self.calculate_threshold()
        return gain >= threshold

    def get_output_power(self, pump_power):
        if self.is_lasting(pump_power):
            gain = self.active_fiber.calculate_gain(pump_power)
            # Output power simple model
            output_power = pump_power * (gain - 1) * (1 - self.reflectivity_mirror2)
            return output_power
        else:
            return 0.0
        

class FiberLaserSystem:
    '''
    Complete fiber laser system.

    Полная система волоконного лазера.    
    '''
    def __init__(self, pump_laser, cavity):
        self.pump_laser = pump_laser
        self.cavity = cavity

    def operate(self):
        pump_power = self.pump_laser.get_power()
        if self.cavity.is_lasting(pump_power):
            output_power = self.cavity.get_output_power(pump_power)
            print(f'Лазер работает. Выходная мощность: {output_power: .2f} Вт')
        else:
            print('Порог генерации не достигнут. Лазер не излучает.')


if __name__ == '__main__':
    pump = PumpLaser(power_watts=5.0)  # 5 Вт мощности накачки (pump power)
    fiber = ActiveFiber(length_m=10, absorption_coeff=0.1, emission_coeff=0.05, doping_concentration=1e25) #1e25)
    cavity = FiberLaserCavity(active_fiber=fiber, reflectivity_mirror1=0.99, reflectivity_mirror2=0.95)
    laser_system = FiberLaserSystem(pump_laser=pump, cavity=cavity)
    
    laser_system.operate()

# PumpLaser == класс, моделирующий источник накачки
# ActiveFiber == класс активного волокна, где происходит усиление
# FiberLaserCavity == резонатор с двумя зеркалами, которые задают порог генерации
# FiberLaserSystem == объединяет все компоненты и управляет работой лазера
# Метод operate запускает систему и выводит результат
