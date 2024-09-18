function countingSort(arr) {
  // Your code here
}

// Driver code
const main = () => {
    const input = JSON.parse(require('fs').readFileSync(0, 'utf-8').trim());
    console.log(JSON.stringify(countingSort(input)));
};

main();