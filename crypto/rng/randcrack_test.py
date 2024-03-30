import random, time
from randcrack import RandCrack

random.seed(time.time())

MAX_INT = 2**32 - 1
rc = RandCrack()

for i in range(624):
    rc.submit(random.getrandbits(32))
    # rc.submit(random.randint(0, MAX_INT - 1))
    # rc.submit(random.randrange(0, MAX_INT))


print("Random result: {}\nCracker result: {}"
    .format(random.randrange(0, MAX_INT), rc.predict_randrange(0, MAX_INT)))
print("Random result: {}\nCracker result: {}"
    .format(random.randint(1, 69696969), rc.predict_randint(1, 69696969)))
