(defproject cljs-chessboard "0.1.0-SNAPSHOT"
  :description "Simple online chessboard written in clojurescript"
  :url "https://github.com/togakangaroo/daily-programmer"
  :license {:name "EPL-2.0 OR GPL-2.0-or-later WITH Classpath-exception-2.0"
            :url "https://www.eclipse.org/legal/epl-2.0/"}

  :dependencies [[org.clojure/clojure "1.11.1"]
                 [org.clojure/clojurescript "1.11.60"]
                 [cljsjs/react-dom "16.6.0-0"]
                 [cljsjs/react "16.6.0-0"]
                 [sablono/sablono "0.8.6"]]

  :profiles {:dev {:dependencies [[com.bhauman/figwheel-main "0.2.17"]
                                  [com.bhauman/rebel-readline-cljs "0.1.4"]
                                  ;; to silence SL4J warnings
                                  [org.slf4j/slf4j-nop "1.7.30"]]}}

  :cljsbuild {:builds {:main {:source-paths ["src"]
                              :compiler {:output-to "target/main.js"
                                         :optimizations :whitespace
                                         :pretty-print false}}}}

  :repl-options {:init-ns cljs-chessboard.core}

  :aliases {"fig"       ["trampoline" "run" "-m" "figwheel.main"]
            "fig:build" ["trampoline" "run" "-m" "figwheel.main" "-b" "flappy" "-r"]})
