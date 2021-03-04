#requirements
charcoalNeededForGrade = 200 #charcoal

woodNeededForCharcoal = 400 #wood
woodNeededPerBuilding = 10 #wood
TreesNeededForwood = 80 #trees

#durations
timeElapsed = 0 #seconds
timetoCutWood = 30 #seconds
timeToMakeCharcoal = 30 #seconds

timeToBecomeBuilder = 120 #seconds
timeToBuildBuilding = 60 #seconds

timetoBecomeExplorer = 60 #seconds

#finishing times
#build all first, then start producing
sixBuildings = 1000 + 1080 #seconds needs 12 wood / 60 seconds

for x in range(1, 10):
    length = "=" * int((6000 / (x) + 180 * x) // 100)
    print(length)

#