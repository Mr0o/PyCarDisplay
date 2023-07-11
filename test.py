import PyCarDisplay.milesLogging as milesLogging

# test the milesLogging module
milesLogging.init_log()
milesLogging.update_log(100, "1:00")

# test the rename_log function
milesLogging.create_new_log()

