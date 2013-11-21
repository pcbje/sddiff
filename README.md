bufldiff
========

Python tool for visuzalizing data similarity. The algorithm is based on the work of Vassil Roussev and Candice Quates on sdhash and does a byte level comparison of two input files.

#### Install

<pre><code>$ sudo python setup.py install</code></pre>

#### Usage

<pre><code>$ python bufldiff.py &lt;path1> &lt;path2> &lt;output.png></code></pre>

#### Demonstration

##### Running
<pre><code>$ python bufldiff.py test/document1.doc test/document2.doc test/result.png</code></pre>

##### Yields result

The white strokes represent the position of differences between the two files.

<div align="center"><img src="https://raw.github.com/pcbje/bufldiff/master/test/output.png" width="500"/></div>

