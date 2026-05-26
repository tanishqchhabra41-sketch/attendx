import os


class AttendanceSystem:

    def add_attendance(self):
        os.system("../c_modules/attendance.exe")

    def view_records(self):

        try:
            file = open("../data/attendance.txt", "r")

            print("\n===== ATTENDANCE RECORDS =====\n")

            data = file.readlines()

            if len(data) == 0:
                print("No records found!")

            else:
                for line in data:
                    print(line.strip())

            file.close()

        except FileNotFoundError:
            print("Attendance file not found!")

    def menu(self):

        while True:

            print("\n===== SMART ATTENDANCE SYSTEM =====")
            print("1. Add Attendance")
            print("2. View Records")
            print("3. Exit")

            choice = input("Enter Choice: ")

            if choice == "1":
                self.add_attendance()

            elif choice == "2":
                self.view_records()

            elif choice == "3":
                print("Exiting...")
                break

            else:
                print("Invalid Choice!")


system = AttendanceSystem()
system.menu()
