import unittest
from datetime import datetime, timedelta
from habit import Habit
from storage import Storage
import analytics
import os
import shutil

class TestAnalytics(unittest.TestCase):
    """test cases for the analytics module."""
    
    def setUp(self):
        """set up test fixtures."""
        # create a temporary data directory for testing
        self.test_data_dir = "test_data"
        if os.path.exists(self.test_data_dir):
            shutil.rmtree(self.test_data_dir)
        os.makedirs(self.test_data_dir)
        
        # create a storage instance
        self.storage = Storage(self.test_data_dir)
        
        # create test habits
        self.daily_habit = Habit("Exercise", "Do 30 minutes of exercise", "daily")
        self.weekly_habit = Habit("Clean House", "Clean the house thoroughly", "weekly")
        
        # add habits to storage
        self.storage.add_habit(self.daily_habit)
        self.storage.add_habit(self.weekly_habit)
    
    def tearDown(self):
        """tear down test fixtures."""
        # remove the temporary data directory
        if os.path.exists(self.test_data_dir):
            shutil.rmtree(self.test_data_dir)
    
    def test_get_all_habits(self):
        """test getting all habits."""
        habits = analytics.get_all_habits(self.storage)
        self.assertEqual(len(habits), 2)
    
    def test_get_habits_by_periodicity(self):
        """test getting habits by periodicity."""
        daily_habits = analytics.get_habits_by_periodicity(self.storage, "daily")
        weekly_habits = analytics.get_habits_by_periodicity(self.storage, "weekly")
        
        self.assertEqual(len(daily_habits), 1)
        self.assertEqual(len(weekly_habits), 1)
        
        self.assertEqual(daily_habits[0].name, "Exercise")
        self.assertEqual(weekly_habits[0].name, "Clean House")
    
    def test_get_longest_streak_habit(self):
        """test getting the habit with the longest streak."""
        # no streaks initially
        habit, streak = analytics.get_longest_streak_habit(self.storage)
        self.assertEqual(streak, 0)
        
        # sdd completions for the daily habit
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        self.daily_habit.completions.append(today)
        self.daily_habit.completions.append(yesterday)
        self.storage.save()
        
        # daily habit should have the longest streak
        habit, streak = analytics.get_longest_streak_habit(self.storage)
        self.assertEqual(habit.name, "Exercise")
        self.assertEqual(streak, 2)
        
        # add completions for the weekly habit
        this_week = today
        last_week = today - timedelta(days=7)
        two_weeks_ago = today - timedelta(days=14)
        self.weekly_habit.completions.append(this_week)
        self.weekly_habit.completions.append(last_week)
        self.weekly_habit.completions.append(two_weeks_ago)
        self.storage.save()
        
        # weekly habit should now have the longest streak
        habit, streak = analytics.get_longest_streak_habit(self.storage)
        self.assertEqual(habit.name, "Clean House")
        self.assertEqual(streak, 3)
    
    def test_get_streak_for_habit(self):
        """test getting the streak for a specific habit."""
        # no streak initially
        self.assertEqual(analytics.get_streak_for_habit(self.daily_habit), 0)
        
        # add completions
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        self.daily_habit.completions.append(today)
        self.daily_habit.completions.append(yesterday)
        
        # streak should be 2
        self.assertEqual(analytics.get_streak_for_habit(self.daily_habit), 2)
    
    def test_get_completion_rate(self):
        """test calculating completion rates."""
        # no completions initially
        completion_rates = analytics.get_completion_rate(self.storage, days=7)
        self.assertEqual(completion_rates[self.daily_habit.name], 0)
        self.assertEqual(completion_rates[self.weekly_habit.name], 0)
        
        # add completions for the daily habit (3 out of 7 days)
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        two_days_ago = today - timedelta(days=2)
        self.daily_habit.completions.append(today)
        self.daily_habit.completions.append(yesterday)
        self.daily_habit.completions.append(two_days_ago)
        
        # add a completion for the weekly habit (1 out of 1 week)
        self.weekly_habit.completions.append(today)
        
        self.storage.save()
        
        # calculate completion rates
        completion_rates = analytics.get_completion_rate(self.storage, days=7)
        
        # daily habit: 3 out of 7 days = 42.9%
        self.assertAlmostEqual(completion_rates[self.daily_habit.name], 42.9, delta=0.1)
        
        # weekly habit: 1 out of 1 week = 100%
        self.assertEqual(completion_rates[self.weekly_habit.name], 100.0)

if __name__ == "__main__":
    unittest.main()