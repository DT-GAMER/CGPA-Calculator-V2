from flask import current_app, url_for
from flask_mail import Message
from app import mail
from math import floor


def send_verification_email(user):
    token = user.get_verification_token()
    msg = Message('Verify Your Email Address', sender=current_app.config['MAIL_USERNAME'], recipients=[user.email])
    msg.body = f'''To verify your email address, please visit the following link:
{url_for('verify_email', token=token, _external=True)}

If you did not make this request, please ignore this email.
'''
    mail.send(msg)

def calculate_grade_point(self):

        """

        Calculates the Grade Point of the course's grade.

        """

        if self.grade == 'A':

            return 5.00

        elif self.grade == 'B':

            return 4.00

        elif self.grade == 'C':

            return 3.00

        elif self.grade == 'D':

            return 2.00

        elif self.grade == 'E':

            return 1.00

        else:

            return 0.00

    def calculate_gpa(course_units, grades):

        """

        Calculate the GPA given the course units and grades.

        """

        if not all(0.00 <= i <= 5.00 for i in grades):

            return {'error': 'Invalid grade value'}

        total_cu = sum(course_units)

        weighted_points = 0

        for i in range(len(course_units)):

            weighted_points += course_units[i] * grades[i]

        gpa = weighted_points / total_cu

        return round(gpa, 2)

    def calculate_cgpa_utme(level, sem, prev_cgpa, gpa):

        """

        Calculate the CGPA for UTME admission mode.

        """

        cgpa = prev_cgpa  # Initialize current CGPA to previous CGPA

        if level == 100:

            if sem == 1:

                cgpa = 0

            elif sem == 2:

                cgpa = (prev_cgpa + gpa) / 2

        elif level == 200:

            if sem == 1:

                cgpa = (prev_cgpa * 2 + gpa) / 3

            elif sem == 2:

                cgpa = (prev_cgpa * 3 + gpa) / 4

        elif level == 300:

            if sem == 1:

                cgpa = (prev_cgpa * 4 + gpa) / 5

            elif sem == 2:

                cgpa = (prev_cgpa * 5 + gpa) / 6

        elif level == 400:

            if sem == 1:

                cgpa = (prev_cgpa * 6 + gpa) / 7

            elif sem == 2:

                cgpa = (prev_cgpa * 7 + gpa) / 8

        elif level == 500:

            if sem == 1:

                cgpa = (prev_cgpa * 8 + gpa) / 9

            elif sem == 2:

                cgpa = (prev_cgpa * 9 + gpa) / 10

        elif level == 600:

            if sem == 1:

                cgpa = (prev_cgpa * 10 + gpa) / 11

            elif sem == 2:

                cgpa = (prev_cgpa * 11 + gpa) / 12

        return round(cgpa, 2)

    def calculate_cgpa_de(level, sem, prev_cgpa, gpa):

        """

        Calculate the CGPA for Direct Entry (DE) admission mode.

        """

        cgpa = prev_cgpa  # Initialize current CGPA to previous CGPA

        if level == 200:

            if sem == 1:

                cgpa = 0

            elif sem == 2:

                cgpa = (prev_cgpa + gpa) / 2

        elif level == 300:

            if sem == 1:

                cgpa = (prev_cgpa * 2 + gpa) / 3

            elif sem == 2:

                cgpa = (prev_cgpa * 3 + gpa) / 4

        elif level == 400:

            if sem == 1:

                cgpa = (prev_cgpa * 4 + gpa) / 5

            elif sem == 2:

                cgpa = (prev_cgpa * 5 + gpa) / 6

        elif level == 500:

            if sem == 1:

                cgpa = (prev_cgpa * 6 + gpa) / 7

            elif sem == 2:

                cgpa = (prev_cgpa * 7 + gpa) / 8

        elif level == 600:

            if sem == 1:

                cgpa = (prev_cgpa * 8 + gpa) / 9

            elif sem == 2:

                cgpa = (prev_cgpa * 9 + gpa) / 10

        return round(cgpa, 2)

def get_grade_trend(courses):
    grades = [course.grade for course in courses]
    grade_counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0}
    for grade in grades:
        grade_counts[grade] += 1
    return [grade_counts['A'], grade_counts['B'], grade_counts['C'], grade_counts['D'], grade_counts['E'], grade_counts['F']]


def get_semester_courses(courses, semester):
    return [course for course in courses if course.semester == semester]
