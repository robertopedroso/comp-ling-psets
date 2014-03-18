The program CLI syntax is as follows:

`python compression.py -d delimiter infile outfile plotfile`

Since my dx1 file (Basque) used tabs as a delimiter, the delimiter defaults to \t.
However, the program is compatible with whitespace delimiters.

For the infile, it expects a properly formatted dx1 file with phonemic representations
of words in the third column of the data.

The outfile is any text file, and the plotfile can be any format compatible with
matplotlib (pdf, eps, png, etc).

1-4) You may refer to the 'code' directory for the source code of the program.

5) Refer to the output-*.txt and plot-*.pdf files in this directory.

6) The most interesting geometrical pattern present in the plot data is the
ordering of plot points into columns and, to a lesser extent, into rows. The clustering
of data into columns and rows reflects biases in the distribution of symbols. Certain
letters appear more frequently, and certain initial letters appear more frequently
than others. Since the initial letter has the most significant effect on the initial
point of the interval, the appearance of columns reflects this bias.

There are some "rows" in the data, but they are less prominent. Once again, this
phenomenon is reflected by biases letter frequency, but it appears that terminal
letters in English and Basque are not so predictable.
