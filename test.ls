(define sub (a b) (- a b))

(define fac (n) (if (= n 1) 1 (* n (fac (- n 1)))))

(sub 3 1)
(fac 8)
(print (fac 8))
(print ("hello world"))
