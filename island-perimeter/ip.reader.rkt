#lang br/quicklang

(require brag/support)
(require "ip.parser.rkt")

(provide read-syntax)
(define (read-syntax path port)
  (define parse-tree (parse path (make-tokenizer port)))
  (define module-datum `(module island-perimeter "ip.expander.rkt"
                          ,parse-tree))
  (datum->syntax #f module-datum))
(define (make-tokenizer port)
  (λ ()
    (define ip-lexer (lexer
                      [any-char lexeme]))
    (ip-lexer port)))
