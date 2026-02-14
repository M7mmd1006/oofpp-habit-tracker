import json
import os
from datetime import datetime, timedelta 
from habit import Habit

class Storage:
    """
    A class for storing and retrieving habits.

    Attributes:
        data_dir: Directory where habit data is stored
        habits: list of habit objects
    """

    def __init__(self, data_dir="data"):
        """
        Intitialize the storage.

        Args:
            data_dir: directory where habit data is stored
        """
        self.data_dir = data_dir
        self.habits = []

        # create data directory if it doesn't exist
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

    def add_habit(self, habit):
        """
        Add a habit to storage

        Args:
            habit: the habit to add
        """
        self.habits.append(habit)
        self.save()

    def remove_habit(self,habit_id):
        """
        Remove a habit from storage

        Args:
            habit_id: ID of the habit to remove

        Returns:
            bool: true if the habit was remove, false otherwise
        """
        for i, habit in enumerate(self.habits):
            if habit.id == habit_id:
                del self.habits[i]
                self.save()
                return True
        return False 
    
    def get_habit(self, habit_id):
        """
        get a habit by ID 

        Args:
            habit_id: id of habit to get
        
        Returns:
            habit: the habit with the given ID, or None if not found
        """
        for habit in self.habits:
            if habit.id == habit_id:
                return habit
        return None
    
    def get_all_habits(self):
        """
        Get all habits

        Returns:
            list: list of all habits
        """
        return self.habits
    
    def save(self):
        """Save all habits to the data directory"""
        habits_data = [habit.to_dict() for habit in self.habits]
        with open(os.path.join(self.data_dir, "habits.json"), "w") as f:
            json.dump(habits_data, f, indent=2)

    def load(self):
        """Load all habits from the data directory"""
        try: 
            with open(os.path.join(self.data_dir, "habits.json"), "r") as f:
                habits_data = json.load(f)
                self.habits = [Habit.from_dict(data) for data in habits_data]
        except FileNotFoundError:
            # no habits file yet, start with empty list
            self.habits = []

    def create_predefined_habits(self):
        """Create predefined habits with example data."""
        # only create predefined habits if there are no habits yet
        if self.habits:
            return
        
        # create 5 predefined habits ( 2 daily, 3 weekly)
        habits = [
            Habit("Morning Exercise", "Do 30 minutes of exercise in the morning", "daily"),
            Habit("Read Book", "Read at least 30 pages of a book", "daily"),
            Habit("Clean House", "Clean the house thoroughly", "weekly"),
            Habit("Call Parents", "Call parents to catch up", "weekly"),
            Habit("Review Goals", "Review and update personal goals", "weekly")
        ]
        
        # add example completion data for the last 4 weeks
        today = datetime.now()

        # for each habit, add completions for the past 4 weeks
        for habit in habits : 
            if habit.periodicity == "daily":
                # add daily completions (with some gaps to make it realistic)
                for i in range(28): # 4 weeks is 28 days
                    # skip some days randomly to simulate missed habits
                    if i % 3 != 0: # skip every third day
                        completion_date = today - timedelta(days=i)
                        habit.completions.append(completion_date)
            else: #weekly
                # add weekly completions
                for i in range(4): # 4 weeks
                    completion_date = today - timedelta(weeks=i)
                    habit.completions.append(completion_date)

        # add habits to storage
        for habit in habits:
            self.add_habit(habit)

