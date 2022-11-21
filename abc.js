//how to addtags in github using python for evry commit? 
A   &lt;-- master


A &lt;- B   &lt;-- master


A &lt;- B &lt;- C   &lt;-- master


A &lt;- B &lt;- C   &lt;-- master
          ^
          |
   tag: sometag


A &lt;- B &lt;- C &lt;- D   &lt;-- master
          ^
          |
   tag: sometag


$ git tag -d sometag


$ git tag sometag master~2


git push --tags origin


git push origin sometag


git push origin master




