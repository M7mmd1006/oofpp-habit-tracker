from functools import reduce 
from datetime import datetime, timedelta 

def get_all_habits(storage):
    """
    Get all habits

    Args:
        storage: the storage instance

    Returns:
        list of all habits
    """

    return storage.get_all_habits()

def get_habits_by_periodicity(storage, periodicity):
    """
    Get all habits with a specific periodicity

    Args:
        storage: the storage instance
        periodicity: filter by 'daily' or 'weekly'

    Returns:
        list of habits with the chosen time period
    """

    return list(filter(lambda habit: habit.periodicity == periodicity, storage.get_all_habits()))

def get_longest_streak_habit(storage):
    """
    Get the habit with the longest streak

    Args:
        storage: the storage instance

    Returns:
        the habit with the longest streak and the streak leangth
    """

    habits = storage.get_all_habits()
    if not habits:
        return None, 0
    
    # map habits to (habit, streak) tuples
    habit_streak = list(map(lambda habit: (habit, habit.get_current_streak()), habits))

    # find the habit with the longest streak
    return reduce(lambda x, y: x if x[1] > y[1] else y, habit_streak)

def get_streak_for_habit(habit):
    """
    Get the current streak for a specific habit

    Args:
        habit to be checked

    Returns:
        streak for the habit
    """

    return habit.get_current_streak()

def get_completion_rate(storage, days=30):
    """
    Calculate the completion rate for all habits over a specifed time period

    Args:
        storage instance

    Returns:
        Dictionary that maps habit names to completion rates (0-100%)
    """

    habits = storage.get_all_habits()
    today = datetime.now()

    result = {}

    for habit in habits:
        # count the number of periods on the specified time range
        if habit.periodicity == 'daily':
            total_periods = days
        else: # weekly
            total_periods = days // 7

        # count completed periods
        completed_periods = 0 
        current_date = today

        for _ in range(total_periods):
            if habit.is_complete_for_period(current_date):
                completed_periods += 1

            # move to the previous period
            if habit.periodicity == 'daily':
                current_date -= timedelta(days=1)
            else: # weekly
                current_date -= timedelta(days=7)
                
        # calculate completion rate
        if total_periods > 0:
            completion_rate = (completed_periods / total_periods) * 100
        else:
            completion_rate = 0

        result[habit.name] = completion_rate

    return result

def get_habits_completed_today(storage):
    """
    get all habits completed today

    Args:
        storage instance

    Returns:
        list of habits done today
    """
    today = datetime.now()
    return list(filter(lambda habit: habit.is_complete_for_period(today), storage.get_all_habits()))

def get_habits_to_complete_today(storage):
    """
    Get all habits that need to be comleted today

    Args:
        storage instance

    Returns:
        list of habits that need to be completed today
    """
    today = datetime.now()
    all_habits = storage.get_all_habits()

    # filter daily habits and weekly habits that are due today
    return list(filter(
        lambda habit: (
            habit.periodicity == 'daily' or 
            (habit.periodicity == 'weekly' and today.weekday() == 0) # monday
        ) and not habit.is_complete_for_period(today),
        all_habits
    ))
