import csv
from datetime import datetime, timedelta

from schedule import Class, Period, Schedule, Status, Weekday

# First set the number of weeks of the current semester,
# the number of work times per week (divided by morning,
# afternoon, and evening), and the start date of the semester.
MAX_PER_WEEK = 6
WEEK_TIME = 18
START = datetime(2024, 2, 26)

if __name__ == '__main__':
    # Second, add the courses that all students need to take,
    # and indicate the number of weeks, weekdays,
    # and time period for each course.
    bh = Class("bh", WEEK_TIME, [("1-18", [(Weekday.WEDNESDAY, Period.AFTERNOON)])]) # checked
    ddxtydkz = Class("ddxtydkz", WEEK_TIME, [("3-13", [(Weekday.TUESDAY, Period.EVENING)])]) # checked
    gjxsyy = Class("gjxsyy", WEEK_TIME, [("1-16", [(Weekday.TUESDAY, Period.MORNING)])]) # checked
    gpgpusjbx = Class("gpgpusjbx", WEEK_TIME, [("2-9", [(Weekday.MONDAY, Period.AFTERNOON)])]) # checked
    kjxzybg = Class("kjxzybg", WEEK_TIME, [("2-5,7", [(Weekday.THURSDAY, Period.MORNING)])]) # checked
    kjxzyzscq = Class("kjxzyzscq", WEEK_TIME, [("2-5,7", [(Weekday.THURSDAY, Period.MORNING)])]) # checked
    rjkkxgc = Class("rjkkxgc", WEEK_TIME, [("2-13", [(Weekday.TUESDAY, Period.MORNING)])]) # checked
    rjtxjg = Class("rjtxjg", WEEK_TIME, [("1-5,7-9,11-18", [(Weekday.THURSDAY, Period.AFTERNOON)])]) # checked
    sfsjyfx = Class("sfsjyfx", WEEK_TIME, [("1-17", [(Weekday.SATURDAY, Period.EVENING)])]) # checked
    sltj = Class("sltj", WEEK_TIME, [("2-14", [(Weekday.MONDAY, Period.MORNING), (Weekday.WEDNESDAY, Period.MORNING)])]) # checked
    xnxszhsy = Class("xnxszhsy", WEEK_TIME, [("2-17", [(Weekday.MONDAY, Period.AFTERNOON)])]) # checked
    yjsjsyl = Class("yjsjsyl", WEEK_TIME, [("2-12", [(Weekday.TUESDAY, Period.AFTERNOON)])]) # checked
    zgmkszyydd = Class("zgmkszyydd", WEEK_TIME, [("3,11", [(Weekday.MONDAY, Period.AFTERNOON)])]) # checked
    zrbzfgl_sh5 = Class("zrbzfgl_sh5", WEEK_TIME, [("11-16", [(Weekday.TUESDAY, Period.AFTERNOON)])]) # checked
    zrbzfgl_xyl1 = Class("zrbzfgl_xyl1 ", WEEK_TIME, [("3-8", [(Weekday.MONDAY, Period.MORNING)])]) # checked
    zrbzfgl_xyl2 = Class("zrbzfgl_xyl2", WEEK_TIME, [("3-8", [(Weekday.WEDNESDAY, Period.MORNING)])]) # checked
    zrbzfgl_xyl5 = Class("zrbzfgl_xyl5", WEEK_TIME, [("3-8", [(Weekday.TUESDAY, Period.AFTERNOON)])]) # checked

    # Third, add each student and the courses they need to take.
    students = [
        Schedule("student1", WEEK_TIME, [sltj, xnxszhsy, # 1
                                rjkkxgc, zrbzfgl_xyl5, # 2
                                bh, # 3
                                kjxzybg, rjtxjg, # 4
                            ]),
        Schedule("student2", WEEK_TIME, [sltj, zgmkszyydd, # 1
                                gjxsyy, rjkkxgc, yjsjsyl, # 2
                                bh, # 3
                                kjxzybg, zrbzfgl_sh5, # 4
                                sfsjyfx, # 6
                            ]),
        Schedule("student3", WEEK_TIME, [gpgpusjbx, # 1
                                yjsjsyl, # 2
                                zrbzfgl_xyl2, bh, # 3
                                kjxzyzscq, rjtxjg, # 4
                            ]),
        Schedule("student4", WEEK_TIME, [zrbzfgl_xyl1, xnxszhsy, # 1
                                bh, # 3
                                kjxzyzscq, # 4
                                sfsjyfx, # 6
                            ]),
        Schedule("student5", WEEK_TIME, [zrbzfgl_xyl1, # 1
                                ddxtydkz, # 2
                                bh, # 3
                                kjxzyzscq, rjtxjg, # 4
                                sfsjyfx, #6
                            ]),
    ]

    # Fourth, calculate each student's class time and schedule their working time.
    for student in students:
        student.fill_class().fill_work(MAX_PER_WEEK, lambda p, s: p in [Period.MORNING, Period.AFTERNOON] and s is Status.NONE)

    # Fifth, configure their schedule according to dingtalk scheduling table(.xls file).
    with open("dingtalk example.csv", 'w', newline='') as stream:
        def schedule(d: dict[Period, Status]) -> str:
            match (d[Period.MORNING], d[Period.AFTERNOON]):
                case (Status.WORK, Status.CLASS | Status.NONE):
                    return "上午班"
                case (Status.CLASS | Status.NONE, Status.WORK):
                    return "下午班"
                case (Status.WORK, Status.WORK):
                    return "全天班"
                case _:
                    return "休"
                
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["姓名"] + [(START + timedelta(date)).strftime(f"%Y/%m/%d") for date in range(WEEK_TIME * 7)])
        for student in students:
            writer.writerow([student.name] + [schedule(arangement[2]) for arangement in student.schedule_flat()])
