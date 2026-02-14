from datetime import datetime, timedelta
import uuid

class Habit:
    """
    the class representing the habit to be tracked

    attributes:
        id: id for each habit
        name: name of habit
        description: description of the habit
        periodicity: how often the habit should be completed i.e. daily or weekly
        created_at: date of habit creation
        completions: list of habit completion dates
    """

    def __init__(self, name, description, periodicity):
        """
        Intitalize a new habit

        Args:
            name: name of the habit
            description: description of the habit
            periodicity: how often the habit should be comleted i.e. daily or weekly
        """
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.periodicity = periodicity.lower()
        self.created_at = datetime.now()
        self.completions = []

        # validate periodicity
        if self.periodicity not in ['daily', 'weekly']:
            raise ValueError("Periodicity must be 'daily' or 'weekly'")
        
    def complete(self):
        """Mark the habit as complete for the current time"""
        self.completions.append(datetime.now())
        print(f"Habit '{self.name}' marked as complete")

    def is_complete_for_period(self, date=None):
        """
        check if the habit is compllete for a specific time period

        Args:
            date: the date to check

        Returns:
            bool: true if the habit is complete for the period, false otherwise
        """
        if date is None:
            date = datetime.now()

        # find the start of the current period
        if self.periodicity == 'daily':
            period_start = datetime(date.year, date.month, date.day)
            period_end = period_start + timedelta(days=1)
        else: # weekly
            # find the start of the week (monday)
            days_since_monday = date.weekday()
            period_start = datetime(date.year, date.month, date.day) - timedelta(days=days_since_monday)
            period_end = period_start + timedelta(days=7)

        # check if any completion falls within the current period
        for completion in self.completions:
            if period_start <= completion < period_end:
                return True
            
        return False
    
    def get_current_streak(self):
        """
        Calculate the current streak for this habit

        Returns:
            the number of consecutive periods the habit has been completed for
        """
        if not self.completions:
            return 0
        

        # start from today and go backwards
        today = datetime.now()
        streak = 0
        current_date = today

        while True:
            # check if the habit is complete for the current period
            if not self.is_complete_for_period(current_date):
                break

            streak += 1

            # move to the previous period
            if self.periodicity == 'daily':
                current_date -= timedelta(days=1)
            else: # weekly
                current_date -= timedelta(days=7)

        return streak
    
    def to_dict(self):
        """
        convert the habit to a dictionary for storage

        Returns:
            dictionary representation of the habit
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'periodicity': self.periodicity,
            'created_at': self.created_at.isoformat(),
            'completions': [completion.isoformat() for completion in self.completions]
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        create a habit from a dictionary

        Args:
            data: dictionary representation of the habit

        Returns:
            Habit: a new habit instance
        """
        habit = cls(data['name'], data['description'], data['periodicity'])
        habit.id = data['id']
        habit.created_at = datetime.fromisoformat(data['created_at'])
        habit.completions = [datetime.fromisoformat(completion) for completion in data['completions']]
        return habit
    
    def __str__(self):
        """string represetation of the habit"""
        return f"{self.name} ({self.periodicity}): {self.description}"
    
