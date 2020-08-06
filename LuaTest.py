import lua_extracting

"""
this file is for testing the lua extracting.
"""

test_keys = lua_extracting.extractkeys(path="testFiles/LockedOut_marsd.lua")
#test_highest = lua_extracting.extract_highest_weekly_key(char_name="Tankzr", path="testFiles/LockedOut_healzr.lua")
print(test_keys)
