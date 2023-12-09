def translateLetter(letter_grades):
    translation_table = {'A+': 4.3, 'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7,
                         'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D+': 1.3, 'D': 1.0, 'D-': 0.7}
    return [translation_table[grade] for grade in letter_grades]

def translatePercentage(percentage_scores):
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

def calculateGPA(points, credits):
    total_points = sum(points)
    total_credits = sum(credits)
    overall_gpa = total_points / total_credits
    return overall_gpa

with open('c:\\LAB_Python\\Shynggys\\Midterm2\\grades\\credits.txt', 'r', encoding='utf-8') as file:
    credits = [int(line.strip()) for line in file]

with open('c:\\LAB_Python\\Shynggys\\Midterm2\\grades\\math.txt', 'r', encoding='utf-8') as file:
    math_grades = [float(line.strip()) for line in file]

with open('c:\\LAB_Python\\Shynggys\\Midterm2\\grades\\chemistry.txt', 'r', encoding='utf-8') as file:
    chemistry_grades = [float(line.strip()) for line in file]

with open('c:\\LAB_Python\\Shynggys\\Midterm2\\grades\\english.txt', 'r', encoding='utf-8') as file:
    english_grades = [float(line.strip()) for line in file]

math_points = translatePercentage(math_grades)
chemistry_points = translatePercentage(chemistry_grades)
english_points = translatePercentage(english_grades)

overall_gpa = calculateGPA(math_points + chemistry_points + english_points, credits)

with open('c:\\LAB_Python\\Shynggys\\Midterm2\\grades\\overallGPAs.txt', 'w', encoding='utf-8') as file:
    file.write(f"{overall_gpa:.2f}")

print("Overall GPA:", overall_gpa)
