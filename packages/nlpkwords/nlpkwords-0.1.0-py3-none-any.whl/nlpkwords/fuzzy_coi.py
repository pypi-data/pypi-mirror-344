def intersection(set1, set2):
    return {key: min(set1.get(key, 0), set2.get(key, 0)) for key in set(set1) & set(set2)}

def complement(fuzzy_set):
    return {key: 1 - value for key, value in fuzzy_set.items()}

def main():
    fuzzy1 = {'a': 0.5, 'b': 0.7}
    fuzzy2 = {'a': 0.6, 'b': 0.2}

    intersection_set = intersection(fuzzy1, fuzzy2)
    complement_intersection = complement(intersection_set)

    complement_fuzzy1 = complement(fuzzy1)
    complement_fuzzy2 = complement(fuzzy2)
    union_complements = {key: max(complement_fuzzy1.get(key, 0), complement_fuzzy2.get(key, 0)) for key in complement_fuzzy1}

    print("Complement of Intersection:", complement_intersection)
    print("Union of Complements:", union_complements)

if __name__ == "__main__":
    main()
