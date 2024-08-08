(ns cljs-chessboard.core)

(def chess-pieces
  {:white-pawn   "♙"
   :white-knight "♘"
   :white-bishop "♗"
   :white-rook   "♖"
   :white-queen  "♕"
   :white-king   "♔"
   :black-pawn   "♟"
   :black-knight "♞"
   :black-bishop "♝"
   :black-rook   "♜"
   :black-queen  "♛"
   :black-king   "♚"})

(defn render-chessboard []
  (js/console.log "Render your chessboard UI here with chess piece Unicode symbols."))

(defn ^:export init []
  (render-chessboard))
