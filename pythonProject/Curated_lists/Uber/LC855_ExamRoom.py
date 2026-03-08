class ExamRoom:

    def __init__(self, n: int):
        self.n = n
        self.students = []

    def seat(self) -> int:

        # CASE 1: Nobody here → sit at 0
        if not self.students:
            self.students.append(0)
            return 0

        # Find the best seat by checking all gaps
        best_seat = -1
        best_dist = -1

        # SPECIAL GAP: before the first student
        # If first student is at seat 3, sitting at 0 gives distance 3
        dist = self.students[0]  # distance from seat 0 to first student
        if dist > best_dist:
            best_dist = dist
            best_seat = 0

        # NORMAL GAPS: between each pair of adjacent students
        for i in range(1, len(self.students)):
            left = self.students[i - 1]
            right = self.students[i]

            # Best seat in this gap is the midpoint
            dist = (right - left) // 2
            seat = left + dist
            if dist > best_dist:
                best_dist = dist
                best_seat = seat

        # SPECIAL GAP: after the last student
        # If last student is at seat 6 and n=10, sitting at 9 gives distance 3
        dist = (self.n - 1) - self.students[-1]
        if dist > best_dist:
            best_dist = dist
            best_seat = self.n - 1

        # Insert in sorted position
        # bisect keeps the list sorted
        import bisect
        bisect.insort(self.students, best_seat)

        return best_seat

    def leave(self, p: int) -> None:
        self.students.remove(p)


if __name__ == "__main__":
    examRoom = ExamRoom(10)
    print(examRoom.seat())
    print(examRoom.seat())
    print(examRoom.seat())