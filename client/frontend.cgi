#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use Moonshine::Element;
#use Moonshine::Parser;
our $r = CGI->new();
our %params = $r->Vars;

print "Content-type: text/html\n\n";

our $e = Moonshine::Element->new({ tag => 'html' });
our $h = $e->add_child({ 
	tag => 'head', 
	children => [
		{
			tag => 'link',
			rel => 'stylesheet',
			href => 'http://localhost/perl/client/css/vanilla.css',
		},
	],
});

# TODO TO FIX THE url.
my $Javascript = qq{
	function callAjax (endpoint, placement, replace) {
		var xmlhttp = new XMLHttpRequest();
		var current_html;
		if (placement.id) current_html = document.getElementById(placement.id);
		var url = 'http://localhost/perl/client/htmlFactory.cgi?req='+endpoint;
		if (placement.value) url = url + '&value=' + placement.value;

		xmlhttp.onreadystatechange = function() {
			if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
				return stoner(placement, xmlhttp.response, replace)
     			}
		}
		xmlhttp.open("GET", url, true);
		xmlhttp.send();
	}
	function stoner (placement, response, replace) {
		var select = document.getElementById(placement.id);
		if (replace == 1) {
			select.innerHTML = response;
		} else {
			var div = document.createElement('div');
			div.innerHTML = response;
			select.appendChild(div);
		}
	}
	function stonerDestroy (ele, placement) {
		var removeNode; 
		if ( ele ) { removeNode = getParent(ele, placement) }
		else { removeNode = document.getElementById(placement.id) }
		removeNode.parentNode.removeChild(removeNode);
	}
	function getParent (ele, placement) {
		if (placement.class && ele.classList.contains(placement.class)) {
			return ele;
		} else { 
			var ele = getParent(ele.parentNode, placement);
			return ele;
		}
	}
};

$h->add_child({
	tag => 'script',
	type => 'application/javascript',
	data => $Javascript,
});

our $c = $e->add_child({
	tag => 'div',	
	class => 'container col-10 col-md-12 centered',
});

navbar();

if ( $params{req} ) {
	goto $params{req};
} else {
	home();
}

print $e->render;

sub home {
	clientForm();
}

sub navbar {
	my $header = $c->add_child({
		tag => 'header',
		class => 'navbar',
	});
	my @menu_items = (
		[
			{ tag => 'a', href => '#', class => 'navbar-brand', data => 'Client' },
		],
		[
			{ tag => 'div', class => 'input-group input-inline', children => [
				{
					tag => 'input',
					class => 'form-input',
					type => 'text',
					placeholder => 'search',
				},
				{
					tag => 'button',
					class => 'btn btn-primary input-group-btn',
					data => 'Search',
				},
			] }
		],
	);
	for my $item ( @menu_items ) {
		my $section = $header->add_child({ tag => 'section', class => "navbar-section col-10" });
		map { $section->add_child($_) } @{ $item };
	}
}

sub clientForm {
	my $form = $c->add_child({
		tag => 'div',
		class => 'input-group col-12',
		children => [
			{
				tag => 'select',
				class => 'form-select col-2 col-xs-3',
				children => [
					(map { { tag => 'option', data => $_ } }
						qw/GET POST PUT DELETE/ )
				],
			},
			{
				class => 'form-input',
				tag => 'input',
				placeholder => '...',
			},
			(map {
				{
					tag => 'button',
					class => 'btn btn-primary input-group-btn col-2 hide-sm',
					data => $_->[0],
					onclick => "callAjax('$_->[1]', {id:'dynamicForm'})",
				},
			} (['Add Header', 'newHeader'], ['Add Body', 'showBodyInput']))
		],
	});
	
	my $res = $form->add_after_element({ tag => 'div', class => 'input-group' });
	my @buttons = (map {
		my $button = {
			tag => 'button',
			class => 'btn btn-primary input-group-btn show-sm',
			style => 'display:none;',
			data => $_->[0],
			onclick => "callAjax('$_->[1]', {id:'dynamicForm'})",
		};
		$res->add_child($button);
	} (['Add Header', 'newHeader'], ['Add Body', 'showBodyInput']));

	$c->add_child({ tag => 'div', id => 'dynamicForm' });
	$c->add_child({ tag => 'div', id => 'headerListContainer' });
}

1;
