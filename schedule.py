#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
from enum import Enum, auto
from typing import Callable


class Period(Enum):
    MORNING = auto()
    AFTERNOON = auto()
    EVENING = auto()
    pass


class Weekday(Enum):
    MONDAY = auto()
    TUESDAY = auto()
    WEDNESDAY = auto()
    THURSDAY = auto()
    FRIDAY = auto()
    SATURDAY = auto()
    SUNDAY = auto()
    pass


class Status(Enum):
    NONE = auto()
    CLASS = auto()
    WORK = auto()
    pass


class Class:
    def __init__(self, title: str, last: int, frames: list[tuple[str, list[tuple[Weekday, Period]]]]) -> None:
        """Class infomation with scheduled class times

        Args:
            title (str): the name of the class
            last (int): last week of the semester
            frames (list[tuple[str, list[tuple[Weekday, Period]]]]): the weekday and time period of the class each week.
                use "1-5,7,9-10" style to represent week numbers with the same weekday and time period
        """
        self.title: str = title
        # map from the week number to the class periods of the week
        self.schedule: dict[int, list[tuple[Weekday, Period]]] = {}
        for frame in frames:
            for week in frame[0].split(','):
                if '-' in week:
                    start, end = map(int, week.split('-'))
                    assert 1 <= start < end <= last
                    for week in range(start, end + 1):
                        self.schedule[week] = frame[1]
                else:
                    week = int(week)
                    assert 1 <= week <= last
                    self.schedule[week] = frame[1]
        return
    pass


class Schedule:
    EMPTY_WEEK: dict[Weekday, dict[Period, Status]] = { weekday:
                                                        { Period.MORNING: Status.NONE,
                                                          Period.AFTERNOON: Status.NONE,
                                                          Period.EVENING: Status.NONE,
                                                        } for weekday in Weekday
                                                    }

    def __init__(self, name: str, last: int, classes: list[Class]) -> None:
        """Student schedule

        Args:
            name (str): the name of the student
            last (int): last week of the semester
            classes (list[Class]): all classes chosen by the student
        """
        self.name: str = name
        self.schedule: dict[int, dict[Weekday, dict[Period, Status]]] \
            = {week: copy.deepcopy(self.EMPTY_WEEK) for week in range(1, last + 1)}
        self.classes: list[Class] = classes
        return

    def fill_class(self) -> 'Schedule':
        """fill class schedule into student's daily schedule

        Returns:
            Schedule: return itself to support chain calls
        """
        for clazz in self.classes:
            for week, schedule in clazz.schedule.items():
                for weekday, period in schedule:
                    self.schedule[week][weekday][period] = Status.CLASS
        return self

    def fill_work(self, perweek: int, workable: Callable[[Period, Status], bool]) -> 'Schedule':
        """fill work schedule into student's daily schedule

        Args:
            perweek (int): maximum number of times per week to work
            workable (Callable[[Period, Status], bool]): function to determine if student need work

        Returns:
            Schedule: return itself to support chain calls
        """
        assert 0 <= perweek
        for week, schedule in self.schedule.items():
            it = 0
            for weekday, arrangement in schedule.items():
                for period, status in arrangement.items():
                    if workable(period, status) and it < perweek:
                        self.schedule[week][weekday][period] = Status.WORK
                        it += 1
        return self

    def schedule_flat(self) -> list[tuple[int, Weekday, dict[Period, Status]]]:
        """flat the schedule

        Returns:
            list[tuple[int, Weekday, dict[Period, Status]]]: an list with the form of (week time, week day, daily schedule)
        """
        ret: list[dict[Period, Status]] = []
        for week, schedule in self.schedule.items():
            for weekday, arrangement in schedule.items():
                ret.append((week, weekday, arrangement))
        return ret
    pass
