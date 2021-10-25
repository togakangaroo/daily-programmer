#lang br/quicklang

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
(require "find-perimeter.rkt")

(provide (rename-out [ip-module-begin #%module-begin]))

(define compact (curry filter identity))
(define mapcompact (compose compact map))

(define/match (parse-island program)
  [((list 'ip-program contents ...)) (~>> contents
                                          (mapcompact parse-island)
                                          sequence->list*
                                          list*->matrix)]
  [((list 'ip-row rows ...)) (mapcompact parse-island rows)]
  [((list 'ip-cell contents ...)) (first (mapcompact parse-island contents))]
  [((list 'ip-vertical-wall _)) #f]
  [((list 'ip-whitespace _)) #f]
  [("\n") #f]
  [((list 'ip-mark (list 'ip-water _))) 'water]
  [((list 'ip-mark (list 'ip-land _))) 'land])

(define-macro (ip-module-begin PARSE-TREE)
  #'(#%module-begin
     (define board (parse-island 'PARSE-TREE))
     (find-perimeter board (first-land-vertex board))))
