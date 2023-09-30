def can_king_move(x1, y1, x2, y2):
    if abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
        return "YES"
    else:
        return "NO"

x1 = int(input())
y1 = int(input())
x2 = int(input())
y2 = int(input())

result = can_king_move(x1, y1, x2, y2)
print(result)
