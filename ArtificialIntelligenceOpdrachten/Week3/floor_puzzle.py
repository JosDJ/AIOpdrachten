# Loes, Marja, Niels, Erik en Joep wonen in een gebouw met 5 verdiepingen, elk op een eigen verdieping.
#
# Loes woont niet in de bovenste verdieping. ok
# Marja woont niet op de begane grond.  ok
# Niels woont niet op de begane grond en ook niet op de bovenste verdieping. ok
# Erik woont (tenminste één verdieping) hoger dan Marja. ==> dus zit minstens 1 verdieping tussen? ok
# Joep woont niet op een verdieping één hoger of lager dan Niels.
# Niels woont niet op een verdieping één hoger of lager dan Marja.
#
#
# Waar woont iedereen?

import itertools
import time

floors = [x for x in range(5)]
print(floors)
oplossing = 0

t0 = time.process_time()
for (L, M, N, E, J) in list(itertools.permutations(floors)):
    if E > M and L < 4 and M > 0 and 0 < N < 4:
        if J == N-1 or J == N+1:
            continue
        elif N == M+1 or N == M-1:
            continue
        else:
            print("Oplossing ")
            print("Loes woont op: ", L)
            print("Marja woont op: ", M)
            print("Niels woont op: ", N)
            print("Erik woont op: ", E)
            print("Joep woont op: ", J)

    # if E > M and L < 4 and M > 0 and 0 < N < 4 and (J != N + 1 or J != N -1) and (N != M + 1 or N != M - 1):
    #     oplossing += 1
    #     print("Oplossing ",oplossing)
    #     print("Loes woont op: ", L)
    #     print("Marja woont op: ", M)
    #     print("Niels woont op: ", N)
    #     print("Erik woont op: ", E)
    #     print("Joep woont op: ", J)

t1 =time.process_time()
print(t1-t0) # t = 0
