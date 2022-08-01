from waspy.hardware_control.motrona_dx350 import MotronaDx350

# Instantiate the Motrona Dx350 class with a specified url and port (depends on hardware controller settings)
motrona_dx350 = MotronaDx350("http://localhost:22100")

# Sets the target charge to reach before stopping. This is converted in the hardware controller to a number of counts
motrona_dx350.set_target_charge(5000)

# Clear the current counting value and start counting until target value
motrona_dx350.start_count_from_zero()

# Pause the counting
motrona_dx350.pause()

# Start/Continue the counting
motrona_dx350.start_count()

# Wait for the counting to be done. Warning this is a blocking call
motrona_dx350.counting_done()

# Retrieves the status of the hardware
print(motrona_dx350.get_status())
