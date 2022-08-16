/*jshint esversion: 6 */
/*jshint -W033 */
/*jshint -W117 */

class Greeter {
    constructor(name) {
        this.name = name
    }

    getGreeting() {
        if (this.name === undefined) {
            return 'Hello, no name!'
        } else {
            return `Hello, ${this.name}`
        }
    }

    showGreeting(greetingMessage) {
        console.log(greetingMessage)
    }

    greet() {
        this.showGreeting(this.getGreeting())
    }
}


class DelayedGreeter extends Greeter {
    delay = 2000

    constructor(name, delay) {
        super(name)
        if (delay !== undefined) {
            this.delay = delay
        }
    }

    greet() {
        setTimeout(() => {
            this.showGreeting(this.getGreeting())
        }, this.delay)
    }
}

const g = new Greeter()

g.greet()

const dg1 = new DelayedGreeter('Ameer Abdulaziz')
const dg2 = new DelayedGreeter('Akram Abdulaziz', 3000)

dg1.greet()
dg2.greet()