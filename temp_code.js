function bubbleSort(arr) {
    le n = arr.length;
    let swapped;
    do {
        swapped = false;
        for (let i = 0; i < n - 1; i++) {
            if (arr[i] > arr[i + 1]) {
                // Swap arr[i] and arr[i + 1]
                let temp = arr[i];
                arr[i] = arr[i + 1];
                arr[i + 1] = temp;
                swapped = true;
            }
        }
        // Reduce the range of the next pass
        n--;
    } while (swapped);
    return arr;
}

// Driver code
const main = () => {
    const input = JSON.parse(require('fs').readFileSync(0, 'utf-8').trim());
    console.log(JSON.stringify(bubbleSort(input)));
};

main();