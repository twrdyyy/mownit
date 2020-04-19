#!/bin/bash
mkdir articles || echo "articles folder exists"
for i in {1..1000}
do
    article=$(lynx --dump https://en.wikipedia.org/wiki/Special:Random \
        | tail -n +2 \
        | sed '/^References/ q' \
        | tr "\n%^&*()[]{},." " " \
        | tr -s " ")

    topic=$(echo $article | awk '{print $1" "$2;}')
    echo $article > ./articles/article$i.txt
    echo "Proceed $i articles with current topic $topic"
done
