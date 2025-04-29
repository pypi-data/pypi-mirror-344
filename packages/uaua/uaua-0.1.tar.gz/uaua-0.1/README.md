# uaua
uaua is a command-line program to check the writing speed of your terminal.

## Example
```sh
$ python -m uaua --line-count 100000
uaua
uaua
uaua
uaua
uaua
...
uaua
uaua
   0.43807244 seconds taken
       100000 uaua
    228272.75 uaua per second
  0.000004381 seconds per uaua
$ python -m uaua --duration 1 > /dev/null
   1.00000167 seconds taken
      1626917 uaua
   1626914.28 uaua per second
  0.000000615 seconds per uaua
$ python -m uaua -c 100000 1 > kočka.txt
   0.02503824 seconds taken
       100000 uaua
   3993890.57 uaua per second
  0.000000250 seconds per uaua
$ python -m uaua -h
```