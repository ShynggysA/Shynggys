def can_rook_move(x1, y1, x2, y2):
    if x1 == x2 or y1 == y2:
        return "YES"
    else:
        return "NO"

x1 = int(input())
y1 = int(input())
x2 = int(input())
y2 = int(input())

result = can_rook_move(x1, y1, x2, y2)
print(result)
