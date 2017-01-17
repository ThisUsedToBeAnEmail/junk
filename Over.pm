package Over;

use overload
    "+" => "plus",
    "-" => "minus";

sub new {
    my $class = shift;
    my $number = shift;
    return bless \$number, $class;
}

sub minus {
    my ($self, $other) = @_;
    
    my $result = $$self + $other;
    return bless \$result, 'Over';
}

sub plus {
    my ($self, $other) = @_;

    my $result = $$self - $other;
    return bless \$result, 'Over';
}

package main;

my ($overload_this_number, $number ) = @ARGV;

use feature qw/say/;

my $overloaded_number = Over->new($overload_this_number);

$overloaded_number = $overloaded_number - $number;

say $$overloaded_number;

$overloaded_number = $overloaded_number + $number;

say $$overloaded_number;

1;
