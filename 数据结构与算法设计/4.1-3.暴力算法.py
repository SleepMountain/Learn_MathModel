def max_subarray_brute_force(arr):
    n = len(arr)
    max_reslut = float('-inf')
    l, r = 0, 0


    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += arr[j]
            if current_sum > max_reslut:
                max_reslut = current_sum
                l = i
                r = j

    return l, r, max_reslut


arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
result = max_subarray_brute_force(arr)
print("brute_force最大子数组起始位置：", result[0])
print("brute_force最大子数组结束位置：", result[1])
print("brute_force最大子数组和：", result[2])
