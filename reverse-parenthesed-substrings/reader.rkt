#lang br/quicklang


(require (for-syntax (only-in racket/format ~a)))
(require threading)
(require (for-syntax threading))
(require (for-syntax (only-in racket/function identity)))
(define-for-syntax (compute stx )
  (syntax-case stx ()
    [(a . b) #`(~a (a . b))]
    [_ (identity (~a (syntax-e stx)))]))
(define-syntax (string-contents stx)
  (syntax-case stx ()
    [(_ args ...)
     #`(string-append #,@(map compute (syntax->list #'(args ...))))]))
(define-for-syntax reverse-string (lambda~> string->list reverse list->string))
(define-syntax (reverse-string-contents stx)
  (syntax-case stx ()
    [(_ args ...)
     #`(string-append #,@(reverse (map (compose reverse-string compute) (syntax->list #'(args ...)))))]))

(define (read-syntax path port)
  (define src-lines (~>> port
                         port->lines
                         (filter non-empty-string?)
                         (map (lambda~> (string-replace "(" "(reverse-string-contents " #:all? #t)))))
  (define src-datums (format-datums '(string-contents ~a) src-lines))
  (define module-datum `(module my-mod "../../../../../Users/gmauer/code/daily-programmer/reverse-parenthesed-substrings/reader.rkt"
                          (string-contents ,@src-datums )))
  (datum->syntax #f module-datum))
(provide read-syntax)


(define-macro (my-module-begin HANDLE-EXPR ...)
  #'(#%module-begin
     HANDLE-EXPR ...))
(provide (rename-out [my-module-begin #%module-begin]))
(provide string-contents reverse-string-contents)
