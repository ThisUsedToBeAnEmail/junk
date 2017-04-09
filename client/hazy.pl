# hazy.pl
use Hazy;

Hazy->new(
	read_dir => 'css/vanilla', 
	write_dir => 'css', 
	file_name => 'vanilla', 
)->process();

1;
