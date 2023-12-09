def translateLetter(*letter_grades):
    translation_table = {'A+': 4.3, 'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7,
                         'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D+': 1.3, 'D': 1.0, 'D-': 0.7}
    return [translation_table[grade] for grade in letter_grades]

def translatePercentage(*percentage_scores):
    translation_table = {
        (95, 100): 4.3, (90, 94): 4.0, (85, 89): 3.7, (80, 84): 3.3, (75, 79): 3.0,
        (70, 74): 2.7, (65, 69): 2.3, (60, 64): 2.0, (55, 59): 1.7, (50, 54): 1.3,
        (45, 49): 1.0, (40, 44): 0.7
    }

    points = []
    for percentage in percentage_scores:
        for score_range, point in translation_table.items():
            if score_range[0] <= percentage <= score_range[1]:
                points.append(point)
                break

    return points

def calculateGPA(math, math_credits, chemistry, chemistry_credits, english, english_credits):
    total_points = (math * math_credits) + (chemistry * chemistry_credits) + (english * english_credits)
    total_credits = math_credits + chemistry_credits + english_credits
    overall_gpa = total_points / total_credits
    return overall_gpa

letter_points = translateLetter('A+', 'B', 'C')
print(letter_points)

percentage_points = translatePercentage(100, 45, 55, 89)
print(percentage_points)

overall_gpa = calculateGPA(3.3, 4, 2.7, 3, 4.0, 4)
print("GPA:", overall_gpa)
