def bubble_sort(arr):

    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                
    return arr

# Driver code
if __name__ == '__main__':
    import sys
    input_data = sys.stdin.read().strip()
    input_list = eval(input_data)  
    # Convert the input string to a list
    result = bubble_sort(input_list)
    print(result)