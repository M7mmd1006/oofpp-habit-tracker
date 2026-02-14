import sys
from habit import Habit
from storage import Storage
import analytics

class HabitTrackerCLI:
    """
    command-line interface for the habit tracker app

    Attributes:
        storage: the storage instance
    """

    def __init__(self):
        """Intitialize the CLI"""
        self.storage = Storage()
        self.storage.load()

        # create predefined habits if none exist
        if not self.storage.get_all_habits():
            self.storage.create_predefined_habits()

    def display_menu(self):
        """display the main menu"""
        print("\n===== Habit Tracker =====")
        print("1. View all habits")
        print("2. Add a new habit")
        print("3. Complete a habit")
        print("4. View habit details")
        print("5. Delete a habit")
        print("6. Analytics")
        print("0. Exit")
        print("========================")

    def run(self):
        """Run the CLI"""
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")

            if choice == '1':
                self.view_all_habits()
            elif choice == '2':
                self.add_habit()
            elif choice == '3':
                self.complete_habit()
            elif choice == '4':
                self.view_habit_details()
            elif choice == '5':
                self.delete_habit()
            elif choice == '6':
                self.show_analytics()
            elif choice == '0':
                print("Goodbye")
                sys.exit(0)
            else:
                print("Invalid choice. Please Try again")

    def view_all_habits(self):
        """View all habits"""
        habits = self.storage.get_all_habits()

        if not habits:
            print("No habits found")
            return
        
        print("\n===== All Habits =====")
        for i, habit in enumerate(habits, 1):
            status = "✓" if habit.is_complete_for_period() else "✗"
            print(f"{i}. [{status}] {habit.name} ({habit.periodicity})")

    def add_habit(self):
        """Add a new habit"""
        print("\n===== Add a New Habit =====")
        name = input("Enter habit name: ")
        description = input("Enter habit description: ")

        while True:
            periodicity = input("Enter periodicity (daily/weekly:)").lower()
            if periodicity in ["daily", "weekly"]:
                break
            print("Invalid periodicity. PLease enter 'daily' or 'weekly'")

        habit = Habit(name, description, periodicity)
        self.storage.add_habit(habit)
        print(f"Habit '{name}' added successfully")

    def complete_habit(self):
        """Complete a habit"""
        self.view_all_habits()

        habits = self.storage.get_all_habits()
        if not habits:
            return
        
        while True:
            choice = input("\nEnter the number of the habit to complete (0 to cancel): ")

            if choice == '0':
                return
            
            try:
                index = int(choice) - 1
                if 0 <= index < len(habits):
                    habit = habits[index]
                    habit.complete()
                    self.storage.save()
                    break
                else:
                    print("Invalid habit number.")
            except ValueError:
                print("Please enter a valid number")

    def view_habit_details(self):
        """View details of a specific habit"""
        self.view_all_habits()

        habits = self.storage.get_all_habits()
        if not habits:
            return
        
        while True:
            choice = input("\nEnter the number of the habit to view (0 to cancel): ")

            if choice == '0':
                return
            
            try:
                index = int(choice) - 1
                if 0 <= index < len(habits):
                    habit = habits[index]
                    self.display_habit_details(habit)
                    break
                else:
                    print("Invalid habit number")
            except ValueError:
                print("Please enter a valid number")

    def display_habit_details(self, habit):
        """
        Display details of a specific habit

        Args:
            habit: the habit to display
        """
        print(f"\n===== {habit.name} =====")
        print(f"Description: {habit.description}")
        print(f"Periodicity: {habit.periodicity}")
        print(f"Created at: {habit.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Current streak: {habit.get_current_streak()} {habit.periodicity} periods")
        print(f"Completed today: {'Yes' if habit.is_complete_for_period() else 'No'}")

        # display recent completions
        print("\nRecent completions: ")
        sorted_completions = sorted(habit.completions, reverse=True)
        for i, completion in enumerate(sorted_completions[:5], 1):
            print(f"{i}. {completion.strftime('%Y-%m-%d %H:%M:%S')}")

    def delete_habit(self):
        """Delete a habit"""
        self.view_all_habits()

        habits = self.storage.get_all_habits()
        if not habits:
            return
        
        while True:
            choice = input("\nEnter the number of the habit to delete (0 to cancel): ")

            if choice == '0':
                return
            
            try:
                index = int(choice) - 1
                if 0 <= index < len(habits):
                    habit = habits[index]
                    confirm = input(f"Are you sure you want to delete '{habit.name}'? (y/n): ")

                    if confirm.lower() == 'y':
                        self.storage.remove_habit(habit.id)
                        print(f"Habit '{habit.name}' deleted successfully")
                    break
                else:
                    print("Invalid habit number")
            except ValueError:
                print("Please enter a valid number")

    def show_analytics(self):
        """Show analytics menu"""
        while True:
            print("\n===== Analytics =====")
            print("1. View all habits")
            print("2. View habits by periodicity")
            print("3. View longest streak")
            print("4. View completion rates")
            print("5. View habits completed today")
            print("6. View habits to complete today")
            print("0. Back to main menu")
            print("=====================")

            choice = input("Enter your choice: ")

            if choice == '1':
                self.show_all_habits()
            elif choice == '2':
                self.show_habits_by_periodicity()
            elif choice == '3':
                self.show_longest_streak()
            elif choice == '4':
                self.show_completion_rates()
            elif choice == '5':
                self.show_habits_completed_today()
            elif choice == '6':
                self.show_habits_to_complete_today()
            elif choice == '0':
                break
            else:
                print("Invalid choice. Please try again")

    def show_all_habits(self):
        """Show all habits"""
        habits = analytics.get_all_habits(self.storage)

        if not habits:
            print("No habits found")
            return
        
        print("\n===== All Habits =====")
        for habit in habits:
            print(f"- {habit}")

    def show_habits_by_periodicity(self):
        """Show habits by periodicity"""
        periodicity = input("Enter periodicity (daily/weekly): ").lower()

        if periodicity not in ["daily", "weekly"]:
            print("INvalid periodicity.")
            return
        
        habits = analytics.get_habits_by_periodicity(self.storage, periodicity)

        if not habits:
            print(f"No {periodicity} habits found")
            return
        
        print(f"\n===== {periodicity.capitalize()} Habits =====")
        for habit in habits:
            print(f"- {habit}")

    def show_longest_streak(self):
        """Show habit with longest streak"""
        habit, streak = analytics.get_longest_streak_habit(self.storage)

        if not habit:
            print("No habits found")
            return
        
        print(f"\nHabit with longest streak: {habit.name} ({streak} {habit.periodicity} periods)")

    def show_completion_rates(self):
        """SHow completion rates"""
        days = input("Enter number of days to analyze (default: 30): ")

        try:
            days = int(days) if days else 30
        except ValueError:
            print("Invalid number of days. Using default (30)")
            days = 30

        completion_rates = analytics.get_completion_rate(self.storage, days)

        if not completion_rates:
            print("No habits found.")
            return
        
        print(f"\n===== Completion Rates (Last {days} Days) =====")
        for habit_name, rate in completion_rates.items():
            print(f"- {habit_name}: {rate:.1f}%")

    def show_habits_completed_today(self):
        """show habits completed today"""
        habits = analytics.get_habits_completed_today(self.storage)

        if not habits:
            print("No habits completed today")
            return
        
        print("\n===== Habits Completed Today =====")
        for habit in habits:
            print(f"- {habit}")

    def show_habits_to_complete_today(self):
        """Show habits to complete today"""
        habits = analytics.get_habits_to_complete_today(self.storage)

        if not habits:
            print("No habits to complete today.")
            return
        
        print("\n===== Habits to Complete today =====")
        for habit in habits:
            print(f"- {habit}")

