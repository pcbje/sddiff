bufldiff
========

Python tool for visuzalizing data similarity. The algorithm is based on the work of Vassil Roussev and Candice Quates on sdhash and does a byte level comparison of two input files.

#### Install

<pre><code>$ sudo python setup.py install</code></pre>

#### Usage

<pre><code>$ python bufldiff.py &lt;path1> &lt;path2> &lt;output.png>

# E.g.:
$ python bufldiff.py document1.doc document2.doc result.png</code></pre>

#### Demonstration

##### Input

###### document1.txt
<pre><code>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean nec lectus purus. 
Maecenas sollicitudin, lectus vel pharetra aliquet, magna nisl tincidunt nisi, 
sit amet pharetra urna orci vitae odio. Aliquam massa purus, pulvinar quis 
ultricies sed, rutrum vitae purus. Aliquam ipsum diam, euismod id mi nec, 
faucibus aliquam velit. Integer adipiscing elit vel sapien cursus vulputate. Donec 
imperdiet leo eget lacus tincidunt tristique. Phasellus mattis diam eu urna 
gravida lacinia. Fusce eu elit eu velit rhoncus tristique eu at diam. Vestibulum 
sollicitudin ligula ipsum, quis accumsan nisl molestie interdum. Aliquam est urna, 
gravida at leo eu, semper pharetra dui.

Etiam et sapien ac orci fermentum pellentesque. Pellentesque eu elit massa. 
Phasellus quis sapien aliquam, posuere sem aliquet, adipiscing mauris. Quisque a 
tincidunt felis, id egestas orci. Quisque sit amet volutpat ante, eu venenatis 
felis. Curabitur nec massa eget eros suscipit iaculis vitae ac nisi. Aliquam vel 
scelerisque ligula. Nulla blandit ipsum eget ipsum aliquam, et eleifend purus 
varius.

Praesent eget cursus odio, sed consectetur orci. In tempus imperdiet consectetur. 
Morbi diam odio, eleifend in urna bibendum, cursus feugiat eros. Fusce commodo 
condimentum consequat. Donec non sem at urna vestibulum aliquam. Proin ut diam ac 
tortor pellentesque dictum non sit amet sem. Nunc mattis nibh sit amet odio 
imperdiet condimentum. Vivamus gravida eu odio vel dapibus.</code></pre>

###### document2.txt
<pre><code>
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean nec lectus purus. 
Maecenas sollicitudin, lectus vel pharetra aliquet, magna nisl tincidunt nisi, 
sit amet pharetra urna orci vitae odio. Aliquam massa purus, pulvinar quis ultricies 
sed, rutrum vitae purus. [...] Donec imperdiet leo eget lacus tincidunt tristique. 
Phasellus mattis diam eu urna gravida lacinia. Fusce eu elit eu velit rhoncus 
tristique eu at diam. Vestibulum sollicitudin ligula ipsum, quis accumsan nisl 
molestie interdum. Aliquam est urna, gravida at leo eu, semper pharetra dui.

[...]

Praesent eget cursus odio, sed consectetur orci. In tempus imperdiet consectetur. 
Morbi diam odio, eleifend in urna bibendum, cursus feugiat eros. Fusce commodo 
condimentum consequat. Donec non sem at urna vestibulum aliquam. Proin ut diam ac 
tortor pellentesque dictum non sit amet sem. Nunc mattis nibh sit amet odio 
imperdiet condimentum. Vivamus gravida eu odio vel dapibus.</code></pre>

#### Output.png

The white strokes represent the position of differences between the two files.

<div align="center"><img src="https://raw.github.com/pcbje/bufldiff/master/test/output.png" width="500"/></div>

