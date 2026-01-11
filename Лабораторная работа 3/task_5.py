# TODO Напишите функцию find_common_participants


def find_common_participants(group1, group2, separator=","):
    set1 = set(group1.split(separator))
    set2 = set(group2.split(separator))
    return sorted(set1 & set2)
participants_first_group = "Иванов|Петров|Сидоров"
participants_second_group = "Петров|Сидоров|Смирнов"

# TODO Проверьте работу функции с разделителем отличным от запятой
result = find_common_participants(
    participants_first_group,
    participants_second_group,
    separator="|"
)

print(result)