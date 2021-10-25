#lang racket
(require racket/match)
(require racket/format)
(require racket/set)
(require racket/vector)
(require racket/generator)
(require racket/pretty)
(require math/matrix)
(require math/array)
(require threading)
(require (except-in data/collection sequence->list))

(provide find-perimeter walk-perimeter first-land-vertex)

(define (first-land-vertex board)
  ;; in-array-indexes guarantees to return indices starting with the innermost iteration first. For a 2d matrix that means sweeping from left to right and downward.
  ;; The upper left vertex would be the same as the cell coordinates. As we're sweeping upper left to lower right, the first land cell we encounter, its upper left vertex must be on the outside
  (for/or ([idx (~> board array-shape in-array-indexes)])
    (if (equal? 'land (array-ref board idx))
        idx
        #f)))

(define (vector+ . vectors) (apply vector-map + vectors))
(define (vector- . vectors) (apply vector-map - vectors))
(define up1 #[-1 0])
(define left1 #[0 -1])

(define (indicies-of-cells-adjacent-to-move vertex-2 vertex-1)
  (match (vector- vertex-1 vertex-2)
    [(vector 0 1)  (list vertex-2 (vector+ vertex-2 up1))]
    [(vector 0 -1) (list vertex-1 (vector+ vertex-1 up1))]
    [(vector 1 0)  (list vertex-2 (vector+ vertex-2 left1))]
    [(vector -1 0) (list vertex-1 (vector+ vertex-1 left1))]))
(define not-equal? (compose not equal?))

(define (try-array-ref board default-value idx)
  "Like array-ref but with a default value returned if the index is out of bounds"
  (with-handlers ([exn:fail? (thunk* default-value)])
    (array-ref board idx)))

(define (move-along-perimeter? board vertex-1 vertex-2)
  (define adjacent-cells (~>> (indicies-of-cells-adjacent-to-move vertex-1 vertex-2)
                              (map (curry try-array-ref board 'water))
                              sequence->list))
  (and (member 'land adjacent-cells)
       (apply not-equal? adjacent-cells)))
(define adjacent-cell-moves (list #[0 1] #[1 0] #[0 -1] #[-1 0]))

(define (walk-perimeter board initial-vertex)
  (in-generator
   (define visited (mutable-set))
   (let step-to ([current-vertex initial-vertex])
     (unless (set-member? visited current-vertex)
       (yield current-vertex)
       (set-add! visited current-vertex)
       (for ([move adjacent-cell-moves])
         (define next-vertex (vector+ current-vertex move))
         (when (move-along-perimeter? board current-vertex next-vertex)
           (step-to next-vertex)))))))

(define (find-perimeter board initial-vertex)
  (sequence-length (walk-perimeter board initial-vertex)))
