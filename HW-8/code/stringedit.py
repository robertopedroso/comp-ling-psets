def alignment_cost(a,b):
    vowels = 'aeiou'

    if a == b: return 0
    elif a in vowels and b in vowels: return 0.5
    elif a not in vowels and b not in vowels: return 0.6
    else: return 1.2

def align_strings(matrix, str1, str2):
    alignment1, alignment2 = '', ''
    i, j = len(str1)-1, len(str2)-1

    while i >= 0 or j >= 0:
        pos = matrix[(i,j)]

        if i >= 0 and (pos == (matrix[(i-1,j)] + 2) or j == -1):
            alignment1 = str1[i] + alignment1
            alignment2 = ' ' + alignment2
            i -= 1

        elif j >= 0 and (pos == (matrix[(i,j-1)] + 2) or i == -1):
            alignment1 = ' ' + alignment1
            alignment2 = str2[j] + alignment2
            j -= 1

        else:
            alignment1 = str1[i] + alignment1
            alignment2 = str2[j] + alignment2
            i -= 1
            j -= 1

    return (alignment1,alignment2)

def optimal_string_edit_distance(str1,str2):
    matrix = {}
    matrix[(-1,-1)] = 0

    for i,x in enumerate(str1):
        matrix[(i,-1)] = matrix[(i-1,-1)] + 2
    for j,x in enumerate(str2):
        matrix[(-1,j)] = matrix[(-1,j-1)] + 2

    for i,c1 in enumerate(str1):
        for j,c2 in enumerate(str2):
            case1 = matrix[(i-1,j-1)] + alignment_cost(c1, c2)
            case2 = matrix[(i-1,j)] + 2
            case3 = matrix[(i,j-1)] + 2

            matrix[(i,j)] = min(case1, case2, case3)

    cost = matrix[(len(str1)-1,len(str2)-1)]
    alignment1, alignment2 = align_strings(matrix, str1, str2)
    return cost, alignment1, alignment2

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('str1', help='')
    parser.add_argument('str2', help='')
    args = parser.parse_args()

    cost, alignment1, alignment2 = optimal_string_edit_distance(args.str1, args.str2)
    print 'Alignment Cost: %s' % cost
    print alignment1
    print alignment2
