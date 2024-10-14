def max_crossing_subarray(arr, low, mid, high):
    l_sum = float('-inf')
    r_sum = float('-inf')
    l_max = 0
    r_max = 0
    total = 0


    for i in range(mid, low - 1, -1):
        total += arr[i]
        if total > l_sum:
            l_sum = total
            l_max = i

    total = 0

    for j in range(mid + 1, high, 1):
        total += arr[j]
        if total > r_sum:
            r_sum = total
            r_max = j

    return l_max, r_max, l_sum + r_sum


def max_subarray_recursive(arr, low, high):
    if high == low:
        return low, high, arr[low]
    else:
        mid = (low + high) // 2
        l_low, l_high, l_sum = max_subarray_recursive(arr, low, mid)
        r_low, r_high, r_sum = max_subarray_recursive(arr, mid + 1, high)
        c_low, c_high, c_sum = max_crossing_subarray(arr, low, mid, high)
        if l_sum >= r_sum and l_sum >= c_sum:
            return l_low, l_high, l_sum
        elif r_sum >= l_sum and r_sum >= c_sum:
            return r_low, r_high, r_sum
        else:
            return c_low, c_high, c_sum


arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
result = max_subarray_recursive(arr, 0, len(arr) - 1)
print("最大子数组起始位置：", result[0])
print("最大子数组结束位置：", result[1])
print("最大子数组和：", result[2])
