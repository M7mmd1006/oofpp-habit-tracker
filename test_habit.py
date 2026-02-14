import unittest
from datetime import datetime, timedelta
from habit import Habit

class TestHabit(unittest.TestCase):
    """Test cases for the Habit class"""

    def setUp(self):
        """Set up test fixtures"""
        self.daily_habit = Habit("Exercise", "Do 30 minutes of exercise", "daily")
        self.weekly_habit = Habit("Clean House", "Clean the house thoroughly", "weekly")
        
    def test_init(self):
        """Test initialization of a habit"""
        self.assertEqual(self.daily_habit.name, "Exercise")
        self.assertEqual(self.daily_habit.description, "Do 30 minutes of exercise")
        self.assertEqual(self.daily_habit.periodicity, "daily")
        self.assertEqual(len(self.daily_habit.completions), 0)

    def test_complete(self):
        """Test completing a habit"""
        self.daily_habit.complete()
        self.assertEqual(len(self.daily_habit.completions), 1)

    def test_is_complete_for_period_daily(self):
        """test checking if a daily habot is complete for a period"""
        # habit is not complete initially
        self.assertFalse(self.daily_habit.is_complete_for_period())

        # complete the habit
        self.daily_habit.complete()

        # habit should now be complete for today
        self.assertTrue(self.daily_habit.is_complete_for_period())

        # habit should not be complete for yesterday
        yesterday = datetime.now() - timedelta(days=1)
        self.assertFalse(self.daily_habit.is_complete_for_period(yesterday))

    def test_is_complete_for_period_weekly(self):
        """test checking if a weekly habit is complete for a period"""
        # habit is not complete initially
        self.assertFalse(self.weekly_habit.is_complete_for_period())
        
        # complete the habit
        self.weekly_habit.complete()
        
        # habit should now be complete for this week
        self.assertTrue(self.weekly_habit.is_complete_for_period())
        
        # habot should not be complete for last week
        last_week = datetime.now() - timedelta(days=7)
        self.assertFalse(self.weekly_habit.is_complete_for_period(last_week))
    
    def test_get_current_streak(self):
        """test calculating the current streak."""
        # no streak initially
        self.assertEqual(self.daily_habit.get_current_streak(), 0)
        
        # complete the habit for today
        self.daily_habit.complete()
        
        # streak should be 1
        self.assertEqual(self.daily_habit.get_current_streak(), 1)
        
        # add a completion for yesterday
        yesterday = datetime.now() - timedelta(days=1)
        self.daily_habit.completions.append(yesterday)
        
        # streak should be 2
        self.assertEqual(self.daily_habit.get_current_streak(), 2)
    
    def test_to_dict_and_from_dict(self):
        """test converting a habit to and from a dictionary"""
        # complete the habit
        self.daily_habit.complete()
        
        # convert to dictionary
        habit_dict = self.daily_habit.to_dict()
        
        # create a new habit from the dictionary
        new_habit = Habit.from_dict(habit_dict)
        
        # check that the new habit has the same attributes
        self.assertEqual(new_habit.id, self.daily_habit.id)
        self.assertEqual(new_habit.name, self.daily_habit.name)
        self.assertEqual(new_habit.description, self.daily_habit.description)
        self.assertEqual(new_habit.periodicity, self.daily_habit.periodicity)
        self.assertEqual(len(new_habit.completions), len(self.daily_habit.completions))

if __name__ == "__main__":
    unittest.main()