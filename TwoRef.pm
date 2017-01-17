package TwoRef;

use overload '%{}' => \&gethash, '@{}' => sub { $ {shift()} };
sub new {
  	my $p = shift;
  	bless \ [@_], $p;
}

sub gethash {
	my %h;
  	my $self = shift;
  	tie %h, ref $self, $self;
  	\%h;
}

sub TIEHASH { my $p = shift; bless \ shift, $p }
 
my %fields;
my $i = 0;
$fields{$_} = $i++ foreach qw{zero one two three};

sub STORE {
	my $self = ${shift()};
    my $key = $fields{shift()};
    defined $key or die "Out of band access";
    $$self->[$key] = shift;
}
  
sub FETCH {
    my $self = ${shift()};
    my $key = $fields{shift()};
    defined $key or die "Out of band access";
    $$self->[$key];
}

package main;

use feature qw/say/;

my $bar = TwoRef->new(1,2,3,4);

$bar->[2] = 11;

say $bar->{two};


