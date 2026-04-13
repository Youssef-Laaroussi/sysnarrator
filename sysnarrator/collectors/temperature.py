"""Temperature Metrics Collector"""
import psutil


class TemperatureCollector:
    """Collects system temperature sensor data"""

    @staticmethod
    def get_temperatures():
        """Get all temperature sensor readings"""
        try:
            return psutil.sensors_temperatures()
        except (AttributeError, OSError):
            return {}

    @staticmethod
    def get_temperature_by_name(sensor_name=None):
        """Get temperature readings, optionally filtered by sensor name"""
        temps = TemperatureCollector.get_temperatures()
        if not sensor_name:
            return temps

        result = {}
        for chip, sensors in temps.items():
            if sensor_name.lower() in chip.lower():
                result[chip] = sensors
        return result

    @staticmethod
    def get_all_readings():
        """Get all temperature readings as a flat list"""
        temps = TemperatureCollector.get_temperatures()
        readings = []
        for chip, sensors in temps.items():
            for sensor in sensors:
                if sensor.current and sensor.current > 0:
                    readings.append({
                        'chip': chip,
                        'label': sensor.label or chip,
                        'current': sensor.current,
                        'high': sensor.high,
                        'critical': sensor.critical,
                    })
        return readings
