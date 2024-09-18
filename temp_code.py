def bubble_sort(arr):
  return sorted(arr)

# Driver code
if __name__ == '__main__':
    import sys
    input_data = sys.stdin.read().strip()
    input_list = eval(input_data)  # Convert the input string to a list
    result = bubble_sort(input_list)
    print(result)