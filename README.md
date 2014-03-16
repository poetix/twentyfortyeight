twentyfortyeight
================

A Python script that plays [Gabriele Cirulli's 2048 game](http://gabrielecirulli.github.io/2048/).

It doesn't seem that there's much mileage in greatly increasing the number of possible future outcomes considered, or looking ahead several moves - that just makes it very slow. It makes 1024 almost always, and 2048 sometimes, which suggests that the game is quite well-balanced.

In theory you could make 4096, but you'd probably get bored by then - this script might manage it once in a while (it doesn't stop until it can't make any more moves).

The strategy followed is ultimately a dumb one: try to make the moves that leave the greatest number of squares unfilled. That in itself is enough to drive the algorithm towards building larger and larger numbers.

I find it a bit hypnotic to watch at speed. It's basically chucking a stream of (pseudo-)random events into a machine that constantly attempts to reduce randomness and find a higher degree of order. Sometimes it succeeds, sometimes it gets jammed up. So it goes.

