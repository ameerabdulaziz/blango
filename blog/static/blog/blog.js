/*jshint esversion: 6 */
/*jshint -W033 */
/*jshint -W117 */

function resolvedCallback(data) {
    console.log(`resolved with data ${data}`)
}

function rejectedCallback(message) {
    console.log(`rejected with message ${message}`)
}

const lazyAdd = (a, b) => {
    const doAdd = (resolve, reject) => {
        if (typeof a !== 'number' || typeof b !== 'number') {
            reject('a and b must be numbers')
        } else {
            const sum = a + b
            resolve(sum)
        }
    }
    return new Promise(doAdd)
}

const p = lazyAdd(5, 3)
p.then(resolvedCallback, rejectedCallback)

lazyAdd("nan", "alsonan").then(resolvedCallback, rejectedCallback)

// function resolvedCallback(data) {
//   console.log('Resolved with data ' +  data)
// }
//
// function rejectedCallback(message) {
//   console.log('Rejected with message ' + message)
// }
//
// const lazyAdd = (a, b) => {
//   const doAdd = (resolve, reject) => {
//     if (typeof a !== "number" || typeof b !== "number") {
//       reject("a and b must both be numbers")
//     } else {
//       const sum = a + b
//       resolve(sum)
//     }
//   }
//
//   return new Promise(doAdd)
// }
//
// const p = lazyAdd(3, 4)
// p.then(resolvedCallback, rejectedCallback)
//
// lazyAdd("nan", "alsonan").then(resolvedCallback, rejectedCallback)