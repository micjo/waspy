from waspy.hardware_control.aml import Aml

# Instantiate the Aml class with a specified url and port
aml = Aml("http://localhost:22100")

# Move the first motor driver to position 10 (this is converted to steps inside the driver software)
aml.move_first(10)

# Move the second motor driver to position 20 (this is converted to steps inside the driver software)
aml.move_second(20)

# Move the 2 motor drivers to the load position (Allows a user to physically access whatever the motor is moving)
aml.load()

# Retrieves the status of the hardware
print(aml.get_status())
