class Student:
    def __init__(self, name, num_courses, scores):
        self.name = name
        self.num_courses = num_courses
        self.scores = scores
        self.gpa = None
        self.status = None

    def calculateGPA(self):
        total_points = 0
        total_credits = 0

        for course, details in self.scores.items():
            total_points += details['score'] * details['credits']
            total_credits += details['credits']

        self.gpa = total_points / total_credits

    def setStatus(self):
        if self.gpa >= 1.0:
            self.status = "Passed"
        else:
            self.status = "Not Passed"

    def showGPA(self):
        if self.gpa is not None:
            print(f"{self.name}'s GPA: {self.gpa:.2f}")
        else:
            print("GPA not calculated. Call calculateGPA() first.")

    def showStatus(self):
        if self.status is not None:
            print(f"{self.name}'s Status: {self.status}")
        else:
            print("Status not determined. Call setStatus() first.")

student_scores = {
    'math': {'score': 4.3, 'credits': 4},
    'chemistry': {'score': 3.3, 'credits': 3},
    'english': {'score': 4.0, 'credits': 4}
}

student1 = Student("John Doe", 3, student_scores)

student1.calculateGPA()
student1.setStatus()

student1.showGPA()
student1.showStatus()
