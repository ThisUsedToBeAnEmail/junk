package symbolic;

use overload nomethod => \&wrap, '""' => \&str, '0+' => \&num;

sub new { shift; bless ['n', @_] }

sub wrap {
    my ($obj, $other, $inv, $meth) = @_;
    ($obj, $other) = ($other, $obj) if $inv;
    return bless [$meth, $obj, $other];
}

sub str {
    my ($meth, $a, $b) = @{+shift};
    $a = 'u' unless defined $a;
    return defined $b ? "[$meth $a $b]" : "[$meth $a]";
}

sub pretty {
    my ($meth, $a, $b) = @{+shift};
    $a = 'u' unless defined $a;
    $b = 'u' unless defined $b;
    $a = $a->pretty if ref $a;
    $b = $b->pretty if ref $b;
    return "[$meth $a $b]";
}

my %subr = (
    n       => sub {$_[0]},
    sqrt    => sub {sqrt $_[0]},
    '-'     => sub {shift() - shift()},
    '+'     => sub {shift() + shift()},
    '/'     => sub {shift() / shift()}, 
    '*'     => sub {shift() * shift()},
    '**'    => sub {shift() ** shift()},
);

sub num {
    my ($meth, $a, $b) = @{+shift};
    my $subr = $subr{$meth}
        or die "Do not know how to ($meth) in symbolic";
    $a = $a->num if ref $a eq __PACKAGE__;
    $b = $b->num if ref $b eq __PACKAGE__;
    $subr->($a, $b);
}

package main;

use feature qw/say/;

my $iter = symbolic->new(2);
my $side = symbolic->new(1);
my $cnt = $iter;

while ($cnt) {
    $cnt = $cnt - 1;
    $side = (sqrt(1 + $side**2) - 1)/$side;
}


say "side:" . $side->pretty;

say "second";

printf "%s=%f\n", $side, $side;
printf "pi=%f\n", $side*(2**($iter+2));

