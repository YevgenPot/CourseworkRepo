(defun sum-even (lst)
  (cond ; lst element is either 0 or atom or a list
    ((null lst) 0)  ; check element 0
    ((atom (car lst))  ; check element atom
     (if (evenp (car lst))  ; atom even
         (+ (car lst) (sum-even (cdr lst)))  ; add it
         (sum-even (cdr lst))))  ; atom odd, skip it
    (t  ; check element list
     (+ (sum-even (car lst)) (sum-even (cdr lst))))))  ; sum this list
