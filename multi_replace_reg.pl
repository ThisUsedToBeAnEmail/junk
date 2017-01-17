use strict;
use warnings;
use feature qw/say/;

my ($sentence, %replace) = @ARGV;
(my $val = $sentence) =~ s/(@{[join "|", keys %replace]})/$replace{$1}/g;
say $val;

1;
