def union(set1, set2):
    return {key: max(set1.get(key, 0), set2.get(key, 0)) for key in set(set1) | set(set2)}

def complement(fuzzy_set):
    return {key: 1 - value for key, value in fuzzy_set.items()}

def main():
    fuzzy1 = {'a': 0.5, 'b': 0.7}
    fuzzy2 = {'a': 0.6, 'b': 0.2}

    union_set = union(fuzzy1, fuzzy2)
    complement_union = complement(union_set)

    complement_fuzzy1 = complement(fuzzy1)
    complement_fuzzy2 = complement(fuzzy2)
    intersection_complements = {key: min(complement_fuzzy1.get(key, 0), complement_fuzzy2.get(key, 0)) for key in complement_fuzzy1}

    print("Complement of Union:", complement_union)
    print("Intersection of Complements:", intersection_complements)

if __name__ == "__main__":
    main()
