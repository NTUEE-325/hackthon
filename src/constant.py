import time

mode = "init"
# modes = [normal, study, night, gym]
last_detect_chair_time = 0
last_time = 0  # last time change mode
buffer_time = 5
chair_pos = 0
chair_size = 0
# detect for the gym mode
detect_times = [time.time()-11, 0, time.time(), 0, time.time()-11]

time_record = [time.time(), time.time(), time.time(), time.time(), time.time()]
# time_record records the starting time for each mode. only one of them is nonzero.
# indices: [quilt_cover_true, quilt_cover_false, gym, normal, study]
GYM_INDEX = 2
NORMAL_INDEX = 3
STUDY_INDEX = 4
QUILT_COVER_FALSE_INDEX = 1
QUILT_COVER_TRUE_INDEX = 0

init_strength = 0.5
# init strength to give the current strength

air_conditioner_strength_time_constant = 10
# time constant for the adjustment of air conditioner strength (exponential interpolation)

air_conditioner_strength = 0.5
# strength of the air conditioner
# when setting the real air conditioner strength, the strength is mapped to 1~5(int):
# floor(air_conditioner_strength*5)+1

STUDY_MODE_BASE_STRENGTH = 0.5
NORMAL_MODE_BASE_STRENGTH = 0.5
GYM_MODE_BASE_STRENGTH = 1.0
QUILT_COVER_MODE_BASE_STRENGTH = 0.3
QUILT_NOT_COVER_MODE_BASE_STRENGTH = 0.0
# final strength of each mode

center = (600, 300)
# direction of the wind: initially at the center
air_conditioner_direction = [0.49, 0.51]
'''
if want to have "opposite direction":
    1. detect the direction of people with respect to the point (0.5, 0.5)
    2. air_conditioner_distance + people_position(respect to (0.5, 0.5)) remains constant (0.5)
    ex. the people is in (0.2, 0.3). then the direction is (0.5, 0.5)+(0.3, 0.2)*sqrt(12)/sqrt(13)

this is implemented in utility.py.
'''
quilt_cover = True
