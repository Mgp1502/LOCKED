import lua_extracting

"""
this file is for testing the lua extracting.
"""

test_keys = lua_extracting.extractkeys(path="testFiles/Empty.lua")
test_keys2 = lua_extracting.extractkeys(path="testFiles/OneKey.lua")

#test_highest = lua_extracting.extract_highest_weekly_key(char_name="Tankzr", path="testFiles/LockedOut_healzr.lua")

print(test_keys)
print(test_keys2)
