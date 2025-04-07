from typing import List

import pandas as pd


def createDataframe(student_data: List[List[int]]) -> pd.DataFrame:
    student_id = []
    age = []
    for list in student_data:
        student_id.append(list[0])
        age.append(list[1])

    data = pd.DataFrame({'student_id': student_id, 'age': age})

    return data

if __name__ == '__main__':
    student_data = [[1, 15],[2, 11],[3, 11],[4, 20]]
    print(createDataframe(student_data))
