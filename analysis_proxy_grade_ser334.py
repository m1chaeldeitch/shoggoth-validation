"""
shoggoth-validation - analysis_proxy_grade_ser334.py

See analysis_proxy_grade_ser222.py for details.
"""
__author__ = "Ruben Acuna"
__copyright__ = "Copyright 2025, Ruben Acuna"

from analysis_proxy_grade_util import was_test_passed_by_name

def compute_proxies_m2_24sc(data):
    proxies = []

    # total: 30pts

    # 1) main menu [2pts]
    t1_1 = was_test_passed_by_name(data, "Main Menu 1") # Main Menu 1 [Hint: Displays Credits.]
    t1_2 = was_test_passed_by_name(data, "Main Menu 2") # Main Menu 2 [Hint: Displays Correct Credit Count.]

    if t1_1 and t1_2:
        proxies += [2.0]
    elif t1_1:
        proxies += [1.0]
    else:
        proxies += [0.0]

    # 2) memory leaks [2pts]
    t2_1 = was_test_passed_by_name(data, "Memory Allocation 3") # 7.3) Memory Allocation 3 [Hint: Frees all Memory on close.]
    t2_2 = was_test_passed_by_name(data, "Memory Allocation 4") # 7.4) Memory Allocation 4 [Hint: Frees Correct Memory addresses on close.]

    if t2_1 and t2_2:
        proxies += [2.0]
    elif t2_1:
        proxies += [1.0]
    else:
        proxies += [0.0]

    # 3) course_insert [7pts]
    t3_1 = was_test_passed_by_name(data, "Insert Course 1") # 2.1) Insert Course 1 [Hint: Basic Behavior.]
    t3_2 = was_test_passed_by_name(data, "Insert Course 2") # 2.2) Insert Course 2 [Hint: Inserts 2 Courses.]
    t3_3 = was_test_passed_by_name(data, "Insert Course 3") # 2.3) Insert Course 3 [Hint: Correct Ordering.]
    t3_4 = was_test_passed_by_name(data, "Insert Course 4") # 2.4) Insert Course 4 [Hint: Inserts 3 Courses.]
    t3_5 = was_test_passed_by_name(data, "Insert Course 5") # 2.5) Insert Course 5 [Hint: Correct Ordering.]
    t3_6 = was_test_passed_by_name(data, "Insert Course 6") # 2.6) Insert Course 6 [Hint: Inserting a Duplicate Course.]
    t3_7 = was_test_passed_by_name(data, "Insert Course 7") # 2.7) Insert Course 7 [Hint: Prints Error Message on Duplicate.]

    if t3_1 and t3_2 and t3_3 and t3_4 and t3_5 and t3_6 and t3_7:
        proxies += [7.0]
    elif t3_1 and t3_2 and t3_4: #NOTE: the rubric has a memory requirement here... probably can skip since not in full points level.
        proxies += [3.5]
    elif t3_1:
        proxies += [1.75]
    else:
        proxies += [0.0]

    # 4) course_insert::memory [2pts]
    t4_1 = was_test_passed_by_name(data, "Memory Allocation 1") # 7.1) Memory Allocation 1 [Hint: Uses Malloc when creating courses.]
    t4_2 = was_test_passed_by_name(data, "Memory Allocation 2")  # 7.2) Memory Allocation 2 [Hint: Frees memory from creating a course.]
    if t4_1 and t4_2:
        proxies += [2.0]
    elif t4_1:
        proxies += [1.0]
    else:
        proxies += [0.0]

    # 5) schedule_print [2pts]
    t5_1 = was_test_passed_by_name(data, "Schedule Print") # 3.1) Schedule Print [Hint: Basic Behavior.]

    if t5_1:
        proxies += [2.0]
    #NOTE: original had partial credit if printed all courses but incomplete data.
    else:
        proxies += [0.0]

    # 6) course_drop [5pts]
    t6_1 = was_test_passed_by_name(data, "Remove Course 1") # 4.1) Remove Course 1 [Hint: Basic Behavior.] (1/1)
    t6_2 = was_test_passed_by_name(data, "Remove Course 2") # 4.2) Remove Course 2 [Hint: Removing first course in a list of 2.] (1/1)
    t6_3 = was_test_passed_by_name(data, "Remove Course 3") # 4.3) Remove Course 3 [Hint: Removing course from list of 3.] (1/1)
    t6_4 = was_test_passed_by_name(data, "Remove Course 4") # 4.4) Remove Course 4 [Hint: Maintaining list after removing course.] (1/1)
    # 4.5) Remove Course 5 [Hint: Removing a course not in the list.] #NOTE: rubric doesn't use.
    if t6_1 and t6_2 and t6_3 and t6_4:
        proxies += [5.0]
    elif t6_1 and t6_2 and t6_3:
        proxies += [2.5]
    elif t6_1:
        proxies += [1.25]
    else:
        proxies += [0.0]

    # 7) course_drop::memory [2pts]
    t7_1 = was_test_passed_by_name(data, "Memory Allocation 5") # 7.4) Memory Allocation 5 [Hint: Frees Memory when removing courses.]
    t7_2 = was_test_passed_by_name(data, "Memory Allocation 6") # 7.5) Memory Allocation 6 [Hint: Frees Correct Memory addresses when removing courses.]

    if t7_1 and t7_2:
        proxies += [2.0]
    elif t7_1:
        proxies += [1.0]
    else:
        proxies += [0.0]

    # 8) schedule_load [4pts]
    t8_1 = was_test_passed_by_name(data, "Load File 1") # 5.1) Load File 1 [Hint: Basic Behavior.]
    t8_2 = was_test_passed_by_name(data, "Load File 2") # 5.2) Load File 2 [Hint: Loads all courses in file.]
    t8_3 = was_test_passed_by_name(data, "Load File 3") # 5.3) Load File 3 [Hint: No file exists.]

    if t8_1 and t8_2 and t8_3:
        proxies += [4.0]
    elif t8_1:
        proxies += [2.0]
    else:
        proxies += [0.0]

    # 9) schedule_save [4pts]
    t9_1 = was_test_passed_by_name(data, "Save File 1") # 6.1) Save File 1 [Hint: Saves a Course.]
    t9_2 = was_test_passed_by_name(data, "Save File 2") # 6.2) Save File 2 [Hint: Correctly Saves all Courses.]

    if t9_1 and t9_2:
        proxies += [4.0]
    elif t9_1:
        proxies += [2.0]
    else:
        proxies += [0.0]

    total_score_proxy = sum([ps for ps in proxies if ps])

    return proxies, total_score_proxy


def compute_proxies_m3_24fc(data):
    proxies = []

    #1) BMP Headers IO (4pts)
    # Competent: Creates structures for the headers of a BMP file and functions which read and write them.
    # Novice: Some mistakes in creating structures for the headers of a BMP file or creating functions which read and write them.
    # No Marks: Most or all functionality is not attempted or is mostly incorrect.

    #t1_1 = was_test_passed_by_name(data, "[1.1]") # DIB Headers IO [Hint: incorrectly sized DIB header struct (remove this)]
    t1_2 = was_test_passed_by_name(data, "[1.2]") # BMP Headers IO [Hint: incorrectly reading and/or writing of BMP header]
    t1_3 = was_test_passed_by_name(data,"[1.3]")  # DIB Headers IO [Hint: incorrectly reading and/or writing of DIB header]

    if t1_2 and t1_3:
        proxies += [4.0]
    elif t1_2 or t1_3:
        proxies += [2.0]
    else:
        proxies += [0.0]

    #TODO: complete below

    #2) Pixels IO
    #3) Input and output file names
    #4) Input Validation
    #5) Filter: Color Shift
    #6) Test: Copy Image
    #7) Image OOP
    #8) Filter: Grayscale
    #9) Filter: Scaling


    total_score_proxy = sum([ps for ps in proxies if ps])

    return proxies, total_score_proxy