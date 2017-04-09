#/usr/bin/perl

use strict;
use warnings;

use CGI;
use Moonshine::Element;
use Moonshine::Parser;

print "Content-type: text/html\n\n";

our $r = CGI->new();
our %params = $r->Vars;

my %valid_endpoints = (
	newHeader => \&addHeaderForm,
	autoCompleteHeader => \&autoCompleteHeader,
	autoCompleteHeaderList => \&autoCompleteHeaderList,
);

if (my $endpoint = $valid_endpoints{$params{req}}) {
	$endpoint->();
} else {
	print 'a miserable death';
}

sub addHeaderForm {
	my $current_element = Moonshine::Parser->new->parse($params{html});
	
	my $element = Moonshine::Element->new(
		{
			tag => 'div',
			class => 'columns',
			children => [
				{
					tag => 'div',
					class => 'column col-sm-12',
					children => [
						{
							tag => 'div',
							class => 'input-group',
							children => [
								autoCompleteHeader(1)
							],
						}
					],
				},
				{
					tag => 'div',
					class => 'column col-sm-12',
					children => [
						{
							tag => 'div',
							class => 'input-group',
							children => [
								{
									class => 'form-input',
									tag => 'input',
									placeholder => 'Header Value',
								},
							],
						}
					],
				},
				{
					tag => 'div',
					class => 'column col-2 col-sm-12',
					children => [
						{
							tag => 'div',
							class => 'input-group',
							children => [
								{
									tag => 'button',
									class => 'btn btn-close input-group-btn',
									data => 'Remove',
									onclick => "stonerDestroy(this, {class:'columns'});",
								},
							],
						}
					],
				},
			],
		},
	);

	print $element->render;
}

sub autoCompleteHeader {
	my $ele = Moonshine::Element->new({
		tag => 'div',
		class => 'form-autocomplete col-12',
		children => [
			{
				tag => 'div',
				class => 'form-autocomplete-input form-input col-12',
				children => [
					{
						class => 'form-input',
						tag => 'input',
						placeholder => 'Header Key',
						onkeyup => "callAjax('autoCompleteHeaderList', {id:'headerListContainer', value:this.value}, 1)",
						onchange => "stonerDestroy(null, {id:'headerList'})"
					},
				],
			},
		],
	});
	
	$_[0] ? return $ele : print $ele->render;
}

sub autoCompleteHeaderList {
	my @headers = qw/Accept Accept-Charset Accept-Encoding Accept-Language Accept-Datetime Authorization Cache-Control Connection Cookie Content-Length Content-MD5 Content-Type Date Expect Forwarded From Host If-Match If-Modified-Since If-None-Match If-Range If-Unmodified-Since Max-Forwards Origin Pragma Proxy-Authorization Range Referer TE User-Agent Upgrade Via Warning/;
	my @search = grep { ($_ =~ m/^$params{value}/i) } @headers;
	
	my $autocomplete = Moonshine::Element->new({
		tag => 'ul',
		class => 'menu',
		id => 'headerList',
		style => 'margin:10px auto;',
		children => [
			(map {
				{
					tag => 'a',
					href => '#',
					onclick => "console.log(this)",
					children => [
						{
							tag => 'div',
							class => 'tile tile-centered',
							children => [
								{
									tag => 'div',
									class => 'tile-content',
									data => $_,
								}
							]
						}
					]
				}
			} @search )
		],
	});

	print $autocomplete->render;
}

1;
